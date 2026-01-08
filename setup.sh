#!/bin/bash

# Coco Assistant Setup Script
# This script sets up the Python environment and dependencies

set -e

echo "🔧 Setting up Coco Assistant..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3 first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $REQUIRED_VERSION or higher is required. You have Python $PYTHON_VERSION."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment. Please install python3-venv:"
        echo "   sudo apt install python3-venv"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "❌ Virtual environment activation failed. Please check your Python installation."
    exit 1
fi

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check for optional dependencies and install if available
echo "🔍 Checking for optional dependencies..."

# Try to install PyAudio (may fail on some systems)
if pip install PyAudio 2>/dev/null; then
    echo "✅ PyAudio installed successfully"
else
    echo "⚠️  PyAudio installation failed (this is normal on some systems)"
    echo "   Voice input will use alternative methods"
fi

# Try to install pywhatkit for YouTube music
if pip install pywhatkit 2>/dev/null; then
    echo "✅ pywhatkit installed for YouTube music support"
else
    echo "⚠️  pywhatkit installation failed"
    echo "   Music playback will use browser search instead"
fi

# Deactivate virtual environment
deactivate

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "To run Coco Assistant:"
echo "  • ./launch.sh (recommended)"
echo "  • python main.py (direct)"
echo ""
echo "To install as desktop app:"
echo "  • sudo ./install.sh"
echo ""
echo "To uninstall:"
echo "  • sudo ./uninstall.sh"