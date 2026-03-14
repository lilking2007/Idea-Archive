#!/usr/bin/env python3
"""
Ghost Clock - Raspberry Pi 5 Digital Clock
Theme: Ghost - crisp white on pure black, maximum legibility
Time source : system clock (datetime.now()) - 100% offline
System stats: /proc and /sys only - no packages needed
Controls:
  Tap/swipe up home bar -> minimize to desktop
  Escape                -> minimize
  F11                   -> toggle fullscreen
"""

import tkinter as tk
import tkinter.font as tkfont
from datetime import datetime
import threading
import time

BG         = "#000000"
FG         = "#ffffff"
DIM        = "#555555"
BAR_COL    = "#2a2a2a"
DIV_COL    = "#1c1c1c"
WIFI_ON    = "#4ade80"
WIFI_OFF   = "#444444"
TEMP_COOL  = "#4ade80"
TEMP_WARM  = "#facc15"
TEMP_HOT   = "#f87171"

FONT_PREF = [
    "Orbitron", "Share Tech Mono", "VT323",
    "Courier New", "DejaVu Sans Mono", "Monospace", "Courier", "Fixed",
]


def pick_font(families):
    for f in FONT_PREF:
        if f in families:
            return f
    return "Courier"


def _read_proc_stat():
    try:
        with open("/proc/stat") as f:
            line = f.readline()
        return list(map(int, line.split()[1:]))
    except Exception:
        return []


def get_cpu_percent(prev):
    cur = _read_proc_stat()
    if not prev or not cur or len(cur) < 4:
        return 0.0, cur
    idle_prev = prev[3] + (prev[4] if len(prev) > 4 else 0)
    idle_cur  = cur[3]  + (cur[4]  if len(cur)  > 4 else 0)
    d_total = sum(cur) - sum(prev)
    d_idle  = idle_cur - idle_prev
    if d_total == 0:
        return 0.0, cur
    return round(100.0 * (1 - d_idle / d_total), 1), cur


def get_cpu_temp():
    for path in [
        "/sys/class/thermal/thermal_zone0/temp",
        "/sys/class/thermal/thermal_zone1/temp",
    ]:
        try:
            with open(path) as f:
                return int(f.read().strip()) / 1000.0
        except Exception:
            continue
    return None


def get_ram_percent():
    try:
        info = {}
        with open("/proc/meminfo") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    info[parts[0].rstrip(":")] = int(parts[1])
        total   = info.get("MemTotal",  1)
        free    = info.get("MemFree",   0)
        cached  = info.get("Cached",    0)
        buffers = info.get("Buffers",   0)
        used    = total - free - cached - buffers
        return round(100.0 * used / total, 1), used // 1024, total // 1024
    except Exception:
        return 0.0, 0, 0


def check_wifi():
    try:
        with open("/proc/net/wireless") as f:
            lines = f.readlines()
        return len([l for l in lines[2:] if l.strip()]) > 0
    except Exception:
        return False


