import os
import pygame
import speech_recognition as sr
import winsound
from termcolor import colored


class Speak:
    def __init__(self, voice="en-US-EricNeural", female=False, english=True) -> None:

        self.voice = voice
        self.gender = female
        self.language = english

        language_support = {
            "Male English": "en-US-EricNeural",
            "Female English": "en-US-AriaNeural",
            "Male Hindi": "hi-IN-MadhurNeural",
            "Female Hindi": "hi-IN-SwaraNeural",
        }

        if (self.gender == True):
            if (self.language == False):
                self.voice = language_support["Female Hindi"]
            else:
                self.voice = language_support["Female English"]
        else:
            if (self.language == False):
                self.voice = language_support["Male Hindi"]
            else:
                self.voice = language_support["Male English"]

    def say(self, text):

        command = f'edge-tts --voice "{self.voice}" --text "{text}" --write-media "data.mp3"'

        os.system(command)

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("data.mp3")

        try:
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except Exception as e:
            print(e)

        finally:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            os.remove("data.mp3")


class Hear:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def recognize_speech_from_mic(self):
        """Transcribe speech recorded from 'microphone'.

        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was successful
        "error": `None` if no error occured, otherwise a string containing an error message if the API could not be reached or speech was unrecognizable
        "transcription": `None` if speech coul not be transcribed, otherwise a string containing the transcribed text
        """

        # check that recognizer and microphone are appropriate type
        if not isinstance(self.recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be a `Recognizer` instance")

        if not isinstance(self.microphone, sr.Microphone):
            raise TypeError("`microphone` must be a `Microphone` instance")

        # adjust thge recognizer sensitivity to ambient noise and record audio from microphone
        with self.microphone as source:
            winsound.Beep(600, 300)
            print(colored("Listening for audio input..", color="green"))
            self.recognizer.pause_threshold = 1
            self.recognizer.energy_threshold = 150
            audio = self.recognizer.listen(source, phrase_time_limit=4)

        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        try:
            print(colored("Attempting to recognize audio transcript..", color="green"))
            response["transcription"] = self.recognizer.recognize_google(audio)
            winsound.Beep(400, 150)
        except sr.RequestError:
            response["success"] = False
            response["error"] = "API unavailable or is currently unreachable"
        except sr.UnknownValueError:
            response["error"] = "Unable to recognize speech from audio"

        return response
