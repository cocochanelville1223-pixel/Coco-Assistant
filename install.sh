#!/bin/bash

# Coco Assistant Installation Script
# This script installs Coco Assistant as a desktop application

set -e

echo "🚀 Installing Coco Assistant..."

# Check if running as root or with sudo
if [[ $EUID -eq 0 ]]; then
   echo "Please do not run this script as root. Use sudo only when prompted."
   exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="coco-assistant"
INSTALL_DIR="/usr/local/share/$APP_NAME"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="/usr/share/applications"
ICON_DIR="/usr/local/share/icons"

# Create directories
echo "📁 Creating directories..."
sudo mkdir -p "$INSTALL_DIR"
sudo mkdir -p "$ICON_DIR"

# Copy application files
echo "📋 Copying application files..."
sudo cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/"

# Create executable wrapper script
echo "🔧 Creating executable wrapper..."
cat > /tmp/coco-assistant-wrapper << 'EOF'
#!/bin/bash
# Coco Assistant Launcher

# Check if we're in the right directory
if [ -f "/usr/local/share/coco-assistant/main.py" ]; then
    cd "/usr/local/share/coco-assistant"

    # Check if virtual environment exists and activate it
    if [ -d "venv" ]; then
        source venv/bin/activate
    elif [ -d ".venv" ]; then
        source .venv/bin/activate
    fi

    # Run the application
    python main.py
else
    echo "Error: Coco Assistant installation not found!"
    exit 1
fi
EOF

sudo mv /tmp/coco-assistant-wrapper "$BIN_DIR/$APP_NAME"
sudo chmod +x "$BIN_DIR/$APP_NAME"

# Create desktop entry
echo "🖥️  Installing desktop entry..."
sudo cp "$SCRIPT_DIR/coco-assistant.desktop" "$DESKTOP_DIR/"

# Create icon (simple "C" letter)
echo "🎨 Creating application icon..."
python3 -c "
from PIL import Image, ImageDraw, ImageFont
import os

# Create a 256x256 icon
img = Image.new('RGBA', (256, 256), (0, 188, 212, 255))  # Turquoise background
draw = ImageDraw.Draw(img)

# Try to use a system font, fallback to default if not available
try:
    # Try common font paths
    font_paths = ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                  '/System/Library/Fonts/Arial.ttf',
                  '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf']
    font = None
    for font_path in font_paths:
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, 180)
            break
    if font is None:
        font = ImageFont.load_default()
except:
    font = ImageFont.load_default()

# Draw the letter 'C' in the center
text = 'C'
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (256 - text_width) // 2
y = (256 - text_height) // 2

# Draw white text with slight shadow effect
draw.text((x+2, y+2), text, font=font, fill=(255, 255, 255, 128))  # Shadow
draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))      # Main text

# Save the icon
img.save('/usr/local/share/icons/coco-assistant.png')
print('Icon created successfully!')
" 2>/dev/null || echo "PIL not available, creating simple icon..."

# If PIL fails, create a simple SVG icon
if [ ! -f "/usr/local/share/icons/coco-assistant.png" ]; then
    sudo tee "$ICON_DIR/coco-assistant.svg" > /dev/null << 'EOF'
<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">
  <rect width="256" height="256" fill="#00bcd4"/>
  <text x="128" y="180" font-family="Arial, sans-serif" font-size="180" font-weight="bold"
        text-anchor="middle" fill="white">C</text>
</svg>
EOF
    # Update desktop file to use SVG
    sudo sed -i 's/Icon=\/usr\/local\/share\/icons\/coco-assistant.png/Icon=\/usr\/local\/share\/icons\/coco-assistant.svg/' "$DESKTOP_DIR/coco-assistant.desktop"
fi

# Update desktop database
echo "🔄 Updating desktop database..."
sudo update-desktop-database 2>/dev/null || echo "Desktop database update skipped (normal in container environments)"

# Set permissions
echo "🔒 Setting permissions..."
sudo chown -R root:root "$INSTALL_DIR"
sudo chmod -R 755 "$INSTALL_DIR"

echo ""
echo "✅ Coco Assistant has been successfully installed!"
echo ""
echo "You can now:"
echo "  • Launch it from your applications menu"
echo "  • Run 'coco-assistant' from the terminal"
echo "  • Find it in your desktop environment's application launcher"
echo ""
echo "To uninstall, run: sudo $INSTALL_DIR/uninstall.sh"