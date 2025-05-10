import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="🎧 Debug: SmartMusic", page_icon="🎶")
st.title("🎧 SmartMusic Debug Version")
st.markdown("Testing direct JioSaavn.dev song search...")

# Function to search songs via JioSaavn.dev API
def search_songs(keyword):
    url = f"https://saavn.dev/api/search/songs?query={keyword}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            st.write("✅ API raw JSON:", data)  # Debug print
            return data.get('data', {}).get('results', [])
        else:
            st.error(f"❌ API Error: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Error fetching songs: {e}")
    return []

# Hardcoded test keyword (bypassing Groq for now)
keyword = st.text_input("🔍 Enter a song keyword to test:", "Arijit Singh")

if st.button("🚀 Test Song Fetching"):
    with st.spinner("Contacting JioSaavn..."):
        songs = search_songs(keyword)
        if songs:
            song_data = []
            for song in songs[:5]:  # limit to 5
                st.write("🎵 Raw Song Object:", song)  # Debug each song

                title = song.get('name', 'Unknown Title')
                artists = song.get('primaryArtists', 'Unknown Artist')

                # Get image and audio link safely
                image = ''
                try:
                    image = song.get('image', [{}]*3)[2].get('link', '')
                except: pass

                # Find audio link in downloadUrl list
                audio_url = None
                for quality in reversed(song.get('downloadUrl', [])):
                    if quality.get('link'):
                        audio_url = quality['link']
                        break

                if audio_url:
                    song_data.append({
                        "Title": title,
                        "Artists": artists,
                        "Audio URL": audio_url
                    })
                    with st.container():
                        st.markdown(f"**🎧 {title}** by *{artists}*")
                        if image:
                            st.image(image, width=150)
                        st.audio(audio_url, format="audio/mp3")
            # Download CSV
            st.markdown("📥 **Download Song Info**")
            song_df = pd.DataFrame(song_data)
            csv = song_df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download CSV", data=csv, file_name="songs.csv", mime="text/csv")
        else:
            st.warning("⚠️ No songs found for this keyword.")
