#!/bin/bash
# Installer for AIM Tmux Dashboard

echo "Installing AIM Tmux Dashboard..."
sudo ln -sf "$(pwd)/bin/aim-dash" /usr/local/bin/aim-dash
echo "✅ Installed successfully! You can now type 'aim-dash' from anywhere to open the TUI."
