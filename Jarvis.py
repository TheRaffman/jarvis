import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
import os
from dotenv import load_dotenv
load_dotenv()

listener = sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)

def talk(text):
    engine.say (text)
    engine.runAndWait()

def take_command():
    command_was_for_jarvis = False
    try:
        with sr.Microphone() as source:
            the_boss = os.environ.get("the_boss")
            talk ("How may I assist you " + the_boss + "?")
            while command_was_for_jarvis == False:
                print ("Listening...")            
                voice = listener.listen(source)
                command = listener.recognize_google(voice)
                command = command.lower()
                if "jarvis" in command:
                    command_was_for_jarvis = True
                    command = command.replace("jarvis", "")
                    print(command)
                else:
                    print("This command wasn't for Jarvis")

    except AssertionError as error:
        print("Exception in 'take_command' " + error)
        pass
    return command

def run_jarvis():
    user_wants_to_continue = True
    command = take_command()
    print(command)
    if "play" in command:
        song = command.replace("play", "")
        talk("right away sir")
        talk("playing" + song)
        pywhatkit.playonyt(song)

    elif "google" in command:
        search_item = command.replace("google", "")
        talk("right away sir")
        talk("Googling" + search_item)
        search_google(search_item)

    elif "time" in command:
        now = datetime.datetime.now()
        hour = now.strftime("%I")
        minute = now.strftime("%M")
        ampm = now.strftime("%p")
        time = hour + ":" + minute + "" + ampm
        time = time [1:]
        print (time)
        talk("Sir the current time is" + hour[1] + " " + minute + " " + ampm)

    elif "search" in command:
        query = command.replace("search", "")
        info = wikipedia.summary(query, sentences=2)
        print (info)
        talk (info)

    elif "joke" in command:
        talk(pyjokes.get_joke())

    elif "exit" in command:
        user_wants_to_continue = False

    else:
        talk("Sorry sir i wasn't listening, say that again")
        print("Sorry sir i wasn't listening, say that again")

    return user_wants_to_continue

def search_google (search_item):
    url = "https://www.google.com/search?q=" + search_item

    response = requests.get(url)

    if response.status_code == 200:
        # Success! Do something with the response data.
        data = response.text
        print(data)
    else:
        # Handle the error.
        print("An error occurred:", response.status_code)

# Main loop
openai_key = os.environ.get("openai_key")

should_i_continue = True
while should_i_continue:
    should_i_continue = run_jarvis()

# User has said exit...
talk("Glad I could help, see you again soon.")
print("Glad I could help, see you again soon.")
