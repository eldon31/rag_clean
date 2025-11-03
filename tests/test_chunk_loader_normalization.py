import json
import logging

from processor.ultimate_embedder.chunk_loader import ChunkLoader


def _make_loader(tmp_path):
    logger = logging.getLogger("chunk-loader-test")
    return ChunkLoader(project_root=tmp_path, is_kaggle=False, logger=logger)


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_chunk_loader_handles_wrapped_chunks(tmp_path):
    chunk_dir = tmp_path / "doc_chunks"
    chunk_dir.mkdir()
    payload = {
        "chunks": [
            {
                "text": "hello world",
                "metadata": {"token_count": 120},
            }
        ]
    }
    _write_json(chunk_dir / "wrapped_chunks.json", payload)

    loader = _make_loader(tmp_path)
    result = loader.load(
        str(chunk_dir),
        preprocess_text=lambda text: text,
        model_name="test-model",
        model_vector_dim=768,
        text_cache=None,
    )

    assert result.summary["total_chunks_loaded"] == 1
    assert result.metadata[0]["model_target"] == "test-model"


def test_chunk_loader_coerces_string_entries(tmp_path):
    chunk_dir = tmp_path / "string_chunks"
    chunk_dir.mkdir()
    payload = [
        {
            "text": "structured entry",
            "metadata": {"token_count": 120},
        },
        "loose text value",
    ]
    _write_json(chunk_dir / "mixed_chunks.json", payload)

    loader = _make_loader(tmp_path)
    result = loader.load(
        str(chunk_dir),
        preprocess_text=lambda text: text,
        model_name="test-model",
        model_vector_dim=768,
        text_cache=None,
    )

    assert result.summary["total_chunks_loaded"] == 1
    assert not result.summary["loading_errors"]


def test_chunk_loader_descends_into_nested_chunked_dir(tmp_path):
    dataset_root = tmp_path / "uploaded_dataset"
    nested_dir = dataset_root / "Chunked" / "Docling"
    nested_dir.mkdir(parents=True)

    payload = [
        {
            "text": "valid chunk",
            "metadata": {"token_count": 120},
        }
    ]
    _write_json(nested_dir / "docling_chunks.json", payload)

    loader = _make_loader(tmp_path)
    result = loader.load(
        str(dataset_root),
        preprocess_text=lambda text: text,
        model_name="test-model",
        model_vector_dim=768,
        text_cache=None,
    )

    assert result.summary["total_chunks_loaded"] == 1
