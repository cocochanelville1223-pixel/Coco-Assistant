import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import requests
import json
import random
import pywhatkit
import openai
import threading
import time
import pytz
import geopy
import re
from geopy.geocoders import Nominatim
from config import OPENWEATHER_API_KEY, NEWS_API_KEY, OPENAI_API_KEY

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Profiles
profiles = {}
current_profile = None
kids_mode = False

# Conversation history
conversation_history = []

# Advanced features
timers = []
reminders = []
notes = []
shopping_list = []
user_location = None
speaking = False

def load_profiles():
    """
    Load profiles from the on-disk "profiles.json" file into the module-level `profiles` variable.
    
    If "profiles.json" exists, parse it as JSON and replace the in-memory `profiles` dict with its contents. If the file does not exist, the function leaves `profiles` unchanged.
    """
    global profiles
    if os.path.exists("profiles.json"):
        with open("profiles.json", "r") as f:
            profiles = json.load(f)

def save_profiles():
    """
    Save the in-memory profiles dictionary to "profiles.json".
    
    Writes the current module-level `profiles` mapping to disk in JSON format, overwriting any existing file.
    """
    with open("profiles.json", "w") as f:
        json.dump(profiles, f)

def create_profile(name, dob):
    """
    Create a new user profile and persist it.
    
    Parameters:
        name (str): The profile name/identifier.
        dob (str): The profile's date of birth as a string (e.g., "YYYY-MM-DD").
    
    Description:
        Adds the profile to the module-level profiles mapping, saves profiles to persistent storage, and speaks a confirmation message.
    """
    profiles[name] = {"dob": dob}
    save_profiles()
    speak(f"Profile for {name} created.")

def switch_profile(name):
    """
    Switch the active user profile and update kids mode based on the profile's date of birth.
    
    If a profile with the given name exists in the module-level `profiles` mapping, this function sets `current_profile` to that name, computes the profile's age from the stored `dob` (expected format "YYYY-MM-DD"), sets the module-level `kids_mode` to True when age is less than or equal to 12 (False otherwise), and speaks a confirmation containing the profile name, computed age, and kids-mode status. If the profile is not found, it speaks an error message.
    
    Parameters:
        name (str): The profile name to switch to; must be a key in the module-level `profiles` dict.
    """
    global current_profile, kids_mode
    if name in profiles:
        current_profile = name
        dob = datetime.datetime.strptime(profiles[name]["dob"], "%Y-%m-%d")
        age = (datetime.datetime.now() - dob).days // 365
        kids_mode = age <= 12
        speak(f"Switched to {name}'s profile. Age: {age}. Kids mode: {'on' if kids_mode else 'off'}.")
    else:
        speak("Profile not found.")

def toggle_kids_mode():
    """
    Toggle the global kids_mode flag for the currently selected profile when that profile is older than 12 years.
    
    If a profile is selected and its computed age is greater than 12, flips the module-level `kids_mode` boolean and announces the new state via speech. If the selected profile's age is 12 or younger, announces that only adults may toggle kids mode. If no profile is selected, announces that no profile is selected.
    """
    global kids_mode
    if current_profile:
        dob = datetime.datetime.strptime(profiles[current_profile]["dob"], "%Y-%m-%d")
        age = (datetime.datetime.now() - dob).days // 365
        if age > 12:
            kids_mode = not kids_mode
            speak(f"Kids mode {'enabled' if kids_mode else 'disabled'}.")
        else:
            speak("Only adults can toggle kids mode.")
    else:
        speak("No profile selected.")

def check_kids_mode():
    """
    Indicates whether the assistant is currently operating in kids mode.
    
    Returns:
        bool: `True` if kids mode is enabled, `False` otherwise.
    """
    return kids_mode
    voices = engine.getProperty('voices')
    print("Available voices:")
    for i, voice in enumerate(voices):
        print(f"{i}: {voice.name} ({voice.languages})")
    
    speak("Please choose a voice by saying the number.")
    while True:
        command = listen()
        if command.isdigit():
            index = int(command)
            if 0 <= index < len(voices):
                engine.setProperty('voice', voices[index].id)
                speak(f"Voice set to {voices[index].name}")
                break
            else:
                speak("Invalid number. Try again.")
        else:
            speak("Please say a number.")

