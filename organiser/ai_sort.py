"""
AI-powered sorting, embeddings, clustering
"""
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.cluster import KMeans

def get_text_embeddings(texts, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    return model.encode(texts)

def cluster_embeddings(embeddings, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)
    return labels
