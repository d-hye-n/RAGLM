import streamlit as st
from pdf_utils import extract_text_by_page
from chunking import chunk_pages
from retrieval import retrieve_chunks
from answering import build_context, answer_question


st.title("RagLm_mini")

api_key = st.text_input("Gemini API Key", type="password")

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
        context = build_context(results)
        answer = answer_question(question, context, api_key)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Searching result")
        for i, result in enumerate(results, start=1):
            st.markdown(f"**{i}. page {result['page']} / score {result['score']:.4f}**")
            st.write(result["text"])
            st.divider()