def speak(text):
    """
    Speak the given text aloud using the configured TTS engine.
    
    Parameters:
        text (str): The text to be spoken.
    
    Notes:
        Sets the module-level `speaking` flag to True for the duration of playback and resets it to False when speaking finishes.
    """
    global speaking
    speaking = True
    def speak_thread():
        """
        Speak the current text buffer via the TTS engine and mark speaking as finished.
        
        This function invokes the configured TTS engine to vocalize the module-level `text` variable and, when playback completes, sets the module-level `speaking` flag to False to indicate no audio is being played.
        """
        global speaking
        engine.say(text)
        engine.runAndWait()
        speaking = False
    t = threading.Thread(target=speak_thread)
    t.start()

def wake_listen():
    """
    Detects a spoken wake word via the microphone and prompts the user to continue.
    
    If a wake word is heard, stops any ongoing speech playback, speaks "Yes?", and returns True; otherwise returns False.
     
    Returns:
        bool: `True` if a wake word was detected and the assistant prompted the user, `False` otherwise.
    """
    global speaking
    wake_words = ["hey coco", "ok coco", "coco", "hi coco"]
    with sr.Microphone() as source:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            command = recognizer.recognize_google(audio).lower()
            for wake in wake_words:
                if wake in command:
                    if speaking:
                        engine.stop()
                        speaking = False
                    speak("Yes?")
                    return True
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            pass
    return False

def listen():
    """
    Capture audio from the default microphone and return the recognized speech as lowercase text.
    
    If the recognizer cannot understand the audio or the speech service is unavailable, the function returns an empty string and emits a brief spoken apology.
    
    Returns:
        str: Recognized speech converted to lowercase, or an empty string if recognition fails or the speech service is down.
    """
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return ""

def get_time():
    """
    Speak the current local time in 12-hour (H:MM AM/PM) format.
    
    This obtains the system's current local time, formats it as hours and minutes with an AM/PM marker, and speaks the resulting string via the assistant's text-to-speech.
    """
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    speak(f"The current time is {time_str}")

def get_date():
    """
    Speak the current date in the format "Month Day, Year".
    
    The spoken phrase will be "Today's date is <Month> <Day>, <Year>" (for example, "Today's date is January 7, 2026").
    """
    now = datetime.datetime.now()
    date_str = now.strftime("%B %d, %Y")
    speak(f"Today's date is {date_str}")

def get_weather(city="New York"):
    """
    Speak the current weather for a given city.
    
    Queries the OpenWeatherMap API for current conditions and speaks a short summary that includes the temperature in degrees Celsius and a brief weather description. If the API key is not configured or the request fails, speaks an appropriate error message.
    
    Parameters:
        city (str): Name of the city to query (default: "New York").
    """
    if not OPENWEATHER_API_KEY:
        speak("Weather API key not set.")
        return
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        speak(f"The weather in {city} is {description} with a temperature of {temp} degrees Celsius.")
    else:
        speak("Sorry, I couldn't fetch the weather.")

def search_wikipedia(query):
    """
    Speak a two-sentence summary from Wikipedia for the given query.
    
    Parameters:
        query (str): The search term or topic to look up on Wikipedia.
    
    Description:
        Retrieves a two-sentence summary for `query` and speaks it aloud. If no summary can be retrieved or an error occurs, speaks an apology indicating the information could not be found.
    """
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except:
        speak("Sorry, I couldn't find information on that.")

def play_music(song):
    """
    Play a song or search query on YouTube and announce playback.
    
    Parameters:
        song (str): Title or search query to play on YouTube.
    """
    pywhatkit.playonyt(song)
    speak(f"Playing {song} on YouTube")

def tell_joke():
    """
    Play a randomly selected joke aloud.
    
    Selects a joke from a kid-appropriate set when kids mode is enabled; otherwise selects from a general set, then speaks the chosen joke.
    """
    if check_kids_mode():
        jokes = [
            "Why did the chicken cross the road? To get to the other side!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why was the math book sad? Because it had too many problems!"
        ]
    else:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What do you call fake spaghetti? An impasta!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!"
        ]
    joke = random.choice(jokes)
    speak(joke)

