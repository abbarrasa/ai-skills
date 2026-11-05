"""Load and resolve the catalog's installation dependencies without third-party packages."""

import json
import re
from pathlib import Path


def load_dependencies(root: Path) -> dict[str, list[str]]:
    try:
        graph = json.loads((root / "skills-dependencies.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError(f"Cannot read skills-dependencies.json: {exc}") from exc
    if not isinstance(graph, dict) or not graph:
        raise ValueError("Dependency manifest must be a nonempty object.")
    for name, dependencies in graph.items():
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"Invalid skill name: {name!r}")
        if not isinstance(dependencies, list) or any(not isinstance(item, str) for item in dependencies):
            raise ValueError(f"{name}: dependencies must be a list of skill names.")
        if len(dependencies) != len(set(dependencies)):
            raise ValueError(f"{name}: duplicate dependency.")
    catalog = {path.parent.name for path in (root / "skills").glob("*/SKILL.md")}
    if set(graph) != catalog:
        raise ValueError(f"Manifest/catalog mismatch: {', '.join(sorted(set(graph) ^ catalog))}")
    resolve_dependencies(graph, list(graph))
    return graph


def resolve_dependencies(graph: dict[str, list[str]], requested: list[str]) -> list[str]:
    """Return each selected skill once, dependencies first; reject missing nodes/cycles."""
    result = []
    visiting = []
    visited = set()

    def visit(name):
        if name not in graph:
            raise ValueError(f"Unknown skill or missing dependency: {name}")
        if name in visiting:
            raise ValueError(f"Dependency cycle: {' -> '.join([*visiting, name])}")
        if name in visited:
            return
        visiting.append(name)
        for dependency in graph[name]:
            visit(dependency)
        visiting.pop()
        visited.add(name)
        result.append(name)

    for name in requested:
        visit(name)
    return result
