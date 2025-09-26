import os 
import ssl
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import re
import google.generativeai as genai

# Simple tokenizer function to replace NLTK
def simple_tokenize(text):
    # Convert to lowercase and split by spaces, punctuation
    text = text.lower()
    # Replace punctuation with spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    # Split and remove empty strings
    return [word for word in text.split() if word]

training_data ={
    "greeting": {
        "patterns": ["Hi", "Hello", "Hey", "Good morning"],
        "responses": ["Hello!", "Hi there!", "Hey!", "Good morning!"]
    },
    "goodbye": {
        "patterns": ["Bye", "See you later", "Goodbye"],
        "responses": ["Goodbye!", "See you later!", "Have a great day!"]
    },
    "thanks": {
        "patterns": ["Thank you", "Thanks", "Thank you so much"],
        "responses": ["You're welcome!", "No problem!", "Glad I could help!"]
    },
    "name": {
        "patterns": ["What's your name?", "Who are you?", "Tell me your name"],
        "responses": ["I am your chatbot made by Tahmid"] 
    }
}
patterns =[] 
labels=[]
for intent,intent_data in training_data.items():
    if "patterns" in intent_data:
      for pattern in intent_data["patterns"]:
        patterns.append(pattern)
        labels.append(intent)
vectorizer = TfidfVectorizer(
    tokenizer=simple_tokenize,
    token_pattern=None,
    lowercase=False  # We handle lowercase in our tokenizer
)
X = vectorizer.fit_transform(patterns)
model = LogisticRegression()
model.fit(X, labels)

def gemini_response(user_input):
    # Get API key from Streamlit secrets or environment variable
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except:
        api_key = os.getenv('GEMINI_API_KEY', "AIzaSyBH6Q78afhCBfXsggBl3m6fFJdiUbPzgHM")
    
    if not api_key:
        return "[Gemini API key not set. Please set GEMINI_API_KEY environment variable.]"
    genai.configure(api_key=api_key)
    
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(user_input)
        return response.text.strip()
    except Exception as e:
        error_msg = str(e)
        if "quota" in error_msg.lower() or "429" in error_msg:
            return "I'm currently experiencing high usage. Please try again in a few minutes or ask simpler questions that I can handle with my basic responses."
        elif "404" in error_msg:
            return "Sorry, I'm having trouble accessing my AI capabilities right now. Please try asking basic questions like greetings or thanks."
        else:
            return f"I encountered an error: {e}. Please try asking something else."

# Modify chatbot_response to use Gemini for unknowns
def chatbot_response(user_input):
    X_test = vectorizer.transform([user_input])
    prediction_probabilities = model.predict_proba(X_test)[0]
    max_confidence = max(prediction_probabilities)
    
    # Only use basic responses if confidence is reasonable (above 0.3)
    if max_confidence > 0.3:
        intent = model.predict(X_test)[0]
        if intent in training_data:
            response = training_data[intent]["responses"]
            return random.choice(response)
    
    # Use Gemini for low confidence or any other question
    return gemini_response(user_input)

import streamlit as st

# Streamlit interface
st.set_page_config(page_title="AI Chatbot made by Tahmid", page_icon="🤖")
st.title("🤖 AI Chatbot made by Tahmid")
st.write("Ask me anything! This intelligent chatbot is made by Tahmid and can help with any question.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Type your message here..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get bot response
    response = chatbot_response(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})