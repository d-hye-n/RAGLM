from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def retrieve_chunks(chunks, query, top_k=3):
    chunk_texts = [chunk["text"] for chunk in chunks]

    vectorizer = TfidfVectorizer()
    chunk_vectors = vectorizer.fit_transform(chunk_texts)
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