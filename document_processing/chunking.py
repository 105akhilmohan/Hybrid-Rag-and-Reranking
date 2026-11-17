import re


def create_chunks(pages, chunk_size=650, overlap=100):
    """Split page text into overlapping word chunks with source metadata."""
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    next_id = 0

    for page_data in pages:
        cleaned = re.sub(r"\s+", " ", page_data["text"]).strip()
        words = cleaned.split()
        start = 0

        while start < len(words):
            end = min(start + chunk_size, len(words))
            text = " ".join(words[start:end])
            if text:
                chunks.append({
                    "id": next_id,
                    "source": page_data["source"],
                    "page": page_data["page"],
                    "text": text
                })
                next_id += 1

            if end == len(words):
                break
            start = end - overlap

    return chunks
