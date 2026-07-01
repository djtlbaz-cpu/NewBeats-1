from __future__ import annotations

import glob
import os
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class RagDoc:
    text: str
    path: str


def _safe_read_text(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


def _normalize_text(s: str) -> str:
    s = s.lower()
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _keyword_overlap_score(query: str, doc: str) -> float:
    q = set(_normalize_text(query).split())
    d = set(_normalize_text(doc).split())
    if not q or not d:
        return 0.0
    return float(len(q & d)) / float(len(q))


def _chunk_text(text: str, chunk_size_chars: int = 800, overlap_chars: int = 100) -> List[str]:
    text = text.strip()
    if not text:
        return []
    if len(text) <= chunk_size_chars:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size_chars)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(0, end - overlap_chars)
    return chunks


class RagEngine:
    """
    Bulletproof RAG:
    - If rag_data/ missing/empty -> returns empty context.
    - If sentence-transformers unavailable -> uses keyword overlap retrieval.
    - Never raises on runtime; best-effort only.
    """

    def __init__(
        self,
        rag_dir: str = "rag_data",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        top_k: int = 4,
    ):
        self.rag_dir = rag_dir
        self.embedding_model = embedding_model
        self.top_k = top_k

        self._docs: List[RagDoc] = []
        self._chunks: List[str] = []
        self._chunk_sources: List[str] = []

        # Embedding mode flags
        self._st_available = False
        self._embedder = None
        self._embeddings = None

        self._load_and_index()

    def _load_and_index(self) -> None:
        # Load docs
        try:
            paths = sorted(glob.glob(os.path.join(self.rag_dir, "*.txt")))
        except Exception:
            paths = []

        for p in paths:
            t = _safe_read_text(p)
            if t and t.strip():
                self._docs.append(RagDoc(text=t, path=p))

        if not self._docs:
            # No data -> no index
            self._chunks = []
            self._chunk_sources = []
            self._embeddings = None
            self._st_available = False
            return

        # Chunk docs
        chunks: List[str] = []
        sources: List[str] = []
        for d in self._docs:
            for c in _chunk_text(d.text):
                chunks.append(c)
                sources.append(d.path)

        self._chunks = chunks
        self._chunk_sources = sources

        # Try sentence-transformers indexing (best-effort)
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore

            # Create embedder
            self._embedder = SentenceTransformer(self.embedding_model)
            # Compute embeddings on CPU; sentence-transformers will handle device internally.
            self._embeddings = self._embedder.encode(
                self._chunks,
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=True,
            )
            self._st_available = True
        except Exception:
            self._st_available = False
            self._embedder = None
            self._embeddings = None

    def _retrieve_top_chunks(self, query: str, top_k: Optional[int] = None) -> List[Tuple[str, float]]:
        top_k = top_k or self.top_k
        top_k = max(1, int(top_k))

        if not self._chunks:
            return []

        query = query or ""
        if not query.strip():
            return []

        # Embedding retrieval
        if self._st_available and self._embeddings is not None and self._embedder is not None:
            try:
                q_emb = self._embedder.encode(
                    [query],
                    show_progress_bar=False,
                    convert_to_numpy=True,
                    normalize_embeddings=True,
                )[0]
                # cosine similarity since embeddings are normalized
                sims = (self._embeddings @ q_emb).tolist()
                scored = list(zip(self._chunks, sims))
                scored.sort(key=lambda x: x[1], reverse=True)
                return scored[:top_k]
            except Exception:
                # fall back
                pass

        # Keyword fallback
        scored = [(c, _keyword_overlap_score(query, c)) for c in self._chunks]
        scored.sort(key=lambda x: x[1], reverse=True)
        # Filter very low scores, but keep at least some context if possible
        filtered = [s for s in scored if s[1] > 0.0]
        return filtered[:top_k] if filtered else scored[:top_k]

    def build_context(self, query: str, top_k: Optional[int] = None, max_chars: int = 1600) -> str:
        try:
            top = self._retrieve_top_chunks(query, top_k=top_k)
            if not top:
                return ""

            parts = []
            total = 0
            for i, (chunk, _score) in enumerate(top, start=1):
                # Ensure bullet-proof truncation
                chunk = chunk.strip()
                if not chunk:
                    continue
                remaining = max_chars - total
                if remaining <= 0:
                    break
                if len(chunk) > remaining:
                    chunk = chunk[:remaining].rstrip() + "…"
                parts.append(f"[{i}] {chunk}")
                total += len(chunk) + 3

            return "\n".join(parts).strip()
        except Exception:
            return ""
