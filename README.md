# AI Chatbot made by Tahmid

An intelligent chatbot built with Python, Streamlit, and Google Gemini AI that can handle both basic conversations and complex questions.

## Features

- 🤖 **Smart Responses**: Uses machine learning to classify user intents
- 🧠 **AI Integration**: Powered by Google Gemini for complex questions
- 💬 **Basic Conversations**: Handles greetings, thanks, name questions, and goodbyes
- 🎯 **Confidence-based Routing**: Automatically decides between basic responses and AI responses
- 🌐 **Web Interface**: Clean and user-friendly Streamlit interface

## How it Works

1. **Basic Patterns**: For simple greetings, thanks, etc., uses pre-defined responses
2. **AI Fallback**: For complex questions, uses Google Gemini AI
3. **Smart Classification**: Uses TF-IDF vectorization and Logistic Regression to classify user intents

## Demo

Try asking:
- "Hi" or "Hello" → Basic greeting response
- "Thank you" → Basic thanks response  
- "What is machine learning?" → AI-powered detailed response
- "Tell me a joke" → AI-generated joke

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ai-chatbot.git
cd ai-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Google Gemini API key:
   - Get an API key from [Google AI Studio](https://aistudio.google.com/)
   - Replace the API key in `chatbot.py` line 50

4. Run the application:
```bash
streamlit run chatbot.py
```

## Deployment

This chatbot can be deployed on:
- **Streamlit Cloud** (Recommended)
- **Heroku**
- **Railway**
- **Render**

## Technologies Used

- **Python** - Core programming language
- **Streamlit** - Web framework for the UI
- **scikit-learn** - Machine learning for intent classification
- **Google Gemini AI** - Advanced AI responses
- **TF-IDF Vectorizer** - Text processing and feature extraction

## Author

**Tahmid** - AI Chatbot Developer

## License

This project is open source and available under the MIT License.