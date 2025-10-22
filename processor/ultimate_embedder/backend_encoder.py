"""Backend encoding helpers extracted from the facade."""

from __future__ import annotations

from typing import Iterable, Sequence

import numpy as np
import torch


def encode_with_backend(embedder, texts: Sequence[str], batch_size: int, logger) -> np.ndarray:
	"""Encode chunks using the facade's non-standard backend models.

	This mirrors the legacy `_encode_with_backend` logic so the facade no longer
	needs to own the implementation. The helper relies on the embedder to
	provide the primary model and utility hooks such as `_unwrap_model`.
	"""

	if embedder.primary_model is None:
		raise RuntimeError("No backend model loaded")

	encode_model = embedder._unwrap_model(embedder.primary_model)

	if hasattr(encode_model, "encode"):
		try:
			logger.debug(
				"Encoding %d texts with backend model (batch_size=%d)",
				len(texts),
				batch_size,
			)
			embeddings = encode_model.encode(  # type: ignore[attr-defined]
				texts,
				batch_size=batch_size,
				show_progress_bar=False,
				convert_to_numpy=True,
				normalize_embeddings=True,
			)
		except Exception as exc:  # pragma: no cover - defensive logging
			logger.error("Backend encoding failed: %s", exc)
			raise RuntimeError(f"Backend encoding failed: {exc}") from exc

		if embeddings.dtype != np.float32:
			embeddings = embeddings.astype(np.float32)
		logger.debug("Backend encode complete: shape=%s", embeddings.shape)
		return embeddings

	if hasattr(embedder.primary_model, "forward") or hasattr(embedder.primary_model, "__call__"):
		try:
			logger.debug(
				"Encoding %d texts via direct backend inference (batch_size=%d)",
				len(texts),
				batch_size,
			)
			from transformers import AutoTokenizer  # lazy import to keep optional

			tokenizer = AutoTokenizer.from_pretrained(embedder.model_config.hf_model_id)
			batches: Iterable[Sequence[str]] = (
				texts[index : index + batch_size]
				for index in range(0, len(texts), batch_size)
			)

			all_embeddings = []
			for batch_texts in batches:
				inputs = tokenizer(
					list(batch_texts),
					padding=True,
					truncation=True,
					max_length=embedder.model_config.max_tokens,
					return_tensors="pt",
				)

				forward = getattr(embedder.primary_model, "forward", embedder.primary_model)
				outputs = forward(**inputs)

				token_embeddings = None
				if isinstance(outputs, dict):
					token_embeddings = outputs.get("last_hidden_state")
				elif hasattr(outputs, "last_hidden_state"):
					token_embeddings = getattr(outputs, "last_hidden_state")

				if token_embeddings is not None:
					attention_mask = inputs["attention_mask"]
					token_embeddings = torch.as_tensor(token_embeddings)
					expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
					embeddings_tensor = torch.sum(token_embeddings * expanded, dim=1) / torch.clamp(
						expanded.sum(dim=1),
						min=1e-9,
					)
				else:
					candidate = outputs[0] if isinstance(outputs, tuple) else outputs
					embeddings_tensor = torch.as_tensor(candidate)

				embeddings_tensor = torch.nn.functional.normalize(embeddings_tensor, p=2, dim=1)
				all_embeddings.append(embeddings_tensor.detach().cpu().numpy().astype(np.float32))

			final_embeddings = np.vstack(all_embeddings)
			logger.debug("Backend direct inference complete: shape=%s", final_embeddings.shape)
			return final_embeddings
		except Exception as exc:  # pragma: no cover - defensive logging
			logger.error("Backend direct inference failed: %s", exc)
			raise RuntimeError(f"Backend encoding failed: {exc}") from exc

	raise RuntimeError(
		"Backend model does not support encoding. Expected an object with an "
		"`encode` or `forward` method."
	)


__all__ = ["encode_with_backend"]
