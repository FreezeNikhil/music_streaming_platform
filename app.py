import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Mood-Based Music Player", layout="centered")

st.title("🎵 AI Mood-Based Music Player")

# Step 1: Select Mood
mood = st.selectbox("How are you feeling today?", ["Happy", "Sad", "Energetic", "Romantic", "Relaxed"])

# Step 2: Select type
song_type = st.radio("What would you like to listen to?", ["Single Track", "Album", "Mix"])

# YouTube links database
songs = {
    "Happy": {
        "Single Track": ("Phir Se Ud Chala - Rockstar", "https://www.youtube.com/embed/VsQtduVb1FA"),
        "Album": ("Zindagi Na Milegi Dobara Album", "https://www.youtube.com/embed/videoseries?list=PLFA4AB3B79564A152"),
        "Mix": ("Happy Bollywood Mix", "https://www.youtube.com/embed/V1bFr2SWP1I"),
    },
    "Sad": {
        "Single Track": ("Agar Tum Saath Ho - Tamasha", "https://www.youtube.com/embed/xRb8hxwN5zc"),
        "Album": ("Sad Hits Bollywood", "https://www.youtube.com/embed/videoseries?list=PLFgquLnL59am3HeY8kOzRXztrYxvKkLk6"),
        "Mix": ("Sad Hindi Mix", "https://www.youtube.com/embed/KPzFvVJaP1Q"),
    },
    "Energetic": {
        "Single Track": ("Malhari - Bajirao Mastani", "https://www.youtube.com/embed/Zea-Iw7yLIE"),
        "Album": ("Gully Boy Album", "https://www.youtube.com/embed/videoseries?list=PLsyeobzWxl7rMEZ1ze4p51RrS3vX5Yf4L"),
        "Mix": ("Bollywood Workout Mix", "https://www.youtube.com/embed/28xjtYY6U_k"),
    },
    "Romantic": {
        "Single Track": ("Tum Hi Ho - Aashiqui 2", "https://www.youtube.com/embed/Umqb9KENgmk"),
        "Album": ("Romantic Bollywood 2023", "https://www.youtube.com/embed/videoseries?list=PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI"),
        "Mix": ("Romantic Hindi Mix", "https://www.youtube.com/embed/Lp_gE8TDS2k"),
    },
    "Relaxed": {
        "Single Track": ("Shayad - Love Aaj Kal", "https://www.youtube.com/embed/EY-Jhynq0J8"),
        "Album": ("Lo-fi Chill Bollywood", "https://www.youtube.com/embed/videoseries?list=PLzAUjD1I4H2GQ-WR3sKjZC3V1y82j4QCE"),
        "Mix": ("Bollywood Lo-fi Mix", "https://www.youtube.com/embed/H-wz2B8Zr90"),
    },
}

# Display selected track
if mood and song_type:
    track_title, youtube_link = songs[mood][song_type]
    st.subheader(f"🎶 Now Playing: {track_title}")
    components.iframe(youtube_link, height=360)
