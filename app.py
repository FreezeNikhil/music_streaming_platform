import streamlit as st
import requests
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Streamlit app configuration
st.set_page_config(page_title="🎵 AI Music Streamer", layout="centered")
st.title("🎶 AI Music Streaming Platform")
st.markdown("Powered by Streamlit, Groq LLaMA3 & JioSaavn API")

# Function to get song recommendation from Groq
def get_song_recommendation(prompt):
    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return chat_completion.choices[0].message.content.strip()

# Function to search songs on JioSaavn
def search_songs(query):
    url = f"https://saavn.dev/api/search/songs?query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("data", {}).get("results", [])
    else:
        return []

# Function to search albums on JioSaavn
def search_albums(query):
    url = f"https://saavn.dev/api/search/albums?query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("data", {}).get("results", [])
    else:
        return []

# Function to search playlists on JioSaavn
def search_playlists(query):
    url = f"https://saavn.dev/api/search/playlists?query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("data", {}).get("results", [])
    else:
        return []

# User input
user_input = st.text_input("Describe your mood or the type of music you want to listen to 🎧")

if st.button("Get Recommendations") and user_input:
    with st.spinner("Fetching recommendations..."):
        # Get song recommendation from Groq
        prompt = f"Suggest some Indian songs, albums, and playlists based on the following mood or description: {user_input}"
        recommendation = get_song_recommendation(prompt)
        st.subheader("🎯 AI Recommendation")
        st.write(recommendation)

        # Search and display songs
        st.subheader("🎵 Songs")
        songs = search_songs(user_input)
        for song in songs[:5]:
            st.markdown(f"**{song['name']}** by {song['primaryArtists']}")
            st.audio(song['downloadUrl'][4]['link'], format="audio/mp3")
            st.image(song['image'][2]['link'])

        # Search and display albums
        st.subheader("💿 Albums")
        albums = search_albums(user_input)
        for album in albums[:3]:
            st.markdown(f"**{album['name']}** by {album['primaryArtists']}")
            st.image(album['image'][2]['link'])
            st.markdown(f"[Listen on JioSaavn]({album['url']})")

        # Search and display playlists
        st.subheader("📻 Playlists")
        playlists = search_playlists(user_input)
        for playlist in playlists[:3]:
            st.markdown(f"**{playlist['title']}**")
            st.image(playlist['image'][2]['link'])
            st.markdown(f"[Listen on JioSaavn]({playlist['url']})")
