import json

from scripts.embed_collections_v5 import CollectionRunResult


def test_collection_summary_includes_rotation_metadata():
    rotation_events = [
        {
            "batch_index": 0,
            "model": "jina-code-embeddings-1.5b",
            "status": "completed",
            "device": "cpu",
        }
    ]

    performance = {
        "ensemble_rotation": rotation_events,
        "ensemble_rotation_limit": 250,
        "ensemble_rotation_overflow": 3,
    }

    result = CollectionRunResult(
        collection="Qdrant",
        status="completed",
        chunks=12,
        performance=performance,
        exports={},
        rotation_events=rotation_events,
    )

    payload = result.to_dict()

    assert payload["performance"]["ensemble_rotation"] == rotation_events
    assert payload["performance"]["ensemble_rotation_limit"] == 250
    assert payload["performance"]["ensemble_rotation_overflow"] == 3
    assert payload["rotation_events"] == rotation_events

    # ensure the payload remains JSON-serializable
    json.dumps(payload)


def test_collection_summary_omits_missing_rotation_overflow():
    rotation_events = []
    performance = {
        "ensemble_rotation": rotation_events,
        "ensemble_rotation_limit": 100,
    }

    result = CollectionRunResult(
        collection="Docling",
        status="completed",
        chunks=5,
        performance=performance,
        exports={},
        rotation_events=rotation_events,
    )

    payload = result.to_dict()

    assert "ensemble_rotation_overflow" not in payload["performance"]
    assert payload["rotation_events"] == rotation_events

    json.dumps(payload)
