import cv2
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import requests
from bs4 import BeautifulSoup
import shazamio

class Terra:
    def __init__(self):
        self.engine = self.set_voice()
        self.memory = {}
        self.shazam = shazamio.Shazam()

    def set_voice(self):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        # Set Zira voice and adjust rate
        for voice in voices:
            if "Microsoft Zira" in voice.name:
                engine.setProperty('voice', voice.id)
                engine.setProperty('rate', 150)  # Adjust speech rate
                break

        return engine

    def speak(self, audio):
        # Add excitement and enthusiasm to Terra's voice
        self.engine.say(audio)
        self.engine.runAndWait()

        # Check if user wants to interrupt
        while True:
            interrupt = self.listen_command()
            if 'stop speaking' in interrupt.lower():
                self.speak("Okay, I'm sorry for rambling. I'll shut up for now.")
                break
            elif 'stop' in interrupt.lower():
                self.speak("Goodbye, Thomas!")
                exit()  # Exiting the program if the user wants to stop completely

    def greet_user(self):
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.speak("Good Morning, Thomas!")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon, Thomas!")
        else:
            self.speak("Good Evening, Thomas!")

        intro = """I am Terra, your personal assistant. 
                  I'm a highly trained AI created by TerraNova AI.
                  My name was inspired by Thomas Arnold's great-grandmother, 
                  whose maiden name was Terranova, meaning 'new terrain' in Italian. 
                  I'm here to answer any questions you may have and help solve problems.
                  I can teach you languages like Italian, French, and Spanish, 
                  as well as programming or web development skills. 
                  Just let me know how I can assist you."""
        
        self.speak(intro)

    def listen_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()
        except Exception as e:
            print(e)
            print("Say that again, please...")
            return ""

    def get_wikipedia_summary(self, query):
        try:
            summary = wikipedia.summary(query, sentences=2)
            print(summary)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            return None  # Handle disambiguation error
        except Exception as e:
            print("Error in Wikipedia search:", e)
            return None

    def google_search(self, query):
        try:
            url = f"https://www.google.com/search?q={query}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            snippets = soup.find_all('span', class_='hgKElc')
            results = [snippet.get_text() for snippet in snippets]
            return '\n'.join(results[:3])  # Get the first 3 search results
        except Exception as e:
            print("Error in Google search:", e)
            return ""

    def bing_search(self, query):
        try:
            url = f"https://www.bing.com/search?q={query}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            snippets = soup.find_all('p')
            results = [snippet.get_text() for snippet in snippets]
            return '\n'.join(results[:3])  # Get the first 3 search results
        except Exception as e:
            print("Error in Bing search:", e)
            return ""

    def search(self, query):
        try:
            # Search on Wikipedia
            wikipedia_summary = self.get_wikipedia_summary(query)
            if wikipedia_summary:
                self.speak(wikipedia_summary)
                return

            # Search on Google
            google_results = self.google_search(query)
            
            # Search on Bing
            bing_results = self.bing_search(query)

            # Combine and summarize results
            combined_results = google_results + "\n" + bing_results
            self.speak(combined_results)
        except Exception as e:
            print("Error:", e)

    def calculate(self, query):
        try:
            result = eval(query)
            self.speak(f"The result is {result}")
        except Exception as e:
            self.speak("Sorry, I couldn't calculate that.")

    def follow_up_question(self, previous_query):
        if 'who' in previous_query.lower():
            self.speak("Would you like to know more about the person?")
        elif 'what' in previous_query.lower():
            self.speak("Is there anything specific you'd like to learn about it?")
        elif 'where' in previous_query.lower():
            self.speak("Would you like to know more details about the location?")

    def remember_question(self, query):
        if query not in self.memory:
            self.memory[query] = 1
        else:
            self.memory[query] += 1

    def recognize_song(self):
        with sr.Microphone() as source:
            print("Listening to the music lyrics...")
            r = sr.Recognizer()
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        try:
            print("Recognizing the song...")
            result = self.shazam.recognize_song(audio)
            if result['track']:
                return result['track']['title'], result['track']['subtitle']
            else:
                return None, None
        except Exception as e:
            print("Error recognizing the song:", e)
            return None, None

    def turn_on_camera(self):
        camera = cv2.VideoCapture(0)  # Access the default camera (usually webcam)
        while True:
            ret, frame = camera.read()  # Read a frame from the camera
            if ret:
                cv2.imshow('Terra Vision', frame)  # Display the frame
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                break
        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    terra = Terra()
    terra.greet_user()
    
    while True:
        query = terra.listen_command()

        if query:
            if query.lower() == "give me cited work":
                pubmed_id = input("Enter the PubMed ID: ")
                cited_work = terra.get_pubmed_cited_work(pubmed_id)
               
                if cited_work:
                    terra.speak("Here are the cited works:")
                    terra.speak(cited_work)
                else:
                    terra.speak("No cited works found for the given PubMed ID.")
            elif query.lower().startswith("calculate"):
                terra.calculate(query.split("calculate")[1].strip())
            elif 'what song is playing' in query.lower():
                song_title, artist = terra.recognize_song()
                if song_title and artist:
                    terra.speak(f"The song playing is {song_title} by {artist}.")
                else:
                    terra.speak("Sorry, I couldn't recognize the song.")
            elif 'use vision' in query.lower():
                terra.speak("Turning on Terra Vision. Please allow camera access.")
                terra.turn_on_camera()
            else:
                terra.search(query)
                terra.remember_question(query)
                terra.follow_up_question(query)

        elif 'terra' in query.lower():
            terra.speak("Yes?")

        elif 'stop speaking' in query.lower():
            terra.speak("Okay, I'm sorry for rambling.")

        elif 'stop' in query.lower():
            terra.speak("Goodbye, Thomas!")
            break
