import streamlit as st
import requests
import os
from groq import Groq

# Set page config
st.set_page_config(page_title="🎵 AI Music Streamer", layout="centered")

# Load Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

st.title("🎶 AI Music Streaming Platform")
st.markdown("Powered by Streamlit, Groq LLaMA3 & Deezer API")

# Function to interact with Groq for song suggestions
def get_song_suggestion(user_input):
    prompt = f"""You are a music assistant. Based on this input, recommend a song name and artist:
    Input: {user_input}
    Format: Song - Artist"""
    
    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return chat_completion.choices[0].message.content.strip()

# Search Deezer
def search_deezer(query):
    url = f"https://api.deezer.com/search?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        return []

# User input
user_query = st.text_input("Tell me how you're feeling or what you want to hear 🎧")

if st.button("Get Recommendation") and user_query:
    with st.spinner("Thinking..."):
        suggestion = get_song_suggestion(user_query)
        st.success(f"💡 Recommended: **{suggestion}**")
        songs = search_deezer(suggestion)

        if songs:
            for song in songs[:1]:
                st.subheader(f"{song['title']} - {song['artist']['name']}")
                st.audio(song['preview'], format="audio/mp3")
                st.image(song['album']['cover_medium'])
        else:
            st.warning("No song found. Try another query.")
