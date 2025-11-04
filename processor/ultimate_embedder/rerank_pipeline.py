"""Cross-encoder reranking pipeline extracted from the embedder facade."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Sequence

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from processor.ultimate_embedder.compat import CrossEncoder
from processor.ultimate_embedder.config import (
    RERANKING_MODELS,
    RerankingConfig,
    get_reranking_model_config,
)


class RerankPipeline:
    """Coordinate CrossEncoder reranking for semantic search."""

    def __init__(self, config: RerankingConfig, logger: logging.Logger) -> None:
        self.config = config
        self.logger = logger
        self.model: Optional[CrossEncoder] = None
        self.device: str = "cpu"

    def ensure_model(self, *, device: str) -> None:
        """Load the reranking model if enabled and not already available."""

        if not self.config.enable_reranking:
            return
        if self.model is not None:
            return

        model_name = self.config.model_name
        if model_name not in RERANKING_MODELS:
            self.logger.warning(
                "Unknown reranker %s, defaulting to jina-reranker-v3", model_name
            )
            model_name = "jina-reranker-v3"
            self.config.model_name = model_name

        spec = get_reranking_model_config(model_name)
        hub_id = spec.hf_model_id
        cross_encoder_kwargs: Dict[str, Any] = {
            "device": device,
            "trust_remote_code": spec.trust_remote_code,
        }

        automodel_args = dict(spec.automodel_args)
        if spec.trust_remote_code:
            automodel_args.setdefault("trust_remote_code", True)
        if automodel_args:
            cross_encoder_kwargs["automodel_args"] = automodel_args

        self.logger.info(
            "Loading reranking model: %s (trust_remote_code=%s)",
            hub_id,
            spec.trust_remote_code,
        )

        try:
            self.model = CrossEncoder(hub_id, **cross_encoder_kwargs)
            self.device = device
            self.logger.info("CrossEncoder reranking model ready")
        except Exception as exc:  # pragma: no cover - defensive path
            self.logger.error("Failed to load reranking model: %s", exc)
            self.config.enable_reranking = False
            self.model = None

    def search(
        self,
        query: str,
        *,
        encode_model: Any,
        device: str,
        embeddings: np.ndarray,
        chunk_texts: Sequence[str],
        chunks_metadata: Sequence[Dict[str, Any]],
        top_k: int = 20,
        initial_candidates: int = 100,
    ) -> List[Dict[str, Any]]:
        """Run a CrossEncoder reranking pass with embedding fallback."""

        if embeddings is None:
            raise ValueError("No embeddings available. Generate embeddings first.")

        query_embedding = self._encode_query(encode_model, query, device)
        similarities = self._compute_similarities(query_embedding, embeddings)

        if not self.config.enable_reranking or self.model is None:
            self.logger.warning("Reranking not enabled, using embedding-only search")
            return self._build_embedding_only_results(
                similarities,
                chunk_texts,
                chunks_metadata,
                top_k,
            )

        top_indices = np.argsort(similarities)[::-1][:initial_candidates]
        query_doc_pairs: List[List[str]] = []
        candidate_indices: List[int] = []

        for idx in top_indices:
            if idx >= len(chunk_texts):
                continue
            doc_text = chunk_texts[idx]
            if not isinstance(doc_text, str):
                doc_text = str(doc_text)
            query_doc_pairs.append([query, doc_text])
            candidate_indices.append(int(idx))

        if not query_doc_pairs:
            self.logger.warning("No valid candidates for reranking")
            return []

        try:
            rerank_scores = self.model.predict(query_doc_pairs)
        except Exception as exc:  # pragma: no cover - defensive path
            self.logger.error("Reranking failed: %s", exc)
            return self._build_embedding_only_results(
                similarities,
                chunk_texts,
                chunks_metadata,
                top_k,
            )

        reranked_indices = np.argsort(rerank_scores)[::-1][:top_k]
        results: List[Dict[str, Any]] = []
        for rank, rerank_idx in enumerate(reranked_indices):
            original_idx = candidate_indices[rerank_idx]
            metadata = chunks_metadata[original_idx] if original_idx < len(chunks_metadata) else {}
            result = {
                "rank": rank + 1,
                "score": float(rerank_scores[rerank_idx]),
                "embedding_similarity": float(similarities[original_idx]),
                "text": chunk_texts[original_idx] if original_idx < len(chunk_texts) else "",
                "metadata": metadata,
                "chunk_id": original_idx,
            }
            results.append(result)

        if results:
            self.logger.info("Reranking complete. Top score: %.4f", results[0]["score"])
        return results

    def _encode_query(self, encode_model: Any, query: str, device: str) -> np.ndarray:
        vector = encode_model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
            device=device,
        )[0]
        return np.array(vector, dtype=np.float32)

    def _compute_similarities(self, query_embedding: np.ndarray, embeddings: np.ndarray) -> np.ndarray:
        matrix = np.array([query_embedding], dtype=np.float32)
        return cosine_similarity(matrix, embeddings)[0]

    def _build_embedding_only_results(
        self,
        similarities: np.ndarray,
        chunk_texts: Sequence[str],
        chunks_metadata: Sequence[Dict[str, Any]],
        top_k: int,
    ) -> List[Dict[str, Any]]:
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results: List[Dict[str, Any]] = []
        for rank, idx in enumerate(top_indices):
            if idx >= len(chunk_texts):
                continue
            doc_text = chunk_texts[idx]
            if not isinstance(doc_text, str):
                doc_text = str(doc_text)
            metadata = chunks_metadata[idx] if idx < len(chunks_metadata) else {}
            results.append(
                {
                    "rank": rank + 1,
                    "score": float(similarities[idx]),
                    "text": doc_text,
                    "metadata": metadata,
                    "chunk_id": int(idx),
                }
            )
        return results


__all__ = ["RerankPipeline"]
