import logging


def test_summarize_batch_sources_counts(build_embedder):
    embedder = build_embedder()
    embedder.chunks_metadata = [
        {"source_path": "docs/A.md"},
        {"source_path": "docs/A.md"},
        {"source_path": "notes/B.md"},
        {},
    ]

    summary = embedder._summarize_batch_sources(0, 4)

    assert "A.md (2)" in summary
    assert "B.md (1)" in summary
    assert "chunk_3 (1)" in summary


def test_summarize_batch_sources_limit_indicator(build_embedder):
    embedder = build_embedder()
    embedder.chunks_metadata = [
        {"source_path": f"file_{idx}.md"} for idx in range(10)
    ]

    summary = embedder._summarize_batch_sources(0, 10, limit=6)

    assert summary.count("(") == 6
    assert "… +4 more" in summary


def test_log_batch_sources_emits_info(build_embedder, caplog):
    embedder = build_embedder()
    embedder.chunks_metadata = [
        {"source_path": "one.md"},
        {"source_path": "two.md"},
    ]

    with caplog.at_level(logging.INFO):
        embedder._log_batch_sources(2, 0, 2)

    assert any("Batch 2 sources" in message for message in caplog.messages)
    assert any("one.md" in message for message in caplog.messages)


def test_get_batch_progress_label_single_source(build_embedder):
    embedder = build_embedder()
    embedder.chunks_metadata = [
        {"source_path": "docs/alpha.md"},
        {"source_path": "docs/alpha.md"},
    ]

    label = embedder._get_batch_progress_label(0, 2)

    assert label == "alpha.md"


def test_get_batch_progress_label_multi_source(build_embedder):
    embedder = build_embedder()
    embedder.chunks_metadata = [
        {"source_path": "docs/alpha.md"},
        {"source_path": "docs/beta.md"},
        {"source_path": "docs/alpha.md"},
        {"source_path": "docs/gamma.md"},
    ]

    label = embedder._get_batch_progress_label(0, 4)

    assert label.startswith("alpha.md")
    assert "+" in label
