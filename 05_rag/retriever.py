"""Multi-index retriever from the "A multi-index RAG pipeline" lesson: merges rankings with RRF.

Reciprocal Rank Fusion: score(doc) = sum over indexes of 1 / (k_rrf + rank of doc in that index).
Only ranks are used, so a cosine distance and a BM25 score never have to be compared directly.
"""

from typing import Protocol


class SearchIndex(Protocol):
    def add_document(self, document) -> None: ...

    def add_documents(self, documents) -> None: ...

    def search(self, query, k=1) -> list: ...


class Retriever:
    def __init__(self, *indexes: SearchIndex):
        if not indexes:
            raise ValueError("At least one index must be provided")
        self._indexes = list(indexes)

    def add_document(self, document):
        for index in self._indexes:
            index.add_document(document)

    def add_documents(self, documents):
        for index in self._indexes:
            index.add_documents(documents)

    def search(self, query_text, k=1, k_rrf=60):
        """Return the k best (document, rrf_score) pairs, highest score first."""
        if k <= 0:
            raise ValueError("k must be a positive integer.")
        if k_rrf < 0:
            raise ValueError("k_rrf must be non-negative.")

        scores = {}  # id(document) -> [document, rrf_score]; every index holds the same dict objects
        for index in self._indexes:
            # look deeper than k in each index: a document ranked 4th in both can beat one ranked 1st in one
            for rank, (document, _) in enumerate(index.search(query_text, k=k * 5), start=1):
                entry = scores.setdefault(id(document), [document, 0.0])
                entry[1] += 1 / (k_rrf + rank)

        ranked = sorted(scores.values(), key=lambda entry: entry[1], reverse=True)
        return [(document, score) for document, score in ranked[:k]]
