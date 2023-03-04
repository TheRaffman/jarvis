import os
import azure.cognitiveservices.speech as speechsdk
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import sys
import json

class JarvisListening:
    # Variables that only THIS instance can see
    # None yet

    def __init__(self):
        print("I'm Listening")

    def recognize_from_microphone_online(self):
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

    def recognize_from_microphone_offline(self):
        # list all audio devices known to your system
        print("Display input/output devices")
        print(sd.query_devices())

        # get the samplerate - this is needed by the Kaldi recognizer
        device_info = sd.query_devices(sd.default.device[0], 'input')
        samplerate = int(device_info['default_samplerate'])

        # display the default input device
        print("===> Initial Default Device Number:{} Description: {}".format(sd.default.device[0], device_info))

        # setup queue and callback function
        q = queue.Queue()

        def recordCallback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            q.put(bytes(indata))

        # build the model and recognizer objects.
        print("===> Build the model and recognizer objects.  This will take a few minutes.")
        model = Model(r"C:\Users\peter\.cache\vosk\vosk-model-small-en-us-0.15")
        recognizer = KaldiRecognizer(model, samplerate)
        recognizer.SetWords(False)

        print("===> Begin recording. Press Ctrl+C to stop the recording ")
        try:
            with sd.RawInputStream(dtype='int16',
                                channels=1,
                                callback=recordCallback):
                while True:
                    data = q.get()        
                    if recognizer.AcceptWaveform(data):
                        recognizerResult = recognizer.Result()
                        # convert the recognizerResult string into a dictionary  
                        resultDict = json.loads(recognizerResult)
                        if not resultDict.get("text", "") == "":
                            print(recognizerResult)
                        else:
                            print("no input sound")

        except KeyboardInterrupt:
            print('===> Finished Recording')
        except Exception as e:
            print(str(e))
