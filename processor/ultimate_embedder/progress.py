from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class BatchProgressContext:
    """Context payload for batch progress updates."""

    batch_index: int
    total_batches: int
    label: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "batch_index": max(0, self.batch_index),
            "total_batches": max(1, self.total_batches),
        }
        if self.label:
            payload["label"] = self.label
        return payload

    def tqdm_description(self) -> Optional[str]:
        if not self.label:
            return None
        return f"Batches({self.label})"
