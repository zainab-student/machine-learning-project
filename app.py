from datetime import date
import streamlit as st
import pickle
import pandas as pd
import os
import requests

# ---------------- Fetch poster from TMDB ----------------
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=6a4c203541b421d2113e46f9ee07c749&language=en-US')
    data = response.json()
    return "http://image.tmdb.org/t/p/w500" + data['poster_path']

# ---------------- Recommendation logic ----------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # make sure 'movie_id' exists in your DataFrame
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# ---------------- Load Pickle Files ----------------
try:
    with open(os.path.join('movie-recommandation-system', 'movie_dict.pkl'), 'rb') as f:
        movie_dict = pickle.load(f)
    movies = pd.DataFrame.from_dict(movie_dict)

    with open(os.path.join('movie-recommandation-system', 'similarity.pkl'), 'rb') as f:
        similarity = pickle.load(f)

except Exception as e:
    st.error(f"Error loading files: {e}")

# ---------------- Streamlit UI ----------------
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    # Display results in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
