"""Unit tests for GPU lease helper (CPU-compatible with mocked torch)."""

import pytest
from unittest.mock import MagicMock, Mock, patch
from processor.ultimate_embedder.gpu_lease import GPULease, lease_gpus


@pytest.fixture
def mock_embedder():
    """Create a mock embedder for testing."""
    embedder = Mock()
    embedder.device = "cuda"
    embedder.device_count = 2
    embedder.telemetry = Mock()
    embedder.telemetry.record_gpu_lease_event = Mock()
    return embedder


@pytest.fixture
def mock_logger():
    """Create a mock logger."""
    return Mock()


class TestGPULease:
    """Test GPU lease lifecycle and telemetry."""

    def test_lease_initialization(self, mock_embedder, mock_logger):
        """Test that lease initializes with correct state."""
        lease = GPULease(mock_embedder, "test-model", mock_logger)
        
        assert lease.model_name == "test-model"
        assert lease.active is False
        assert lease.device_ids == []
        assert lease.vram_before == {}
        assert lease.vram_after == {}

    @patch("processor.ultimate_embedder.gpu_lease.collect_gpu_snapshots")
    @patch("processor.ultimate_embedder.gpu_lease.torch")
    @patch("processor.ultimate_embedder.gpu_lease.gc")
    def test_lease_acquire(
        self,
        mock_gc,
        mock_torch,
        mock_collect_snapshots,
        mock_embedder,
        mock_logger,
    ):
        """Test GPU lease acquisition."""
        # Mock CUDA operations
        mock_torch.cuda.empty_cache = Mock()
        
        # Mock snapshot collection
        mock_snapshots = {0: Mock(), 1: Mock()}
        mock_collect_snapshots.return_value = mock_snapshots
        
        lease = GPULease(mock_embedder, "test-model", mock_logger)
        lease.acquire(device_ids=[0, 1])
        
        # Verify state
        assert lease.active is True
        assert lease.device_ids == [0, 1]
        assert lease.vram_before == mock_snapshots
        
        # Verify CUDA cache cleared
        assert mock_torch.cuda.empty_cache.call_count >= 1
        
        # Verify telemetry recorded
        mock_embedder.telemetry.record_gpu_lease_event.assert_called_once()
        call_args = mock_embedder.telemetry.record_gpu_lease_event.call_args
        assert call_args[1]["event_type"] == "acquire"
        assert call_args[1]["model"] == "test-model"
        assert call_args[1]["device_ids"] == [0, 1]

    @patch("processor.ultimate_embedder.gpu_lease.collect_gpu_snapshots")
    @patch("processor.ultimate_embedder.gpu_lease.torch")
    @patch("processor.ultimate_embedder.gpu_lease.gc")
    def test_lease_release(
        self,
        mock_gc,
        mock_torch,
        mock_collect_snapshots,
        mock_embedder,
        mock_logger,
    ):
        """Test GPU lease release."""
        # Mock CUDA operations
        mock_torch.cuda.empty_cache = Mock()
        mock_torch.cuda.synchronize = Mock()
        
        # Mock snapshot collection
        mock_snapshots_before = {0: Mock(), 1: Mock()}
        mock_snapshots_after = {0: Mock(), 1: Mock()}
        mock_collect_snapshots.side_effect = [mock_snapshots_before, mock_snapshots_after]
        
        lease = GPULease(mock_embedder, "test-model", mock_logger)
        lease.acquire(device_ids=[0, 1])
        
        # Reset mock to check release call
        mock_embedder.telemetry.record_gpu_lease_event.reset_mock()
        
        lease.release()
        
        # Verify state
        assert lease.active is False
        assert lease.device_ids == []
        assert lease.vram_after == mock_snapshots_after
        
        # Verify CUDA synchronize called
        mock_torch.cuda.synchronize.assert_called_once()
        
        # Verify telemetry recorded
        mock_embedder.telemetry.record_gpu_lease_event.assert_called_once()
        call_args = mock_embedder.telemetry.record_gpu_lease_event.call_args
        assert call_args[1]["event_type"] == "release"
        assert call_args[1]["model"] == "test-model"

    def test_lease_double_acquire_warning(self, mock_embedder, mock_logger):
        """Test that double acquire logs a warning."""
        with patch("processor.ultimate_embedder.gpu_lease.collect_gpu_snapshots"):
            with patch("processor.ultimate_embedder.gpu_lease.torch"):
                lease = GPULease(mock_embedder, "test-model", mock_logger)
                lease.acquire()
                lease.acquire()  # Second acquire should warn
                
                # Check logger was called with warning
                assert any("already active" in str(call) for call in mock_logger.warning.mock_calls)

    def test_lease_release_without_acquire(self, mock_embedder, mock_logger):
        """Test that release without acquire is safe."""
        with patch("processor.ultimate_embedder.gpu_lease.collect_gpu_snapshots"):
            with patch("processor.ultimate_embedder.gpu_lease.torch"):
                lease = GPULease(mock_embedder, "test-model", mock_logger)
                lease.release()  # Should not crash
                
                # Verify no telemetry recorded for release
                mock_embedder.telemetry.record_gpu_lease_event.assert_not_called()

    @patch("processor.ultimate_embedder.gpu_lease.collect_gpu_snapshots")
    @patch("processor.ultimate_embedder.gpu_lease.torch")
    @patch("processor.ultimate_embedder.gpu_lease.gc")
    def test_lease_context_manager(
        self,
        mock_gc,
        mock_torch,
        mock_collect_snapshots,
        mock_embedder,
        mock_logger,
    ):
        """Test GPU lease as context manager."""
        # Mock CUDA operations
        mock_torch.cuda.empty_cache = Mock()
        mock_torch.cuda.synchronize = Mock()
        
        # Mock snapshot collection
        mock_snapshots = {0: Mock(), 1: Mock()}
        mock_collect_snapshots.return_value = mock_snapshots
        
        with lease_gpus(mock_embedder, "test-model", mock_logger) as lease:
            # Inside context, lease should be active
            assert lease.active is True
            assert lease.model_name == "test-model"
        
        # After context, lease should be released
        assert lease.active is False

    @patch("processor.ultimate_embedder.gpu_lease.collect_gpu_snapshots")
    @patch("processor.ultimate_embedder.gpu_lease.torch")
    def test_lease_summarize(
        self,
        mock_torch,
        mock_collect_snapshots,
        mock_embedder,
        mock_logger,
    ):
        """Test lease summary generation."""
        # Mock snapshots with allocated bytes
        mock_snapshot_before = Mock()
        mock_snapshot_before.allocated_bytes = 1e9  # 1 GB
        
        mock_snapshot_after = Mock()
        mock_snapshot_after.allocated_bytes = 2.5e9  # 2.5 GB
        
        mock_collect_snapshots.side_effect = [
            {0: mock_snapshot_before, 1: mock_snapshot_before},
            {0: mock_snapshot_after, 1: mock_snapshot_after},
        ]
        
        lease = GPULease(mock_embedder, "test-model", mock_logger)
        lease.acquire(device_ids=[0, 1])
        lease.release()
        
        summary = lease.summarize()
        
        assert summary["model"] == "test-model"
        assert summary["device_ids"] == [0, 1]  # Preserved for summary
        assert summary["active"] is False
        assert "vram_deltas_gb" in summary
        assert summary["vram_deltas_gb"]["gpu_0"] == 1.5  # 2.5 - 1.0
        assert summary["vram_deltas_gb"]["gpu_1"] == 1.5


class TestExclusiveEnsembleConfig:
    """Test that exclusive ensemble configuration is properly wired."""

    def test_config_has_exclusive_mode_flag(self):
        """Test that EnsembleConfig has exclusive_mode attribute."""
        from processor.ultimate_embedder.config import EnsembleConfig
        
        config = EnsembleConfig()
        assert hasattr(config, "exclusive_mode")
        assert config.exclusive_mode is False  # Default should be disabled

    def test_config_exclusive_mode_can_be_enabled(self):
        """Test that exclusive_mode can be enabled."""
        from processor.ultimate_embedder.config import EnsembleConfig
        
        config = EnsembleConfig(exclusive_mode=True)
        assert config.exclusive_mode is True

    def test_config_has_warm_cache_flag(self):
        """Test that EnsembleConfig has warm_cache_after_release attribute."""
        from processor.ultimate_embedder.config import EnsembleConfig
        
        config = EnsembleConfig()
        assert hasattr(config, "warm_cache_after_release")
        assert config.warm_cache_after_release is False  # Default should be disabled


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
