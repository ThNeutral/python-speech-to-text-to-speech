import time
import os
import glob
import pyttsx3
import speech_recognition as sr
from pygame import mixer, _sdl2 as devices

# mixer.init()
# print("Outputs:", devices.audio.get_audio_device_names(False))
# mixer.quit()

mixer.init(devicename='Line 1 (Virtual Audio Cable)')

recognizer = sr.Recognizer()
microphone = sr.Microphone()
with microphone as source:
    recognizer.adjust_for_ambient_noise(source)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 170)
engine.setProperty('voice', voices[1].id)
i = 0
try:
    with microphone as source:
        while True:
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio, language="ru-RU")
                print("Google Speech Recognition thinks you said " + text)
                path = 'speech{}.wav'.format(i)
                engine.save_to_file(text, path)
                engine.runAndWait()

                mixer.music.load(path)
                mixer.music.play()
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            i = i + 1
            time.sleep(0.1)
except KeyboardInterrupt:
    for f in glob.glob("speech*.wav"):
        try:
            os.remove(f)
        except PermissionError:
            time.sleep(1)
            os.remove(f)