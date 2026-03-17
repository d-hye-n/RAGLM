from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

@st.cache_data
def build_tfidf_index(chunk_texts):
    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
    chunk_vectors = vectorizer.fit_transform(chunk_texts)
    return vectorizer, chunk_vectors

def retrieve_chunks(chunks, query, top_k=3):
    chunk_texts = [chunk["text"] for chunk in chunks]

    vectorizer, chunk_vectors = build_tfidf_index(chunk_texts)
    query_vector = vectorizer.transform([query])

    scores = cosine_similarity(query_vector, chunk_vectors).flatten()
    ranked_indices = scores.argsort()[::-1][:top_k]

    results = []
    for idx in ranked_indices:
        results.append({
            "page": chunks[idx]["page"],
            "text": chunks[idx]["text"],
            "score": float(scores[idx])
        })

    return results