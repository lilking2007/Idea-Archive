# 🕐 Ghost Clock — Raspberry Pi 5

> Minimalist fullscreen digital clock for Raspberry Pi 5 with mini LCD screen.
> White on black. 24-hour time. Live Pi system stats. Fully offline. Auto-boots on startup.

![Ghost Clock](https://img.shields.io/badge/Platform-Raspberry%20Pi%205-red) ![Python](https://img.shields.io/badge/Python-3.x-blue) ![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 What It Looks Like

```
┌─────────────────────────────────────────┐
│ CPU    0.9%                    WiFi  ●  │
│ TEMP   39.7C                            │
│ RAM    15.7%  (1266M/8062M)             │
│                                         │
│                                         │
│         21:45:09                        │
│                                         │
│              ────                       │
│        SATURDAY   14 MAR 2026           │
│                                         │
│                  ▬▬▬▬▬                  │
└─────────────────────────────────────────┘
```

---

## ✅ Features

- 24-hour fullscreen digital clock
- Live Raspberry Pi system stats (CPU, temperature, RAM, WiFi)
- Temperature colour coding — green (cool) → amber (warm) → red (hot)
- iPhone-style home bar at the bottom to minimize back to desktop
- Auto-boots into clock on every startup
- 100% offline — uses system clock and reads directly from `/proc` and `/sys`
- No internet required, ever
- Auto-scales to any screen resolution

---

## 🛠️ Requirements

- Raspberry Pi 5 (works on Pi 4 too)
- Raspberry Pi OS Bookworm or Bullseye with **desktop**
- Python 3 (pre-installed on Pi OS)
- `python3-tk` (usually pre-installed)
- Pi must be set to **boot to desktop with auto-login**

---

## 📁 File Structure

```
~/ghost-clock/
├── clock.py       ← main application
└── install.sh     ← run once to set everything up
```

---

## 🚀 Fresh Installation (Start Here)

### Step 1 — Make sure you are booting to desktop with auto-login

```
raspi-config → System Options → Boot / Auto Login → Desktop Autologin
```

This is required. The clock cannot auto-launch if you boot to CLI.

---

### Step 2 — Create the folder

```bash
mkdir -p ~/ghost-clock
```

---

### Step 3 — Fix permissions on the folder

```bash
sudo chown -R $USER:$USER ~/ghost-clock
sudo chmod 755 ~/ghost-clock
```

---

### Step 4 — Copy `clock.py` and `install.sh` into `~/ghost-clock/`

Use a USB stick, file browser, or SCP. Once the files are in the folder, fix their permissions:

```bash
sudo chmod 644 ~/ghost-clock/clock.py
sudo chmod +x ~/ghost-clock/install.sh
```

---

### Step 5 — Set up the XDG autostart entry (auto-boot the clock)

This is the most reliable autostart method on Raspberry Pi OS. Paste this whole block into the terminal:

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/ghost-clock.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Ghost Clock
Exec=bash -c 'sleep 8 && DISPLAY=:0 /usr/bin/python3 /home/$USER/ghost-clock/clock.py'
X-GNOME-Autostart-enabled=true
EOF
```

---

### Step 6 — Set up the LXDE autostart as a backup

```bash
mkdir -p ~/.config/lxsession/LXDE-pi
cat > ~/.config/lxsession/LXDE-pi/autostart << 'EOF'
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@bash -c 'sleep 8 && DISPLAY=:0 /usr/bin/python3 /home/pi/ghost-clock/clock.py'
EOF
```

> ⚠️ Replace `pi` with your actual username if different (e.g. `lilking`)

Check it looks right:

```bash
cat ~/.config/lxsession/LXDE-pi/autostart
```

You should see all 4 lines.

---

### Step 7 — Enable linger so services start at boot

```bash
sudo loginctl enable-linger $USER
```

---

### Step 8 — Install Orbitron font (optional but looks great)

```bash
mkdir -p ~/.local/share/fonts
wget -q -O ~/.local/share/fonts/Orbitron.ttf \
  "https://github.com/google/fonts/raw/main/ofl/orbitron/Orbitron%5Bwght%5D.ttf"
fc-cache -fv ~/.local/share/fonts
```

If you are offline, the clock falls back to `Courier New` automatically — still looks clean.

---

### Step 9 — Test the clock right now (without rebooting)

```bash
DISPLAY=:0 python3 ~/ghost-clock/clock.py &
```

The `&` runs it in the background so closing the terminal does not kill it.

---

### Step 10 — Reboot to confirm autostart works

```bash
sudo reboot
```

After the desktop loads, wait about 8–10 seconds — the clock will appear automatically.

---

## 🎮 Controls

| Action | Result |
|---|---|
| Tap or swipe up the home bar | Minimize → back to desktop |
| Press `Escape` | Minimize → back to desktop |
| Press `F11` | Toggle fullscreen on/off |
| Close terminal | Clock keeps running (background) |

---

## 🔧 Making Changes to clock.py

### Edit the file

Use nano directly in the terminal:

```bash
nano ~/ghost-clock/clock.py
```

Save with `Ctrl+X` → `Y` → `Enter`

Or use a file browser (FileBrowser, VSCode, etc.) to edit and save the file visually.

---

### Restart the clock after any change

Kill the running clock and start the updated version:

```bash
pkill -f clock.py && DISPLAY=:0 python3 ~/ghost-clock/clock.py &
```

> Always use this command after editing `clock.py`. The `&` keeps it running in the background.

---

### Check if the clock is currently running

```bash
pgrep -a -f clock.py
```

If it returns a line with the process ID, the clock is running. If nothing returns, it is not running.

---

### Stop the clock

```bash
pkill -f clock.py
```

---

### Start the clock manually

```bash
DISPLAY=:0 python3 ~/ghost-clock/clock.py &
```

---

## 🎨 Customisation

All customisation is done by editing `clock.py`. After any change, restart using the command above.

### Switch between 12-hour and 24-hour time

Find the `_tick` method and change:

**24-hour (current default):**
```python
self.lbl_time.configure(
    text=f"{h24:02d}:{m:02d}:{s:02d}",
    fg=FG if s % 2 == 0 else "#cccccc")
self.lbl_date.configure(text=now.strftime("%A   %d %b %Y").upper())
```

**12-hour with AM/PM:**
```python
ampm = "PM" if h24 >= 12 else "AM"
h12  = h24 % 12 or 12
self.lbl_time.configure(
    text=f"{h12:02d}:{m:02d}:{s:02d}",
    fg=FG if s % 2 == 0 else "#cccccc")
self.lbl_ampm.configure(text=ampm)
self.lbl_date.configure(text=now.strftime("%A   %d %b %Y").upper())
```

---

### Change colours

Find the colour palette at the top of `clock.py`:

```python
BG         = "#000000"   # background (pure black)
FG         = "#ffffff"   # main time colour (white)
DIM        = "#555555"   # secondary text (stats, date)
BAR_COL    = "#2a2a2a"   # home bar colour
DIV_COL    = "#1c1c1c"   # divider line
WIFI_ON    = "#4ade80"   # wifi dot when connected (green)
WIFI_OFF   = "#444444"   # wifi dot when disconnected
TEMP_COOL  = "#4ade80"   # temperature below 55C (green)
TEMP_WARM  = "#facc15"   # temperature 55-70C (amber)
TEMP_HOT   = "#f87171"   # temperature above 70C (red)
```

---

### Change font sizes

Font sizes are calculated automatically from screen height. To override, find these lines in `_build_ui`:

```python
sz_time = max(38, sh // 7)   # main clock digits
sz_date = max(11, sh // 42)  # date text
sz_stat = max(9,  sh // 68)  # stats bar text
```

Lower the divider number to make text bigger (e.g. `sh // 5` is bigger than `sh // 7`).

---

### Change temperature thresholds

```python
TEMP_COOL  = "#4ade80"   # below 55C
TEMP_WARM  = "#facc15"   # 55 to 70C
TEMP_HOT   = "#f87171"   # above 70C
```

To change the threshold values, find `_apply_stats`:

```python
col = (TEMP_COOL if temp < 55 else
       TEMP_WARM if temp < 70 else TEMP_HOT)
```

---

## ❗ Troubleshooting

### Clock does not appear on boot

Check the autostart file is correct:

```bash
cat ~/.config/lxsession/LXDE-pi/autostart
cat ~/.config/autostart/ghost-clock.desktop
```

Make sure the username in the path matches yours.

---

### Permission denied errors

Fix ownership of the entire folder:

```bash
sudo chown -R $USER:$USER ~/ghost-clock
sudo chmod 755 ~/ghost-clock
sudo chmod 644 ~/ghost-clock/clock.py
sudo chmod +x ~/ghost-clock/install.sh
```

---

### `no display name and no $DISPLAY environment variable` error

Always launch the clock with `DISPLAY=:0` in front:

```bash
DISPLAY=:0 python3 ~/ghost-clock/clock.py &
```

Never launch it without `DISPLAY=:0` from a terminal.

---

### Font looks plain (not Orbitron)

Rebuild the font cache and reboot:

```bash
fc-cache -fv
sudo reboot
```

---

### `python3-tk` missing

```bash
sudo apt update && sudo apt install python3-tk -y
```

---

### Check what display the Pi is using

```bash
ls /tmp/.X11-unix/
```

Should show `X0`. If it shows `X1`, replace `:0` with `:1` in all commands and autostart entries.

---

### Clock crashes or freezes

Check the log:

```bash
cat /tmp/ghost-clock.log
```

Restart it:

```bash
pkill -f clock.py && DISPLAY=:0 python3 ~/ghost-clock/clock.py &
```

---

## 📊 How the System Stats Work

Everything is read directly from Linux kernel files — no external packages needed, works fully offline.

| Stat | Source | Update interval |
|---|---|---|
| CPU % | `/proc/stat` — delta between two snapshots | every 2 seconds |
| Temperature | `/sys/class/thermal/thermal_zone0/temp` | every 2 seconds |
| RAM | `/proc/meminfo` | every 2 seconds |
| WiFi | `/proc/net/wireless` | every 2 seconds |

---

## 🗂️ Full Command Reference

| Task | Command |
|---|---|
| Start clock | `DISPLAY=:0 python3 ~/ghost-clock/clock.py &` |
| Stop clock | `pkill -f clock.py` |
| Restart clock after edit | `pkill -f clock.py && DISPLAY=:0 python3 ~/ghost-clock/clock.py &` |
| Check if running | `pgrep -a -f clock.py` |
| Edit clock file | `nano ~/ghost-clock/clock.py` |
| Check autostart | `cat ~/.config/lxsession/LXDE-pi/autostart` |
| Check XDG autostart | `cat ~/.config/autostart/ghost-clock.desktop` |
| Rebuild font cache | `fc-cache -fv` |
| Fix permissions | `sudo chown -R $USER:$USER ~/ghost-clock` |
| Reboot | `sudo reboot` |

---

*Built for Raspberry Pi 5 with mini LCD display. Ghost theme — white on black, clean and minimal.*
