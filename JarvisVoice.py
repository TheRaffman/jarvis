import pyttsx3
import os

class JarvisVoice:
    # Variables that only THIS instance can see

    def __init__(self):
        print("Finding installed voices...")
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty("voices")

        for voiceinfo in voices:
            print("  * Found Voice: " + voiceinfo.id)
        voice_id = int(os.environ.get("voice_id"))
        self.engine.setProperty("voice",voices[voice_id].id)
        print("Voice ready")

    def talk(self, text):
        self.engine.say (text)
        self.engine.runAndWait()
