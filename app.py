import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os  

file_id = "1cHJu4bNdWVzB2oOvRCHldYFiN2k4opSL"
output_file = "similarity.pkl"

if not os.path.exists(output_file):  # Check if file exists
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output_file, quiet=False)


similarity = pickle.load(open(output_file, "rb"))


movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)


TMDB_API_KEY = "b43e2fd6d6cb75e1ecc0957576d03f0a"

def fetch_poster(movie_id):
    """Fetch movie poster URL from TMDb API."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url).json()

    if "poster_path" in response and response["poster_path"]:
        return "https://image.tmdb.org/t/p/w500/" + response["poster_path"]

    return "https://via.placeholder.com/500x750.png?text=No+Image"  


def recommend(movie):
    """Recommend similar movies based on cosine similarity."""
    movie_idx = movies[movies["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_idx])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:  # Get top 5 similar movies
        movie_id = movies.iloc[i[0]].id #Fetch movie id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("🔎 Select a movie you like", movies["title"].values)

if st.button("🎥 Show Recommendations"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])  # Display movie name
            st.image(recommended_movie_posters[i])  # Display movie poster
