"""Parse the original PDP ``advent.dat`` file.

Copyright 2010-2015 Brandon Rhodes.  Licensed as free software under the
Apache License, Version 2.0 as detailed in the accompanying README.txt.

"""

import speech_recognition as sr
import pyttsx3
import numpy as np
import pyaudio
# import engineio

def load_commands(filename):
    data = []
    i=0
    for x in open(filename, 'r'):
        data.append(x.replace("\n", ""))

    map = [[] for y in range(len(data))]

    for i in range(len(data)):
        map[i] = (data[i], 1.0)
    data.sort()
    return data

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

    #wczytywanie credentials
    import json
    with open('inlaid-fire-300213-a4809b4c6569.json', 'r') as j:
        json_data = json.load(j)
        # print(json_data)

    json_s = json.dumps(json_data)

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Speak command: '.upper())
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        try:
            text = r.recognize_google_cloud(audio, language="en-GB", credentials_json=json_s, preferred_phrases=["south", "north", "gully"])
            return text
        except sr.UnknownValueError:
            print("repeat please".upper())
            synthesis("repeat please")
            return ''
        except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech service; \n {0}".format(e))
