import streamlit as st

# Song database
songs = [
    {
        "name": "Tum Hi Ho",
        "artist": "Arijit Singh",
        "album": "Aashiqui 2",
        "cover": "https://c.saavncdn.com/430/Aashiqui-2-Hindi-2013-500x500.jpg",
        "audio": "http://aac.saavncdn.com/430/5c5ea5cc00e3bff45616013226f376fe_320.mp4"
    },
    {
        "name": "Shayad",
        "artist": "Arijit Singh",
        "album": "Love Aaj Kal",
        "cover": "https://c.saavncdn.com/533/Love-Aaj-Kal-Hindi-2020-20200213151002-500x500.jpg",
        "audio": "http://aac.saavncdn.com/533/6463bba690b2ec44b68890cdecc7b368_320.mp4"
    },
    {
        "name": "Kesariya",
        "artist": "Arijit Singh",
        "album": "Brahmāstra",
        "cover": "https://c.saavncdn.com/387/Kesariya-From-Brahmastra-Hindi-2022-20220717131006-500x500.jpg",
        "audio": "http://aac.saavncdn.com/387/80d09c08d1c04b1a4d5d6d3a2e189771_320.mp4"
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
st.audio(selected_song["audio"], format="audio/mp4", start_time=0)
