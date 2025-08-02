import pickle
import streamlit as st
import requests
import time

# 🌐 Page config
st.set_page_config(page_title="🎬 Suggesteria", page_icon="🎥", layout="wide")

# 💄 Custom background color (light gray)
st.markdown("""
    <style>
    .stApp {
        background-color: #f7f9fc;
    }
    </style>
""", unsafe_allow_html=True)

# 🌟 App title and subtitle
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎬 Suggesteria</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Your Personalized Movie Recommender</h4>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 📦 Load model files
try:
    movies = pickle.load(open('model/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading model files: {e}")
    st.stop()

# 🖼️ Fetch poster using TMDb Search API
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

# 🧠 Recommendation logic
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

    return reco

