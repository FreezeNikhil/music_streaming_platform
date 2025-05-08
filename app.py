import streamlit as st
import requests
import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Check API key
if not groq_api_key:
    st.error("❌ GROQ_API_KEY not found. Please check your .env file.")
    st.stop()

# Set up OpenAI client for Groq
client = OpenAI(
    api_key=groq_api_key,
    base_url="https://api.groq.com/openai/v1"
)

# Streamlit app title
st.set_page_config(page_title="🎧 SmartMusic - AI Music Recommender", page_icon="🎶")
st.title("🎧 SmartMusic: AI-Powered Indian Music Recommender")
st.markdown("Powered by **Groq API + JioSaavn.dev**")

# Function to get music prompt from Groq
def get_music_prompt(mood_or_genre):
    prompt = f"""
You are a music assistant. Suggest 5 Indian songs or playlists based on the user's input: "{mood_or_genre}". 
Output just keywords or artist names best suited for a JioSaavn search.
Example: Arijit Singh, Romantic Hindi, Punjabi Workout, 90s Bollywood, Lo-Fi Hindi
Respond in a comma-separated list of 5.
"""
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You're a helpful music assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        reply = response.choices[0].message.content
        return [x.strip() for x in reply.split(",") if x.strip()]
    except Exception as e:
        st.error(f"❌ Groq API Error: {e}")
        return []

# Function to search songs via JioSaavn.dev API
def search_songs(keyword):
    url = f"https://saavn.dev/api/search/songs?query={keyword}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('data', {}).get('results', [])
    except Exception as e:
        st.error(f"❌ Error fetching songs: {e}")
    return []

# Input from user
user_input = st.text_input("🎵 Enter a mood, artist, or genre:", "romantic hindi")

if st.button("🎯 Get AI Music Recommendations"):
    with st.spinner("Thinking like a DJ..."):
        suggestions = get_music_prompt(user_input)
        if suggestions:
            st.success("🎶 AI recommends these themes:")
            st.write(", ".join(suggestions))

            all_songs = []
            for theme in suggestions:
                songs = search_songs(theme)
                all_songs.extend(songs)

            if all_songs:
                st.subheader("🎵 Songs (Play All Mode)")
                song_data = []

                for song in all_songs[:5]:
                    title = song.get('name', 'Unknown Title')
                    artists = song.get('primaryArtists', 'Unknown Artist')
                    image = song.get('image', [{}]*3)[2].get('link', '') if len(song.get('image', [])) > 2 else ''
                    audio_links = song.get('downloadUrl', [])
                    audio_url = audio_links[4].get('link') if len(audio_links) > 4 else None

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
                st.download_button("⬇️ Download as CSV", data=csv, file_name="recommended_songs.csv", mime="text/csv")

                # Info
                st.info("ℹ️ Due to browser restrictions, audio autoplay is not supported. Please play each song manually.")
            else:
                st.warning("⚠️ No songs found for the suggested themes.")
        else:
            st.warning("⚠️ No suggestions returned. Try another keyword or genre.")
