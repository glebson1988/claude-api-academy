"""BM25 lexical index from the "BM25 lexical search" lesson.

Scores documents by the query's words: rare words weigh more, repeated words count with diminishing
returns, long documents are penalized. search() returns (document, distance) pairs like VectorIndex,
smaller = better, so both can go into one Retriever.
"""

import math
import re
from collections import Counter


class BM25Index:
    def __init__(self, k1=1.5, b=0.75, tokenizer=None):
        self.documents = []
        self._corpus_tokens = []
        self._doc_freqs = Counter()  # term -> number of documents that contain it
        self.k1 = k1  # how fast repeats of a word stop adding score
        self.b = b  # how much document length matters (0 = not at all, 1 = fully)
        self._tokenizer = tokenizer or self._default_tokenizer

    @staticmethod
    def _default_tokenizer(text):
        return [token for token in re.split(r"\W+", text.lower()) if token]

    def add_document(self, document):
        if "content" not in document:
            raise ValueError("Document dictionary must contain a 'content' key.")
        tokens = self._tokenizer(document["content"])
        self.documents.append(document)
        self._corpus_tokens.append(tokens)
        self._doc_freqs.update(set(tokens))

    def add_documents(self, documents):
        for document in documents:
            self.add_document(document)

    def idf(self, term):
        """Weight of a term: high for rare terms, near 0 for terms in every document."""
        n, freq = len(self.documents), self._doc_freqs[term]
        return math.log((n - freq + 0.5) / (freq + 0.5) + 1)

    def _score(self, query_tokens, doc_index):
        tokens = self._corpus_tokens[doc_index]
        counts = Counter(tokens)
        avg_len = sum(len(t) for t in self._corpus_tokens) / len(self._corpus_tokens)
        length_norm = 1 - self.b + self.b * len(tokens) / avg_len

        score = 0.0
        for token in query_tokens:
            tf = counts[token]
            if tf:
                score += self.idf(token) * tf * (self.k1 + 1) / (tf + self.k1 * length_norm)
        return score

    def search(self, query, k=1, score_normalization_factor=0.1):
        """Return up to k (document, distance) pairs, best first. Documents without any query word are skipped.

        distance = exp(-0.1 * bm25_score): 1 = no match, closer to 0 = better match.
        """
        if k <= 0:
            raise ValueError("k must be a positive integer.")
        query_tokens = self._tokenizer(query)
        if not self.documents or not query_tokens:
            return []

        scored = [(self._score(query_tokens, i), document) for i, document in enumerate(self.documents)]
        scored = sorted((item for item in scored if item[0] > 0), key=lambda item: item[0], reverse=True)
        return [(document, math.exp(-score_normalization_factor * score)) for score, document in scored[:k]]

    def __len__(self):
        return len(self.documents)

    def __repr__(self):
        return f"BM25Index(count={len(self)}, k1={self.k1}, b={self.b})"
