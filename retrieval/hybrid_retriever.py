
import re
import os
import numpy as np
import faiss

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from reranking.reranker import PassageReranker


class HybridRetriever:

    def __init__(
        self,
        embedding_model_name="BAAI/bge-small-en-v1.5",
        reranker_model_name="BAAI/bge-reranker-base"
    ):

        # Load public Hugging Face models without an expired token
        self.embedding_model = SentenceTransformer(
            embedding_model_name,
            token=False
        )

        self.reranker = PassageReranker(
            reranker_model_name
        )

        self.chunks = []
        self.bm25 = None
        self.faiss_index = None

    @staticmethod
    def tokenize(text):
        return re.findall(r"\b\w+\b", text.lower())

    def build(self, chunks):

        if not chunks:
            raise ValueError("No chunks supplied to the retriever.")

        self.chunks = chunks

        # BM25 keyword index
        tokenized = [
            self.tokenize(item["text"])
            for item in chunks
        ]

        self.bm25 = BM25Okapi(tokenized)

        # Generate embedding vectors
        texts = [
            item["text"]
            for item in chunks
        ]

        vectors = self.embedding_model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True
        ).astype("float32")

        # FAISS vector index
        self.faiss_index = faiss.IndexFlatIP(
            vectors.shape[1]
        )

        self.faiss_index.add(vectors)

    def search(
        self,
        question,
        candidate_k=20,
        final_k=5,
        rrf_k=60
    ):

        if self.bm25 is None or self.faiss_index is None:
            raise RuntimeError(
                "Build the indexes before searching."
            )

        candidate_k = min(
            candidate_k,
            len(self.chunks)
        )

        # BM25 keyword retrieval
        bm25_scores = self.bm25.get_scores(
            self.tokenize(question)
        )

        bm25_order = np.argsort(
            bm25_scores
        )[::-1][:candidate_k].tolist()

        # Dense semantic retrieval
        query_vector = self.embedding_model.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        _, vector_indices = self.faiss_index.search(
            query_vector,
            candidate_k
        )

        vector_order = [
            int(i)
            for i in vector_indices[0]
            if i >= 0
        ]

        # Reciprocal Rank Fusion
        fused_scores = {}

        for result_list in (
            bm25_order,
            vector_order
        ):

            for rank, chunk_index in enumerate(
                result_list,
                start=1
            ):

                fused_scores[chunk_index] = (
                    fused_scores.get(chunk_index, 0.0)
                    + 1.0 / (rrf_k + rank)
                )

        fused_order = sorted(
            fused_scores,
            key=fused_scores.get,
            reverse=True
        )

        candidates = [
            self.chunks[index]
            for index in fused_order
        ]

        # Cross-encoder reranking
        reranked = self.reranker.rerank(
            question,
            candidates
        )

        return reranked[:final_k]
