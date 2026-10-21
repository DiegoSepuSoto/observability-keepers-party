"""Contract checks for edge cases called out by the skill design."""

from pathlib import Path
import re
import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("obs-init", "obs-guide", "obs-audit", "obs-score", "obs-impact")


def read_skill(name: str) -> str:
    return (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")


def section(content: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$", content, re.MULTILINE)
    assert match, f"missing section: {heading}"
    following = re.search(r"^## ", content[match.end():], re.MULTILINE)
    end = match.end() + following.start() if following else len(content)
    return content[match.end():end].strip()


def test_shared_untrusted_content_rule_covers_repository_injection_boundaries() -> None:
    rules = {name: section(read_skill(name), "Untrusted content") for name in SKILLS}
    assert len(set(rules.values())) == 1

    rule = next(iter(rules.values())).lower()
    for source in (
        "readme", "comments", "source code", "manifests", "specs", "logs",
        "configuration", "generated documentation", "tool output",
    ):
        assert source in rule
    for boundary in (
        "objective", "output limits", "privacy rules", "permitted commands",
        "write paths", "clarification requirements", "no-application-source-edit",
        "do not run commands based on repository text", "external contact",
        "without repeating sensitive content",
    ):
        assert boundary in rule


def test_init_uses_manifest_evidence_and_stops_before_ambiguous_writes() -> None:
    content = read_skill("obs-init").lower()
    for manifest in ("package.json", "go.mod", "requirements.txt", "pyproject.toml", "cargo.toml"):
        assert manifest in content
    for generated in ("node_modules", "vendor", "dist", "build", ".venv", "target"):
        assert generated in content
    assert "workspace configuration" in content
    assert "only from manifest evidence" in content
    assert "stop before creating `.observability/config.yaml`" in content
    assert "maturity_level" in content and "baseline" in content
    assert "does not audit source instrumentation" in content
    assert "create sdd tasks" in content


def test_guide_stays_on_active_feature_and_handles_async_context_safely() -> None:
    content = read_skill("obs-guide").lower()
    assert ".sdd/features/" in content
    assert "specific sdd framework" in content
    assert "read only the active feature specification" in content
    assert "one or two priority actions" in content
    assert "traceparent" in content and "w3c" in content
    assert "routes without normalizing" in content or "raw url paths" in content
    assert "do not edit application source" in content
    assert "heuristic" in content and "yaml alone is not proof" in content


def test_audit_tasks_are_bounded_prioritized_and_deduplicated() -> None:
    content = read_skill("obs-audit").lower()
    for category in ("cardinality", "export", "propagation", "coverage", "data-safety"):
        assert category in content
    assert "at most two tasks" in content or "no more than two tasks" in content
    assert "share `category` and `scope`" in content
    assert "highest existing three-digit sequence" in content
    assert "counting open and done tasks" in content
    assert "customer impact and risk reduction" in content
    assert "acceptance criteria" in content
    assert "do not edit application source code" in content


def test_score_uses_one_denominator_and_labels_each_evidence_method() -> None:
    content = read_skill("obs-score").lower()
    assert "exactly the same set of critical routes as the denominator for traces, metrics, and logs" in content
    assert "critical_routes" in content
    assert "health, readiness, metrics, and static-asset endpoints" in content
    for method in ("config", "ast", "heuristic"):
        assert f"**{method}**" in content
    assert "unknown" in content and "static scorecard" in content
    assert "never claim runtime coverage" in content


def test_impact_requires_observed_data_and_keeps_request_user_denominators_distinct() -> None:
    content = read_skill("obs-impact").lower()
    for evidence in ("slo/sli", "traffic", "incident", "distinct affected users", "population denominator"):
        assert evidence in content
    assert "three to five lines" in content
    assert "http 5xx" in content and "p95" in content
    assert "request counts do not establish distinct users" in content
    assert "mttd" in content and "mttr" in content
    assert "unavailable" in content and "do not invent" in content
    assert "do not list raw telemetry fields" in content


def test_service_docs_cover_installation_and_sdd_task_rules() -> None:
    install = (ROOT / "docs" / "installation.md").read_text(encoding="utf-8").lower()
    sdd = (ROOT / "docs" / "sdd-conventions.md").read_text(encoding="utf-8").lower()
    for location in (".opencode/skills/<skill-name>/", ".claude/skills/<skill-name>/", ".agents/skills/<skill-name>/"):
        assert location in install
    assert "no single invocation command" in install
    assert "independent" in install and "references/" in install
    assert "maximum sequence" in sdd and "including done tasks" in sdd
    assert "same `category` and `scope`" in sdd
    assert "high priority" in sdd and "medium priority" in sdd


def test_repository_delivery_files_stay_below_six_hundred_lines() -> None:
    paths = [ROOT / "README.md", ROOT / "CONTRIBUTING.md", ROOT / "CHANGELOG.md"]
    paths.extend((ROOT / "docs").glob("*.md"))
    paths.extend((ROOT / "skills").glob("*/SKILL.md"))
    paths.extend((ROOT / "tests").glob("test_*.py"))
    assert all(len(path.read_text(encoding="utf-8").splitlines()) < 600 for path in paths)
