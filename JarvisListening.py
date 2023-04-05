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
        self.__initialise_offline()
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

    def __initialise_offline(self):
        print("Initialise_offline member variables...")

        # list all audio devices known to your system
        print("Display input/output devices")
        print(sd.query_devices())

        # get the samplerate - this is needed by the Kaldi recognizer
        self.device_info = sd.query_devices(sd.default.device[0], 'input')
        self.samplerate = int(self.device_info['default_samplerate'])

        # display the default input device
        print("===> Initial Default Device Number:{} Description: {}".format(sd.default.device[0], self.device_info))

        # setup queue and callback function
        self.q = queue.Queue()

        # build the model and recognizer objects.
        print("===> Build the model and recognizer objects.  This will take a few minutes.")
        model = Model(os.environ.get("vosk_model_path"))
        self.recognizer = KaldiRecognizer(model, self.samplerate)
        self.recognizer.SetWords(False)

    def recognize_from_microphone_offline(self):
        def recordCallback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            self.q.put(bytes(indata))

        spokenPhrase = "I didn't hear a thing boss"

        try:
            with sd.RawInputStream(dtype='int16',
                                channels=1,
                                callback=recordCallback):
                while True:
                    data = self.q.get()        
                    if self.recognizer.AcceptWaveform(data):
                        recognizerResult = self.recognizer.Result()
                        resultDictionary = json.loads(recognizerResult)
                        if not resultDictionary.get("text", "") == "":
                            resultsJson = json.loads(recognizerResult)
                            spokenPhrase = resultsJson["text"]
                            break

        except Exception as e:
            print(str(e))
        
        return spokenPhrase
