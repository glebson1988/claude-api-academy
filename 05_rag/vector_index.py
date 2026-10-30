"""In-memory vector store from the "Implementing the RAG flow" lesson.

A stand-in for a real vector database: it keeps every vector in a list and compares the query
with all of them. Fine for a few hundred chunks.
"""

import math


class VectorIndex:
    def __init__(self, distance_metric="cosine", embedding_fn=None):
        if distance_metric not in ("cosine", "euclidean"):
            raise ValueError("distance_metric must be 'cosine' or 'euclidean'")
        self.vectors = []
        self.documents = []
        self._vector_dim = None
        self._distance_metric = distance_metric
        self._embedding_fn = embedding_fn

    def add_vector(self, vector, document):
        if "content" not in document:
            raise ValueError("Document dictionary must contain a 'content' key.")
        if self._vector_dim is None:
            self._vector_dim = len(vector)
        elif len(vector) != self._vector_dim:
            raise ValueError(f"Inconsistent vector dimension. Expected {self._vector_dim}, got {len(vector)}")
        self.vectors.append(list(vector))
        self.documents.append(document)

    def add_document(self, document):
        self.add_documents([document])

    def add_documents(self, documents):
        """Embed all documents in one request. embedding_fn(texts, input_type=...) returns one vector per text."""
        if not self._embedding_fn:
            raise ValueError("Embedding function not provided during initialization.")
        vectors = self._embedding_fn([document["content"] for document in documents], input_type="document")
        for vector, document in zip(vectors, documents, strict=True):
            self.add_vector(vector, document)

    def search(self, query, k=1):
        """Return the k closest documents as (document, distance) pairs, closest first."""
        if k <= 0:
            raise ValueError("k must be a positive integer.")
        if not self.vectors:
            return []
        if isinstance(query, str):
            if not self._embedding_fn:
                raise ValueError("Embedding function not provided for string query.")
            query = self._embedding_fn(query, input_type="query")
        if len(query) != self._vector_dim:
            raise ValueError(f"Query vector dimension mismatch. Expected {self._vector_dim}, got {len(query)}")

        distance = self._cosine_distance if self._distance_metric == "cosine" else self._euclidean_distance
        scored = sorted(
            ((distance(query, vector), document) for vector, document in zip(self.vectors, self.documents, strict=True)),
            key=lambda item: item[0],
        )
        return [(document, dist) for dist, document in scored[:k]]

    @staticmethod
    def _euclidean_distance(vec1, vec2):
        return math.dist(vec1, vec2)

    @staticmethod
    def _cosine_distance(vec1, vec2):
        """1 - cosine similarity: 0 = same direction, 1 = unrelated, 2 = opposite."""
        mag1, mag2 = math.hypot(*vec1), math.hypot(*vec2)
        if mag1 == 0 or mag2 == 0:
            return 0.0 if mag1 == mag2 else 1.0
        similarity = sum(p * q for p, q in zip(vec1, vec2, strict=True)) / (mag1 * mag2)
        return 1.0 - max(-1.0, min(1.0, similarity))

    def __len__(self):
        return len(self.vectors)

    def __repr__(self):
        has_embed_fn = "Yes" if self._embedding_fn else "No"
        return (
            f"VectorIndex(count={len(self)}, dim={self._vector_dim}, "
            f"metric='{self._distance_metric}', has_embedding_fn='{has_embed_fn}')"
        )
