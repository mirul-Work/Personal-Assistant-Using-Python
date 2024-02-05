import speech_recognition as sr
import pyttsx3
import datetime
import pyaudio
import json

class PersonalAssistant:
    def __init__(self):
        self.user_data = {}
        self.load_user_data()

    def speak(self, text):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.8)
        engine.say(text)
        engine.runAndWait()

    def get_input_device(self):
        p = pyaudio.PyAudio()
        print("Available input devices:")
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            print(f"{i + 1}. {info['name']}")

        while True:
            try:
                choice = int(input("Select the input device number: "))
                if 1 <= choice <= p.get_device_count():
                    return choice - 1  # Return the index of the selected device
                else:
                    print("Invalid choice. Please enter a valid device number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def listen_microphone(self, device_index):
        recognizer = sr.Recognizer()

        with sr.Microphone(device_index=device_index) as source:
            print(f"Listening using device {device_index}. Say something...")
            self.speak("I am listening go ahead..")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            try:
                audio = recognizer.listen(source)
                print("Audio captured successfully.")
                return audio
            except sr.WaitTimeoutError:
                print("Timeout: No speech detected.")
                return None

    def load_user_data(self):
        try:
            with open('user_data.json', 'r') as file:
                self.user_data = json.load(file)
        except FileNotFoundError:
            # If the file does not exist, initialize user_data as an empty dictionary
            self.user_data = {}

    def save_user_data(self):
        with open('user_data.json', 'w') as file:
            json.dump(self.user_data,file)

    def learn_from_user(self, question):
        self.speak(question)
        user_input = input("Your response: ")
        return user_input

    def main(self):
        print("Welcome to Your Personal Assistant!")

        # Get user's preferred input device
        input_device_index = self.get_input_device()

        while True:
            # Listen to the user
            audio_input = self.listen_microphone(input_device_index)

            # Recognize speech using Google Web Speech API
            recognizer = sr.Recognizer()
            try:
                text = recognizer.recognize_google(audio_input).lower()
                print(f"You said: {text}")

                # Perform actions based on recognized text
                if "hello" in text:
                    self.speak("Hello! How can I assist you today?")
                elif "time" in text:
                    current_time = datetime.datetime.now().strftime("%H:%M")
                    self.speak(f"The current time is {current_time}")
                elif "date" in text:
                    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    self.speak(f"Today's date is {current_date}")
                elif "thank you" in text or "thanks" in text:
                    self.speak("You're welcome!")
                elif "bye" in text:
                    self.speak("Goodbye!")
                    self.save_user_data()
                    break  # Exit the loop on saying "bye"
                else:
                    # Learn from the user and store the information
                    if text not in self.user_data:
                        response = self.learn_from_user("I don't know how to respond. Please teach me.")
                        self.user_data[text] = response
                        print("I have learned from you!")

                    # Provide the learned response
                    if text in self.user_data:
                        self.speak(self.user_data[text])
                    else:
                        self.speak("I'm still learning. Can you please provide more details?")

                    # Ask for the next question
                    self.speak("What else would you like to know?")

            except sr.UnknownValueError:
                print("Sorry, I couldn't understand what you said.")
            except sr.RequestError as e:
                print(f"Error with the speech recognition service; {e}")

if __name__ == "__main__":
    assistant = PersonalAssistant()
    assistant.main()
