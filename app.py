import streamlit as st

# Song list (extendable)
songs = [
    {
        "title": "Khamoshiyan",
        "artist": "Jeet Gannguli & Arijit Singh",
        "album": "Khamoshiyan (Original Motion Picture Soundtrack)",
        "genre": "Bollywood",
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/c7/a6/7d/c7a67d5e-177d-c6e6-d3c4-734bf84a162f/886445025378.jpg/500x500bb.jpg",
        "audio": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview211/v4/fa/77/eb/fa77ebd3-1965-bdb9-2837-71bf88b9a81b/mzaf_14953669034681086405.plus.aac.p.m4a"
    },
    {
        "title": "Ghungroo",
        "artist": "Vishal & Shekhar, Arijit Singh & Shilpa Rao",
        "album": "War (Original Motion Picture Soundtrack)",
        "genre": "Bollywood",
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/36/03/a0/3603a004-3288-484c-9783-305ffebc91ba/849486006348_cover.jpg/500x500bb.jpg",
        "audio": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview116/v4/d9/fb/7f/d9fb7faa-00d9-5960-7995-bfca765d0a00/mzaf_10550088996822444584.plus.aac.p.m4a"
    }
]

st.set_page_config(page_title="🎵 Music Autoplayer", layout="centered")
st.title("🎶 Bollywood Music Player")

# Session state for track index
if "song_index" not in st.session_state:
    st.session_state.song_index = 0

# Navigation buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⏮️ Previous", use_container_width=True):
        st.session_state.song_index = (st.session_state.song_index - 1) % len(songs)
with col3:
    if st.button("Next ⏭️", use_container_width=True):
        st.session_state.song_index = (st.session_state.song_index + 1) % len(songs)

# Current song
song = songs[st.session_state.song_index]

# Display song details
st.markdown(f"### 🎧 {song['title']} - {song['artist']}")
st.image(song["cover"], width=300)
st.markdown(f"**Album:** {song['album']}  \n**Genre:** {song['genre']}")

# Autoplay + single play audio player (via HTML + JS)
html_audio = f"""
<audio id="player" controls autoplay>
    <source src="{song['audio']}" type="audio/mp4">
    Your browser does not support the audio element.
</audio>
<script>
const audios = document.querySelectorAll("audio");
audios.forEach((audio, index) => {{
    audio.addEventListener("play", () => {{
        audios.forEach((a, i) => {{
            if (i !== index) a.pause();
        }});
    }});
}});

// Autoplay next on end
document.getElementById("player").addEventListener("ended", function() {{
    fetch("{st.experimental_get_query_params().get('next_url', ['/'])[0]}")
}});
</script>
"""

# Trigger next song via rerun on audio end
next_index = (st.session_state.song_index + 1) % len(songs)
st.experimental_set_query_params(next_url=f"/?song_index={next_index}")

# Handle query param update
params = st.experimental_get_query_params()
if "song_index" in params:
    st.session_state.song_index = int(params["song_index"][0])

# Render audio player
st.markdown(html_audio, unsafe_allow_html=True)
