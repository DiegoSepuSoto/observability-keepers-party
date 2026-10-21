"""Keep the package's stable version record and release notes aligned."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def test_current_version_is_semver_and_has_a_dated_changelog_entry() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert re.fullmatch(r"\d+\.\d+\.\d+", version)

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## [Unreleased]" in changelog
    assert re.search(rf"^## \[{re.escape(version)}\] - \d{{4}}-\d{{2}}-\d{{2}}$", changelog, re.MULTILINE)


def test_readme_and_contributing_explain_version_source_and_release_steps() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    assert f"Current release: **{version}** ([version record](VERSION)" in readme
    assert "Semantic Versioning" in contributing
    assert "canonical current stable version" in contributing
    assert "vX.Y.Z" in contributing
