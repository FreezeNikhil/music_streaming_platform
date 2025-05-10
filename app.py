import streamlit as st
import requests

st.set_page_config(page_title="🎧 iTunes Music Explorer", layout="centered")
st.title("🎶 Song Suggestion using iTunes API")

# Search input
search_term = st.text_input("Enter artist name, song, or album", value="Arijit Singh")

# Fetch songs from iTunes
if search_term:
    response = requests.get(f"https://itunes.apple.com/search", params={
        "term": search_term,
        "media": "music",
        "limit": 10
    })

    data = response.json()

    if data["resultCount"] > 0:
        song_titles = [f"{track['trackName']} - {track['artistName']}" for track in data["results"]]
        selected_title = st.selectbox("Select a song", song_titles)

        selected_song = next(track for track in data["results"]
                             if f"{track['trackName']} - {track['artistName']}" == selected_title)

        # Display song details
        st.image(selected_song["artworkUrl100"].replace("100x100", "500x500"), width=300,
                 caption=selected_song.get("collectionName", "Album Cover"))
        st.markdown(f"**Track:** {selected_song['trackName']}")
        st.markdown(f"**Artist:** {selected_song['artistName']}")
        st.markdown(f"**Album:** {selected_song.get('collectionName', 'N/A')}")

        # Audio player
        st.audio(selected_song["previewUrl"], format="audio/mp4")
    else:
        st.warning("No results found. Try another artist or song.")