def get_news():
    """
    Fetches and speaks the top five US news headlines.
    
    Requires the module-level NEWS_API_KEY to be set. If the API key is missing or the request fails, speaks an appropriate error message instead of headlines.
    """
    if not NEWS_API_KEY:
        speak("News API key not set.")
        return
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data['articles'][:5]
        speak("Here are the top news headlines:")
        for article in articles:
            speak(article['title'])
    else:
        speak("Sorry, I couldn't fetch the news.")

def open_website(site):
    """
    Open a common website based on a keyword found in the provided site string.
    
    Checks the `site` text for known keywords ("google", "youtube", "facebook") and opens the corresponding URL in the default web browser. If no known keyword is present, notifies the user via `speak()`.
    
    Parameters:
        site (str): Keyword or phrase indicating which website to open (e.g., "open youtube", "google").
    """
    if "google" in site:
        webbrowser.open("https://www.google.com")
    elif "youtube" in site:
        webbrowser.open("https://www.youtube.com")
    elif "facebook" in site:
        webbrowser.open("https://www.facebook.com")
    else:
        speak("Sorry, I don't know that website.")

def set_timer(duration):
    """
    Schedule a background timer that announces when the specified duration elapses.
    
    Parameters:
        duration (int | float): Number of seconds to wait before announcing the timer.
    
    Description:
        Starts a background timer (thread) that waits for the given duration and then speaks a notification. The timer thread is recorded in the module-level `timers` list and the function immediately confirms that the timer was set.
    """
    def timer_thread():
        """
        Waits for the configured duration then notifies the user that the timer has finished.
        
        Blocks for the timer duration and, when elapsed, speaks a message announcing that the timer for that many seconds is up.
        """
        time.sleep(duration)
        speak(f"Timer for {duration} seconds is up!")
    t = threading.Thread(target=timer_thread)
    t.start()
    timers.append(t)
    speak(f"Timer set for {duration} seconds.")

def set_reminder(message, delay):
    """
    Schedule a spoken reminder to play after a given delay.
    
    Schedules the provided message to be spoken after `delay` seconds, acknowledges the scheduling immediately, and stores the background reminder handle in the module-level `reminders` list.
    
    Parameters:
        message (str): The reminder text to be spoken when the timer elapses.
        delay (int | float): Seconds to wait before speaking the reminder.
    """
    def reminder_thread():
        """
        Waits for the configured delay interval and then announces the reminder message.
        
        This function sleeps for the outer-scope `delay` (in seconds) and, after waking, invokes the assistant's speech output to say "Reminder: {message}" where `message` is taken from the enclosing scope.
        """
        time.sleep(delay)
        speak(f"Reminder: {message}")
    t = threading.Thread(target=reminder_thread)
    t.start()
    reminders.append(t)
    speak(f"Reminder set for {delay} seconds from now.")

def take_note(note):
    """
    Append a note to the in-memory notes list and persist it to disk.
    
    Parameters:
    	note (str): Text content of the note to store.
    
    Description:
    	Appends `note` to the module-level `notes` list, appends the note followed by a newline to "notes.txt", and invokes `speak` to confirm the action.
    """
    notes.append(note)
    with open("notes.txt", "a") as f:
        f.write(note + "\n")
    speak("Note taken.")

def read_notes():
    """
    Speak all stored user notes aloud.
    
    If any notes exist, speak each note in insertion order; otherwise notify the user that there are no notes.
    """
    if notes:
        speak("Your notes are:")
        for note in notes:
            speak(note)
    else:
        speak("You have no notes.")

def calculate(expression):
    """
    Evaluate a mathematical expression provided as a string and speak the result.
    
    Parameters:
        expression (str): A mathematical expression (for example "2 + 2*3" or "sqrt(9)") to be evaluated; the function will speak the computed value. If the expression cannot be evaluated, the function will speak an error message.
    """
    try:
        result = eval(expression)
        speak(f"The result is {result}")
    except:
        speak("Sorry, I couldn't calculate that.")

