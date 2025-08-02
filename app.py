import pickle
import streamlit as st
import requests
import time

# Set page config
st.set_page_config(page_title="🎬 Suggesteria", page_icon="🎥", layout="wide")

# Custom CSS: Gradient, Glass Effect, Animations
st.markdown("""
    <style>
    /* Background Gradient */
    body {
        background: linear-gradient(135deg, #1f1c2c, #928DAB);
        color: #FFFFFF;
        font-family: 'Helvetica Neue', sans-serif;
    }

    .main {
        background: transparent;
    }

    header, footer {visibility: hidden;}

    /* Poster Card */
    .poster-container {
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 10px;
        transition: transform 0.3s ease;
        animation: fadeIn 1s ease forwards;
    }

    .poster-container:hover {
        transform: scale(1.05);
    }

    /* Poster Image */
    .poster-container img {
        width: 100%;
        border-radius: 12px;
        opacity: 0;
        animation: fadeInPoster 1s ease-in forwards;
    }

    /* Animations */
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }

    @keyframes fadeInPoster {
        to {opacity: 1;}
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 20px 0;
        font-size: 14px;
        color: #ff4b4b;
        text-shadow: 0 0 10px #ff4b4b;
    }

    /* Buttons */
    div.stButton > button {
        border-radius: 30px;
        background: linear-gradient(90deg, #ff512f, #dd2476);
        color: white;
        padding: 0.75em 2em;
        font-weight: bold;
        border: none;
        cursor: pointer;
        transition: background 0.3s ease;
    }

    div.stButton > button:hover {
        background: linear-gradient(90deg, #ff512f, #ff512f);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='font-size: 52px; color: #ff4b4b;'>🎬 Suggesteria</h1>
        <h3 style='color: #DDDDDD;'>Your Personalized Movie Recommender</h3>
    </div>
""", unsafe_allow_html=True)

# Load model files
try:
    movies = pickle.load(open('model/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading model files: {e}")
    st.stop()

# Fetch poster using TMDb Search API
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

# UI Logic
movie_list = movies['title'].values
selected_movie = st.selectbox("🎞️ Type or select a movie", movie_list)

if st.button("✨ Show Recommendations"):
    names, posters = recommend(selected_movie)
    if names:
        cols = st.columns(5)
        for i in range(len(names)):
            with cols[i]:
                st.markdown(f"""
                    <div class="poster-container">
                        <img src="{posters[i]}">
                        <p style='text-align: center; margin-top: 8px; font-weight: bold; color: #FFFFFF;'>{names[i]}</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No recommendations found.")

# Footer with glow effect
st.markdown("""
    <hr>
    <div class='footer'>
        Made with ❤️ by <strong>Pranjal Bopate</strong>
    </div>
""", unsafe_allow_html=True)



