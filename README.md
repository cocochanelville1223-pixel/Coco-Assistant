# Coco-Assistant

Coco Assistant is a virtual assistant inspired by Alexa and Google Assistant. It can perform various tasks like telling time, weather, playing music, searching Wikipedia, telling jokes, and more.

Coco Assistant disclaims responsibility for any errors, as it is currently under development.

## Features

- **Modern GUI Interface**: Chat-like window with buttons and controls (automatic detection)
  - Voice input toggle button
  - Change voice settings
  - Profile management
  - Settings panel
  - Real-time chat display with timestamps
- **Text Interface Fallback**: Command-line mode for servers and headless environments
- Wake word detection: Responds to "Hey Coco", "OK Coco", "Coco", "Hi Coco" (can interrupt speech) - falls back to text input in headless environments
- Voice recognition and text-to-speech with selectable natural male/female voices (uses Festival for natural speech, eSpeak as fallback) - falls back to console output when TTS unavailable
- User profiles with date of birth and kids mode for ages 12 and under
- Parental controls: Restrict certain content in kids mode, toggle kids mode (adults only)
- Sing songs by reciting lyrics (e.g., "Everything at Once" by Lenka)
- Shopping list management: Add, remove, read items
- Unit conversions (temperature, length, weight)
- Tell stories
- Play games (guess the number)
- Math help using SymPy
- Get current time and date
- Fetch weather information (location-aware)
- Search Wikipedia
- Play music on YouTube (automated if pywhatkit available, otherwise browser search)
- Tell jokes (filtered for kids mode)
- Get news headlines (restricted in kids mode)
- Open websites (some restricted in kids mode)
- Change voice during interaction
- Set timers and reminders
- Take and read notes
- Perform calculations
- Translate text
- Read recipes
- Location-based services

## Setup

### Quick Setup (Recommended)

1. **Run the automated setup:**
   ```bash
   ./setup.sh
   ```
   This will create a virtual environment and install all dependencies.

2. **Get API keys:**
   - OpenWeatherMap: Sign up at https://openweathermap.org/api and get your API key.
   - NewsAPI: Sign up at https://newsapi.org/ and get your API key.

3. **Update `config.py` with your API keys.**

4. **Run the assistant:**
   ```bash
   ./launch.sh
   ```

### Desktop Application Installation

To install Coco Assistant as a desktop application (Linux):

1. **Setup the application:**
   ```bash
   ./setup.sh
   ```

2. **Install as desktop app:**
   ```bash
   sudo ./install.sh
   ```

3. **Launch from your applications menu** or run `coco-assistant` from terminal.

4. **To uninstall:**
   ```bash
   sudo ./uninstall.sh
   ```

**Note:** The desktop installation requires administrator privileges and will:
- Install the application to `/usr/local/share/coco-assistant`
- Create a desktop entry in your applications menu
- Add a launcher script to `/usr/local/bin`
- Create an application icon (stylized "C" on turquoise background)

### Windows Installation

For Windows users, you can create a desktop shortcut:

1. Right-click on `launch.bat` → Create Shortcut
2. Right-click the shortcut → Properties
3. Change icon if desired
4. Move to desktop or start menu

### macOS Installation

For macOS, you can add to Applications:

1. Create an alias: `ln -s /path/to/coco-assistant /Applications/Coco-Assistant`
2. Or use the Automator to create an application launcher

### Manual Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Get API keys:
   - OpenWeatherMap: Sign up at https://openweathermap.org/api and get your API key.
   - NewsAPI: Sign up at https://newsapi.org/ and get your API key.

3. Update `config.py` with your API keys.

4. Run the assistant:
   ```
   python main.py
   ```

   **Or use the launcher scripts:**
   ```bash
   # Linux/macOS
   ./launch.sh

   # Windows
   launch.bat
   ```

### Running Modes

- **GUI Mode**: Automatically launches if display is available (desktop environments)
  - Modern chat interface with turquoise and dark blue theme
  - Voice input toggle, settings, profile management
  - Real-time chat display with timestamps

- **Text Mode**: Falls back to command-line interface in headless environments (servers, SSH sessions)

**For GUI Mode on Linux:**
- Install display server if needed: `sudo apt install xorg`
- Run with display: `DISPLAY=:0 python main.py` (if you have X11)
- Or use: `DISPLAY=:0 ./launch.sh`

   **For Text Mode:**
   - Works in terminals, SSH sessions, and headless servers
   - Type commands directly and press Enter
   - Type 'quit', 'exit', or 'stop' to close

### Environment-Specific Setup

#### On Ubuntu/Debian Linux (including Chromebook Linux terminal):

For full TTS support with natural voices:
```bash
sudo apt update
sudo apt install espeak-ng festival festvox-us1 festvox-us2 festvox-us3
```

