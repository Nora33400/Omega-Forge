"""Local project indexing for Omega-Forge.

ProjectIndex gives the forge a first repository understanding layer without
requiring embeddings, vector databases, or external services.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_IGNORED_DIRS: set[str] = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
    "env",
}

DEFAULT_TEXT_EXTENSIONS: set[str] = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".ini",
    ".cfg",
    ".csv",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".sh",
    ".ps1",
}


@dataclass(frozen=True)
class IndexedFile:
    """A file known by ProjectIndex."""

    path: str
    extension: str
    size_bytes: int
    line_count: int = 0
    preview: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ProjectIndex:
    """Index and search a local project directory."""

    def __init__(
        self,
        root: str | Path,
        ignored_dirs: set[str] | None = None,
        text_extensions: set[str] | None = None,
        max_preview_chars: int = 800,
    ) -> None:
        self.root = Path(root).resolve()
        if not self.root.exists():
            raise FileNotFoundError(f"Project root does not exist: {self.root}")
        if not self.root.is_dir():
            raise NotADirectoryError(f"Project root is not a directory: {self.root}")
        self.ignored_dirs = set(ignored_dirs or DEFAULT_IGNORED_DIRS)
        self.text_extensions = set(text_extensions or DEFAULT_TEXT_EXTENSIONS)
        self.max_preview_chars = max_preview_chars
        self.files: list[IndexedFile] = []

    def build(self) -> "ProjectIndex":
        self.files = []
        for path in sorted(self.root.rglob("*")):
            if not path.is_file():
                continue
            if self._is_ignored(path):
                continue
            self.files.append(self._index_file(path))
        return self

    def search(self, query: str, limit: int = 10) -> list[IndexedFile]:
        clean_query = query.strip().lower()
        if not clean_query:
            return []
        scored: list[tuple[int, IndexedFile]] = []
        for file in self.files:
            score = 0
            path_text = file.path.lower()
            preview_text = file.preview.lower()
            if clean_query in path_text:
                score += 10
            if clean_query in preview_text:
                score += 3
            if file.extension.lower().lstrip(".") == clean_query:
                score += 5
            if score:
                scored.append((score, file))
        scored.sort(key=lambda item: (-item[0], item[1].path))
        return [file for _, file in scored[:limit]]

    def by_extension(self, extension: str) -> list[IndexedFile]:
        normalized = extension if extension.startswith(".") else f".{extension}"
        return [file for file in self.files if file.extension == normalized]

    def summary(self) -> dict[str, Any]:
        by_ext: dict[str, int] = {}
        total_size = 0
        for file in self.files:
            by_ext[file.extension] = by_ext.get(file.extension, 0) + 1
            total_size += file.size_bytes
        return {
            "root": str(self.root),
            "file_count": len(self.files),
            "total_size_bytes": total_size,
            "extensions": dict(sorted(by_ext.items())),
        }

    def export(self) -> dict[str, Any]:
        return {
            "summary": self.summary(),
            "files": [file.to_dict() for file in self.files],
        }

    def _is_ignored(self, path: Path) -> bool:
        relative_parts = path.relative_to(self.root).parts
        return any(part in self.ignored_dirs for part in relative_parts)

    def _index_file(self, path: Path) -> IndexedFile:
        relative = path.relative_to(self.root).as_posix()
        extension = path.suffix.lower() or "<none>"
        size = path.stat().st_size
        preview = ""
        line_count = 0
        if extension in self.text_extensions:
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
                line_count = len(text.splitlines())
                preview = text[: self.max_preview_chars]
            except OSError:
                preview = ""
        return IndexedFile(
            path=relative,
            extension=extension,
            size_bytes=size,
            line_count=line_count,
            preview=preview,
        )
