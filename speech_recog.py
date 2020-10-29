"""
Reference:
https://realpython.com/python-speech-recognition/
"""

import speech_recognition as sr
import sys

r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    while True:
        print("Say something!")
        audio = r.listen(source)
        text = ""

        try:
            text = r.recognize_google(audio)
            print("Recognizing ...")
            print(f"You said: {text}")
        except sr.UnknownValueError:
            print("You said is not identified correctly")

        if text == "exit":
            sys.exit(0)
