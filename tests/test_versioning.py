"""Tests for prompt versioning system."""

from __future__ import annotations

import time

from prompt_engineering_lab.versioning import (
    PromptVersion,
    PromptVersionManager,
    VersionDiff,
)


class TestPromptVersionManager:
    def test_create_version_returns_version(self) -> None:
        mgr = PromptVersionManager()
        v = mgr.create_version("Hello {name}")
        assert isinstance(v, PromptVersion)
        assert v.template == "Hello {name}"
        assert v.version_id

    def test_create_version_with_metadata(self) -> None:
        mgr = PromptVersionManager()
        v = mgr.create_version("Test", metadata={"author": "test"})
        assert v.metadata == {"author": "test"}

    def test_get_version_exists(self) -> None:
        mgr = PromptVersionManager()
        v = mgr.create_version("Template A")
        retrieved = mgr.get_version(v.version_id)
        assert retrieved is not None
        assert retrieved.template == "Template A"

    def test_get_version_missing(self) -> None:
        mgr = PromptVersionManager()
        assert mgr.get_version("nonexistent") is None

    def test_list_versions_ordered(self) -> None:
        mgr = PromptVersionManager()
        v1 = mgr.create_version("First")
        mgr.create_version("Second")
        v3 = mgr.create_version("Third")
        versions = mgr.list_versions()
        assert len(versions) == 3
        assert versions[0].version_id == v1.version_id
        assert versions[2].version_id == v3.version_id

    def test_list_versions_empty(self) -> None:
        mgr = PromptVersionManager()
        assert mgr.list_versions() == []

    def test_diff_shows_added_and_removed(self) -> None:
        mgr = PromptVersionManager()
        v1 = mgr.create_version("hello world foo")
        v2 = mgr.create_version("hello world bar")
        d = mgr.diff(v1.version_id, v2.version_id)
        assert isinstance(d, VersionDiff)
        assert "bar" in d.added_words
        assert "foo" in d.removed_words

    def test_diff_identical_versions(self) -> None:
        mgr = PromptVersionManager()
        v1 = mgr.create_version("same text")
        v2 = mgr.create_version("same text")
        d = mgr.diff(v1.version_id, v2.version_id)
        assert d.added_words == []
        assert d.removed_words == []
        assert d.similarity == 1.0

    def test_diff_missing_version_raises(self) -> None:
        mgr = PromptVersionManager()
        v1 = mgr.create_version("test")
        try:
            mgr.diff(v1.version_id, "missing")
            assert False, "Should have raised"
        except KeyError:
            pass

    def test_rollback_sets_active(self) -> None:
        mgr = PromptVersionManager()
        v1 = mgr.create_version("Version 1")
        mgr.create_version("Version 2")
        result = mgr.rollback(v1.version_id)
        assert result.version_id == v1.version_id
        assert mgr.active_version is not None
        assert mgr.active_version.version_id == v1.version_id

    def test_rollback_missing_raises(self) -> None:
        mgr = PromptVersionManager()
        try:
            mgr.rollback("missing")
            assert False, "Should have raised"
        except KeyError:
            pass

    def test_record_performance(self) -> None:
        mgr = PromptVersionManager()
        v = mgr.create_version("test")
        assert mgr.record_performance(v.version_id, {"score": 0.95, "latency": 120.0})
        assert v.performance["score"] == 0.95

    def test_record_performance_missing_version(self) -> None:
        mgr = PromptVersionManager()
        assert not mgr.record_performance("missing", {"score": 0.5})

    def test_record_performance_updates(self) -> None:
        mgr = PromptVersionManager()
        v = mgr.create_version("test")
        mgr.record_performance(v.version_id, {"score": 0.5})
        mgr.record_performance(v.version_id, {"score": 0.9})
        assert v.performance["score"] == 0.9

    def test_get_best_higher_is_better(self) -> None:
        mgr = PromptVersionManager()
        v1 = mgr.create_version("low")
        v2 = mgr.create_version("high")
        mgr.record_performance(v1.version_id, {"score": 0.5})
        mgr.record_performance(v2.version_id, {"score": 0.9})
        best = mgr.get_best("score", higher_is_better=True)
        assert best is not None
        assert best.version_id == v2.version_id

    def test_get_best_lower_is_better(self) -> None:
        mgr = PromptVersionManager()
        v1 = mgr.create_version("fast")
        v2 = mgr.create_version("slow")
        mgr.record_performance(v1.version_id, {"latency": 50.0})
        mgr.record_performance(v2.version_id, {"latency": 200.0})
        best = mgr.get_best("latency", higher_is_better=False)
        assert best is not None
        assert best.version_id == v1.version_id

    def test_get_best_no_data(self) -> None:
        mgr = PromptVersionManager()
        mgr.create_version("test")
        assert mgr.get_best("score") is None

    def test_get_best_empty_manager(self) -> None:
        mgr = PromptVersionManager()
        assert mgr.get_best("score") is None

    def test_changelog_ordered(self) -> None:
        mgr = PromptVersionManager()
        mgr.create_version("First", metadata={"tag": "v1"})
        mgr.create_version("Second", metadata={"tag": "v2"})
        changelog = mgr.get_changelog()
        assert len(changelog) == 2
        assert changelog[0]["metadata"] == {"tag": "v1"}
        assert changelog[1]["metadata"] == {"tag": "v2"}

    def test_changelog_empty(self) -> None:
        mgr = PromptVersionManager()
        assert mgr.get_changelog() == []

    def test_active_version_tracks_latest(self) -> None:
        mgr = PromptVersionManager()
        assert mgr.active_version is None
        v1 = mgr.create_version("First")
        assert mgr.active_version is not None
        assert mgr.active_version.version_id == v1.version_id
        v2 = mgr.create_version("Second")
        assert mgr.active_version.version_id == v2.version_id

    def test_created_at_is_timestamp(self) -> None:
        mgr = PromptVersionManager()
        before = time.time()
        v = mgr.create_version("test")
        after = time.time()
        assert before <= v.created_at <= after
