# -*- coding: utf-8 -*-
"""preprocessed_model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1urkeSktrWRFVMxMERBc8X3dV-yZQXHCc
"""

import numpy as np
import pandas as pd
from transformers import pipeline

# Load data
books = pd.read_csv("/content/sample_data/reddit_data_after_new_analysis.csv")

# Fill missing text fields
books['text_for_embedding'] = books['description'].fillna(books['title'])

# Load model (CPU or GPU as needed)
feature_extractor = pipeline("feature-extraction", model="sentence-transformers/all-MiniLM-L6-v2")

# Compute and store embeddings
embeddings = []
for text in books['text_for_embedding']:
    emb = feature_extractor(text, truncation=True, max_length=512)
    embeddings.append(np.array(emb[0][0]))

# Convert and save
emb_matrix = np.vstack(embeddings)
np.save("book_embeddings.npy", emb_matrix)
books.to_csv("books_with_embeddings.csv", index=False)

