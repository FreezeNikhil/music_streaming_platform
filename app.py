import streamlit as st
import requests
import math

st.set_page_config(page_title="🎧 iTunes Music Explorer", layout="centered")
st.title("🎶 Song Streaming platform ")

# Input from user
artist = st.text_input("Enter artist name", value="Arijit Singh")
genre_filter = st.text_input("Optional: Filter by genre (e.g., Pop, Rock, Bollywood)")

# Pagination
songs_per_page = 10
page = st.number_input("Page", min_value=1, step=1, value=1)

if artist:
    # Prepare query
    query = artist + " " + genre_filter if genre_filter else artist

    # Request up to 200 songs (iTunes max)
    response = requests.get("https://itunes.apple.com/search", params={
        "term": query,
        "media": "music",
        "entity": "musicTrack",
        "limit": 200
    })

    data = response.json()
    results = data.get("results", [])

    if results:
        # Pagination logic
        total_pages = math.ceil(len(results) / songs_per_page)
        start = (page - 1) * songs_per_page
        end = start + songs_per_page
        current_songs = results[start:end]

        for song in current_songs:
            st.markdown(f"### {song['trackName']} - {song['artistName']}")
            st.image(song['artworkUrl100'].replace("100x100", "500x500"), width=300)
            st.markdown(f"**Album:** {song.get('collectionName', 'N/A')}")
            st.markdown(f"**Genre:** {song.get('primaryGenreName', 'N/A')}")
            st.audio(song['previewUrl'], format="audio/mp4")
            st.markdown("---")

        st.markdown(f"**Page {page} of {total_pages}**")
    else:
        st.warning("No songs found. Try another artist or genre.")
