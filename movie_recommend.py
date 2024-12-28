# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 00:23:42 2024

@author: stfu
"""

import streamlit as st
import pandas as pd
import pickle

# Load movie data and similarity matrix
@st.cache_data
def load_data():
    movies = pd.read_csv('movies.csv')  # Replace with your actual movie dataset
    similarity = pickle.load(open('similarity.pkl', 'rb'))  # Replace with your similarity matrix
    return movies, similarity

movies, similarity = load_data()

# Function to recommend movies
def recommend_movies(movie_name, movies, similarity):
    movie_name = movie_name.lower()  # Make the search case-insensitive
    movie_index = movies[movies['title'].str.lower() == movie_name].index
    if len(movie_index) == 0:
        return ["Movie not found. Please try another name."]
    movie_index = movie_index[0]
    similarity_score = list(enumerate(similarity[movie_index]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)[1:11]
    recommended_movies = [movies.iloc[i[0]]['title'] for i in sorted_similar_movies]
    return recommended_movies

# Streamlit UI
st.title("Movie Recommendation System 🎥")
st.write("Type in a movie name and get similar recommendations!")

# Input for movie name
movie_name = st.text_input("Enter a Movie Name:", value="")

# Button to get recommendations
if st.button("Get Recommendations"):
    if movie_name.strip():
        recommendations = recommend_movies(movie_name, movies, similarity)
        st.write("### Recommended Movies:")
        for rec in recommendations:
            st.write("- ", rec)
    else:
        st.write("Please enter a valid movie name!")
