import streamlit as st
import random

# Set up page
st.set_page_config(page_title="🎧 Mood-Based Music Player", layout="centered")
st.title("🎵 Mood-Based Music Streaming Player")

# Song Database
music_library = {
    "Happy": {
        "singles": [
            {
                "title": "Love You Zindagi",
                "artist": "Amit Trivedi",
                "cover": "https://c.saavncdn.com/709/Dear-Zindagi-Hindi-2016-500x500.jpg",
                "audio": "https://aac.saavncdn.com/709/753c90e9bbccaf69e731ed86edafff3c_320.mp4"
            },
            {
                "title": "Kar Gayi Chull",
                "artist": "Badshah, Fazilpuria",
                "cover": "https://c.saavncdn.com/190/Kapoor-Sons-Hindi-2016-500x500.jpg",
                "audio": "https://aac.saavncdn.com/190/ca1a3e6f0b55e1be9a57e949a34b75bc_320.mp4"
            }
        ],
        "albums": [
            {
                "album_name": "Yeh Jawaani Hai Deewani",
                "songs": [
                    {
                        "title": "Badtameez Dil",
                        "artist": "Benny Dayal",
                        "cover": "https://c.saavncdn.com/504/Yeh-Jawaani-Hai-Deewani-Hindi-2013-500x500.jpg",
                        "audio": "https://aac.saavncdn.com/504/e3768cf5e35c8a9b64790b8d5c800bcb_320.mp4"
                    }
                ]
            }
        ]
    },
    "Sad": {
        "singles": [
            {
                "title": "Channa Mereya",
                "artist": "Arijit Singh",
                "cover": "https://c.saavncdn.com/612/Ae-Dil-Hai-Mushkil-Hindi-2016-500x500.jpg",
                "audio": "https://aac.saavncdn.com/612/730c97da0975a4c3f71b1a68fd02ba45_320.mp4"
            }
        ],
        "albums": [
            {
                "album_name": "Aashiqui 2",
                "songs": [
                    {
                        "title": "Tum Hi Ho",
                        "artist": "Arijit Singh",
                        "cover": "https://c.saavncdn.com/430/Aashiqui-2-Hindi-2013-500x500.jpg",
                        "audio": "https://aac.saavncdn.com/430/5c5ea5cc00e3bff45616013226f376fe_320.mp4"
                    }
                ]
            }
        ]
    },
    "Chill": {
        "singles": [
            {
                "title": "Ilahi",
                "artist": "Arijit Singh",
                "cover": "https://c.saavncdn.com/504/Yeh-Jawaani-Hai-Deewani-Hindi-2013-500x500.jpg",
                "audio": "https://aac.saavncdn.com/504/b9b8036a4db7b91e8c60e96b78cf6212_320.mp4"
            }
        ],
        "albums": []
    },
    "Romantic": {
        "singles": [
            {
                "title": "Shayad",
                "artist": "Arijit Singh",
                "cover": "https://c.saavncdn.com/533/Love-Aaj-Kal-Hindi-2020-20200213151002-500x500.jpg",
                "audio": "https://aac.saavncdn.com/533/6463bba690b2ec44b68890cdecc7b368_320.mp4"
            }
        ],
        "albums": []
    }
}

# Select Mood
mood = st.selectbox("🎭 Choose your Mood", list(music_library.keys()))

# Mix songs (random pick from all types)
if st.button("🔀 Play a Mood-Based Mix"):
    all_songs = []
    for cat in music_library[mood].values():
        if isinstance(cat, list):
            for entry in cat:
                if "songs" in entry:
                    all_songs.extend(entry["songs"])
                else:
                    all_songs.append(entry)
    if all_songs:
        random_song = random.choice(all_songs)
        st.subheader("🎶 Now Playing (Mix):")
        st.image(random_song["cover"], width=300)
        st.markdown(f"**{random_song['title']}** by *{random_song['artist']}*")
        st.audio(random_song["audio"])
    else:
        st.warning("No songs available for this mood.")

st.markdown("### 🎧 Explore Single Tracks")
singles = music_library[mood]["singles"]
single_titles = [f"{s['title']} - {s['artist']}" for s in singles]
selected_single = st.selectbox("Choose a Single Track", single_titles)
selected_song = singles[single_titles.index(selected_single)]

st.image(selected_song["cover"], width=300)
st.markdown(f"**{selected_song['title']}** by *{selected_song['artist']}*")
st.audio(selected_song["audio"])

# Albums
albums = music_library[mood]["albums"]
if albums:
    st.markdown("### 💽 Explore Albums")
    album_names = [a["album_name"] for a in albums]
    selected_album = st.selectbox("Choose an Album", album_names)

    album_songs = next(a["songs"] for a in albums if a["album_name"] == selected_album)
    album_song_titles = [f"{s['title']} - {s['artist']}" for s in album_songs]
    selected_album_song = st.selectbox("Choose a Song from Album", album_song_titles)
    album_selected_song = album_songs[album_song_titles.index(selected_album_song)]

    st.image(album_selected_song["cover"], width=300)
    st.markdown(f"**{album_selected_song['title']}** by *{album_selected_song['artist']}*")
    st.audio(album_selected_song["audio"])
