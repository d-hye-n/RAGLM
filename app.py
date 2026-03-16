import streamlit as st
from pdf_utils import extract_text_by_page
from chunking import chunk_pages
from retrieval import retrieve_chunks

st.title("RagLm_mini")
uploaded_file = st.file_uploader("Upload PDF file", type="pdf")
question = st.text_input("Input Question")

if uploaded_file is not None:
    st.success(f"Upload Complete: {uploaded_file.name}")

    pages = extract_text_by_page(uploaded_file)
    chunks = chunk_pages(pages, chunk_size=500, overlap=100)

    st.write(f"Total Pages: {len(pages)}")
    st.write(f"Total Chunks: {len(chunks)}")

    if question:
        results = retrieve_chunks(chunks, question, top_k=3)

        st.subheader("Search Result")
        for i, result in enumerate(results, start=1):
            st.markdown(f"**{i}. page {result['page']} / score {result['score']:.4f}**")
            st.write(result["text"])
            st.divider()