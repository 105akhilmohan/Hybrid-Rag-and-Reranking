from sentence_transformers import CrossEncoder


class PassageReranker:
    def __init__(self, model_name="BAAI/bge-reranker-base"):
        self.model = CrossEncoder(model_name)

    def rerank(self, question, chunks):
        if not chunks:
            return []

        pairs = [[question, chunk["text"]] for chunk in chunks]
        scores = self.model.predict(pairs)

        # Copy dictionaries so the original chunk objects are not modified.
        ranked = []
        for chunk, score in zip(chunks, scores):
            item = dict(chunk)
            item["rerank_score"] = float(score)
            ranked.append(item)

        ranked.sort(key=lambda item: item["rerank_score"], reverse=True)
        return ranked
