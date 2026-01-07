# Coco-Assistant

Coco Assistant is a virtual assistant inspired by Alexa and Google Assistant. It can perform various tasks like telling time, weather, playing music, searching Wikipedia, telling jokes, and more.

Coco Assistant disclaims responsibility for any errors, as it is currently under development.

## Features

- Wake word detection: Responds to "Hey Coco", "OK Coco", "Coco", "Hi Coco" (can interrupt speech)
- Voice recognition and text-to-speech with selectable voices (male/female, calm and conversational)
- Conversational AI using OpenAI for natural responses and handling interruptions contextually
- User profiles with date of birth and kids mode for ages 12 and under
- Parental controls: Restrict certain content in kids mode, toggle kids mode (adults only)
- Sing songs by reciting lyrics (e.g., "Everything at Once" by Lenka)
- Shopping list management: Add, remove, read items
- Unit conversions (temperature, length, weight)
- Tell stories
- Play games (guess the number)
- Math help
- Get current time and date
- Fetch weather information (location-aware)
- Search Wikipedia
- Play music on YouTube
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

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Get API keys:
   - OpenWeatherMap: Sign up at https://openweathermap.org/api and get your API key.
   - NewsAPI: Sign up at https://newsapi.org/ and get your API key.
   - OpenAI: Sign up at https://openai.com/ and get your API key.

3. Update `config.py` with your API keys.

4. Run the assistant:
   ```
   python main.py
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

This is a basic implementation of a virtual assistant. It does not include advanced features like wake word detection, natural language understanding, IoT integrations, or the full range of services provided by Alexa or Google Assistant. For a more complete assistant, consider using frameworks like Rasa or integrating with AI services like OpenAI's GPT.

The wake word detection is simulated using speech recognition and may not be as efficient as dedicated hardware wake word engines.

Coco Assistant disclaims responsibility for any errors, as it is currently under development.
