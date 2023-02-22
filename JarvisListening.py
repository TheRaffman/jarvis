import os
import azure.cognitiveservices.speech as speechsdk

class JarvisListening:
    # Variables that only THIS instance can see
    # None yet

    def __init__(self):
        print("I'm Listening")

    def recognize_from_microphone(self):
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
