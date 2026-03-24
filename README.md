# NotebookLM

A lightweight PDF-based question answering web app inspired by NotebookLM.

Users can upload a PDF, ask questions about the document, retrieve relevant passages, and get an answer grounded in the retrieved evidence.

This project was built as a portfolio-scale MVP focused on the core RAG pipeline:
PDF upload → text extraction → chunking → retrieval → answer generation → evidence display.

---

## Features

- Upload a PDF file
- Extract text page by page
- Split the document into overlapping chunks
- Retrieve relevant chunks for a given question
- Generate an answer with Gemini
- Show supporting evidence with page numbers
- Let the user adjust the number of evidence chunks
- Reduce unnecessary recomputation with Streamlit caching and forms

---

## Tech Stack

- Python
- Streamlit
- PyPDF
- scikit-learn
- Google Gemini API (`google-genai`)

---

## Project Structure

```text
.
├── app.py
├── pdf_utils.py
├── chunking.py
├── retrieval.py
├── answering.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env.example
└── README.md
```

---

## How It Works

```text
PDF upload
→ text extraction
→ chunking
→ retrieval
→ context construction
→ Gemini answer generation
→ evidence display
```

The app does not send the whole document directly to the model.
Instead, it first retrieves relevant passages and then sends only the selected context to the LLM.

---

## Local Development

### 1. Create a virtual environment

#### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

---

## Docker

### Build image
```bash
docker build -t raglm-mini .
```

### Run container
```bash
docker run -p 8501:8501 raglm-mini
```

Then open:

```text
http://localhost:8501
```

This project is designed so that users can input their own Gemini API key in the app UI,
so a server-side API key is not strictly required for basic demo usage.

---

## Why I Built It This Way

The goal of this project was not to make a simple “upload a PDF and call an API” demo.

I wanted to implement the core flow of a document-based RAG system directly:

- break documents into chunks instead of sending everything at once
- retrieve relevant evidence before answer generation
- show evidence with page numbers
- improve retrieval quality for Korean question forms
- reduce unnecessary recomputation in Streamlit

---

## Problem-Solving Process

### 1. Started from the smallest working pipeline

I first implemented the smallest end-to-end flow:

- upload a PDF
- extract text page by page
- split the text into chunks
- retrieve relevant chunks
- generate an answer

At this stage, the priority was not optimization but making the whole pipeline work from start to finish.

---

### 2. Separated retrieval from answer generation

Instead of sending the whole PDF content directly to the model, I explicitly separated the system into two steps:

1. retrieve relevant chunks
2. generate an answer from retrieved context

This made the application easier to debug and closer to an actual retrieval-augmented generation pipeline.

It also made it easier to inspect whether a bad answer came from retrieval quality or from the LLM itself.

---

### 3. Found retrieval quality issues in Korean question forms

While testing the app, I noticed that short keyword-like queries often worked better than natural Korean questions.

For example:

- `MDP`
- `What is MDP?`

These two queries should behave similarly, but the retriever did not always rank results consistently.

The issue was not in Gemini itself.
The problem was in the retrieval stage.

---

### 4. Identified the cause: word-level TF-IDF was weak for Korean particles and inflected forms

The initial retriever used the default word-level TF-IDF setup.

That worked reasonably well for short exact keywords, but it was weaker when Korean particles or question endings were attached to the core term.

For example, a keyword like `MDP` could behave differently from `What is MDP?`,
even though they refer to the same concept from a user perspective.

This showed that the real issue was tokenization behavior in retrieval, not answer generation.

---

### 5. Improved retrieval using char n-gram TF-IDF

To make retrieval more robust to Korean question forms, I changed the retriever to use character n-grams:

```python
TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
```

This improved stability for queries such as:

- `MDP`
- `What is MDP?`

The reason was simple:
character n-grams can match overlapping subword patterns even when particles or endings are attached.

This was one of the most important improvements in the project because it directly improved the retrieval layer rather than hiding the problem behind the LLM.

---

### 6. Found performance issues caused by Streamlit reruns

Another issue appeared during interactive use.

Because Streamlit reruns the script when widget state changes, expensive steps were being repeated too often:

- PDF parsing
- chunk generation
- TF-IDF index construction

This made the app feel slower than necessary.

---

### 7. Reduced unnecessary recomputation

To improve responsiveness, I added:

- `st.cache_data` for extracted pages
- `st.cache_data` for chunk generation
- cached TF-IDF index creation
- form-based submission for API key input
- form-based submission for question input

This reduced unnecessary reruns and improved the perceived speed of the app significantly.

---

### 8. Improved the UI around retrieval control

Instead of exposing `top_k` directly as a technical parameter, I changed it into a user-facing control called **evidence count**.

This made the UI easier to understand and also helped demonstrate an important trade-off:

- fewer evidence chunks can miss relevant context
- more evidence chunks can introduce noise

This was useful both from a UX perspective and from a portfolio/demo perspective.

---

## Key Design Choices

### Chunking before generation
I did not send the full document directly to the model.
Chunking makes retrieval possible and keeps the context focused.

### Retrieval before answer generation
I wanted the answer to be grounded in document evidence, not generated from the model’s general knowledge alone.

### Show evidence with page numbers
This makes the answer more inspectable and helps users verify where the answer came from.

### Keep the first version simple
I used TF-IDF retrieval instead of jumping straight to embeddings or a vector database.
For this MVP, simplicity and explainability were more important than building a larger stack too early.

---

## Current Limitations

This project is an MVP and still has several limitations:

- no multi-turn conversation memory
- no OCR for scanned PDFs
- retrieval is TF-IDF based, so semantic search is limited
- answer quality still depends strongly on retrieved chunks
- only basic single-document QA behavior is supported well

---

## Future Improvements

Possible next steps include:

- multi-turn conversation support
- query rewriting for follow-up questions
- embedding-based retrieval
- vector database integration
- OCR support for scanned PDFs
- document summarization
- highlighting retrieved evidence in the UI
- multi-document comparison

---

## What I Learned

At first glance, this looked like a simple “PDF + LLM” project.

In practice, the more important parts were:

- retrieval quality
- chunk design
- context construction
- rerun/caching behavior in Streamlit
- presenting evidence clearly

The most meaningful part of the project was not just connecting Gemini,
but identifying why retrieval failed on certain Korean question forms and improving it with char n-gram TF-IDF.

This project helped me understand the core structure of a document-based RAG application
and the difference between “calling an API” and actually building a system around retrieval and grounded answering.