def sing_song(song_name):
    """
    Sing a known song by speaking its lyrics aloud.
    
    If the song is recognized, temporarily lowers the TTS speech rate, announces the song, recites stored lyrics, and then restores the original speech rate. If the song is not recognized, speaks a short apology and suggests available titles.
    
    Parameters:
        song_name (str): Title of the song to sing (supported: "everything at once", "happy birthday").
    """
    songs = {
        "everything at once": """
        Something just isn't right
        I'm losing my sight
        But I can't see it
        I'm caught in the fight
        But I don't know it
        I'm feeling the weight
        But I can't take it
        I'm feeling the strain
        But I can't fake it

        Everything at once
        Everything at once
        Everything at once
        Everything at once

        I'm breaking in two
        But I can't undo
        What I've done
        I'm falling apart
        But I can't restart
        What I've become

        Everything at once
        Everything at once
        Everything at once
        Everything at once
        """,
        "happy birthday": """
        Happy birthday to you
        Happy birthday to you
        Happy birthday dear [name]
        Happy birthday to you
        """
    }
    if song_name in songs:
        # Set slower rate for "singing"
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate - 50)
        speak(f"Singing {song_name}.")
        speak(songs[song_name])
        engine.setProperty('rate', rate)  # Reset
    else:
        speak("Sorry, I don't know that song. Try 'everything at once' or 'happy birthday'.")

def add_to_shopping_list(item):
    """
    Add an item to the user's shopping list and announce the addition.
    
    Parameters:
        item (str): Text of the item to add to the shopping list.
    """
    shopping_list.append(item)
    speak(f"Added {item} to shopping list.")

def remove_from_shopping_list(item):
    """
    Remove an item from the in-memory shopping list and notify the user.
    
    If the item exists, removes its first occurrence from the shopping_list and speaks a confirmation message; otherwise speaks that the item was not found.
    
    Parameters:
        item (str): The name of the item to remove from the shopping list.
    """
    if item in shopping_list:
        shopping_list.remove(item)
        speak(f"Removed {item} from shopping list.")
    else:
        speak("Item not found in shopping list.")

def read_shopping_list():
    """
    Speak the current shopping list items aloud.
    
    If the module-level shopping_list contains items, first speak a header ("Your shopping list:") then speak each item in the list. If the list is empty, speak that the shopping list is empty.
    """
    if shopping_list:
        speak("Your shopping list:")
        for item in shopping_list:
            speak(item)
    else:
        speak("Your shopping list is empty.")

def unit_convert(value, from_unit, to_unit):
    """
    Convert a numeric value between supported units and announce the result.
    
    Supported conversions: Celsius <-> Fahrenheit, meters <-> feet, kilograms (kg) <-> pounds (lbs).
    On a supported conversion, the function speaks a formatted message like "X from_unit is Y to_unit."
    If the conversion pair is not supported, the function speaks an apology message.
    
    Parameters:
        value (float|int): The numeric value to convert.
        from_unit (str): The unit of the input value (e.g., "celsius", "meters", "kg").
        to_unit (str): The unit to convert to (e.g., "fahrenheit", "feet", "lbs").
    """
    conversions = {
        ("celsius", "fahrenheit"): lambda x: x * 9/5 + 32,
        ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
        ("meters", "feet"): lambda x: x * 3.28084,
        ("feet", "meters"): lambda x: x / 3.28084,
        ("kg", "lbs"): lambda x: x * 2.20462,
        ("lbs", "kg"): lambda x: x / 2.20462,
    }
    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        result = conversions[key](value)
        speak(f"{value} {from_unit} is {result:.2f} {to_unit}.")
    else:
        speak("Sorry, I don't know that conversion.")

def tell_story():
    """
    Speaks a randomly selected short story.
    
    Chooses one of a small set of predefined short stories and speaks it aloud.
    """
    stories = [
        "Once upon a time, there was a little robot who loved to help people. One day, it met a human who needed directions. The robot used its smart brain to guide the human safely home. And they became best friends forever.",
        "In a faraway land, a brave knight set out on a quest. Along the way, he met talking animals and solved riddles. Finally, he found the treasure: kindness and friendship."
    ]
    story = random.choice(stories)
    speak(story)

