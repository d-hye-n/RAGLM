import streamlit as st
from pdf_utils import extract_text_by_page
from chunking import chunk_pages
from retrieval import retrieve_chunks
from answering import build_context, answer_question


st.title("RagLm_mini")

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

with st.sidebar:
    st.subheader("Settings Gemini")

    with st.form("api_form"):
        api_key_input = st.text_input(
            "Gemini API Key",
            type="password",
            value=st.session_state.api_key
        )
        api_submitted = st.form_submit_button("API Key Save")

    if api_submitted:
        st.session_state.api_key = api_key_input.strip()
        if st.session_state.api_key:
            st.success("API Key Saved")
        else:
            st.warning("API Key is Empty")


uploaded_file = st.file_uploader("Upload PDF file", type="pdf")

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    pages = extract_text_by_page(file_bytes)
    chunks = chunk_pages(pages, chunk_size=500, overlap=100)
    evidence_k = st.slider("Number of evidence",
                           min_value=3,
                           max_value=7,
                           value=3,
                           step=1,
                           help="larger number can find wider, but it also can find wrong."
    )

    st.write(f"Total Pages: {len(pages)}")
    st.write(f"Total Chunks: {len(chunks)}")

    with st.form("Question_form"):
        question = st.text_input("Input Question")
        qa_submitted = st.form_submit_button("Submit")

    if qa_submitted:
        if not st.session_state.api_key:
            st.error("Save API Key First")
        elif not question.strip():
            st.warning("Please Submit Question")
        else:
            results = retrieve_chunks(chunks, question, top_k=evidence_k)
            context = build_context(results)
            answer = answer_question(question,
                                     context,
                                     st.session_state.api_key
                                     )

            st.subheader("Answer")
            st.write(answer)

            st.subheader("Searching result")
            for i, result in enumerate(results, start=1):
                st.markdown(f"**{i}. page {result['page']} / score {result['score']:.4f}**")
                st.write(result["text"])
                st.divider()