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

# Streamlit setup
st.set_page_config(page_title="🎵 AI Music Streamer", layout="centered")
st.title("🎶 AI Music Streaming Platform")
st.markdown("Powered by Streamlit, Groq LLaMA3 & JioSaavn API")

# AI recommendation
def get_song_recommendation(prompt):
    try:
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"AI recommendation failed: {e}"

# Search functions with safe fallback
def search_songs(query):
    url = f"https://saavn.dev/api/search/songs?query={query}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("data", {}).get("results", []) or []
    except:
        pass
    return []

def search_albums(query):
    url = f"https://saavn.dev/api/search/albums?query={query}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("data", {}).get("results", []) or []
    except:
        pass
    return []

def search_playlists(query):
    url = f"https://saavn.dev/api/search/playlists?query={query}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("data", {}).get("results", []) or []
    except:
        pass
    return []

# User input
user_input = st.text_input("Describe your mood or the Indian music you want 🎧")

if st.button("🎯 Get AI Music Recommendations") and user_input:
    with st.spinner("Thinking with AI..."):
        # AI Suggestions
        prompt = f"Suggest Indian songs, albums, and playlists based on: {user_input}"
        recommendation = get_song_recommendation(prompt)
        st.subheader("💡 AI Recommendation")
        st.write(recommendation)

        # SONGS
        st.subheader("🎵 Songs")
        songs = search_songs(user_input)
        if isinstance(songs, list) and songs:
            for song in songs[:5]:
                title = song.get('name', 'Unknown Title')
                artists = song.get('primaryArtists', 'Unknown Artist')
                image = song.get('image', [{}]*3)[2].get('link', '') if len(song.get('image', [])) > 2 else ''
                audio_links = song.get('downloadUrl', [])
                audio_url = audio_links[4].get('link') if len(audio_links) > 4 else None

                st.markdown(f"**{title}** by {artists}")
                if audio_url:
                    st.audio(audio_url, format="audio/mp3")
                if image:
                    st.image(image)
        else:
            st.warning("No songs found for this input.")

        # ALBUMS
        st.subheader("💿 Albums")
        albums = search_albums(user_input)
        if isinstance(albums, list) and albums:
            for album in albums[:3]:
                name = album.get('name', 'Unknown Album')
                artist = album.get('primaryArtists', 'Unknown Artist')
                image = album.get('image', [{}]*3)[2].get('link', '') if len(album.get('image', [])) > 2 else ''
                url = album.get('url', '#')

                st.markdown(f"**{name}** by {artist}")
                if image:
                    st.image(image)
                st.markdown(f"[🔗 Listen on JioSaavn]({url})")
        else:
            st.warning("No albums found.")

        # PLAYLISTS
        st.subheader("📻 Playlists")
        playlists = search_playlists(user_input)
        if isinstance(playlists, list) and playlists:
            for playlist in playlists[:3]:
                title = playlist.get('title', 'Untitled Playlist')
                image = playlist.get('image', [{}]*3)[2].get('link', '') if len(playlist.get('image', [])) > 2 else ''
                url = playlist.get('url', '#')

                st.markdown(f"**{title}**")
                if image:
                    st.image(image)
                st.markdown(f"[🎧 Listen on JioSaavn]({url})")
        else:
            st.warning("No playlists found.")
