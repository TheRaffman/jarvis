from JarvisHue import JarvisHue
from JarvisListening import JarvisListening
from JarvisVoice import JarvisVoice
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Hue lights instance and group
raffs_hue = JarvisHue()
raff_bedroom_group_name = 'Raff’s Bedroom'

# listening
listening = JarvisListening()

# Voice
voice = JarvisVoice()

def take_command():
    the_boss = os.environ.get("the_boss")
    voice.talk ("How may I assist you " + the_boss + "?")
    # command = listening.recognize_from_microphone_online()
    command = listening.recognize_from_microphone_offline()
    print("take command heard: " + command)
    return command.lower()

def wait_for_instruction():
    command_was_for_jarvis = False
    while command_was_for_jarvis == False:
        print ("Listening for wake word...")
        command = listening.recognize_from_microphone_offline()
        print("wait_for_instruction heard: " + command)
        command = command.lower()
        if "jarvis" in command:
            command_was_for_jarvis = True
        else:
            print(".", end = '')

    return command_was_for_jarvis

def run_jarvis():
    user_wants_to_continue = True
    wait_for_instruction()
    command = take_command()
    print(command)
    if "play" in command:
        song = command.replace("play", "")
        voice.talk("right away sir")
        voice.talk("playing" + song)
        pywhatkit.playonyt(song)

    elif "google" in command:
        search_item = command.replace("google", "")
        voice.talk("right away sir")
        voice.talk("Googling" + search_item)
        search_google(search_item)

    elif "time" in command:
        now = datetime.datetime.now()
        hour = now.strftime("%I")
        minute = now.strftime("%M")
        ampm = now.strftime("%p")
        time = hour + ":" + minute + "" + ampm
        time = time [1:]
        print (time)
        voice.talk("Sir the current time is" + hour[1] + " " + minute + " " + ampm)

    elif "search" in command:
        query = command.replace("search", "")
        info = wikipedia.summary(query, sentences=2)
        print (info)
        voice.talk (info)

    elif "joke" in command:
        voice.talk(pyjokes.get_joke())

    elif "exit" in command:
        user_wants_to_continue = False

    elif "join bridge" in command:
        raffs_hue.join_hue_bridge()

    elif "lights on" in command:
        raffs_hue.turn_on_group(raff_bedroom_group_name)

    elif "lights off" in command:
        raffs_hue.turn_off_group(raff_bedroom_group_name)

    else:
        voice.talk("Sorry sir i wasn't listening, say that again")
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

print("")
should_i_continue = True
while should_i_continue:
    should_i_continue = run_jarvis()

# User has said exit...
voice.talk("Glad I could help, see you again soon.")
print("Glad I could help, see you again soon.")
