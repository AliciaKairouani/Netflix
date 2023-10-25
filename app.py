import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.document_loaders.csv_loader import CSVLoader
from dotenv import load_dotenv
from supabase import create_client, Client
import os

st.set_page_config(layout="wide")
st.title("Movies App")

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
docs
