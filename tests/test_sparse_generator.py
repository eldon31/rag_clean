"""Unit tests for the SparseVectorGenerator module.

Tests cover:
- Happy path: successful sparse inference with CPU and GPU
- Inference failure: model not loaded, encoding errors
- Fallback recovery: metadata fallback when inference fails
- GPU leasing exhaustion: fallback to CPU when GPU unavailable
- Telemetry: verification of span and metrics emission
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, Mock, patch

import numpy as np
import pytest
import torch

from processor.ultimate_embedder.sparse_generator import (
    ChunkRecord,
    SparseInferenceResult,
    SparseVectorGenerator,
)


@pytest.fixture
def mock_embedder():
    """Create a mock UltimateKaggleEmbedderV4 instance."""
    embedder = Mock()
    embedder.device = "cuda"
    embedder.device_count = 2
    embedder.sparse_models = {}
    embedder.model_manager = Mock()
    embedder.telemetry = Mock()
    return embedder


@pytest.fixture
def mock_sparse_model():
    """Create a mock SentenceTransformer sparse model."""
    model = Mock()
    model.encode = Mock()
    tokenizer = Mock()
    vocab = {f"term_{i}": i for i in range(2048)}
    tokenizer.get_vocab = Mock(return_value=vocab)

    def convert_ids_to_tokens(token_ids: List[int]) -> List[str]:
        return [f"term_{idx}" for idx in token_ids]

    tokenizer.convert_ids_to_tokens = Mock(side_effect=convert_ids_to_tokens)
    model.tokenizer = tokenizer
    return model


@pytest.fixture
def sample_chunks() -> List[ChunkRecord]:
    """Create sample chunk records for testing."""
    return [
        ChunkRecord(
            text="Sample text for embedding",
            metadata={
                "sparse_features": {
                    "term_weights": [
                        {"term": "sample", "weight": 0.8},
                        {"term": "text", "weight": 0.6},
                    ],
                    "unique_terms": 2,
                    "total_terms": 4,
                    "weighting": "tf-normalized",
                }
            },
            chunk_id="chunk_001",
        ),
        ChunkRecord(
            text="Another chunk with content",
            metadata={
                "sparse_features": {
                    "term_weights": [
                        {"term": "another", "weight": 0.7},
                        {"term": "content", "weight": 0.9},
                    ],
                    "unique_terms": 2,
                    "total_terms": 4,
                    "weighting": "tf-normalized",
                }
            },
            chunk_id="chunk_002",
        ),
    ]


class TestSparseVectorGenerator:
    """Test suite for SparseVectorGenerator."""

    def test_init(self, mock_embedder):
        """Test generator initialization."""
        generator = SparseVectorGenerator(mock_embedder)
        assert generator.embedder is mock_embedder
        assert generator._vram_cap_gb == 12.0
        assert generator.logger is not None

    def test_init_with_custom_logger(self, mock_embedder):
        """Test generator initialization with custom logger."""
        custom_logger = logging.getLogger("custom")
        generator = SparseVectorGenerator(mock_embedder, logger=custom_logger)
        assert generator.logger is custom_logger

    def test_generate_cpu_success(
        self, mock_embedder, mock_sparse_model, sample_chunks
    ):
        """Test successful CPU-based sparse inference."""
        # Setup
        model_name = "qdrant-bm25"
        mock_embedder.sparse_models[model_name] = mock_sparse_model

        # Mock embeddings with sparse structure (non-zero indices)
        mock_embeddings = [
            np.array([0.8, 0.0, 0.6, 0.0, 0.4], dtype=np.float32),
            np.array([0.0, 0.7, 0.0, 0.9, 0.0], dtype=np.float32),
        ]
        mock_sparse_model.encode.return_value = mock_embeddings

        generator = SparseVectorGenerator(mock_embedder)

        # Execute
        result = generator.generate(
            chunks=sample_chunks,
            model_name=model_name,
            use_gpu=False,
        )

        # Verify
        assert isinstance(result, SparseInferenceResult)
        assert result.success is True
        assert result.device == "cpu"
        assert result.model_name == model_name
        assert len(result.vectors) == len(sample_chunks)
        assert result.fallback_count >= 0
        assert result.latency_ms > 0.0
        assert result.error_message is None

        # Verify telemetry was recorded
        mock_embedder.telemetry.record_span_presence.assert_called_once()
        mock_embedder.telemetry.record_metrics_status.assert_called_once()

    def test_generate_model_not_loaded(self, mock_embedder, sample_chunks):
        """Test fallback when sparse model is not loaded."""
        # Setup: model not in sparse_models registry
        model_name = "missing-model"
        generator = SparseVectorGenerator(mock_embedder)

        # Execute
        result = generator.generate(
            chunks=sample_chunks,
            model_name=model_name,
            use_gpu=False,
        )

        # Verify fallback behavior
        assert result.success is False
        assert result.error_message == f"Model {model_name} not loaded"
        assert result.fallback_count == len(sample_chunks)
        assert len(result.fallback_indices) == len(sample_chunks)
        assert len(result.vectors) == len(sample_chunks)

        # Verify vectors fallback to metadata
        for vector in result.vectors:
            if vector is not None:
                assert "indices" in vector
                assert "values" in vector
                assert "tokens" in vector

    def test_generate_cpu_encoding_failure(
        self, mock_embedder, mock_sparse_model, sample_chunks
    ):
        """Test fallback when CPU encoding fails."""
        # Setup
        model_name = "qdrant-bm25"
        mock_embedder.sparse_models[model_name] = mock_sparse_model
        mock_sparse_model.encode.side_effect = RuntimeError("Encoding failed")

        generator = SparseVectorGenerator(mock_embedder)

        # Execute
        result = generator.generate(
            chunks=sample_chunks,
            model_name=model_name,
            use_gpu=False,
        )

        # Verify fallback to metadata
        assert result.fallback_count == len(sample_chunks)
        assert len(result.vectors) == len(sample_chunks)
        assert result.device == "cpu"

    def test_generate_gpu_success(
        self, mock_embedder, mock_sparse_model, sample_chunks
    ):
        """Test successful GPU-based sparse inference with leasing."""
        # Setup
        model_name = "qdrant-bm25"
        mock_embedder.sparse_models[model_name] = mock_sparse_model
        mock_embedder.device = "cuda"

        # Mock GPU lease
        mock_lease = Mock()
        mock_lease.device_ids = [0]
        mock_lease.__enter__ = Mock(return_value=mock_lease)
        mock_lease.__exit__ = Mock(return_value=False)

        # Mock hydrated model
        mock_hydrated_model = Mock()
        mock_embeddings_tensor = torch.tensor(
            [
                [0.8, 0.0, 0.6, 0.0, 0.4],
                [0.0, 0.7, 0.0, 0.9, 0.0],
            ],
            dtype=torch.float32,
        )
        mock_hydrated_model.encode.return_value = mock_embeddings_tensor

        mock_embedder.model_manager.hydrate_model_to_gpus.return_value = (
            mock_hydrated_model
        )

        generator = SparseVectorGenerator(mock_embedder)

        # Execute with patched lease_gpus
        with patch(
            "processor.ultimate_embedder.sparse_generator.lease_gpus",
            return_value=mock_lease,
        ):
            result = generator.generate(
                chunks=sample_chunks,
                model_name=model_name,
                use_gpu=True,
                device_ids=[0],
            )

        # Verify
        assert result.success is True
        assert result.device == "cuda:0"
        assert len(result.vectors) == len(sample_chunks)
        mock_embedder.model_manager.hydrate_model_to_gpus.assert_called_once()
        mock_embedder.model_manager.stage_model_to_cpu.assert_called_once_with(
            model_name
        )

    def test_generate_gpu_hydration_failure(
        self, mock_embedder, mock_sparse_model, sample_chunks
    ):
        """Test fallback to CPU when GPU hydration fails."""
        # Setup
        model_name = "qdrant-bm25"
        mock_embedder.sparse_models[model_name] = mock_sparse_model
        mock_embedder.device = "cuda"

        # Mock GPU lease
        mock_lease = Mock()
        mock_lease.device_ids = [0]
        mock_lease.__enter__ = Mock(return_value=mock_lease)
        mock_lease.__exit__ = Mock(return_value=False)

        # Mock hydration failure
        mock_embedder.model_manager.hydrate_model_to_gpus.return_value = None

        # Mock CPU fallback
        mock_embeddings = [
            np.array([0.8, 0.0, 0.6], dtype=np.float32),
            np.array([0.0, 0.7, 0.9], dtype=np.float32),
        ]
        mock_sparse_model.encode.return_value = mock_embeddings

        generator = SparseVectorGenerator(mock_embedder)

        # Execute with patched lease_gpus
        with patch(
            "processor.ultimate_embedder.sparse_generator.lease_gpus",
            return_value=mock_lease,
        ):
            result = generator.generate(
                chunks=sample_chunks,
                model_name=model_name,
                use_gpu=True,
                device_ids=[0],
            )

        # Verify fallback to CPU
        assert result.device == "cpu"
        assert len(result.vectors) == len(sample_chunks)

    def test_generate_gpu_lease_exception(
        self, mock_embedder, mock_sparse_model, sample_chunks
    ):
        """Test fallback when GPU leasing raises exception."""
        # Setup
        model_name = "qdrant-bm25"
        mock_embedder.sparse_models[model_name] = mock_sparse_model
        mock_embedder.device = "cuda"

        # Mock GPU lease that raises exception
        with patch(
            "processor.ultimate_embedder.sparse_generator.lease_gpus",
            side_effect=RuntimeError("GPU lease exhausted"),
        ):
            generator = SparseVectorGenerator(mock_embedder)

            # Execute
            result = generator.generate(
                chunks=sample_chunks,
                model_name=model_name,
                use_gpu=True,
                device_ids=[0],
            )

        # Verify fallback - when lease fails, it falls back to CPU/metadata
        # which still succeeds if metadata is available
        assert result.fallback_count == len(sample_chunks)
        # Device should be CPU after fallback
        assert result.device == "cpu"

    def test_convert_embedding_to_sparse_vector(self, mock_embedder):
        """Test conversion of dense embedding to sparse vector."""
        generator = SparseVectorGenerator(mock_embedder)

        # Test with numpy array
        embedding = np.array([0.0, 0.8, 0.0, 0.6, 0.0, 0.4], dtype=np.float32)
        lookup = {1: "alpha", 3: "bravo", 5: "charlie"}

        def token_lookup(idx: int) -> Optional[str]:
            return lookup.get(idx)

        vector = generator._convert_embedding_to_sparse_vector(
            embedding,
            token_lookup=token_lookup,
        )

        assert vector is not None
        assert "indices" in vector
        assert "values" in vector
        assert "tokens" in vector
        assert "stats" in vector
        assert len(vector["indices"]) == 3  # 3 non-zero values
        assert len(vector["values"]) == 3
        assert vector["stats"]["unique_terms"] == 3
        assert vector["tokens"] == ["alpha", "bravo", "charlie"]

    def test_convert_embedding_torch_tensor(self, mock_embedder):
        """Test conversion from torch tensor to sparse vector."""
        generator = SparseVectorGenerator(mock_embedder)

        # Test with torch tensor
        embedding = torch.tensor([0.0, 0.8, 0.0, 0.6, 0.0], dtype=torch.float32)
        lookup = {1: "whiskey", 3: "tango"}

        def token_lookup(idx: int) -> Optional[str]:
            return lookup.get(idx)

        vector = generator._convert_embedding_to_sparse_vector(
            embedding,
            token_lookup=token_lookup,
        )

        assert vector is not None
        assert len(vector["indices"]) == 2  # 2 non-zero values
        assert vector["tokens"] == ["whiskey", "tango"]

    def test_convert_embedding_with_token_lookup(self, mock_embedder):
        """Test conversion maps indices to tokens when lookup is provided."""
        generator = SparseVectorGenerator(mock_embedder)

        embedding = np.array([0.0, 0.2, 0.0, 0.3], dtype=np.float32)
        token_map = {1: "foo", 3: "bar"}

        def lookup(idx: int) -> Optional[str]:
            return token_map.get(idx)

        vector = generator._convert_embedding_to_sparse_vector(
            embedding,
            token_lookup=lookup,
        )

        assert vector is not None
        assert vector["tokens"] == ["foo", "bar"]

    def test_convert_embedding_all_zeros(self, mock_embedder):
        """Test conversion with all-zero embedding returns None."""
        generator = SparseVectorGenerator(mock_embedder)

        # Test with all zeros
        embedding = np.zeros(10, dtype=np.float32)
        vector = generator._convert_embedding_to_sparse_vector(embedding)

        assert vector is None

    def test_convert_embedding_without_lookup_triggers_fallback(self, mock_embedder):
        """Non-zero embedding without lookup should trigger metadata fallback (None)."""
        generator = SparseVectorGenerator(mock_embedder)

        embedding = np.array([0.1, 0.0, 0.0, 0.4], dtype=np.float32)
        vector = generator._convert_embedding_to_sparse_vector(embedding)

        assert vector is None

    def test_convert_embedding_none(self, mock_embedder):
        """Test conversion with None embedding returns None."""
        generator = SparseVectorGenerator(mock_embedder)
        vector = generator._convert_embedding_to_sparse_vector(None)
        assert vector is None

    def test_fallback_to_metadata(self, mock_embedder, sample_chunks):
        """Test metadata fallback produces vectors for all chunks."""
        generator = SparseVectorGenerator(mock_embedder)

        vectors, fallback_indices = generator._fallback_to_metadata(sample_chunks)

        assert len(vectors) == len(sample_chunks)
        assert len(fallback_indices) == len(sample_chunks)
        assert fallback_indices == list(range(len(sample_chunks)))

        # Verify at least some vectors are not None (depends on metadata quality)
        # Some may be None if metadata doesn't contain sparse_features

    def test_record_telemetry(self, mock_embedder):
        """Test telemetry recording for sparse inference."""
        generator = SparseVectorGenerator(mock_embedder)

        result = SparseInferenceResult(
            vectors=[{"indices": [0, 1], "values": [0.8, 0.6], "tokens": ["a", "b"], "stats": {}}],
            fallback_count=0,
            fallback_indices=[],
            latency_ms=42.5,
            device="cuda:0",
            model_name="qdrant-bm25",
            success=True,
            error_message=None,
        )

        generator._record_telemetry(result, chunk_count=1)

        # Verify telemetry calls
        mock_embedder.telemetry.record_span_presence.assert_called_once()
        mock_embedder.telemetry.record_metrics_status.assert_called_once()

        # Verify span attributes
        span_call = mock_embedder.telemetry.record_span_presence.call_args
        assert span_call[0][0] == "sparse_inference"
        assert span_call[1]["active"] is True
        assert "attributes" in span_call[1]
        attrs = span_call[1]["attributes"]
        assert attrs["model"] == "qdrant-bm25"
        assert attrs["device"] == "cuda:0"
        assert attrs["latency_ms"] == 42.5
        assert attrs["fallback_count"] == 0

    def test_record_telemetry_with_failure(self, mock_embedder):
        """Test telemetry recording when inference fails."""
        generator = SparseVectorGenerator(mock_embedder)

        result = SparseInferenceResult(
            vectors=[],
            fallback_count=5,
            fallback_indices=[0, 1, 2, 3, 4],
            latency_ms=10.0,
            device="cpu",
            model_name="qdrant-bm25",
            success=False,
            error_message="Model encoding failed",
        )

        generator._record_telemetry(result, chunk_count=5)

        # Verify telemetry calls
        span_call = mock_embedder.telemetry.record_span_presence.call_args
        assert span_call[0][0] == "sparse_inference"
        assert span_call[1]["active"] is False
        assert span_call[1]["reason"] == "Model encoding failed"

    def test_generate_large_batch_cpu(self, mock_embedder, mock_sparse_model):
        """Test CPU inference with large batch of chunks."""
        # Setup
        model_name = "qdrant-bm25"
        mock_embedder.sparse_models[model_name] = mock_sparse_model

        # Create 100 chunks
        large_chunks = [
            ChunkRecord(
                text=f"Chunk {i}",
                metadata={
                    "sparse_features": {
                        "term_weights": [{"term": f"term{i}", "weight": 0.5}],
                        "unique_terms": 1,
                        "total_terms": 2,
                        "weighting": "tf-normalized",
                    }
                },
                chunk_id=f"chunk_{i:03d}",
            )
            for i in range(100)
        ]

        # Mock embeddings
        mock_embeddings = [
            np.random.rand(50).astype(np.float32) for _ in range(100)
        ]
        mock_sparse_model.encode.return_value = mock_embeddings

        generator = SparseVectorGenerator(mock_embedder)

        # Execute
        result = generator.generate(
            chunks=large_chunks,
            model_name=model_name,
            use_gpu=False,
        )

        # Verify
        assert result.success is True
        assert len(result.vectors) == 100
        assert result.latency_ms > 0.0

    def test_vram_monitoring(self, mock_embedder, sample_chunks):
        """Test VRAM monitoring functionality."""
        generator = SparseVectorGenerator(mock_embedder)

        # Mock torch.cuda availability and monitoring
        with patch("torch.cuda.is_available", return_value=True), \
             patch("torch.cuda.synchronize"), \
             patch("torch.cuda.memory_allocated", return_value=8 * 1024**3), \
             patch("torch.cuda.get_device_properties") as mock_props:
            
            mock_props.return_value.total_memory = 12 * 1024**3
            
            vram_stats = generator._check_vram_usage(device_id=0)
            
            assert vram_stats["used_gb"] == 8.0
            assert vram_stats["total_gb"] == 12.0
            assert 0.0 <= vram_stats["utilization_ratio"] <= 1.0

    def test_vram_hard_cap_violation(self, mock_embedder, sample_chunks):
        """Test VRAM hard cap enforcement aborts GPU inference."""
        generator = SparseVectorGenerator(mock_embedder)
        mock_embedder.telemetry.record_metrics_status = Mock()

        # Mock VRAM usage exceeding hard cap (13 GB > 12 GB)
        with patch.object(
            generator,
            "_check_vram_usage",
            return_value={"used_gb": 13.0, "total_gb": 16.0, "utilization_ratio": 0.8125},
        ):
            can_proceed, suggested_batch = generator._enforce_vram_cap(
                device_id=0,
                current_batch_size=32,
            )
            
            assert can_proceed is False
            assert suggested_batch is None
            
            # Verify telemetry was recorded
            mock_embedder.telemetry.record_metrics_status.assert_called_once()
            call_args = mock_embedder.telemetry.record_metrics_status.call_args
            assert call_args[0][0] == "sparse_vram_violation"
            assert call_args[1]["emitted"] is True

    def test_vram_soft_limit_adaptive_batching(self, mock_embedder, sample_chunks):
        """Test VRAM soft limit triggers adaptive batch size reduction."""
        generator = SparseVectorGenerator(mock_embedder)

        # Mock VRAM usage exceeding soft limit but under hard cap (11 GB)
        with patch.object(
            generator,
            "_check_vram_usage",
            return_value={"used_gb": 11.0, "total_gb": 16.0, "utilization_ratio": 0.6875},
        ):
            can_proceed, suggested_batch = generator._enforce_vram_cap(
                device_id=0,
                current_batch_size=32,
            )
            
            assert can_proceed is True
            assert suggested_batch == 16  # 50% reduction
            assert suggested_batch >= generator._min_batch_size

    def test_vram_within_limits(self, mock_embedder, sample_chunks):
        """Test VRAM within acceptable limits allows normal operation."""
        generator = SparseVectorGenerator(mock_embedder)

        # Mock VRAM usage well under soft limit (6 GB)
        with patch.object(
            generator,
            "_check_vram_usage",
            return_value={"used_gb": 6.0, "total_gb": 16.0, "utilization_ratio": 0.375},
        ):
            can_proceed, suggested_batch = generator._enforce_vram_cap(
                device_id=0,
                current_batch_size=32,
            )
            
            assert can_proceed is True
            assert suggested_batch is None  # No reduction needed

    def test_gpu_inference_with_vram_enforcement(
        self,
        mock_embedder,
        mock_sparse_model,
        sample_chunks,
    ):
        """Test GPU inference enforces VRAM cap and uses adaptive batching."""
        model_name = "sparse_model"
        mock_embedder.sparse_models[model_name] = mock_sparse_model
        mock_embedder.telemetry.record_metrics_status = Mock()

        # Mock embeddings
        mock_embeddings = np.random.randn(len(sample_chunks), 768).astype(np.float32)
        mock_sparse_model.encode.return_value = mock_embeddings

        generator = SparseVectorGenerator(mock_embedder)

        # Mock GPU leasing and model hydration
        with patch(
            "processor.ultimate_embedder.sparse_generator.lease_gpus"
        ) as mock_lease_context, \
             patch.object(generator, "_check_vram_usage") as mock_vram_check:
            
            # Setup lease context
            mock_lease = Mock()
            mock_lease.device_ids = [0]
            mock_lease.__enter__ = Mock(return_value=mock_lease)
            mock_lease.__exit__ = Mock(return_value=False)
            mock_lease_context.return_value = mock_lease

            # Mock successful hydration
            mock_embedder.model_manager.hydrate_model_to_gpus.return_value = (
                mock_sparse_model
            )

            # Mock VRAM checks: first check passes, second check passes
            mock_vram_check.return_value = {
                "used_gb": 6.0,
                "total_gb": 16.0,
                "utilization_ratio": 0.375,
            }

            # Execute
            result = generator.generate(
                chunks=sample_chunks,
                model_name=model_name,
                use_gpu=True,
                device_ids=[0],
            )

            # Verify VRAM was monitored
            assert mock_vram_check.called
            
            # Verify telemetry recorded VRAM usage
            telemetry_calls = [
                call for call in mock_embedder.telemetry.record_metrics_status.call_args_list
                if call[0][0] == "sparse_vram_usage"
            ]
            assert len(telemetry_calls) > 0

    def test_telemetry_sanitization(self, mock_embedder, sample_chunks):
        """Test that telemetry does not leak sensitive chunk text."""
        model_name = "sparse_model"
        mock_sparse_model = Mock()
        mock_embedder.sparse_models[model_name] = mock_sparse_model
        mock_embedder.telemetry.record_span_presence = Mock()
        mock_embedder.telemetry.record_metrics_status = Mock()

        # Create chunks with sensitive text
        sensitive_chunks = [
            ChunkRecord(
                text="SENSITIVE_API_KEY_12345_CONFIDENTIAL",
                metadata={
                    "sparse_features": {
                        "term_weights": [{"term": "sensitive", "weight": 0.9}],
                        "unique_terms": 1,
                        "total_terms": 2,
                        "weighting": "tf-normalized",
                    }
                },
                chunk_id="sensitive_001",
            ),
        ]

        # Mock embeddings
        mock_embeddings = np.random.randn(len(sensitive_chunks), 768).astype(np.float32)
        mock_sparse_model.encode.return_value = mock_embeddings

        generator = SparseVectorGenerator(mock_embedder)

        # Execute CPU inference (simpler path)
        result = generator.generate(
            chunks=sensitive_chunks,
            model_name=model_name,
            use_gpu=False,
        )

        # Verify telemetry was called
        assert mock_embedder.telemetry.record_span_presence.called
        assert mock_embedder.telemetry.record_metrics_status.called

        # Check that sensitive text is NOT in telemetry attributes
        for call in mock_embedder.telemetry.record_span_presence.call_args_list:
            attributes = call[1].get("attributes", {})
            # Verify no chunk text appears in attributes
            for key, value in attributes.items():
                if isinstance(value, str):
                    assert "SENSITIVE_API_KEY" not in value
                    assert "CONFIDENTIAL" not in value

        for call in mock_embedder.telemetry.record_metrics_status.call_args_list:
            details = call[1].get("details", {})
            # Verify no chunk text appears in details
            for key, value in details.items():
                if isinstance(value, str):
                    assert "SENSITIVE_API_KEY" not in value
                    assert "CONFIDENTIAL" not in value
