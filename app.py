import streamlit as st
import pymysql
import pandas as pd
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.document_loaders.csv_loader import CSVLoader
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

st.set_page_config(layout="wide")

st.title("Movies App")

load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
database = os.getenv("DATABASE")

conn = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(conn)

movies = pd.read_sql_query("SELECT movie_title FROM movie_metadata; ", conn)

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local("model", embeddings)

query = st.selectbox("movie title", movies)
docs = db.similarity_search(query, k=6)
docs
