"""Chunking strategies from the "Text chunking strategies" lesson, shared by the RAG notebooks."""

import re


def chunk_by_char(text, chunk_size=150, chunk_overlap=20):
    if not 0 <= chunk_overlap < chunk_size:
        raise ValueError("chunk_overlap must be at least 0 and less than chunk_size")

    chunks = []
    start_idx = 0

    while start_idx < len(text):
        end_idx = min(start_idx + chunk_size, len(text))
        chunks.append(text[start_idx:end_idx])
        start_idx = end_idx - chunk_overlap if end_idx < len(text) else len(text)

    return chunks


def chunk_by_sentence(text, max_sentences_per_chunk=5, overlap_sentences=1):
    if not 0 <= overlap_sentences < max_sentences_per_chunk:
        raise ValueError("overlap_sentences must be at least 0 and less than max_sentences_per_chunk")

    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks = []
    start_idx = 0

    while start_idx < len(sentences):
        end_idx = min(start_idx + max_sentences_per_chunk, len(sentences))
        chunks.append(" ".join(sentences[start_idx:end_idx]))
        if end_idx == len(sentences):
            break
        start_idx += max_sentences_per_chunk - overlap_sentences

    return chunks


def chunk_by_section(document_text):
    # Split before each "## " header (lookahead), so every chunk keeps its header
    return [section.strip() for section in re.split(r"\n(?=## )", document_text) if section.strip()]
