import os
import winsound
import pygame
import speech_recognition as sr
from termcolor import colored


class Speak:
    def __init__(self, gender="female", language="english") -> None:
        """Default Text-to-Speech class.

        Takes 2 optional inputs
        "gender": defaults to `female`. You can change the gender of the TTS by passing a suitable gender value.
        "language": defaults to `english`. You can change the language of the TTS by passing a suitable langauge value.
        """
        self.gender = gender
        self.language = language

        if (self.gender == "female"):
            if (self.language == "hindi"):
                self.voice = "hi-IN-SwaraNeural"
            else:
                self.voice = "en-US-AriaNeural"
        else:
            if (self.language == "hindi"):
                self.voice = "hi-IN-MadhurNeural"
            else:
                self.voice = "en-US-EricNeural"

    def say(self, text):
        """Fetches a `.mp3` file of the text passed.

        Takes 1 input
        "text": The text that is to converted to TTS. Passed as a `string` value.
        """

        os.system(
            f'edge-tts --voice "{self.voice}" --text "{text}" --write-media "data.mp3"')
        print(colored(f"Sara: {text}", color="blue"))

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("data.mp3")

        try:
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except Exception as e:
            print(colored(e, color="red"))

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

        if not isinstance(self.recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be a `Recognizer` instance")

        if not isinstance(self.microphone, sr.Microphone):
            raise TypeError("`microphone` must be a `Microphone` instance")

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
