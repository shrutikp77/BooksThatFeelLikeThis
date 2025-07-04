# -*- coding: utf-8 -*-
"""streamlit_book_recommendations.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1V3fx7X00Xn-_H50YNyhiDdR1Imyriyfj
"""



# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity

# Cache and load preprocessed data and model
@st.cache_resource
def load_data():
    books = pd.read_csv("books_with_embeddings.csv")
    emb_matrix = np.load("book_embeddings.npy")
    feature_extractor = pipeline("feature-extraction", model="sentence-transformers/all-MiniLM-L6-v2")
    return books, emb_matrix, feature_extractor

books, emb_matrix, feature_extractor = load_data()

# Recommendation function
def recommend_top5_by_feeling(user_feeling, top_k=5):
    user_emb = np.array(
        feature_extractor(user_feeling, truncation=True, max_length=512)[0][0]
    ).reshape(1, -1)
    sims = cosine_similarity(user_emb, emb_matrix)[0]
    top_ids = np.argsort(sims)[-top_k:][::-1]
    return [
        {
            "title": books.iloc[i]["clean_title_new"],
            "similarity": round(sims[i], 3)
        } for i in top_ids
    ]

# Streamlit UI
st.set_page_config(page_title="Book Recommender", page_icon="📚")
st.title("📚 Mood-Based Book Recommender")

st.write(
    "Tell us how you're feeling, and we'll recommend books that match your vibe"
)

user_input = st.text_input("How are you feeling today?", placeholder="e.g., nostalgic, hopeful, anxious...")

if user_input:
    with st.spinner("Finding the best books for your mood..."):
        recommendations = recommend_top5_by_feeling(user_input)

    st.subheader("Top 5 Book Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"**{i}. {rec['title']}** — _similarity score: {rec['similarity']}_")

