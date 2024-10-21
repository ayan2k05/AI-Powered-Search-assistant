#this Voice assistant is made by Ayan Pathan(B.Tech AI&DS Modi institute of technology), Aasma ansari(B.Sc Physics)[Passionate about NLP]
#voice assistant is nothing more than a project for us
#You can clone this repository, Express your reviews
#to be honest we just wanted to make extraction and Main Context extractor from Google and Wikipedia Searches
#I used ChatGPT-neo because i dont have api key of chatgpt3/4
#install the requirement.txt file and install the following libraries
#pip install -r requirements.txt



import pyttsx3
import datetime
import wikipedia
from googlesearch import search as google_search
import tensorflow as tf
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

LOG_FILE = "user_search_log.txt"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def log_search(query, response):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"Query: {query}\nResponse: {response}\nTimestamp: {datetime.datetime.now()}\n\n")

def get_input():
    user_input = input("Write your Query (or 'q' to quit): ")
    print(f"Searching for: {user_input}\n")
    return user_input

def wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        print("Good Morning Sir")
        speak("Good Morning Sir!")
    elif 12 <= hour < 17:
        print("Good Afternoon Sir")
        speak("Good Afternoon Sir!")
    elif 17 <= hour < 21:
        print("Good Evening Sir")
        speak("Good Evening Sir!")
    else:
        print("Good night Sir")
        speak("Good night Sir!")

def search_wikipedia(query):
    try:
        print(f"Searching Wikipedia for {query}...")
        result = wikipedia.summary(query, sentences=2)
        print(result)
        speak(result)
        log_search(query, result)
    except Exception as e:
        error_msg = f"Could not find any Wikipedia results for {query}. Error: {e}"
        print(error_msg)
        speak("I couldn't find any information on Wikipedia.")
        log_search(query, error_msg)

def search_google_and_read(query):
    print(f"Searching Google for {query}...")
    speak(f"Searching Google for {query}")
    try:
        results = google_search(query, num_results=3)
        for idx, result in enumerate(results, start=1):
            print(f"Fetching content from result {idx}: {result}")
            page_content = extract_content(result)
            if page_content:
                print(f"Summary of result {idx}:\n{page_content}")
                speak(f"Here is what I found in result {idx}. {page_content}")
                log_search(query, page_content)
                break
    except Exception as e:
        error_msg = f"An error occurred while searching Google: {e}"
        print(error_msg)
        speak("I encountered an error while searching Google.")
        log_search(query, error_msg)

def extract_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text_content = ' '.join([para.get_text() for para in paragraphs[:8]])
        text_content = ' '.join(text_content.split())
        return text_content if text_content else "I couldn't extract readable content from the page."
    
    except Exception as e:
        print(f"Failed to extract content from {url}. Error: {e}")
        return None

def process_tensorflow():
    print("TensorFlow example: Adding two constants")
    a = tf.constant(5.0)
    b = tf.constant(6.0)
    result = a + b
    
    print(f"The result of adding 5.0 and 6.0 is: {result.numpy()}")

def generate_ai_response(prompt):
    detailed_prompt = f"Respond to the following user query concisely: {prompt}"
    response = generator(detailed_prompt, max_length=150, num_return_sequences=1)
    return response[0]['generated_text']

if __name__ == "__main__":
    wish()
    while True:
        user_input = get_input().lower()
        if user_input == 'q':
            print("Goodbye!")
            speak("Goodbye!")
            break

        if 'time' in user_input:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strtime)
            speak(f"Sir, the time is {strtime}")

        elif user_input.startswith("search") or user_input.startswith("find"):
            search_term = user_input.replace('search', '').replace('find', '').strip()
            search_google_and_read(search_term)

        elif 'ai' in user_input or 'AI' in user_input:
            prompt = user_input.replace('ai', '').replace('AI', '').strip()
            ai_response = generate_ai_response(prompt)
            print(ai_response)
            speak(ai_response)
            log_search(prompt, ai_response)

        else:
            search_wikipedia(user_input)

        if 'tensorflow' in user_input:
            process_tensorflow()
