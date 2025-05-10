import streamlit as st
from streamlit_player import st_player
import requests

# Function to fetch songs from JioSaavn API based on mood
def fetch_songs_by_mood(mood):
    # Mapping moods to search queries
    mood_queries = {
        "Happy": "happy songs",
        "Sad": "sad songs",
        "Energetic": "energetic songs",
        "Relaxed": "relaxing music"
    }
    query = mood_queries.get(mood, "top songs")
    
    # JioSaavn API endpoint for search
    api_url = f"https://www.saavn.com/api.php?__call=autocomplete.get&query={query}&_format=json&_marker=0"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        songs = data.get('songs', {}).get('data', [])
        return songs
    except Exception as e:
        st.error("Failed to fetch songs. Please try again later.")
        return []

# Streamlit app layout
st.title("🎶 Mood-Based Music Player")
st.write("Select your current mood to get song recommendations.")

# Mood selection
mood = st.selectbox("Choose your mood:", ["Happy", "Sad", "Energetic", "Relaxed"])

# Fetch and display songs
if mood:
    st.subheader(f"Recommended {mood} Songs:")
    songs = fetch_songs_by_mood(mood)
    
    if songs:
        for song in songs[:10]:  # Display top 10 songs
            song_title = song.get('title')
            song_url = song.get('perma_url')
            st.write(f"**{song_title}**")
            if song_url:
                st_player(song_url)
    else:
        st.write("No songs found for the selected mood.")
