
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv(
        "OPENROUTER_BASE_URL",
        "https://openrouter.ai/api/v1"
    )
)

def generate_answer(question, chunks, ollama_url=None, model=None):

    if not chunks:
        return "I could not find relevant information in the uploaded documents."

    context = "\n\n".join(
        f"[Source: {chunk['source']}, Page: {chunk['page']}]\n{chunk['text']}"
        for chunk in chunks
    )

    prompt = f"""You are an educational question-answering assistant.

Use only the document context below to answer the question.

Rules:
- Explain clearly in student-friendly language.
- Do not invent facts or use outside knowledge.
- If the context does not answer the question, say that the uploaded
  documents do not provide enough information.
- Cite the source filename and page number when possible.

DOCUMENT CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    try:
        response = client.chat.completions.create(
            model=os.getenv(
                "LLM_MODEL",
                "nvidia/nemotron-3.5-super-vl:free"
            ),
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        return response.choices[0].message.content.strip()

    except Exception as error:
        return f"Answer generation failed: {error}"
