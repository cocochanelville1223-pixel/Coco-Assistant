#!/bin/bash
# Microphone Diagnostic Script for Coco Assistant
# This script helps diagnose microphone and audio issues

echo "🎤 Coco Assistant - Microphone Diagnostic"
echo "=========================================="

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Not running in virtual environment"
    echo "   Consider activating: source .venv/bin/activate"
fi

echo ""
echo "1. Checking Python audio libraries..."

python3 -c "
import sys
print('Python version:', sys.version)

try:
    import speech_recognition as sr
    print('✓ SpeechRecognition available')
except ImportError as e:
    print('✗ SpeechRecognition missing:', e)

try:
    import pyaudio
    print('✓ PyAudio available')
    audio = pyaudio.PyAudio()
    device_count = audio.get_device_count()
    print(f'  Audio devices found: {device_count}')
    audio.terminate()
except ImportError as e:
    print('✗ PyAudio missing:', e)

try:
    import speech_recognition as sr
    print('')
    print('2. Testing microphone access...')
    with sr.Microphone() as source:
        print('✓ Microphone accessible')
        source.close()
except Exception as e:
    print('✗ Microphone not accessible:', e)
"

echo ""
echo "3. System audio information:"
echo "   - Check if microphone is enabled in system settings"
echo "   - Ensure microphone permissions are granted"
echo "   - Try different microphone devices"

echo ""
echo "4. Installation commands if needed:"
echo "   Ubuntu/Debian:"
echo "   sudo apt update"
echo "   sudo apt install python3-pyaudio portaudio19-dev python3-dev"
echo "   pip install --upgrade --force-reinstall pyaudio"
echo ""
echo "   macOS:"
echo "   brew install portaudio"
echo "   pip install pyaudio"
echo ""
echo "   Windows:"
echo "   pip install pyaudio"