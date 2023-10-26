import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.document_loaders.csv_loader import CSVLoader
from dotenv import load_dotenv
from supabase import create_client, Client
import os
import re
from function import extract_movie_titles

# generate_background_image()
st.set_page_config(layout="wide")
st.title("Movies App")

background_image = 'url("https://www.themoviedb.org/t/p/original/xGexTKCJDkl12dTW4YCBDXWb1AD.jpg")'

# CSS pour définir l'image de fond
st.markdown(f"""
    <style>
        .stApp {{
            background-image: {background_image};
            background-size: cover;
        }}

    .sidebar .sidebar-content {{
        background: #262730;
    }}
    .Widget {{
        color: white;
    }}
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stFileUploader > div > input {{
        background-color: #555e6f;
        color: white;
    }}
    .stTextInput > div > div > input::placeholder, .stTextArea > div > div > textarea::placeholder {{
        color: white;
    }}
    .stCheckbox label, .stRadio label {{
        color: white;
    }}
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
        color: white;
    }}
    .stSelectbox div[role="button"] {{
        color: white;
    }}
    </style>
    """,
            unsafe_allow_html=True)

load_dotenv()

key = os.getenv("SUPABASE_KEY")
url = os.getenv("SUPABASE_URL")

supabase: Client = create_client(url, key)
response = supabase.table('mytable').select("movie_title").execute()
movies = pd.DataFrame(response.data)

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local("model", embeddings)

query = st.selectbox("movie title", movies)
docs = db.similarity_search(query, k=5)


list_movies = extract_movie_titles(docs)
st.write(' -- '.join(str(x) for x in list_movies))



