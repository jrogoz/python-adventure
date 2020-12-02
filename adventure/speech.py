"""Parse the original PDP ``advent.dat`` file.

Copyright 2010-2015 Brandon Rhodes.  Licensed as free software under the
Apache License, Version 2.0 as detailed in the accompanying README.txt.

"""

import speech_recognition as sr
import pyttsx3
import numpy as np
import pyaudio
# import engineio

def synthesis(text):

    text = text.replace("\n", " ")

    engineio = pyttsx3.init()

    voices = engineio.getProperty('voices')
    engineio.setProperty('rate', 130)
    engineio.setProperty('voice', voices[1].id)  # 0 - polski, 1 - angielski

    sentence = text

    engineio.say(sentence)
    engineio.runAndWait()

def recognition():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Speak command: '.upper())
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            return text
        except:
            print("repeat please".upper())
            synthesis("repeat please")
            return ''

