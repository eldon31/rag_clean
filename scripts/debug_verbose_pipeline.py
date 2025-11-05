#!/usr/bin/env python3
"""Run the Kaggle embedder with DEBUG logging for rerank and sparse components."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Iterable, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import scripts.embed_collections_v7 as embed_v7

VERBOSE_LOGGERS = [
    "processor.ultimate_embedder.core",
    "processor.ultimate_embedder.cross_encoder_executor",
    "processor.ultimate_embedder.rerank_pipeline",
    "processor.ultimate_embedder.sparse_generator",
]
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def _enable_verbose_logging() -> None:
    """Attach a stream handler and promote key loggers to DEBUG."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    if not root_logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        root_logger.addHandler(handler)
    else:
        for handler in root_logger.handlers:
            handler.setLevel(logging.DEBUG)
            if handler.formatter is None:
                handler.setFormatter(logging.Formatter(LOG_FORMAT))

    for logger_name in VERBOSE_LOGGERS:
        logging.getLogger(logger_name).setLevel(logging.DEBUG)

    # Keep third-party libraries at info to avoid drowning out embedder traces.
    for noisy in ("transformers", "sentence_transformers"):
        logging.getLogger(noisy).setLevel(logging.INFO)

    logging.getLogger(__name__).debug("Verbose logging enabled for rerank and sparse stages")


def main(argv: Optional[Iterable[str]] = None) -> int:
    argv_list = list(argv) if argv is not None else sys.argv[1:]

    original_configure_logging = embed_v7._configure_logging

    def _verbose_configure_logging() -> None:
        original_configure_logging()
        _enable_verbose_logging()

    embed_v7._configure_logging = _verbose_configure_logging

    try:
        return embed_v7.main(argv_list)
    finally:
        embed_v7._configure_logging = original_configure_logging


if __name__ == "__main__":
    sys.exit(main())