def play_game():
    """
    Start an interactive "guess the number" game where the assistant selects a random integer from 1 to 10 and prompts the user to guess it.
    
    The user has up to five attempts. After each guess the assistant responds with "Too low", "Too high", or prompts for a numeric response. If the user guesses correctly the assistant announces the win and ends the game; if all attempts are used, the assistant reveals the chosen number.
    """
    number = random.randint(1, 10)
    speak("I'm thinking of a number between 1 and 10. Guess it!")
    attempts = 0
    while attempts < 5:
        guess = listen()
        if guess.isdigit():
            g = int(guess)
            if g == number:
                speak("Correct! You win.")
                return
            elif g < number:
                speak("Too low.")
            else:
                speak("Too high.")
        else:
            speak("Please say a number.")
        attempts += 1
    speak(f"Sorry, the number was {number}. Better luck next time!")

def math_help(problem):
    """
    Provide step-by-step help for a math problem and speak the explanation aloud.
    
    If an OpenAI API key is configured, the function sends the problem to the assistant, appends the user prompt to the conversation history, speaks the assistant's reply, and preserves the conversation context. If no OpenAI API key is available, the function speaks a message indicating that math help requires an OpenAI key.
    
    Parameters:
        problem (str): The math problem or question expressed as a natural-language string.
    """
    # Simple, use OpenAI for complex
    if OPENAI_API_KEY:
        conversation_history.append({"role": "user", "content": f"Help me with this math problem: {problem}"})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            max_tokens=200
        )
        reply = response.choices[0].message.content
        speak(reply)
    else:
        speak("Math help requires OpenAI key.")

def get_location():
    """
    Obtain the user's city for location-based services.
    
    If a city is not already stored, prompts the user to speak their city and listens for a response, then stores it in the module-level `user_location`.
    
    Returns:
        str or None: The stored city name, or `None` if no location was provided.
    """
    # For demo, use a default or ask
    global user_location
    if not user_location:
        speak("Please say your city for location-based services.")
        city = listen()
        if city:
            user_location = city
    return user_location

