import streamlit as st
import re

def extract_movie_titles(data):
    titles = []

    st.write("Here the folowwing recommandation based on the film provided")
    for item in data:
        # Find the index of 'movie_title'
        title = item.metadata["movie_title"]
        # st.write(title)
        titles.append(title)

    return titles
