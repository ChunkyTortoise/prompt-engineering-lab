"""Prompt versioning system for tracking template evolution and performance."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from difflib import SequenceMatcher


@dataclass
class PromptVersion:
    """A single version of a prompt template."""

    version_id: str
    template: str
    created_at: float
    metadata: dict[str, object] = field(default_factory=dict)
    performance: dict[str, float] = field(default_factory=dict)


@dataclass
class VersionDiff:
    """Diff between two prompt versions."""

    version_a: str
    version_b: str
    added_words: list[str]
    removed_words: list[str]
    similarity: float


class PromptVersionManager:
    """Manages prompt template versions with performance tracking and rollback."""

    def __init__(self) -> None:
        self._versions: dict[str, PromptVersion] = {}
        self._order: list[str] = []
        self._active_id: str | None = None

    def create_version(self, template: str, metadata: dict[str, object] | None = None) -> PromptVersion:
        """Create a new prompt version."""
        version_id = uuid.uuid4().hex[:8]
        version = PromptVersion(
            version_id=version_id,
            template=template,
            created_at=time.time(),
            metadata=metadata or {},
        )
        self._versions[version_id] = version
        self._order.append(version_id)
        self._active_id = version_id
        return version

    def get_version(self, version_id: str) -> PromptVersion | None:
        """Retrieve a version by ID."""
        return self._versions.get(version_id)

    def list_versions(self) -> list[PromptVersion]:
        """List all versions in creation order."""
        return [self._versions[vid] for vid in self._order]

    def diff(self, version_a: str, version_b: str) -> VersionDiff:
        """Compute diff between two versions."""
        va = self._versions.get(version_a)
        vb = self._versions.get(version_b)
        if va is None or vb is None:
            msg = "Version not found"
            raise KeyError(msg)

        words_a = set(va.template.split())
        words_b = set(vb.template.split())

        added = sorted(words_b - words_a)
        removed = sorted(words_a - words_b)
        similarity = SequenceMatcher(None, va.template, vb.template).ratio()

        return VersionDiff(
            version_a=version_a,
            version_b=version_b,
            added_words=added,
            removed_words=removed,
            similarity=round(similarity, 4),
        )

    def rollback(self, version_id: str) -> PromptVersion:
        """Set a previous version as the active version."""
        if version_id not in self._versions:
            msg = f"Version {version_id} not found"
            raise KeyError(msg)
        self._active_id = version_id
        return self._versions[version_id]

    def record_performance(self, version_id: str, metrics: dict[str, float]) -> bool:
        """Record performance metrics for a version."""
        version = self._versions.get(version_id)
        if version is None:
            return False
        version.performance.update(metrics)
        return True

    def get_best(self, metric: str, higher_is_better: bool = True) -> PromptVersion | None:
        """Find the version with the best value for a given metric."""
        candidates = [v for v in self._versions.values() if metric in v.performance]
        if not candidates:
            return None
        return (
            max(candidates, key=lambda v: v.performance[metric])
            if higher_is_better
            else min(candidates, key=lambda v: v.performance[metric])
        )

    def get_changelog(self) -> list[dict[str, object]]:
        """Return changelog of all versions in chronological order."""
        entries: list[dict[str, object]] = []
        for vid in self._order:
            v = self._versions[vid]
            entries.append(
                {
                    "version_id": v.version_id,
                    "created_at": v.created_at,
                    "metadata": v.metadata,
                    "template_preview": v.template[:80],
                }
            )
        return entries

    @property
    def active_version(self) -> PromptVersion | None:
        """Get the currently active version."""
        if self._active_id is None:
            return None
        return self._versions.get(self._active_id)
