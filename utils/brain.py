import os
import nltk
from neuralintents import GenericAssistant
from termcolor import colored

from utils.speech_synthesizer import Speak


class Brain:
    def __init__(self) -> None:
        self.speaker = Speak(female=True, english=True)

    def run(self):
        self.speaker.say("Initializing system!")
        PATH = f'{os.getcwd()}\data'

        nltk.data.path = [PATH]
        print(colored(f'PATHS found: {nltk.data.path}', "green"))
        try:
            nltk.download('punkt', download_if_missing=True)
            nltk.download('wordnet', download_if_missing=True)
        except Exception as e:
            print(colored("The 'punkt' and 'wordnet' data package already exists.", "yellow"))

        assistant = GenericAssistant('intents.json')
        assistant.train_model()
        assistant.save_model()

        done = False
        self.speaker.say("System initialization completed!")
        self.speaker.say("System is up and running!")

        while not done:
            message = input("Enter a message: ")
            if message == "exit":
                done = True
            else:
                transcript = assistant.request(message)
                print(transcript)
                self.speaker.say(transcript)
