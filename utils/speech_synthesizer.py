import winsound
import pygame
import speech_recognition as sr
from termcolor import colored


class Speak:
    def __init__(self) -> None:
        """
        Initializes an instance of the Speak class.
        """

    def say(self, file_to_audio, text):
        """
        Prints the given text and plays an audio file.

        Args:
            file_to_audio (str): The path to the audio file to play.
            text (str): The content of the audio file that needs to be printed.

        Returns:
            None: The method doesn't return anything.

        Raises:
            pygame.error: If there's an error with the pygame module.

        Example:
            >>> speaker = Speak()
            >>> speaker.say('/path/to/audio.mp3', 'Hello, world!')
            Computer: Hello, world!
        """

        print(colored(f"Computer: {text}", color="blue"))

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(file_to_audio)

        try:
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except Exception as e:
            print(colored(e, color="red"))

        finally:
            pygame.mixer.music.stop()
            pygame.mixer.quit()


class Hear:
    def __init__(self) -> None:
        """
        Initializes an instance of the Hear class.

        The constructor creates a Recognizer and a Microphone instance to be used later in the recognize_speech_from_mic() method.
        """
        self.recognizer = sr.Recognizer()
        if not isinstance(self.recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be a `Recognizer` instance")

        self.microphone = sr.Microphone()
        if not isinstance(self.microphone, sr.Microphone):
            raise TypeError("`microphone` must be a `Microphone` instance")

    def recognize_speech_from_mic(self):
        """
        Transcribes speech recorded from the microphone.

        The method prompts the user to speak and records audio from the microphone for up to 4 seconds.
        It then tries to transcribe the audio using the Google Web Speech API through the SpeechRecognition module.
        If the transcription is successful, the method returns a dictionary with the following keys:
        - "success": a boolean indicating whether or not the API request was successful
        - "error": `None` if no error occurred, otherwise a string containing an error message if the API could not be reached or speech was unrecognizable
        - "transcription": `None` if speech could not be transcribed, otherwise a string containing the transcribed text

        If the transcription fails, the method returns a dictionary with "success" set to False and an appropriate error message.
        If the API is unavailable or unreachable, the method also sets "success" to False and returns an error message.

        Raises:
        - TypeError: If the recognizer or microphone instances are not of the expected type.

        Returns:
        - A dictionary containing the transcription, the success status and an error message (if any).
        - The transcription is a string containing the recognized speech, or None if speech could not be transcribed.
        - The success status is a boolean indicating whether or not the API request was successful.
        - The error message is a string containing an error message if the API could not be reached or speech was unrecognizable, or None if no error occurred.

        Example:
        >>> listener = Hear()
        >>> response = listener.recognize_speech_from_mic()
        >>> if response["success"]:
        >>>     print(f"Transcription: {response['transcription']}")
        >>> else:
        >>>     print(f"Error: {response['error']}")
        """

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
