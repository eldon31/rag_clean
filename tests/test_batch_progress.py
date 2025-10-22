import numpy as np
import pytest

from processor.ultimate_embedder.core import BatchProgressContext


@pytest.mark.parametrize("device", ["cpu", "cuda:0"])
def test_call_encode_adds_tqdm_kwargs(build_embedder, device):
    embedder = build_embedder()
    model = embedder._get_primary_model()

    context = BatchProgressContext(batch_index=0, total_batches=3, label="alpha.md")

    result = embedder._call_encode(
        model,
        ["chunk-0", "chunk-1"],
        batch_size=2,
        device=device,
        progress_context=context,
    )

    assert isinstance(result, np.ndarray)
    assert model.last_tqdm_kwargs == {"desc": "Batches(alpha.md)"}


def test_call_encode_skips_tqdm_when_unsupported(build_embedder):
    embedder = build_embedder()

    class NoTqdmModel:
        def __init__(self) -> None:
            self.kwargs = None

        def encode(
            self,
            texts,
            batch_size: int = 1,
            show_progress_bar: bool = False,
            convert_to_numpy: bool = True,
            normalize_embeddings: bool = True,
            device: str | None = None,
        ):
            self.kwargs = {
                "batch_size": batch_size,
                "show_progress_bar": show_progress_bar,
                "convert_to_numpy": convert_to_numpy,
                "normalize_embeddings": normalize_embeddings,
                "device": device,
            }
            return np.zeros((len(texts), 16), dtype=np.float32)

    model = NoTqdmModel()
    context = BatchProgressContext(batch_index=1, total_batches=4, label="beta")

    result = embedder._call_encode(
        model,
        ["chunk-0"],
        batch_size=1,
        device="cpu",
        progress_context=context,
    )

    assert isinstance(result, np.ndarray)
    assert "tqdm_kwargs" not in (model.kwargs or {})


def test_call_encode_retries_without_tqdm_kwargs(build_embedder):
    embedder = build_embedder()
    model = embedder._get_primary_model()
    model.fail_on_tqdm_once = True

    context = BatchProgressContext(batch_index=2, total_batches=5, label="gamma")

    result = embedder._call_encode(
        model,
        ["chunk-0", "chunk-1", "chunk-2"],
        batch_size=3,
        device="cpu",
        progress_context=context,
    )

    assert isinstance(result, np.ndarray)
    assert model.last_tqdm_kwargs is None
