from flask import Flask, request, jsonify
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
engine = pyttsx3.init()

@app.route('/query', methods=['POST'])
def process_query():
    data = request.json
    command = data['query']
    
    # Process the command
    response = process_command(command)
    
    return jsonify({'response': response})

def process_command(command):
    if command.lower() == "give me cited work":
        return get_pubmed_cited_work()
    else:
        return search(command)

def set_terra_voice():
    voices = engine.getProperty('voices')

    # Set Zira voice and adjust rate
    for voice in voices:
        if "Microsoft Zira" in voice.name:
            engine.setProperty('voice', voice.id)
            engine.setProperty('rate', 150)  # Adjust speech rate
            break

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning, Thomas!")
    elif 12 <= hour < 18:
        speak("Good Afternoon, Thomas!")
    else:
        speak("Good Evening, Thomas!")

    intro = """I am Terra, your personal assistant. 
              I'm a highly trained AI created by TerraNovaAI.
              My name was inspired by Thomas Arnold's great-grandmother, 
              whose maiden name was Terranova, meaning 'new terrain' in Italian. 
              I'm here to answer any questions you may have and help solve problems.
              I can teach you languages like Italian, French, and Spanish, 
              as well as programming or web development skills. 
              Just let me know how I can assist you."""
    
    speak(intro)

def listen_command():
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
        return "None"

def get_wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        print(summary)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return None  # Handle disambiguation error
    except Exception as e:
        print("Error in Wikipedia search:", e)
        return None

def google_search(query):
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

def bing_search(query):
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

def search(query):
    set_terra_voice()
    wikipedia_summary = get_wikipedia_summary(query)
    if wikipedia_summary:
        speak(wikipedia_summary)
        return wikipedia_summary

    google_results = google_search(query)
    bing_results = bing_search(query)
    combined_results = google_results + "\n" + bing_results
    speak(combined_results)
    return combined_results

def get_pubmed_cited_work():
    try:
        # Example: Searching for articles citing a specific PMID (PubMed ID)
        base_url = "https://pubmed.ncbi.nlm.nih.gov/"
        # Provide the PubMed ID to search for
        query = "your_pubmed_id_here"
        url = base_url + f"?term=cites%3A{query}"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extracting titles of the articles
        article_titles = [title.text for title in soup.find_all('a', class_='docsum-title')]
        
        return "\n".join(article_titles)
    except Exception as e:
        print("Error in PubMed search:", e)
        return []

def follow_up_question(previous_query):
    if 'who' in previous_query.lower():
        speak("Would you like to know more about the person?")
    elif 'what' in previous_query.lower():
        speak("Is there anything specific you'd like to learn about it?")
    elif 'where' in previous_query.lower():
        speak("Would you like to know more details about the location?")

if __name__ == "__main__":
    greet_user()
    app.run(debug=True)
