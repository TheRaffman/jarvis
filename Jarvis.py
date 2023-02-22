import azure.cognitiveservices.speech as speechsdk
from phue import Bridge
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
bridge_ip_address = os.environ.get("bridge_ip_address")
hue_bridge = Bridge(bridge_ip_address)

print("")
print("Finding installed voices...")
engine = pyttsx3.init('sapi5')
voices = engine.getProperty("voices")

for voiceinfo in voices:
    print("  * Found Voice: " + voiceinfo.id)
voice_id = int(os.environ.get("voice_id"))
engine.setProperty("voice",voices[voice_id].id)

print("")
print("Finding Hue lights...")
lights = hue_bridge.get_light_objects('name')
for light in lights:
    print("  * Found light: " + light)

print("")
print("Finding Hue light groups...")
raff_bedroom_group_name = 'Raff’s Bedroom'
light_groups = hue_bridge.get_group()
for light_group in light_groups:
    print("  * Found light group with ID: " + light_group + " and name: " + light_groups[light_group]['name'])
    if (light_groups[light_group]['name'] == raff_bedroom_group_name):
        raff_bedroom_group_id = light_group
        print("    >> Found and stored Raff’s Bedroom (" + raff_bedroom_group_id + ")")

def join_hue_bridge():
    hue_bridge.connect()
    print("Hue bridge is now connected.")

def control_hue():
    print("ok")

def talk(text):
    engine.say (text)
    engine.runAndWait()

def take_command():
    the_boss = os.environ.get("the_boss")
    talk ("How may I assist you " + the_boss + "?")
    command = recognize_from_microphone()
    print("take command heard: " + command)
    return command.lower()

def wait_for_instruction():
    command_was_for_jarvis = False
    while command_was_for_jarvis == False:
        print ("Listening for wake word...")
        command = recognize_from_microphone()
        print("wait_for_instruction heard: " + command)
        command = command.lower()
        if "jarvis" in command:
            command_was_for_jarvis = True
        else:
            print(".", end = '')

    return command_was_for_jarvis

def recognize_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    azure_cognitiveservices_key = os.environ.get("azure_cognitiveservices_key")
    speech_config = speechsdk.SpeechConfig(subscription=azure_cognitiveservices_key, region="uksouth")
    speech_config.speech_recognition_language="en-GB"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        return (speech_recognition_result.text)
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

def run_jarvis():
    user_wants_to_continue = True
    wait_for_instruction()
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

    elif "join bridge" in command:
        join_hue_bridge()

    elif "light on" in command:
        raffs_bedroom = hue_bridge.get_group_id_by_name("Raff's Bedroom")
        raffs_bedroom.on = True

    elif "light off" in command:
        #lights["Raff main"].on = False
        raffs_bedroom = hue_bridge.get_group_id_by_name("Raff's Bedroom")
        raffs_bedroom.on = False

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



print("")
should_i_continue = True
#while should_i_continue:
#    should_i_continue = run_jarvis()

lights_in_group = hue_bridge.get_group(raff_bedroom_group_name, 'lights')
for light in lights_in_group:
    hue_bridge.set_light(int(light), 'on', True)

# User has said exit...
talk("Glad I could help, see you again soon.")
print("Glad I could help, see you again soon.")
