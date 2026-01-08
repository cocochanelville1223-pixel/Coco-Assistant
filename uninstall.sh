#!/bin/bash

# Coco Assistant Uninstallation Script
# This script removes Coco Assistant from the system

set -e

echo "🗑️  Uninstalling Coco Assistant..."

# Check if running as root or with sudo
if [[ $EUID -eq 0 ]]; then
   echo "Please do not run this script as root. Use sudo only when prompted."
   exit 1
fi

APP_NAME="coco-assistant"
INSTALL_DIR="/usr/local/share/$APP_NAME"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="/usr/share/applications"
ICON_DIR="/usr/local/share/icons"

# Remove desktop entry
echo "🖥️  Removing desktop entry..."
sudo rm -f "$DESKTOP_DIR/coco-assistant.desktop"

# Remove executable
echo "🔧 Removing executable..."
sudo rm -f "$BIN_DIR/$APP_NAME"

# Remove icons
echo "🎨 Removing icons..."
sudo rm -f "$ICON_DIR/coco-assistant.png"
sudo rm -f "$ICON_DIR/coco-assistant.svg"

# Remove application directory
echo "📁 Removing application files..."
sudo rm -rf "$INSTALL_DIR"

# Update desktop database
echo "🔄 Updating desktop database..."
sudo update-desktop-database 2>/dev/null || echo "Desktop database update skipped (normal in container environments)"

# Clean up any user data (optional - ask user)
echo ""
read -p "Do you want to remove user data (profiles, config)? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 Removing user data..."
    rm -rf "$HOME/.coco-assistant"
    rm -f "$HOME/profiles.json"
    echo "User data removed."
else
    echo "User data preserved."
fi

echo ""
echo "✅ Coco Assistant has been successfully uninstalled!"
echo ""
echo "Note: Python dependencies installed via pip are not removed."
echo "You can remove them manually with: pip uninstall -r requirements.txt"