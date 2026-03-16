def chunk_pages(pages, chunk_size=500, overlap=100):
    chunks = []

    for page_data in pages:
        page = page_data["page"]
        text = page_data["text"].strip()

        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "page": page,
                    "text": chunk_text
                })

            if end >= text_length:
                break

            start += chunk_size - overlap

    return chunks