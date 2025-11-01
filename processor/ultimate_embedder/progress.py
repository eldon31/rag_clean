from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class BatchProgressContext:
    """Context payload for batch progress updates."""

    batch_index: int
    total_batches: int
    label: Optional[str] = None
    model_name: Optional[str] = None

    def tqdm_description(self) -> Optional[str]:
        if not self.label:
            return None
        return f"Batches({self.label})"
    
    def tqdm_postfix(self) -> Optional[str]:
        """Return the model name for tqdm postfix display."""
        return self.model_name