def process_command(command):
    """
    Dispatches a parsed voice command to the appropriate assistant action.
    
    Parameters:
        command (str): The recognized user command text to process.
    
    Returns:
        bool: `False` if the assistant should stop running (on "stop" or "exit"), `True` otherwise.
    
    Notes:
        This function performs side effects such as speaking responses, updating global state (e.g., `conversation_history`, profiles, timers, reminders, notes, shopping list), calling external services (weather, news, OpenAI, etc.), and invoking other command handlers based on the command content.
    """
    global conversation_history
    if check_kids_mode():
        restricted = ["news", "open facebook", "open youtube"]  # Example restrictions
        if any(r in command for r in restricted):
            speak("Sorry, that's restricted in kids mode.")
            return True
    if "time" in command:
        get_time()
    elif "date" in command:
        get_date()
    elif "weather" in command:
        city = get_location() or "New York"
        if "in" in command:
            city = command.split("in")[-1].strip()
        get_weather(city)
    elif "wikipedia" in command or "search" in command:
        query = command.replace("wikipedia", "").replace("search", "").strip()
        search_wikipedia(query)
    elif "play" in command:
        song = command.replace("play", "").strip()
        play_music(song)
    elif "joke" in command:
        tell_joke()
    elif "news" in command:
        get_news()
    elif "open" in command:
        site = command.replace("open", "").strip()
        open_website(site)
    elif "change voice" in command:
        select_voice()
    elif "set timer" in command:
        # Parse duration, e.g., "set timer for 5 minutes"
        import re
        match = re.search(r'(\d+)\s*(second|minute|hour)s?', command)
        if match:
            num = int(match.group(1))
            unit = match.group(2)
            if unit == "minute":
                num *= 60
            elif unit == "hour":
                num *= 3600
            set_timer(num)
        else:
            speak("Please specify duration, like 'set timer for 5 minutes'")
    elif "remind me" in command:
        # Parse, e.g., "remind me to call mom in 10 minutes"
        parts = command.split("to")
        if len(parts) > 1:
            message = parts[1].strip()
            match = re.search(r'in (\d+)\s*(second|minute|hour)s?', command)
            if match:
                num = int(match.group(1))
                unit = match.group(2)
                if unit == "minute":
                    num *= 60
                elif unit == "hour":
                    num *= 3600
                set_reminder(message, num)
            else:
                speak("Please specify time, like 'remind me to call mom in 10 minutes'")
        else:
            speak("What should I remind you about?")
    elif "take a note" in command or "note" in command:
        note = command.replace("take a note", "").replace("note", "").strip()
        take_note(note)
    elif "read notes" in command:
        read_notes()
    elif "calculate" in command or "what is" in command:
        expr = command.replace("calculate", "").replace("what is", "").strip()
        calculate(expr)
    elif "translate" in command:
        text = command.replace("translate", "").strip()
        translate(text)
    elif "read recipe" in command:
        if check_kids_mode():
            speak("In kids mode, recipes are simplified.")
        recipe = command.replace("read recipe", "").replace("for", "").strip()
        read_recipe(recipe)
    elif "sing" in command:
        song = command.replace("sing", "").strip()
        sing_song(song)
    elif "add to shopping list" in command:
        item = command.replace("add to shopping list", "").strip()
        add_to_shopping_list(item)
    elif "remove from shopping list" in command:
        item = command.replace("remove from shopping list", "").strip()
        remove_from_shopping_list(item)
    elif "read shopping list" in command:
        read_shopping_list()
    elif "convert" in command:
        # Parse e.g., "convert 10 celsius to fahrenheit"
        parts = command.replace("convert", "").strip().split(" to ")
        if len(parts) == 2:
            from_part = parts[0].split()
            to_unit = parts[1]
            if len(from_part) >= 2:
                value = float(from_part[0])
                from_unit = " ".join(from_part[1:])
                unit_convert(value, from_unit, to_unit)
            else:
                speak("Please specify value and units, like 'convert 10 celsius to fahrenheit'")
        else:
            speak("Please say 'convert [value] [from] to [to]'")
    elif "tell a story" in command:
        tell_story()
    elif "play a game" in command:
        play_game()
    elif "help with math" in command:
        problem = command.replace("help with math", "").strip()
        math_help(problem)
    elif "create profile" in command:
        # Parse name and dob
        parts = command.replace("create profile", "").strip().split("born on")
        if len(parts) == 2:
            name = parts[0].strip()
            dob = parts[1].strip()
            create_profile(name, dob)
        else:
            speak("Please say 'create profile [name] born on [YYYY-MM-DD]'")
    elif "switch to profile" in command:
        name = command.replace("switch to profile", "").strip()
        switch_profile(name)
    elif "toggle kids mode" in command:
        toggle_kids_mode()
    elif "stop" in command or "exit" in command:
        speak("Goodbye!")
        return False
    else:
        # Use OpenAI for conversational response
        if OPENAI_API_KEY:
            conversation_history.append({"role": "user", "content": command})
            messages = conversation_history.copy()
            if check_kids_mode():
                messages.insert(0, {"role": "system", "content": "You are a friendly assistant for kids. Keep responses simple, fun, and safe. Avoid adult topics."})
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=150
                )
                reply = response.choices[0].message.content
                conversation_history.append({"role": "assistant", "content": reply})
                speak(reply)
            except Exception as e:
                speak("Sorry, I couldn't process that.")
        else:
            speak("Sorry, I don't understand that command.")
    return True

def main():
    """
    Initialize the voice assistant and run its wake-word driven main loop.
    
    Loads saved profiles, selects the voice, announces readiness, then repeatedly waits for the wake word, listens for a command, and dispatches it to the command processor until a stop/exit command ends the loop.
    """
    load_profiles()
    select_voice()
    speak("Coco Assistant is ready. Say a wake word like 'Hey Coco' to start.")
    running = True
    while running:
        if wake_listen():
            command = listen()
            if command:
                running = process_command(command)

if __name__ == "__main__":
    main()