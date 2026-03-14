#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# Ghost Clock Installer — Raspberry Pi 5
# Tested and verified working setup including all autostart fixes
# ─────────────────────────────────────────────────────────────

set -e

USERNAME="$(whoami)"
INSTALL_DIR="/home/$USERNAME/ghost-clock"
FONT_DIR="/home/$USERNAME/.local/share/fonts"
AUTOSTART_DIR="/home/$USERNAME/.config/lxsession/LXDE-pi"
XDG_DIR="/home/$USERNAME/.config/autostart"

echo ""
echo "  Ghost Clock Installer"
echo "  ─────────────────────"
echo ""

# ── Step 1: Fix ownership and permissions ─────────────────────
echo "[1/6] Fixing folder permissions..."
sudo chown -R "$USERNAME:$USERNAME" "$INSTALL_DIR"
sudo chmod 755 "$INSTALL_DIR"
sudo chmod 644 "$INSTALL_DIR/clock.py"
echo "      done"

# ── Step 2: Install Orbitron font ─────────────────────────────
echo "[2/6] Installing Orbitron font..."
mkdir -p "$FONT_DIR"
FONT_URL="https://github.com/google/fonts/raw/main/ofl/orbitron/Orbitron%5Bwght%5D.ttf"
if wget -q -O "$FONT_DIR/Orbitron.ttf" "$FONT_URL" 2>/dev/null; then
    fc-cache -fv "$FONT_DIR" > /dev/null 2>&1
    echo "      done"
else
    echo "      skipped (offline) - fallback font will be used"
fi

# ── Step 3: Enable linger so user services start at boot ──────
echo "[3/6] Enabling linger for $USERNAME..."
sudo loginctl enable-linger "$USERNAME"
echo "      done"

# ── Step 4: XDG autostart (most reliable method on Pi OS) ─────
echo "[4/6] Setting up XDG autostart..."
mkdir -p "$XDG_DIR"
cat > "$XDG_DIR/ghost-clock.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Ghost Clock
Exec=bash -c 'sleep 8 && DISPLAY=:0 /usr/bin/python3 $INSTALL_DIR/clock.py > /tmp/ghost-clock.log 2>&1'
X-GNOME-Autostart-enabled=true
EOF
echo "      done"

# ── Step 5: LXDE autostart (backup method) ────────────────────
echo "[5/6] Setting up LXDE autostart..."
mkdir -p "$AUTOSTART_DIR"
AUTOSTART_FILE="$AUTOSTART_DIR/autostart"
cat > "$AUTOSTART_FILE" << EOF
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@bash -c 'sleep 8 && DISPLAY=:0 /usr/bin/python3 $INSTALL_DIR/clock.py > /tmp/ghost-clock.log 2>&1'
EOF
echo "      done"

# ── Step 6: Verify everything looks correct ───────────────────
echo "[6/6] Verifying setup..."
echo ""
echo "  LXDE autostart:"
cat "$AUTOSTART_FILE"
echo ""
echo "  XDG autostart:"
cat "$XDG_DIR/ghost-clock.desktop"
echo ""

echo "  ─────────────────────────────────────────"
echo "  Ghost Clock installed successfully!"
echo "  ─────────────────────────────────────────"
echo ""
echo "  Test it right now (no reboot needed):"
echo "    DISPLAY=:0 python3 $INSTALL_DIR/clock.py &"
echo ""
echo "  Restart after editing clock.py:"
echo "    pkill -f clock.py && DISPLAY=:0 python3 $INSTALL_DIR/clock.py &"
echo ""
echo "  Then reboot to confirm autostart:"
echo "    sudo reboot"
echo ""
