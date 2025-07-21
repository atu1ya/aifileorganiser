"""
AI-powered sorting, embeddings, clustering
"""

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    from sklearn.cluster import KMeans
    AI_DEPENDENCIES_AVAILABLE = True
except ImportError:
    AI_DEPENDENCIES_AVAILABLE = False



def get_text_embeddings(texts, model_name="all-MiniLM-L6-v2"):
    if not AI_DEPENDENCIES_AVAILABLE:
        raise ImportError("sentence-transformers, numpy, or scikit-learn not installed. Please install them for AI sorting.")
    model = SentenceTransformer(model_name)
    return model.encode(texts)


def cluster_embeddings(embeddings, n_clusters=5):
    if not AI_DEPENDENCIES_AVAILABLE:
        raise ImportError("sentence-transformers, numpy, or scikit-learn not installed. Please install them for AI sorting.")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)
    return labels
