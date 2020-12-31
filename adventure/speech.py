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
    return map

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
        print(json_data)

    json_s = json.dumps(json_data)

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Speak command: '.upper())
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        try:
            keywords = load_commands('commands.txt')
            text = r.recognize_sphinx(audio, keyword_entries=keywords)
            #text = r.recognize_sphinx(audio, grammar='counting.gram',keyword_entries=[("south", 1.0), ("north", 1.0), ("east", 1.0),("explore", 1.0)])
            text = text.split("  ")
            return text#[::-1]
        except sr.UnknownValueError:
            print("repeat please".upper())
            synthesis("repeat please")
            return ''
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


        #GC API
        # try:
        #     print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, credentials_json=json_s))
        # except sr.UnknownValueError:
        #     print("Google Cloud Speech could not understand audio")
        # except sr.RequestError as e:
        #     print("Could not request results from Google Cloud Speech service; {0}".format(e))
