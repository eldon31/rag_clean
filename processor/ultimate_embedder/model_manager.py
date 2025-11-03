"""Model lifecycle manager extracted from the Ultimate Embedder facade."""

from __future__ import annotations

import gc
import logging
import time
from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import torch
from huggingface_hub import snapshot_download
from processor.ultimate_embedder.config import (
    KAGGLE_OPTIMIZED_MODELS,
    SPARSE_MODELS,
)

if TYPE_CHECKING:  # pragma: no cover - typing only
    from sentence_transformers import SentenceTransformer
else:
    from .compat import SentenceTransformer

_ORT_IMPORT_ERROR: Optional[str] = None
try:  # Optional ONNX acceleration via Optimum
    from optimum.onnxruntime import ORTModelForFeatureExtraction  # type: ignore

    ONNX_AVAILABLE = True
except Exception as exc:  # pragma: no cover - Optimum missing or incompatible
    ORTModelForFeatureExtraction = None  # type: ignore
    ONNX_AVAILABLE = False
    _ORT_IMPORT_ERROR = f"{type(exc).__name__}: {exc}"

try:  # Hugging Face hub compatibility across versions
    from huggingface_hub.utils import LocalEntryNotFoundError  # type: ignore
except ImportError:  # pragma: no cover - old hub versions
    try:
        from huggingface_hub.utils._validators import LocalEntryNotFoundError  # type: ignore
    except ImportError:  # pragma: no cover - fallback
        LocalEntryNotFoundError = FileNotFoundError  # type: ignore

LocalEntryNotFoundErrorType = (LocalEntryNotFoundError,)

if TYPE_CHECKING:  # pragma: no cover - type checking only
    from .core import UltimateKaggleEmbedderV4


