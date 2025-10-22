"""Record the public surface of processor.ultimate_embedder.core for Task 1.2."""

from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import processor.ultimate_embedder.core as core  # noqa: E402


def collect_module_surface() -> Dict[str, Any]:
    module_items = {}
    module_name = core.__name__
    for name, value in inspect.getmembers(core):
        if name.startswith("_"):
            continue
        if inspect.ismodule(value):
            continue
        if inspect.isbuiltin(value):
            continue

        if inspect.isfunction(value):
            if value.__module__ != module_name:
                continue
            module_items.setdefault("functions", []).append(name)
        elif inspect.isclass(value):
            if value.__module__ != module_name:
                continue
            module_items.setdefault("classes", []).append(name)
        else:
            value_module = getattr(type(value), "__module__", "")
            if not name.isupper() and value_module != module_name:
                continue
            module_items.setdefault("attributes", []).append(name)

    for category in module_items:
        module_items[category] = sorted(set(module_items[category]))

    return module_items


def collect_class_surface(cls: type) -> Dict[str, Any]:
    surface: Dict[str, Any] = {"methods": [], "class_methods": [], "static_methods": [], "properties": []}

    for name, member in inspect.getmembers(cls):
        if name.startswith("_"):
            continue

        if isinstance(member, property):
            surface["properties"].append(name)
            continue

        original = getattr(cls, name)
        if isinstance(original, staticmethod):
            surface["static_methods"].append(name)
            continue
        if isinstance(original, classmethod):
            surface["class_methods"].append(name)
            continue
        if inspect.isfunction(member):
            surface["methods"].append(name)

    for category in surface:
        surface[category] = sorted(set(surface[category]))

    return surface


def main() -> None:
    report = {
        "module": collect_module_surface(),
        "UltimateKaggleEmbedderV4": collect_class_surface(core.UltimateKaggleEmbedderV4),
    }

    target = Path(__file__).resolve().parent / "core_public_surface.json"
    with target.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)

    print(f"Public surface report written to {target}")


if __name__ == "__main__":
    main()