class GhostClock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ghost Clock")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.attributes("-topmost", True)
        self._fullscreen = True

        self.bind("<Escape>", lambda e: self.minimize())
        self.bind("<F11>",    lambda e: self.toggle_fullscreen())
        self.bind("<Map>",    lambda e: self._on_restore())

        self.update_idletasks()
        self.sw = self.winfo_screenwidth()
        self.sh = self.winfo_screenheight()

        self._swipe_y  = None
        self._cpu_prev = _read_proc_stat()

        families = set(tkfont.families())
        self.clock_font = pick_font(families)
        self.mono_font  = pick_font(families)

        self._build_ui()
        self._tick()
        self._poll_system()

    def _build_ui(self):
        sw, sh = self.sw, self.sh

        sz_time = max(38, sh // 7)
        sz_date = max(11, sh // 42)
        sz_stat = max(9,  sh // 68)

        # --- Status bar: Pi stats left, WiFi right ---
        self.lbl_cpu = tk.Label(
            self, text="CPU  ---%",
            bg=BG, fg=DIM, font=(self.mono_font, sz_stat), anchor="w")
        self.lbl_cpu.place(x=14, y=10)

        self.lbl_temp = tk.Label(
            self, text="TEMP  ---C",
            bg=BG, fg=DIM, font=(self.mono_font, sz_stat), anchor="w")
        self.lbl_temp.place(x=14, y=10 + sz_stat + 6)

        self.lbl_ram = tk.Label(
            self, text="RAM  ---%",
            bg=BG, fg=DIM, font=(self.mono_font, sz_stat), anchor="w")
        self.lbl_ram.place(x=14, y=10 + (sz_stat + 6) * 2)

        self.wifi_canvas = tk.Canvas(
            self, width=8, height=8, bg=BG, highlightthickness=0)
        self.wifi_oval = self.wifi_canvas.create_oval(
            0, 0, 8, 8, fill=WIFI_OFF, outline="")
        self.wifi_canvas.place(relx=1.0, x=-14, y=14, anchor="ne")

        self.lbl_wifi = tk.Label(
            self, text="WiFi",
            bg=BG, fg=DIM, font=(self.mono_font, sz_stat), anchor="e")
        self.lbl_wifi.place(relx=1.0, x=-26, y=10, anchor="ne")

        # --- Centre block: time, divider, date ---
        sb_h    = 10 + (sz_stat + 6) * 3
        block_h = sz_time + 14 + 1 + 14 + sz_date
        top     = sb_h + (sh - sb_h - block_h) // 2

        self.lbl_time = tk.Label(
            self, text="",
            bg=BG, fg=FG,
            font=(self.clock_font, sz_time, "bold"), anchor="center")
        self.lbl_time.place(relx=0.5, y=top, anchor="n")

        self.divider = tk.Frame(self, bg=DIV_COL, height=1)
        self.divider.place(
            relx=0.5, y=top + sz_time + 14, anchor="n", width=44)

        self.lbl_date = tk.Label(
            self, text="",
            bg=BG, fg=DIM,
            font=(self.mono_font, sz_date), anchor="center")
        self.lbl_date.place(
            relx=0.5, y=top + sz_time + 22, anchor="n")

        # --- Home bar ---
        bar_w = max(60, sw // 8)
        self.homebar = tk.Frame(
            self, bg=BAR_COL, height=5, width=bar_w, cursor="hand2")
        self.homebar.place(x=(sw - bar_w) // 2, y=sh - 14)
        self.homebar.bind("<ButtonPress-1>",  self._swipe_start)
        self.homebar.bind("<B1-Motion>",       self._swipe_move)
        self.homebar.bind("<ButtonRelease-1>", self._swipe_end)
        self.bind("<ButtonRelease-1>", self._global_tap)

    def _tick(self):
        now       = datetime.now()
        h24, m, s = now.hour, now.minute, now.second
        self.lbl_time.configure(
            text=f"{h24:02d}:{m:02d}:{s:02d}",
            fg=FG if s % 2 == 0 else "#cccccc")
        self.lbl_date.configure(text=now.strftime("%A   %d %b %Y").upper())
        self.after(1000, self._tick)

    def _poll_system(self):
        def _worker():
            while True:
                cpu_pct, self._cpu_prev = get_cpu_percent(self._cpu_prev)
                temp = get_cpu_temp()
                ram_pct, ram_used, ram_total = get_ram_percent()
                wifi = check_wifi()
                self.after(0, self._apply_stats,
                           cpu_pct, temp, ram_pct, ram_used, ram_total, wifi)
                time.sleep(2)
        threading.Thread(target=_worker, daemon=True).start()

    def _apply_stats(self, cpu_pct, temp, ram_pct, ram_used, ram_total, wifi):
        self.lbl_cpu.configure(text=f"CPU   {cpu_pct:5.1f}%")
        if temp is not None:
            col = (TEMP_COOL if temp < 55 else
                   TEMP_WARM if temp < 70 else TEMP_HOT)
            self.lbl_temp.configure(text=f"TEMP  {temp:.1f}C", fg=col)
        else:
            self.lbl_temp.configure(text="TEMP   N/A", fg=DIM)
        self.lbl_ram.configure(
            text=f"RAM   {ram_pct:.1f}%  ({ram_used}M/{ram_total}M)")
        self.wifi_canvas.itemconfig(
            self.wifi_oval, fill=WIFI_ON if wifi else WIFI_OFF)

    def minimize(self):
        self.attributes("-topmost", False)
        self.iconify()

    def _on_restore(self):
        self.attributes("-topmost", True)
        if self._fullscreen:
            self.attributes("-fullscreen", True)

    def toggle_fullscreen(self):
        self._fullscreen = not self._fullscreen
        self.attributes("-fullscreen", self._fullscreen)

    def _swipe_start(self, event):
        self._swipe_y = event.y_root

    def _swipe_move(self, event):
        if self._swipe_y is not None and self._swipe_y - event.y_root > 18:
            self.minimize()
            self._swipe_y = None

    def _swipe_end(self, event):
        if self._swipe_y is not None:
            if abs(self._swipe_y - event.y_root) < 8:
                self.minimize()
        self._swipe_y = None

    def _global_tap(self, event):
        if event.y_root > self.sh - 28:
            self.minimize()


if __name__ == "__main__":
    app = GhostClock()
    app.mainloop()
