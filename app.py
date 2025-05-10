import streamlit as st

# Song database with working mp3 sample links
songs = [
    {
        "name": "Tum Hi Ho",
        "artist": "Arijit Singh",
        "album": "Aashiqui 2",
        "cover": "https://c.saavncdn.com/430/Aashiqui-2-Hindi-2013-500x500.jpg",
        "audio": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    },
    {
        "name": "Shayad",
        "artist": "Arijit Singh",
        "album": "Love Aaj Kal",
        "cover": "https://c.saavncdn.com/533/Love-Aaj-Kal-Hindi-2020-20200213151002-500x500.jpg",
        "audio": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"
    },
    {
        "name": "Kesariya",
        "artist": "Arijit Singh",
        "album": "Brahmāstra",
        "cover": "https://c.saavncdn.com/387/Kesariya-From-Brahmastra-Hindi-2022-20220717131006-500x500.jpg",
        "audio": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"
    }
]

# Streamlit app
st.set_page_config(page_title="🎵 Streamlit Music Player", layout="centered")

st.title("🎶 Streamlit Music Streaming Player")
st.markdown("Choose a song from the list below to start playing:")

# Song selector
song_titles = [f"{song['name']} - {song['artist']}" for song in songs]
selected_title = st.selectbox("Select a Song", song_titles)

# Find selected song
selected_song = next(song for song in songs if f"{song['name']} - {song['artist']}" == selected_title)

# Display song info
st.image(selected_song["cover"], width=300, caption=selected_song["album"])
st.markdown(f"**Title:** {selected_song['name']}")
st.markdown(f"**Artist:** {selected_song['artist']}")
st.markdown(f"**Album:** {selected_song['album']}")

# Audio player
st.audio(selected_song["audio"], format="audio/mp3", start_time=0)
