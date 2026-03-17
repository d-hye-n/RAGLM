from pypdf import PdfReader
import streamlit as st

@st.cache_data
def extract_text_by_page(file_bytes):
    from io import BytesIO
    reader = PdfReader(BytesIO(file_bytes))
    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages.append({
                "page" : i+1,
                "text": text
            })

    return pages
