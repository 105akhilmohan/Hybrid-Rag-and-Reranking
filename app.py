
import re
import markdown
import bleach

from flask import Flask, render_template, request, redirect, url_for, flash

from document_processing.pdf_loader import extract_pages_from_pdf
from document_processing.chunking import create_chunks
from retrieval.hybrid_retriever import HybridRetriever
from generation.answer_generator import generate_answer

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret"

retriever = None
documents = []
selected_passages = []


@app.route("/")
def home():
    return render_template(
        "index.html",
        indexed=retriever is not None,
        documents=documents
    )


@app.route("/upload", methods=["POST"])
def upload():
    global retriever, documents

    files = request.files.getlist("pdf_files")

    if not files or all(not file.filename for file in files):
        flash("Please select PDF files.")
        return redirect(url_for("home"))

    try:
        pages = []
        new_documents = []

        for file in files:
            if not file.filename.lower().endswith(".pdf"):
                continue

            pages.extend(
                extract_pages_from_pdf(
                    file.read(),
                    file.filename,
                    True
                )
            )

        chunks = create_chunks(pages)

        if not chunks:
            flash("No text extracted. Check OCR or PDF content.")
            return redirect(url_for("home"))

        new_retriever = HybridRetriever()
        new_retriever.build(chunks)

        for file in files:
            if file.filename:
                file_chunks = [
                    chunk for chunk in chunks
                    if chunk.get("source") == file.filename
                ]

                new_documents.append({
                    "name": file.filename,
                    "chunks": len(file_chunks)
                })

        retriever = new_retriever
        documents = new_documents

        flash(f"Successfully indexed {len(chunks)} chunks.")

    except Exception as error:
        app.logger.exception("PDF upload failed")
        flash(f"Upload failed: {error}")

    return redirect(url_for("home"))


@app.route("/ask", methods=["POST"])
def ask():
    global selected_passages

    if retriever is None:
        flash("Upload a PDF and build the index first.")
        return redirect(url_for("home"))

    question = request.form.get("question", "").strip()

    if not question:
        flash("Please enter a question.")
        return redirect(url_for("home"))

    try:
        selected = retriever.search(
            question,
            candidate_k=20,
            final_k=5
        )

        answer = generate_answer(question, selected)

        selected_passages = selected

        # Remove source citation lines
        clean_answer = re.sub(
            r"(?im)^\s*(?:\*{1,2})?sources?(?:\*{1,2})?\s*:.*$",
            "",
            answer
        )

        # Convert Markdown to HTML
        formatted_answer = markdown.markdown(
            clean_answer.strip(),
            extensions=["extra", "nl2br"]
        )

        # Sanitize generated HTML
        allowed_tags = [
            "p", "br", "strong", "b", "em", "i",
            "h1", "h2", "h3", "h4",
            "ul", "ol", "li", "blockquote",
            "code", "pre", "hr"
        ]

        safe_answer = bleach.clean(
            formatted_answer,
            tags=allowed_tags,
            strip=True
        )

        return render_template(
            "answer.html",
            question=question,
            answer=safe_answer,
            passages=selected
        )

    except Exception as error:
        app.logger.exception("Question answering failed")
        flash(f"Could not generate answer: {error}")
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
