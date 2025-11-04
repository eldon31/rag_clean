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

try:  # Lazy import for optional transformer-based loaders
    from transformers import AutoModel
except ImportError:  # pragma: no cover - transformers required for reranker loaders
    AutoModel = None  # type: ignore[assignment]


class _JinaRerankerAdapter:
    """Adapter exposing a predict() API compatible with CrossEncoder usage."""

    def __init__(self, model: Any) -> None:
        self._model = model

    def to(self, device: str) -> "_JinaRerankerAdapter":
        self._model.to(device)
        return self

    def eval(self) -> None:
        self._model.eval()

    def predict(self, query_doc_pairs: Sequence[Sequence[str]]) -> List[float]:
        if not query_doc_pairs:
            return []

        queries = {pair[0] for pair in query_doc_pairs if pair}
        if not queries:
            return []
        if len(queries) != 1:
            raise ValueError("Jina reranker expects batches with a single unique query")

        query = next(iter(queries))
        documents = [pair[1] for pair in query_doc_pairs]

        results = self._model.rerank(
            query=query,
            documents=documents,
            top_n=len(documents),
            return_embeddings=False,
        )

        scores: List[float] = [0.0] * len(documents)
        for entry in results:
            try:
                index = int(entry.get("index", -1))
            except Exception:  # pragma: no cover - defensive cast
                index = -1
            if 0 <= index < len(scores):
                score = entry.get("relevance_score", 0.0)
                scores[index] = float(score)

        return scores


def create_reranker_from_spec(
    *,
    model_name: str,
    spec: Any,
    device: str,
    logger: logging.Logger,
) -> Any:
    """Instantiate a reranker implementation based on the provided spec."""

    if getattr(spec, "loader", "cross_encoder") == "jina_reranker":
        if AutoModel is None:  # pragma: no cover - defensive
            raise RuntimeError(
                "transformers AutoModel unavailable; install transformers to load jina reranker"
            )

        model_kwargs = dict(getattr(spec, "model_kwargs", {}))
        tokenizer_kwargs = dict(getattr(spec, "tokenizer_kwargs", {}))

        if spec.trust_remote_code:
            model_kwargs.setdefault("trust_remote_code", True)

        logger.info(
            "Loading jina reranker via AutoModel: %s (kwargs=%s)",
            spec.hf_model_id,
            {k: v for k, v in model_kwargs.items() if k != "trust_remote_code"},
        )

        base_model = AutoModel.from_pretrained(
            spec.hf_model_id,
            **model_kwargs,
        )
        base_model.eval()
        if tokenizer_kwargs:
            logger.debug("Tokenizer kwargs provided but unused by AutoModel: %s", tokenizer_kwargs)

        if device and device != "cpu":
            base_model.to(device)

        return _JinaRerankerAdapter(base_model)

    cross_encoder_kwargs: Dict[str, Any] = {"device": device}
    if spec.trust_remote_code:
        cross_encoder_kwargs["trust_remote_code"] = True
    if getattr(spec, "model_kwargs", None):
        cross_encoder_kwargs["model_kwargs"] = dict(spec.model_kwargs)
    if getattr(spec, "tokenizer_kwargs", None):
        cross_encoder_kwargs["tokenizer_kwargs"] = dict(spec.tokenizer_kwargs)

    logger.info(
        "Loading CrossEncoder reranker: %s (trust_remote_code=%s)",
        spec.hf_model_id,
        spec.trust_remote_code,
    )
    return CrossEncoder(spec.hf_model_id, **cross_encoder_kwargs)


class RerankPipeline:
    """Coordinate CrossEncoder reranking for semantic search."""

    def __init__(self, config: RerankingConfig, logger: logging.Logger) -> None:
        self.config = config
        self.logger = logger
        self.model: Optional[Any] = None
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

        try:
            self.model = create_reranker_from_spec(
                model_name=model_name,
                spec=spec,
                device=device,
                logger=self.logger,
            )
            self.device = device
            self.logger.info("Reranking model ready (%s)", getattr(spec, "loader", "cross_encoder"))
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
