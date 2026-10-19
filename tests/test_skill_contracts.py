from pathlib import Path
import re
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("obs-init", "obs-guide", "obs-audit", "obs-impact", "obs-score")


def read_skill(name: str) -> str:
    path = ROOT / "skills" / name / "SKILL.md"
    assert path.is_file(), f"skill file is missing: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def has_word(content: str, word: str) -> bool:
    return re.search(rf"\b{re.escape(word)}\b", content) is not None


def section(content: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$", content, re.MULTILINE)
    assert match, f"missing section: {heading}"
    next_heading = re.search(r"^## ", content[match.end():], re.MULTILINE)
    end = match.end() + next_heading.start() if next_heading else len(content)
    return content[match.end():end].strip()


def first_paragraph(content: str) -> str:
    return content.split("\n\n", 1)[0].strip()


def read_frontmatter(name: str) -> dict[str, Any]:
    content = read_skill(name)
    parts = content.split("---", 2)
    assert len(parts) == 3 and parts[0].strip() == "", (
        f"{name} must begin with YAML frontmatter"
    )
    metadata = yaml.safe_load(parts[1])
    assert isinstance(metadata, dict), f"{name} frontmatter must be a mapping"
    return metadata


def test_obs_init_metadata_is_portable() -> None:
    metadata = read_frontmatter("obs-init")

    assert metadata["name"] == "obs-init"
    assert isinstance(metadata["description"], str) and metadata["description"].strip()


def test_baseline_config_matches_requested_schema() -> None:
    path = ROOT / "skills" / "obs-init" / "references" / "observability-config.yaml"
    assert path.is_file(), "obs-init must bundle its baseline contract template"

    actual = yaml.safe_load(path.read_text(encoding="utf-8"))
    expected = {
        "version": "1.0",
        "service": "unnamed-service",
        "telemetry_standard": "opentelemetry",
        "maturity_level": "baseline",
        "guardrails": {
            "forbidden_metric_labels": [
                "user_id",
                "email",
                "account_id",
                "order_id",
                "transaction_id",
                "session_id",
                "request_id",
                "ip_address",
            ],
            "fail_silent": True,
            "async_export": True,
            "event_driven_propagation": True,
        },
        "pillars": {
            "traces": {
                "required_in_scopes": True,
                "sampling_ratio": 1.0,
                "propagation": "w3c",
                "mandatory_attributes": ["app.environment"],
            },
            "metrics": {
                "framework_defaults": True,
                "custom_metrics_limit_per_scope": 2,
                "required_types": ["counter", "histogram"],
            },
            "logs": {
                "structured": True,
                "inject_trace_id": True,
                "min_level": "info",
            },
        },
    }

    assert actual == expected


def test_baseline_template_comments_document_optional_examples() -> None:
    path = ROOT / "skills" / "obs-init" / "references" / "observability-config.yaml"
    content = path.read_text(encoding="utf-8")
    assert "# slo:" in content
    assert "# critical_routes:" in content
    assert "# sampling_ratio: 1.0" in content


def test_obs_init_preserves_existing_contract() -> None:
    content = read_skill("obs-init").lower()

    assert "do not overwrite" in content
    assert ".observability/config.yaml" in content


def test_obs_init_treats_unknown_stack_as_unknown() -> None:
    content = read_skill("obs-init").lower()

    assert "unknown" in content
    assert "do not guess" in content or "never guess" in content


def test_obs_init_stops_on_ambiguous_service_candidates() -> None:
    content = read_skill("obs-init").lower()

    assert "multiple independent services" in content
    assert "manifest paths" in content
    assert "stop before creating" in content
    assert "selected service root" in content


def test_obs_init_uses_template_for_defaults_without_source_audit_steps() -> None:
    content = read_skill("obs-init").lower()

    assert "references/observability-config.yaml" in content
    assert "template" in content and "authoritative" in content
    assert "one concise english line" in content
    assert not has_word(content, "AST")
    assert not has_word(content, "regex")


def test_obs_guide_limits_scope_and_priorities() -> None:
    content = read_skill("obs-guide").lower()

    assert ".observability/config.yaml" in content
    assert "feature" in content and ".sdd/" in content
    assert "one or two" in content
    assert "target function" in content or "target code path" in content
    assert "boilerplate" in content
    assert "do not edit application source" in content


def test_obs_guide_applies_cardinality_and_sanitization_rules() -> None:
    content = read_skill("obs-guide").lower()

    assert "user_id" in content and "email" in content
    assert "account_id" in content and "order_id" in content
    assert "transaction_id" in content
    assert "metric label" in content
    assert "sanitized" in content


def test_config_drives_metric_guardrails_with_an_unconditional_floor() -> None:
    floor = (
        "user_id", "email", "account_id", "order_id", "transaction_id",
        "session_id", "request_id", "ip_address",
    )
    for name in ("obs-guide", "obs-audit", "obs-score"):
        content = read_skill(name).lower()
        assert "guardrails.forbidden_metric_labels" in content, name
        assert all(label in content for label in floor), name

    for name in ("obs-impact", "obs-init"):
        assert "metric label" not in read_skill(name).lower(), name


def test_obs_guide_keeps_instrumentation_guardrails() -> None:
    content = read_skill("obs-guide").lower()

    assert "batchspanprocessor" in content
    assert "fail-silent" in content
    assert "non-blocking" in content
    assert "traceparent" in content and "w3c" in content
    assert "raw request bodies" in content


def test_obs_guide_requires_ast_first_and_qualifies_static_evidence() -> None:
    raw_content = read_skill("obs-guide")
    content = raw_content.lower()

    assert "use an available language-aware ast parser first" in content
    assert has_word(raw_content, "AST")
    assert "if unavailable" in content and "targeted regex/search" in content
    assert "label" in content and "heuristic" in content
    assert "file and line" in content
    assert "yaml alone is not proof" in content
    assert "static evidence is not runtime coverage" in content


def test_obs_audit_requires_source_evidence() -> None:
    content = read_skill("obs-audit")

    assert "source" in content
    assert "yaml" in content and "proof" in content
    assert has_word(content, "AST")


def test_obs_audit_marks_regex_as_heuristic() -> None:
    content = read_skill("obs-audit")

    assert has_word(content, "regex")
    assert "heuristic" in content
    assert "file" in content and "line" in content


def test_obs_audit_checks_async_guardrails() -> None:
    content = read_skill("obs-audit").lower()

    assert "batchspanprocessor" in content
    assert "fail-silent" in content or "fail silent" in content
    assert "non-blocking" in content or "nonblocking" in content
    assert "traceparent" in content and "w3c" in content
    assert "kafka" in content and "rabbitmq" in content and "sqs" in content
    assert "user_id" in content and "transaction_id" in content


def test_obs_audit_caps_sdd_tasks() -> None:
    content = read_skill("obs-audit").lower()

    assert ".sdd/observability/" in content
    assert "sdd-xxx-<feature>.md" in content
    assert "at most two" in content or "no more than two" in content
    assert "acceptance criteria" in content
    assert "duplicate" in content


def test_obs_audit_defines_task_state_and_equivalence() -> None:
    content = read_skill("obs-audit").lower()

    for field in ("status", "category", "scope", "open", "done", "equivalent"):
        assert field in content
    assert "missing or unparseable" in content
    assert "highest existing three-digit sequence" in content
    assert "counting open and done tasks" in content
    assert "mention the skipped duplicate" in content


def test_obs_impact_summary_length_and_business_language() -> None:
    content = read_skill("obs-impact").lower()

    assert "three to five lines" in content or "3 to 5 lines" in content
    assert "customer" in content
    assert "http 5xx" in content
    assert "p95" in content and "slo" in content
    assert "optional `slo` block" in content
    assert "within these same lines" in content
    assert content.count("include no more than one or two prioritized actions") == 0


def test_obs_impact_reports_unknown_without_inputs() -> None:
    content = read_skill("obs-impact").lower()

    assert ".observability/config.yaml" in content
    assert "mttd" in content and "mttr" in content
    assert "affected-user" in content or "affected user" in content
    assert "unavailable" in content
    assert "do not invent" in content or "never invent" in content


def test_obs_impact_requires_matching_user_evidence_for_user_percentages() -> None:
    content = read_skill("obs-impact").lower()

    assert "distinct affected users" in content
    assert "clearly defined affected-user cohort" in content
    assert "and a matching user-population denominator" in content
    assert "same observation window" in content
    assert "request counts do not establish distinct users" in content
    assert "if only request traffic" in content
    assert "report request impact" in content
    assert "mark user impact unavailable" in content


def test_obs_impact_protects_summary_privacy_without_instrumentation_steps() -> None:
    content = read_skill("obs-impact").lower()

    assert "do not list raw telemetry fields" in content
    assert "secrets, credentials, raw request bodies, or unnecessary personal data" in content
    assert "batchspanprocessor" not in content
    assert "traceparent" not in content
    assert "metric label" not in content


def test_obs_score_uses_per_pillar_route_evidence() -> None:
    content = read_skill("obs-score").lower()

    assert "critical route" in content and "denominator" in content
    assert "server span" in content
    assert "counter" in content and "histogram" in content
    assert "structured log" in content and "trace context" in content
    assert "percentage" in content or "%" in content


def test_obs_score_keeps_metric_cardinality_and_output_privacy() -> None:
    content = read_skill("obs-score").lower()

    assert "low-cardinality" in content
    assert "dynamic identifiers" in content
    assert "keep dynamic identifiers out of the scorecard" in content
    assert "raw request bodies" in content
    assert "batchspanprocessor" not in content
    assert "traceparent" not in content


def test_obs_score_reports_unknown_without_routes() -> None:
    content = read_skill("obs-score").lower()

    assert "unknown" in content
    assert "no critical routes" in content or "no routes" in content
    assert "static" in content and "runtime" in content
    assert "do not claim runtime coverage" in content or "never claim runtime coverage" in content


def test_obs_score_route_denominator_is_reproducible() -> None:
    content = read_skill("obs-score")

    assert "critical_routes" in content
    assert "health" in content and "readiness" in content
    assert all(f"**{method}**" in content for method in ("config", "AST", "heuristic"))
    assert "does not count toward the two-action limit" in content
    assert "file:line" in content


def test_service_scoped_skills_handle_child_config_candidates() -> None:
    for name in ("obs-guide", "obs-audit", "obs-score", "obs-impact"):
        content = read_skill(name).lower()
        assert "service root" in content, name
        assert "exactly one child directory" in content, name
        assert "several child directories" in content, name
        assert "audited repository root" not in content, name


def test_installation_documents_all_native_skill_paths() -> None:
    path = ROOT / "docs" / "installation.md"
    assert path.is_file(), "cross-platform installation guide is missing"
    content = path.read_text(encoding="utf-8").lower()

    assert ".opencode/skills/" in content
    assert ".claude/skills/" in content
    assert ".agents/skills/" in content
    assert "copy" in content and "link" in content
    assert "opencode" in content and "claude code" in content and "codex" in content


def test_installation_keeps_documentation_fallback_for_user_level_paths() -> None:
    content = (ROOT / "docs" / "installation.md").read_text(encoding="utf-8").lower()
    for host in ("opencode", "claude code", "codex"):
        start = content.index(f"## {host}")
        next_heading = content.find("\n## ", start + 1)
        section_content = content[start:next_heading if next_heading >= 0 else len(content)]
        assert "user-level" in section_content, host
        assert "documentation" in section_content, host


def test_documentation_does_not_promise_universal_invocation() -> None:
    paths = [ROOT / "README.md", ROOT / "docs" / "installation.md"]
    for path in paths:
        assert path.is_file(), f"documentation is missing: {path.relative_to(ROOT)}"

    content = "\n".join(path.read_text(encoding="utf-8").lower() for path in paths)

    assert "host-specific" in content or "platform-specific" in content
    assert "opencode run obs-init" not in content
    for name in SKILLS:
        assert name in content


def test_sdd_conventions_are_documented_and_linked() -> None:
    conventions = ROOT / "docs" / "sdd-conventions.md"
    assert conventions.is_file()
    content = conventions.read_text(encoding="utf-8").lower()
    assert ".sdd/features/" in content and "title" in content and "description" in content
    assert "sdd-xxx-<feature>.md" in content
    assert "status" in content and "category" in content and "scope" in content
    for path in (ROOT / "README.md", ROOT / "docs" / "installation.md"):
        assert "sdd-conventions.md" in path.read_text(encoding="utf-8").lower()
        assert "specific sdd framework" in path.read_text(encoding="utf-8").lower()


def test_behavior_fixtures_have_expected_outcomes() -> None:
    fixtures = ROOT / "tests" / "fixtures"
    cases = sorted(path for path in fixtures.iterdir() if path.is_dir())
    assert cases
    for case in cases:
        expected = case / "EXPECTED.md"
        assert expected.is_file(), f"missing expected behavior: {case.name}"
        content = expected.read_text(encoding="utf-8").lower()
        assert "obs-" in content, case.name
        assert "expected results:" in content and len(content.split("expected results:", 1)[1].strip()) > 0, case.name


def test_high_cardinality_fixture_covers_configured_label_outside_floor() -> None:
    path = ROOT / "tests" / "fixtures" / "high-cardinality-label" / ".observability" / "config.yaml"
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    configured = config["guardrails"]["forbidden_metric_labels"]
    floor = {
        "user_id", "email", "account_id", "order_id", "transaction_id",
        "session_id", "request_id", "ip_address",
    }
    assert "tenant_code" in configured
    assert not set(configured) & floor


def test_repository_docs_describe_role_specific_guardrails() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8").lower()

    assert "same guardrails" not in readme
    assert "obs-guide" in readme and "obs-impact" in readme
    assert "guardrails specific to its responsibility" in contributing
    assert "obs-audit" in contributing and "obs-score" in contributing
    for content in (readme, contributing):
        assert "fantasy naming" in content and "fantasy-naming" in content
        assert "paraphrases do not activate" in content


def test_all_skills_have_matching_portable_frontmatter() -> None:
    for name in SKILLS:
        metadata = read_frontmatter(name)

        assert metadata["name"] == name
        assert isinstance(metadata["description"], str) and metadata["description"].strip()


def test_instrumentation_skills_keep_shared_telemetry_guardrails() -> None:
    identifiers = ("user_id", "email", "account_id", "order_id", "transaction_id")
    for name in ("obs-guide", "obs-audit"):
        raw_content = read_skill(name)
        content = raw_content.lower()

        assert all(identifier in content for identifier in identifiers), name
        assert "metric label" in content, name
        assert "async" in content and "fail-silent" in content, name
        assert "non-blocking" in content or "nonblocking" in content, name
        assert "batchspanprocessor" in content, name
        assert "traceparent" in content and "w3c" in content, name
        assert has_word(raw_content, "AST") and has_word(content, "regex"), name
        assert "source" in content, name
        assert "one or two" in content, name


def test_shared_output_style_paragraph_is_identical() -> None:
    paragraphs = {
        name: first_paragraph(section(read_skill(name), "Output style"))
        for name in SKILLS
    }

    assert len(set(paragraphs.values())) == 1, paragraphs
    assert "paraphrases do not activate it" in next(iter(paragraphs.values()))


def test_untrusted_content_rule_is_identical() -> None:
    rules = {name: section(read_skill(name), "Untrusted content") for name in SKILLS}

    assert len(set(rules.values())) == 1, rules


def test_each_skill_has_its_character_and_opt_in_phrase() -> None:
    characters = {
        "obs-init": "Cartographer",
        "obs-score": "Cartographer",
        "obs-guide": "Sentinel Guard",
        "obs-audit": "Spectral Inquisitor",
        "obs-impact": "Troubadour",
    }

    for name, character in characters.items():
        content = read_skill(name)
        assert character in content, name
        assert "fantasy naming" in content, name
        assert "fantasy-naming" in content, name
        assert "case-insensitive" in content, name