For voice input (microphone):
```bash
# Ubuntu/Debian
sudo apt install python3-pyaudio portaudio19-dev python3-dev

# Or install via pip (after system dependencies)
pip install pyaudio

# Alternative: Use system audio (may work better)
sudo apt install libasound2-dev
pip install --upgrade --force-reinstall pyaudio
```

**Microphone Setup:**
- Uses Google Speech Recognition for accurate voice input
- Automatic ambient noise adjustment
- Works with most USB microphones and built-in laptop mics
- Falls back to text input when microphone unavailable
- Supports wake word detection for hands-free operation
- **GUI Mode**: Includes microphone test button and status indicator

**Microphone Troubleshooting:**
- **Test Button**: Use the "Test Mic" button in GUI mode to verify functionality
- **Diagnostic Script**: Run `./check_microphone.sh` to diagnose audio issues
- **Permission Issues**: Ensure microphone permissions are granted to your application
- **Audio Drivers**: On Linux, check ALSA/PulseAudio configuration
- **Virtual Environments**: May need additional audio device passthrough

**Alternative Speech Recognition (if PyAudio issues):**
- The assistant can use web-based speech recognition as fallback
- Or text-only mode for environments without audio hardware

For automated YouTube playback (optional, requires GUI):
```bash
pip install pywhatkit
```
Note: pywhatkit requires a GUI environment and may not work in headless servers.

**Voice Options:**
- **eSpeak-ng**: Basic robotic voices (fast, works offline)
- **Festival**: More natural male/female voices (slower, very natural)
- The assistant automatically uses the best available TTS engine

**Voice Quality & Conversations:**
- Natural male/female voices available with Festival TTS
- Voice selection during runtime with "change voice" command
- Full conversation support with custom NLP (no external AI services)
- Interruptible speech for natural interaction flow

#### On macOS:
TTS should work out of the box. For voice input, PyAudio may need installation.

#### On Windows:
TTS and voice input should work. pywhatkit may work with Edge/Chrome.

#### In headless environments (servers, codespaces):
- TTS will fall back to console output
- Voice input will use text input prompts
- YouTube playback will open browser search pages instead of auto-playing

### Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Start the assistant with `python main.py`. It will listen for wake words. Once activated, speak your command. You can interrupt Coco while it's speaking by saying a wake word.

Wake words: "Hey Coco", "OK Coco", "Coco", "Hi Coco"

Then speak commands like:
- "Create profile John born on 2010-05-15"
- "Switch to profile John"
- "Toggle kids mode" (adults only)
- "What time is it?"
- "What's the weather in London?"
- "Search Wikipedia for Python"
- "Play Shape of You"
- "Tell me a joke"
- "What's the news?" (restricted in kids mode)
- "Open Google"
- "Change voice"
- "Set timer for 5 minutes"
- "Remind me to call mom in 10 minutes"
- "Take a note: buy milk"
- "Read notes"
- "Calculate 2 + 2"
- "Translate hello to Spanish"
- "Read recipe for chocolate cake"
- "Sing everything at once"
- "Add to shopping list milk"
- "Remove from shopping list milk"
- "Read shopping list"
- "Convert 10 celsius to fahrenheit"
- "Tell a story"
- "Play a game"
- "Help with math solve 2x + 3 = 7"
- "Stop" to exit

## Requirements

- Python 3.x
- Microphone for voice input
- Speakers for voice output
- Internet connection for API calls

## Note

This is a basic implementation of a virtual assistant. It does not include advanced features like wake word detection, natural language understanding, IoT integrations, or the full range of services provided by Alexa or Google Assistant. For a more complete assistant, consider using frameworks like Rasa or integrating with AI services.

The wake word detection is simulated using speech recognition and may not be as efficient as dedicated hardware wake word engines.

Coco Assistant now uses custom natural language processing instead of external AI services, making it more privacy-focused and self-contained.

The assistant adapts to different environments:
- In GUI environments with TTS support: Full voice interaction
- In headless environments: Text-based interaction with browser integration
- YouTube playback: Automated if possible, otherwise opens search results

## Project Files

- `main.py` - Main application with GUI and core functionality
- `config.py` - API keys and configuration
- `requirements.txt` - Python dependencies
- `setup.sh` - Automated environment setup script
- `install.sh` - Desktop application installer (Linux)
- `uninstall.sh` - Desktop application uninstaller (Linux)
- `launch.sh` - Linux/macOS launcher script
- `launch.bat` - Windows launcher script
- `check_microphone.sh` - Audio diagnostics script
- `coco-assistant.desktop` - Desktop application entry
- `README.md` - This documentation

Coco Assistant disclaims responsibility for any errors, as it is currently under development.
