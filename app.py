import streamlit as st
import requests
import math

st.set_page_config(page_title="🎧 iTunes Music Explorer", layout="centered")
st.title("🎶 Music Streaming with Autoplay & One-at-a-Time Playback")

# Input fields
artist = st.text_input("Enter artist name", value="Arijit Singh")
genre_filter = st.text_input("Optional: Genre filter (e.g., Bollywood, Pop, Chill)")

songs_per_page = 5
page = st.number_input("Page", min_value=1, step=1, value=1)

if artist:
    # Query iTunes API
    query = artist + " " + genre_filter if genre_filter else artist
    response = requests.get("https://itunes.apple.com/search", params={
        "term": query,
        "media": "music",
        "entity": "musicTrack",
        "limit": 200
    })
    data = response.json()
    results = data.get("results", [])

    if results:
        total_pages = math.ceil(len(results) / songs_per_page)
        start = (page - 1) * songs_per_page
        end = start + songs_per_page
        current_songs = results[start:end]

        # Generate HTML audio blocks with autoplay and stop logic
        audio_blocks = ""
        for idx, song in enumerate(current_songs):
            audio_id = f"audio{idx}"
            block = f"""
            <div style='margin-bottom:30px;'>
                <h4>{song['trackName']} - {song['artistName']}</h4>
                <img src="{song['artworkUrl100'].replace('100x100', '500x500')}" width="300"><br>
                <p><b>Album:</b> {song.get('collectionName', 'N/A')}<br>
                   <b>Genre:</b> {song.get('primaryGenreName', 'N/A')}</p>
                <audio id="{audio_id}" controls preload="none">
                    <source src="{song['previewUrl']}" type="audio/mp4">
                </audio>
            </div>
            """
            audio_blocks += block

        # JavaScript to ensure only one song plays at a time and autoplay the first one
        js_script = f"""
        <script>
        const audios = document.querySelectorAll("audio");
        audios.forEach((audio, index) => {{
            audio.addEventListener("play", () => {{
                audios.forEach((a, i) => {{
                    if (i !== index) a.pause();
                }});
            }});
        }});
        window.onload = function() {{
            setTimeout(() => {{
                document.querySelector("audio").play();
            }}, 500);
        }};
        </script>
        """

        st.markdown(audio_blocks + js_script, unsafe_allow_html=True)
        st.markdown(f"**Page {page} of {total_pages}**")
    else:
        st.warning("No songs found. Try a different artist or genre.")