class ModelManager:
    """Encapsulate model loading and lifecycle management concerns."""

    def __init__(self, embedder: "UltimateKaggleEmbedderV4", logger: logging.Logger) -> None:
        self.embedder = embedder
        self.logger = logger

        if _ORT_IMPORT_ERROR:
            logger.warning(
                "Optimum ORT backend disabled, falling back to PyTorch models: %s",
                _ORT_IMPORT_ERROR,
            )


    # ------------------------------------------------------------------
    # Initialization orchestrators
    # ------------------------------------------------------------------

    def initialize_primary_model(self) -> None:
        embedder = self.embedder
        logger = self.logger

        logger.info("Loading embedding model: %s", embedder.model_config.hf_model_id)
        optimal_batch = embedder.gpu_config.get_optimal_batch_size(embedder.model_config)
        logger.info("Optimal batch size: %s", optimal_batch)

        model_kwargs = self._build_sentence_transformer_kwargs()
        model_kwargs["trust_remote_code"] = embedder.model_config.trust_remote_code

        if embedder.gpu_config.precision == "fp16" and embedder.device == "cuda":
            model_kwargs["torch_dtype"] = torch.float16
            logger.info("Using FP16 precision for T4 optimization")

        if (
            embedder.model_config.supports_flash_attention
            and embedder.gpu_config.enable_memory_efficient_attention
        ):
            try:
                import sentence_transformers  # pylint: disable=import-outside-toplevel

                st_version = tuple(
                    map(int, sentence_transformers.__version__.split(".")[:2])
                )
                if st_version >= (3, 0):
                    logger.info(
                        "Flash Attention 2 will be used automatically (sentence-transformers >= 3.0)"
                    )
                else:
                    logger.info(
                        "Flash Attention requires sentence-transformers >= 3.0.0 (current: %s)",
                        sentence_transformers.__version__,
                    )
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.debug("Flash Attention check failed: %s", exc)

        try:
            self._ensure_model_snapshot(embedder.model_config.hf_model_id)
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.warning(
                "Snapshot preparation failed for %s: %s",
                embedder.model_config.hf_model_id,
                exc,
            )

        if embedder.gpu_config.backend == "onnx" and ONNX_AVAILABLE:
            logger.info("Attempting ONNX backend optimization...")
            try:
                embedder.primary_model = self._load_onnx_model()
                logger.info("ONNX backend loaded successfully")
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.warning("ONNX backend failed, using PyTorch: %s", exc)
                embedder.primary_model = self._load_pytorch_model(model_kwargs, optimal_batch)
        else:
            embedder.primary_model = self._load_pytorch_model(model_kwargs, optimal_batch)

        if isinstance(embedder.primary_model, SentenceTransformer):
            self._maybe_enable_transformer_checkpointing(embedder.primary_model)

        embedder.models[embedder.model_name] = embedder.primary_model
        embedder._record_model_dtype(embedder.model_name, embedder.primary_model)

        # Stage primary model to CPU if exclusive ensemble mode is enabled
        if (
            embedder.enable_ensemble
            and embedder.ensemble_config
            and embedder.ensemble_config.exclusive_mode
            and embedder.device == "cuda"
        ):
            logger.info("Exclusive ensemble mode: staging primary model to CPU")
            self.stage_model_to_cpu(embedder.model_name)

        if embedder.enable_ensemble:
            self._initialize_ensemble_models()

        if embedder.device == "cuda":
            torch.cuda.empty_cache()
            logger.info("GPU memory cache cleared")

    def initialize_companion_models(self) -> None:
        embedder = self.embedder
        logger = self.logger

        if not embedder.companion_dense_model_names:
            return

        for companion_name in embedder.companion_dense_model_names:
            if companion_name == embedder.model_name:
                logger.debug(
                    "Skipping companion %s because it matches the primary model",
                    companion_name,
                )
                continue

            config = KAGGLE_OPTIMIZED_MODELS.get(companion_name)
            if config is None:
                logger.warning("Companion model %s not found in registry; skipping", companion_name)
                continue

            if companion_name in embedder.companion_models:
                continue

            try:
                logger.info(
                    "Loading companion dense model: %s (%sD)",
                    config.hf_model_id,
                    config.vector_dim,
                )

                target_device = "cpu"
                if embedder.device == "cuda":
                    if embedder.device_count > 1:
                        target_device = "cuda:1"
                        embedder.companion_device_map[companion_name] = target_device
                        embedder._record_mitigation(
                            "companion_gpu_routed",
                            companion=companion_name,
                            device=target_device,
                        )
                    else:
                        target_device = "cuda:0"
                        embedder.companion_device_map[companion_name] = target_device
                        embedder._record_mitigation(
                            "companion_gpu_shared",
                            companion=companion_name,
                            device=target_device,
                        )
                else:
                    embedder.companion_device_map[companion_name] = target_device
                    embedder._record_mitigation(
                        "companion_cpu_fallback",
                        companion=companion_name,
                    )

                self._ensure_model_snapshot(config.hf_model_id)
                companion_kwargs = self._build_sentence_transformer_kwargs(device=target_device)
                companion_kwargs["trust_remote_code"] = config.trust_remote_code

                model = SentenceTransformer(
                    config.hf_model_id,
                    **companion_kwargs,
                )

                if (
                    embedder.gpu_config.precision == "fp16"
                    and isinstance(target_device, str)
                    and target_device.startswith("cuda")
                ):
                    model = model.half()

                if embedder.gpu_config.gradient_checkpointing:
                    self._maybe_enable_transformer_checkpointing(model)

                embedder.companion_models[companion_name] = model
                embedder.companion_model_configs[companion_name] = config
                batch_size = embedder.gpu_config.get_optimal_batch_size(config)
                if target_device == "cpu":
                    batch_size = max(1, min(batch_size, 4))
                embedder.companion_batch_sizes[companion_name] = batch_size
                embedder.models.setdefault(companion_name, model)
                embedder._record_model_dtype(companion_name, model)
                logger.info(
                    "Companion model %s ready (batch size %s, device %s)",
                    companion_name,
                    batch_size,
                    target_device,
                )
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.error("Failed to load companion model %s: %s", companion_name, exc)
                embedder._record_mitigation(
                    "companion_missing",
                    companion=companion_name,
                    error=str(exc),
                )

        if embedder.device == "cuda" and embedder.companion_models:
            torch.cuda.empty_cache()

    def initialize_sparse_models(self) -> None:
        embedder = self.embedder
        logger = self.logger

        if not embedder.sparse_model_names:
            logger.info("No sparse models specified")
            if embedder.enable_sparse and not embedder._sparse_runtime_reason:
                embedder._sparse_runtime_reason = "No sparse models configured"
            return

        logger.info("Loading sparse models: %s", embedder.sparse_model_names)

        load_failures: List[str] = []

        for sparse_name in embedder.sparse_model_names:
            if sparse_name not in SPARSE_MODELS:
                logger.warning("Unknown sparse model: %s, skipping", sparse_name)
                load_failures.append(f"{sparse_name}: unknown model")
                continue

            sparse_config = SPARSE_MODELS[sparse_name]

            try:
                target_device = "cpu"
                logger.info(
                    "Loading sparse model: %s (device=%s)",
                    sparse_config["hf_model_id"],
                    target_device,
                )
                sparse_model = SentenceTransformer(
                    sparse_config["hf_model_id"],
                    trust_remote_code=True,
                    device=target_device,
                )
                embedder.sparse_models[sparse_name] = sparse_model
                embedder.sparse_device_map[sparse_name] = target_device
                embedder._record_model_dtype(sparse_name, sparse_model)
                logger.info("Sparse model %s staged to CPU", sparse_name)
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.error("Failed to load sparse model %s: %s", sparse_name, exc)
                load_failures.append(f"{sparse_name}: {exc}")

        if not embedder.sparse_models:
            logger.warning("No sparse models loaded successfully; disabling sparse mode")
            embedder.enable_sparse = False
            if load_failures:
                message = ", ".join(load_failures)
                embedder._sparse_runtime_reason = f"Sparse load failures: {message[:200]}"
            elif not embedder._sparse_runtime_reason:
                embedder._sparse_runtime_reason = "Sparse mode disabled: no models available"
        else:
            embedder._sparse_runtime_reason = None
            logger.info("Loaded %d sparse models", len(embedder.sparse_models))

    # ------------------------------------------------------------------
    # Public helper proxies for the facade
    # ------------------------------------------------------------------

    def build_sentence_transformer_kwargs(
        self,
        device: Optional[str] = None,
        **overrides: Any,
    ) -> Dict[str, Any]:
        return self._build_sentence_transformer_kwargs(device=device, **overrides)

    def ensure_model_snapshot(self, repo_id: str) -> Path:
        return self._ensure_model_snapshot(repo_id)

    def maybe_enable_transformer_checkpointing(self, model: SentenceTransformer) -> None:
        self._maybe_enable_transformer_checkpointing(model)

    # ------------------------------------------------------------------
    # Helper utilities mirrored from the legacy facade
    # ------------------------------------------------------------------

    def _build_sentence_transformer_kwargs(
        self,
        device: Optional[str] = None,
        **overrides: Any,
    ) -> Dict[str, Any]:
        embedder = self.embedder
        kwargs: Dict[str, Any] = {
            "device": device or embedder.device,
            "cache_folder": str(embedder.hf_cache_dir),
        }
        if embedder.local_files_only:
            kwargs["local_files_only"] = True
        kwargs.update(overrides)
        effective_device = kwargs.get("device", device or embedder.device)
        if effective_device != "cuda":
            cpu_model_kwargs = kwargs.setdefault("model_kwargs", {})
            cpu_model_kwargs.setdefault("low_cpu_mem_usage", True)
            if torch is not None:
                dtype = getattr(torch, "bfloat16", None) or getattr(torch, "float16", None)
                cpu_model_kwargs.setdefault("torch_dtype", dtype)
        return kwargs

    def _ensure_model_snapshot(self, repo_id: str) -> Path:
        embedder = self.embedder
        logger = self.logger

        repo_cache_dir = embedder.hf_cache_dir / f"models--{repo_id.replace('/', '--')}"
        if repo_cache_dir.exists() and not embedder.force_cache_refresh:
            snapshot_root = next(repo_cache_dir.glob("snapshots/*"), repo_cache_dir)
            event = {
                "model_id": repo_id,
                "path": str(snapshot_root),
                "status": "cache_hit",
            }
            embedder.telemetry.record_cache_event(event)
            logger.debug("Cache hit for %s at %s", repo_id, snapshot_root)
            return snapshot_root

        try:
            snapshot_path = snapshot_download(
                repo_id=repo_id,
                cache_dir=str(embedder.hf_cache_dir),
                local_files_only=embedder.local_files_only,
                resume_download=not embedder.force_cache_refresh,
                force_download=embedder.force_cache_refresh and not embedder.local_files_only,
            )
        except Exception as exc:  # pragma: no cover - defensive logging
            if isinstance(exc, LocalEntryNotFoundErrorType):
                message = (
                    f"Model {repo_id} not present in local cache and offline mode is enabled."
                )
                logger.error(message)
                raise FileNotFoundError(message) from exc

            logger.error("Snapshot download failed for %s: %s", repo_id, exc)
            raise

        event = {
            "model_id": repo_id,
            "path": snapshot_path,
            "status": "downloaded" if not embedder.force_cache_refresh else "refreshed",
        }
        embedder.telemetry.record_cache_event(event)
        logger.info("Cache ready for %s -> %s", repo_id, snapshot_path)
        return Path(snapshot_path)

    def _load_pytorch_model(self, model_kwargs: Dict[str, Any], optimal_batch: int) -> Any:
        embedder = self.embedder
        logger = self.logger

        st_kwargs = model_kwargs.copy()
        torch_dtype = st_kwargs.pop("torch_dtype", None)

        try:
            model = SentenceTransformer(embedder.model_config.hf_model_id, **st_kwargs)
            if torch_dtype is not None and torch_dtype == torch.float16 and embedder.device == "cuda":
                model = model.half()
                logger.info("Converted model to FP16 after loading")
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error("Failed to load model: %s", exc)
            raise

        if embedder.device_count > 1:
            logger.info("Setting up multi-GPU processing (%s GPUs)", embedder.device_count)
            if embedder.gpu_config.strategy == "data_parallel":
                logger.info("Applying DataParallel wrapper to %s", type(model).__name__)
                model = torch.nn.DataParallel(model)
                logger.info("Data parallel enabled")

        if embedder.gpu_config.enable_torch_compile and hasattr(torch, "compile"):
            try:
                logger.info("Applying torch.compile to %s", type(model).__name__)
                model = torch.compile(model, mode="reduce-overhead")  # type: ignore[attr-defined]
                logger.info("torch.compile successful")
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.warning("PyTorch compilation failed: %s", exc)

        return model

    def _load_onnx_model(self) -> Any:
        embedder = self.embedder

        if not ONNX_AVAILABLE:
            raise ImportError("ONNX runtime not available")
        if ORTModelForFeatureExtraction is None:
            raise ImportError("Optimum ORT model class not available")

        providers = []
        if torch.cuda.is_available():
            providers.append(
                (
                    "CUDAExecutionProvider",
                    {
                        "device_id": 0,
                        "arena_extend_strategy": "kSameAsRequested",
                        "gpu_mem_limit": int(embedder.gpu_config.vram_per_gpu_gb * 0.8 * 1e9),
                        "cudnn_conv_algo_search": "EXHAUSTIVE",
                        "do_copy_in_default_stream": True,
                    },
                )
            )
        providers.append("CPUExecutionProvider")

        ort_model_cls = ORTModelForFeatureExtraction
        model = ort_model_cls.from_pretrained(  # type: ignore[operator]
            embedder.model_config.hf_model_id,
            export=True,
            provider=providers[0][0] if providers else "CPUExecutionProvider",
        )
        return model

    def _maybe_enable_transformer_checkpointing(self, model: SentenceTransformer) -> None:
        embedder = self.embedder

        if not embedder.gpu_config.gradient_checkpointing:
            return

        target = None
        if hasattr(model, "model"):
            target = model.model
        elif hasattr(model, "_model"):
            target = model._model

        if target is None:
            return

        try:
            if hasattr(target, "gradient_checkpointing_enable"):
                target.gradient_checkpointing_enable()  # type: ignore[attr-defined]
                embedder._record_mitigation(
                    "gradient_checkpointing_enabled",
                    model=getattr(model, "name_or_path", embedder.model_name),
                )
        except Exception as exc:  # pragma: no cover - defensive logging
            self.logger.debug("Gradient checkpointing enable failed: %s", exc)

    def _initialize_ensemble_models(self) -> None:
        embedder = self.embedder
        logger = self.logger

        if not embedder.enable_ensemble or not embedder.ensemble_config:
            return

        if embedder.embedding_backend != "local":
            logger.info("Companion models are unavailable for API-backed embeddings")
            return

        logger.info("Loading ensemble models: %s", embedder.ensemble_config.ensemble_models)

        if embedder.device != "cuda":
            logger.info("CPU execution detected; deferring ensemble model loads until rotation")
            return

        # Determine initial device: CPU if exclusive mode, GPU otherwise
        initial_device = "cpu" if embedder.ensemble_config.exclusive_mode else embedder.device

        for model_name in embedder.ensemble_config.ensemble_models:
            if model_name not in KAGGLE_OPTIMIZED_MODELS:
                logger.warning("Unknown ensemble model %s, skipping", model_name)
                continue
            if model_name == embedder.model_name:
                continue

            try:
                self._load_ensemble_model(model_name, initial_device)
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.error("Failed to load ensemble model %s: %s", model_name, exc)

    # ------------------------------------------------------------------
    # Exclusive ensemble mode: staging and hydration
    # ------------------------------------------------------------------

    def stage_model_to_cpu(self, model_name: str) -> None:
        """Move an ensemble model to CPU to free GPU memory."""
        embedder = self.embedder
        logger = self.logger

        model = embedder.models.get(model_name)
        if model is None:
            logger.warning("Cannot stage %s: model not loaded", model_name)
            return

        # Unwrap DataParallel if present
        if isinstance(model, torch.nn.DataParallel):
            logger.debug("Unwrapping DataParallel for %s before staging to CPU", model_name)
            embedder.models[model_name] = model.module
            model = model.module

        # Move to CPU
        if hasattr(model, "to"):
            model = model.to("cpu")
            embedder.models[model_name] = model
            embedder._record_model_dtype(model_name, model)
            logger.info("Model %s staged to CPU", model_name)
        else:
            logger.warning("Model %s does not support .to() method", model_name)

    def dispose_model(self, model_name: str, *, keep_primary: bool = False) -> None:
        """Remove a model reference to free host memory."""

        embedder = self.embedder

        if keep_primary and model_name == embedder.model_name:
            return

        model = embedder.models.pop(model_name, None)
        if model is None:
            return

        if model_name == embedder.model_name:
            embedder.primary_model = None

        with suppress(Exception):
            if hasattr(model, "to"):
                model.to("cpu")

        del model
        gc.collect()
        if embedder.device == "cuda":
            torch.cuda.empty_cache()

    def hydrate_model_to_gpus(
        self,
        model_name: str,
        device_ids: Optional[List[int]] = None,
    ) -> Any:
        """Hydrate an ensemble model from CPU onto leased GPUs.

        Returns the model ready for encoding, potentially wrapped in DataParallel.
        """
        embedder = self.embedder
        logger = self.logger

        model = embedder.models.get(model_name)
        if model is None:
            try:
                model = self._load_ensemble_model(model_name, "cpu")
                logger.info("Ensemble model %s loaded on-demand", model_name)
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.error("Failed to load ensemble model %s: %s", model_name, exc)
                return None

        # Unwrap DataParallel if it was previously wrapped
        if isinstance(model, torch.nn.DataParallel):
            logger.debug("Unwrapping existing DataParallel for %s", model_name)
            model = model.module

        # Determine target device
        if device_ids is None:
            device_ids = list(range(embedder.device_count))

        if embedder.device == "cuda":
            primary_device = f"cuda:{device_ids[0]}" if device_ids else "cuda:0"
        else:
            primary_device = "cpu"

        if embedder.device != "cuda":
            logger.debug("CPU execution; %s remains on CPU", model_name)
            return model

        start_time = time.perf_counter()
        status = "skipped"
        success = False
        error_message: Optional[str] = None

        try:
            if not device_ids:
                logger.warning("Cannot hydrate %s: no device IDs provided", model_name)
                status = "no_devices"
                return model

            if hasattr(model, "to"):
                model = model.to(primary_device)
                logger.debug("Model %s moved to %s", model_name, primary_device)

                if embedder.gpu_config.precision == "fp16" and embedder.device == "cuda":
                    model = model.half()
                    logger.debug("Model %s converted to FP16", model_name)

                if (
                    embedder.device == "cuda"
                    and embedder.ensemble_config
                    and embedder.ensemble_config.exclusive_mode
                ):
                    for gpu_id in device_ids:
                        torch.cuda.set_per_process_memory_fraction(0.75, device=gpu_id)
                    logger.info(
                        "Set GPU memory limit to 12GB (75%%) for %s on GPUs %s",
                        model_name,
                        device_ids,
                    )

                    for gpu_id in device_ids:
                        mem_allocated = torch.cuda.memory_allocated(gpu_id) / (1024**3)
                        mem_reserved = torch.cuda.memory_reserved(gpu_id) / (1024**3)
                        logger.debug(
                            "GPU %d memory: %.2fGB allocated, %.2fGB reserved",
                            gpu_id,
                            mem_allocated,
                            mem_reserved,
                        )

                if (
                    len(device_ids) > 1
                    and embedder.ensemble_config
                    and embedder.ensemble_config.sequential_data_parallel
                ):
                    logger.debug(
                        "Wrapping %s with DataParallel on devices %s",
                        model_name,
                        device_ids,
                    )
                    model = torch.nn.DataParallel(model, device_ids=device_ids)
                    logger.info(
                        "Model %s wrapped with DataParallel across %d GPUs",
                        model_name,
                        len(device_ids),
                    )

                embedder.models[model_name] = model
                embedder._record_model_dtype(model_name, model)
                logger.info("Model %s hydrated to GPUs %s", model_name, device_ids)
                status = "hydrated"
                success = True
                return model

            logger.warning("Model %s does not support .to() method", model_name)
            embedder._record_model_dtype(model_name, model)
            status = "unsupported"
            return model
        except Exception as exc:  # pragma: no cover - defensive guard
            error_message = str(exc)
            status = "error"
            raise
        finally:
            duration = time.perf_counter() - start_time
            event = {
                "timestamp": time.time(),
                "model": model_name,
                "device_ids": list(device_ids or []),
                "primary_device": primary_device,
                "duration_seconds": round(duration, 6),
                "status": status,
                "success": success,
            }
            if error_message:
                event["error"] = error_message[:200]
            embedder.processing_stats["hydration_events"].append(event)

    def _load_ensemble_model(self, model_name: str, device: str) -> Any:
        embedder = self.embedder
        logger = self.logger

        config = KAGGLE_OPTIMIZED_MODELS.get(model_name)
        if config is None:
            raise KeyError(f"Unknown ensemble model '{model_name}'")

        logger.info("Loading ensemble model: %s on device %s", config.hf_model_id, device)
        self._ensure_model_snapshot(config.hf_model_id)

        kwargs = self._build_sentence_transformer_kwargs(device=device)
        kwargs["trust_remote_code"] = config.trust_remote_code

        model = SentenceTransformer(config.hf_model_id, **kwargs)

        if embedder.gpu_config.precision == "fp16" and device != "cpu":
            model = model.half()

        embedder.models[model_name] = model
        embedder._record_model_dtype(model_name, model)
        logger.info("Ensemble model %s loaded on %s", model_name, device)
        return model


__all__ = ["ModelManager"]
