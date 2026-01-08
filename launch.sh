#!/bin/bash
# Coco Assistant Launcher
# This script helps launch Coco Assistant with the appropriate interface

echo "🤖 Coco Assistant Launcher"
echo "=========================="

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    echo "✓ Activating virtual environment..."
    source .venv/bin/activate
fi

# Check if we're in a GUI environment
if [ -n "$DISPLAY" ]; then
    echo "✓ Display detected - attempting GUI mode..."
    python main.py
else
    echo "⚠ No display detected - using text mode..."
    echo "For GUI mode, run: DISPLAY=:0 $0"
    echo ""
    python main.py
fi