# -*- coding: utf-8 -*-


import speech_recognition as sr
from time import ctime
import time
import os
import subprocess
import threading
from gtts import gTTS
import nltk
from nltk.corpus import stopwords

def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")
    
def startVideo():
    global procid
    procid=subprocess.Popen(['python','Streamer.py'])
    

def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        print("Say something!")
        audio = r.listen(source)
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return data

def jarvis(data):
    print(data)
    if "Aasas" in data:
        speak(ctime())
        
    if "help" in data:
        global x
        x = threading.Thread(target=startVideo, args=())
        x.start()
        # os.system("python Streamer.py")
    if "orange" in data:
        print("oooo")
        global procid
        procid.kill()
     

    
# initialization
speak("hey")
time.sleep(2)
while 1:
    data = recordAudio()
    jarvis(data)