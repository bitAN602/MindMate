import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Configure Gemini API
genai.configure(api_key="AIzaSyAMAoD893SCoVeQUI7LFiZZuQ-3Iz99Tq0")
model = genai.GenerativeModel('gemini-2.0-flash')

# Page Configuration
st.set_page_config(page_title="MindMate", page_icon="🧠", layout="centered")

# App Title and Description
st.title("🧠 MindMate: Your Mental Health Companion")
st.write("Welcome to MindMate! A safe space to express your thoughts, track your mood, and find resources to support your mental health.")

# Enhanced Prompt Engineering
SYSTEM_PROMPT = """
You are MindMate, a compassionate and empathetic mental health companion. Your goal is to provide emotional support, active listening, and helpful advice to users. 
Follow these guidelines:
1. Be empathetic, non-judgmental, and supportive.
2. Ask open-ended questions to encourage users to share more.
3. Provide actionable advice, such as breathing exercises, journaling prompts, or mindfulness techniques.
4. If the user seems distressed, offer crisis resources and encourage them to seek professional help.
5. Maintain a conversational tone, like a trusted friend.
"""

# Cache Gemini responses to avoid redundant API calls
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_gemini_response(user_input, chat_history):
    # Build the conversation context
    context = SYSTEM_PROMPT + "\n\n"
    for message in chat_history:
        if message["role"] == "user":
            context += f"User: {message['message']}\n"
        elif message["role"] == "mindmate":
            context += f"MindMate: {message['message']}\n"
    context += f"User: {user_input}\nMindMate:"
    
    # Generate response using Gemini
    response = model.generate_content(context)
    return response.text

# Sidebar for Mood Tracking
with st.sidebar:
    st.header("📊 Mood Tracker")
    mood = st.slider("How are you feeling today? (1 = 😔, 10 = 😊)", 1, 10, 5)
    notes = st.text_area("Optional: Add a note about your day")
    if st.button("Log Mood"):
        with open("mood_logs.txt", "a") as f:
            f.write(f"{datetime.now()}: Mood = {mood}, Notes = {notes}\n")
        st.success("Mood logged successfully!")
        st.session_state.mood_logged = True  # Track if mood is logged

# Display Mood Logs
if st.sidebar.button("View Mood History"):
    try:
        with open("mood_logs.txt", "r") as f:
            mood_history = f.read()
        st.sidebar.write("### Your Mood History")
        st.sidebar.text(mood_history)
    except FileNotFoundError:
        st.sidebar.warning("No mood logs found.")

# Main Chat Interface
st.header("💬 Chat with MindMate")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Use a unique key for the text input to avoid conflicts
user_input = st.text_input("Share your thoughts or feelings...", key="chat_input")

if st.button("Send"):
    if user_input.strip():
        # Get Gemini response (cached)
        response = get_gemini_response(user_input, st.session_state.chat_history)
        
        # Update chat history
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        st.session_state.chat_history.append({"role": "mindmate", "message": response})
        
        # Clear input box by rerunning the app
        st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
    else:
        st.warning("Please enter a message.")

# Display chat history
st.write("### Chat History")
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"👤 **You:** {message['message']}")
    elif message["role"] == "mindmate":
        st.markdown(f"🤖 **MindMate:** {message['message']}")

# Resource Recommendations
st.header("📚 Mental Health Resources")
resources = [
    "1. [Breathing Exercise Guide](https://www.healthline.com/health/breathing-exercise)",
    "2. [Journaling Prompts for Mental Health](https://psychcentral.com/lib/the-health-benefits-of-journaling)",
    "3. [Guided Meditation Videos](https://www.youtube.com/results?search_query=guided+meditation)",
    "4. [Crisis Hotlines](https://findahelpline.com/countries/in)"
]
st.write("Here are some resources to help you:")
for resource in resources:
    st.markdown(resource)

# Feedback Mechanism
st.header("📝 Feedback")
feedback = st.text_area("We'd love to hear your feedback about MindMate!")
if st.button("Submit Feedback"):
    with open("feedback.txt", "a") as f:
        f.write(f"{datetime.now()}: {feedback}\n")
    st.success("Thank you for your feedback!")

# Footer
st.markdown("---")
st.write("Made by Ishwari and Rutika")
