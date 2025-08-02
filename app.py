import pickle
import streamlit as st
import requests
import time

# Set page title and layout
st.set_page_config(page_title="🎬 Suggesteria", page_icon="🎥", layout="wide")

# Custom CSS for background, fonts, animation
st.markdown("""
    <style>
    body {
        background-color: #f4f4f4;
        color: #333333;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .main {
        background-color: #f4f4f4;
    }
    header {
        visibility: hidden;
    }
    footer {
        visibility: hidden;
    }

    /* Fade-in animation */
    .poster-container img {
        opacity: 0;
        animation: fadeIn 1s ease-in forwards;
    }

    @keyframes fadeIn {
        to {
            opacity: 1;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Beautiful header
st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='font-size: 48px; color: #ff4b4b;'>🎬 Suggesteria</h1>
        <h3 style='color: #555555;'>Your Personalized Movie Recommender</h3>
    </div>
""", unsafe_allow_html=True)

# Load model files
try:
    movies = pickle.load(open('model/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading model files: {e}")
    st.stop()

# Fetch poster using TMDb Search API (by title)
def fetch_poster(movie_title):
    api_key = "2e14804309c8641fbd7197e4fd53c2ef"
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"

    try:
        time.sleep(0.5)  # avoid TMDb rate limiting
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("results"):
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"

    except Exception as e:
        print(f"Error fetching poster for '{movie_title}': {e}")

    return "https://via.placeholder.com/500x750?text=No+Image"

# Recommendation logic
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error("Selected movie not found in dataset.")
        return [], []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances:
        movie_title = movies.iloc[i[0]].title
        recommended_movie_names.append(movie_title)
        recommended_movie_posters.append(fetch_poster(movie_title))

    return recommended_movie_names, recommended_movie_posters

# Original UI preserved here
movie_list = movies['title'].values
selected_movie = st.selectbox("🎞️ Type or select a movie", movie_list)

if st.button("🎥 Show Recommendations"):
    names, posters = recommend(selected_movie)
    if names:
        cols = st.columns(5)
        for i in range(len(names)):
            with cols[i]:
                st.markdown(f"""
                    <div class="poster-container">
                        <img src="{posters[i]}" style="width: 100%; border-radius: 10px;">
                        <p style='text-align: center; margin-top: 8px; font-weight: bold;'>{names[i]}</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No recommendations found.")

# Footer with credit
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #888888; font-size: 14px; padding: 10px 0;'>
        Made with ❤️ by <strong>Pranjal Bopate</strong>
    </div>
""", unsafe_allow_html=True)


