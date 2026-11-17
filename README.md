# Hybrid RAG and Reranking

An AI-powered document question-answering system that combines **Semantic Search, BM25 Keyword Search, Hybrid Retrieval, and Reranking** to provide accurate, context-aware answers from uploaded PDF documents.

## Overview

Hybrid RAG and Reranking is a Retrieval-Augmented Generation (RAG) application designed to extract information from PDF documents, textbooks, notes, and educational materials.

Instead of relying only on an LLM's pre-trained knowledge, the system retrieves relevant information from uploaded documents and uses the retrieved passages to generate answers.

The application combines semantic similarity and keyword-based retrieval to improve document search accuracy. A reranking stage then prioritizes the most relevant passages before answer generation.

## Key Features

- **PDF Upload:** Upload PDF documents through a web interface.
- **Text Extraction:** Extract text from PDF documents, with OCR support.
- **Document Chunking:** Split extracted content into smaller passages for efficient retrieval.
- **Semantic Search:** Find relevant passages based on the meaning of the query.
- **BM25 Keyword Search:** Retrieve documents using keyword relevance.
- **Hybrid Retrieval:** Combine semantic and keyword-based search results.
- **Reranking:** Reorder retrieved passages based on their relevance to the user's question.
- **AI Answer Generation:** Generate context-aware answers using retrieved document content.
- **Source Passages:** Display relevant retrieved passages alongside generated answers.

## Architecture

The system follows a multi-stage RAG pipeline:

```text
              PDF Documents
                    |
                    v
            PDF Text Extraction
                    |
                    v
              OCR Processing
                    |
                    v
             Text Chunking
                    |
                    v
             Document Indexing
                    |
          +---------+---------+
          |                   |
          v                   v
    Vector Search         BM25 Search
    (Semantic)             (Keyword)
          |                   |
          +---------+---------+
                    |
                    v
             Hybrid Retrieval
                    |
                    v
                Reranking
                    |
                    v
          Top Relevant Passages
                    |
                    v
            LLM Answer Generation
                    |
                    v
             Final Answer
```

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Flask | Web application backend |
| Sentence Transformers | Semantic embeddings |
| FAISS | Vector similarity search |
| BM25 | Keyword-based retrieval |
| Reranking | Improve retrieval relevance |
| PyMuPDF | PDF text extraction |
| Tesseract OCR | Extract text from scanned documents |
| NumPy | Numerical operations |
| HTML, CSS | User interface |

## Retrieval and Reranking

### 1. Semantic Search

Uses embedding models to convert document chunks and user queries into numerical vectors.

FAISS searches for passages that are semantically similar to the user's question, even when the exact keywords are different.

### 2. BM25 Keyword Search

BM25 is a ranking algorithm used for keyword-based information retrieval.

It identifies relevant passages by considering query-term frequency and document-term importance.

### 3. Hybrid Retrieval

Combines the results of semantic search and BM25 search.

This approach provides two complementary retrieval methods:

- Semantic search understands the meaning of the question.
- BM25 identifies exact keywords and terminology.

### 4. Reranking

The retrieved passages are passed through a reranking stage to prioritize the most relevant content.

The application initially retrieves up to 20 candidate passages and selects the top 5 passages for answer generation.

### 5. Answer Generation

The selected passages are passed to the answer-generation component, which generates a response based on the retrieved document context.

## Project Structure

```text
Hybrid-Rag-and-Reranking/
│
├── document_processing/
│   ├── pdf_loader.py
│   └── chunking.py
│
├── retrieval/
│   └── hybrid_retriever.py
│
├── reranking/
│
├── generation/
│   └── answer_generator.py
│
├── evaluation/
│
├── static/
│   └── css/
│
├── templates/
│
├── app.py
│
├── requirements.txt
│
├── .gitignore
│
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/105akhilmohan/Hybrid-Rag-and-Reranking.git
```

### 2. Navigate to the Project Directory

```bash
cd Hybrid-Rag-and-Reranking
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Tesseract OCR

Install Tesseract OCR if you need to process scanned PDF documents.

Official repository:

https://github.com/tesseract-ocr/tesseract

Make sure Tesseract is installed and accessible to your Python environment.

### 6. Run the Application

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

## Evaluation

The project includes an evaluation module for assessing retrieval performance.

Possible evaluation dimensions include:

- Retrieval relevance
- Search accuracy
- Ranking quality
- Context relevance
- Answer quality

## Use Cases

- Question answering from educational textbooks.
- Searching and retrieving information from PDF documents.
- Understanding technical documentation.
- Extracting information from research papers.
- Building document-based AI assistants.
- Creating knowledge-base question-answering systems.

## Future Improvements

- Support for multiple document formats.
- Advanced document chunking strategies.
- Improved reranking models.
- Conversation history and contextual follow-up questions.
- Retrieval evaluation using Recall@K, Precision@K, MRR, and nDCG.
- Improved answer grounding and citation verification.
- Deployment using Docker and cloud platforms.

## Author

**Akhil Mohan**

GitHub: https://github.com/105akhilmohan

---

⭐ If you find this project useful, consider giving it a star!
