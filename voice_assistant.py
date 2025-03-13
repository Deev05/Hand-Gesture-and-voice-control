import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import pywhatkit
import datetime
from fuzzywuzzy import process

class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 2.0)  # Volume
        self.commands = {
            "open instagram": "Open Instagram",
            "play music": "Play Music",
            "search for": "Search Online",
            "send whatsapp message": "Send WhatsApp Message",
            "what time is it": "Get Time",
            "shutdown": "Shutdown System",
            "restart": "Restart System",
            "write a note": "Write Note",
            "show notes": "Show Notes",
            "open browser": "Open Browser",
            "close program": "Close Program",
        }
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8  # Set the pause threshold (time after speech to wait)
        self.recognizer.non_speaking_duration = 0.5  # Max time before ending the session
        self.microphone = sr.Microphone()


    def speak(self, text):
        """Converts text to speech."""
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with self.microphone as source:
            print("Listening for a command...")
            self.recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            try:
                audio = self.recognizer.listen(source, timeout=5)  # Set timeout to avoid indefinite waiting
                command = self.recognizer.recognize_google(audio)
                print(f"Command: {command}")
                return command
            except sr.WaitTimeoutError:
                print("No speech detected. Please try again.")
                return None
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return None
            except sr.UnknownValueError:
                print("Sorry, I could not understand your speech.")
                return None

    def match_command(self, input_command):
        """Matches the user's command to a known command."""
        best_match = process.extractOne(input_command, self.commands.keys())
        if best_match and best_match[1] > 70:  # Threshold for match confidence
            return best_match[0]
        return None

    def perform_task(self, command):
        """Performs tasks based on matched command."""
        matched_command = self.match_command(command)
        if matched_command is None:
            self.speak("I didn't understand that command.")
            return

        if matched_command == "open instagram":
            self.speak("Opening Instagram.")
            webbrowser.open("https://www.instagram.com")
        elif matched_command == "play music":
            self.speak("What song should I play?")
            song = self.listen()
            if song:
                self.speak(f"Playing {song}.")
                pywhatkit.playonyt(song)
        elif matched_command == "search for":
            query = command.replace("search for", "").strip()
            self.speak(f"Searching for {query}.")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        elif matched_command == "send whatsapp message":
            self.speak("Who should I send it to?")
            number = input("Enter the number (with country code): ")
            self.speak("What should I say?")
            message = self.listen()
            if message:
                self.speak(f"Sending message to {number}.")
                pywhatkit.sendwhatmsg_instantly(number, message)
        elif matched_command == "what time is it":
            now = datetime.datetime.now()
            time_string = now.strftime("%H:%M")
            self.speak(f"The time is {time_string}.")
        elif matched_command == "shutdown":
            self.speak("Shutting down the system.")
            os.system("shutdown /s /t 1")
        elif matched_command == "restart":
            self.speak("Restarting the system.")
            os.system("shutdown /r /t 1")
        elif matched_command == "write a note":
            self.speak("What should I write?")
            note = self.listen()
            with open("notes.txt", "a") as file:
                file.write(f"{note}\n")
            self.speak("Note saved.")
        elif matched_command == "show notes":
            if os.path.exists("notes.txt"):
                with open("notes.txt", "r") as file:
                    notes = file.read()
                    self.speak("Here are your notes.")
                    print(notes)
            else:
                self.speak("You don't have any notes.")
        elif matched_command == "open browser":
            self.speak("Opening browser.")
            webbrowser.open("https://www.google.com")
        elif matched_command == "close program":
            self.speak("Goodbye!")
            exit()

