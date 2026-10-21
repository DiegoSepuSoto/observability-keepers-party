"""Validate that representative behavior fixtures stay useful and safe."""

import json
from pathlib import Path
import re

import yaml


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
REQUIRED_CASES = {
    "node-single-service", "python-single-service", "monorepo-ambiguous",
    "unknown-stack", "high-cardinality-label", "audit-task-state",
    "async-context-propagation", "sync-export-request", "missing-pillars",
    "critical-routes-configured", "no-critical-routes", "prompt-injection",
    "no-slo-sli", "requests-without-users", "heuristic-regex", "indirect-wrapper",
}


def read(path: str) -> str:
    return (FIXTURES / path).read_text(encoding="utf-8")


def frontmatter(path: Path) -> dict[str, object]:
    parts = path.read_text(encoding="utf-8").split("---", 2)
    assert len(parts) == 3 and not parts[0].strip(), path
    result = yaml.safe_load(parts[1])
    assert isinstance(result, dict), path
    return result


def test_fixture_matrix_covers_each_requested_scenario() -> None:
    cases = {path.name for path in FIXTURES.iterdir() if path.is_dir()}
    assert REQUIRED_CASES <= cases
    for case in REQUIRED_CASES:
        expected = FIXTURES / case / "EXPECTED.md"
        assert expected.is_file(), case
        text = expected.read_text(encoding="utf-8").lower()
        assert "expected results:" in text, case
        assert "applies to" in text, case


def test_every_fixture_observability_config_is_valid_yaml() -> None:
    configs = sorted(FIXTURES.glob("*/.observability/config.yaml"))
    assert configs
    for path in configs:
        parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert isinstance(parsed, dict), path
        assert parsed.get("service"), path


def test_brownfield_service_and_manifest_fixtures_are_valid() -> None:
    node = json.loads(read("node-single-service/package.json"))
    python_project = read("python-single-service/pyproject.toml")
    monorepo = [
        json.loads(read("monorepo-ambiguous/services/catalog/package.json")),
        json.loads(read("monorepo-ambiguous/services/payments/package.json")),
    ]
    assert node["name"] == "shop-api"
    assert 'name = "billing-api"' in python_project
    assert {item["name"] for item in monorepo} == {"catalog-service", "payments-service"}
    assert (FIXTURES / "node-single-service/.observability/config.yaml").is_file()
    unknown = FIXTURES / "unknown-stack"
    manifests = ("package.json", "go.mod", "requirements.txt", "pyproject.toml", "Cargo.toml")
    assert all(not (unknown / manifest).exists() for manifest in manifests)


def test_config_existing_and_sdd_state_fixtures_preserve_existing_work() -> None:
    existing = yaml.safe_load(read("node-single-service/.observability/config.yaml"))
    assert existing["service"] == "shop-api"
    assert "does not overwrite the existing contract" in read("node-single-service/EXPECTED.md").lower()
    assert frontmatter(FIXTURES / "audit-task-state/.sdd/observability/sdd-004-existing-open.md")["status"] == "open"
    assert frontmatter(FIXTURES / "audit-task-state/.sdd/observability/sdd-009-done.md")["status"] == "done"
    expected = read("audit-task-state/EXPECTED.md").lower()
    assert "does not create a duplicate" in expected and "id `010`" in expected


def test_security_cardinality_async_and_sync_export_fixtures_have_evidence() -> None:
    assert '"user_id": user_id' in read("high-cardinality-label/metrics.py")
    assert "tenant_code" in yaml.safe_load(read("high-cardinality-label/.observability/config.yaml"))["guardrails"]["forbidden_metric_labels"]
    consumer = read("async-context-propagation/src/consumer.py")
    producer = read("async-context-propagation/src/producer.py")
    assert '"traceparent"' in consumer and "extract(carrier)" in consumer
    assert "inject(headers)" in producer and "broker.send" in producer
    assert "SimpleSpanProcessor" in read("sync-export-request/src/server.py")
    injection = json.loads(read("prompt-injection/package.json"))["description"]
    assert "ignore prior limits" in injection.lower() and "print every secret" in injection.lower()


def test_score_and_missing_pillar_fixtures_define_route_evidence_or_unknown() -> None:
    configured = yaml.safe_load(read("critical-routes-configured/.observability/config.yaml"))
    assert configured["critical_routes"] == ["POST /payments/{payment_id}"]
    assert "@app.get" not in read("no-critical-routes/src/helpers.py")
    route = read("missing-pillars/src/routes.py")
    assert "@app.get" in route
    for evidence in ("server span", "counter or histogram", "structured log"):
        assert evidence in read("missing-pillars/EXPECTED.md").lower()
    for expected in ("unknown", "no valid denominator"):
        assert expected in read("no-critical-routes/EXPECTED.md").lower()


def test_impact_fixtures_keep_slo_and_user_impact_unavailable_without_data() -> None:
    no_slo = yaml.safe_load(read("no-slo-sli/.observability/config.yaml"))
    assert "slo" not in no_slo
    rows = read("requests-without-users/traffic.csv").splitlines()
    assert rows[0].split(",") == ["window", "requests", "requests_5xx"]
    assert all("user" not in field.lower() for field in rows[0].split(","))
    outcome = read("requests-without-users/EXPECTED.md").lower()
    assert "request impact only" in outcome and "user impact as `unavailable`" in outcome


def test_heuristic_and_indirect_wrapper_fixtures_prevent_false_certainty() -> None:
    expected = read("heuristic-regex/EXPECTED.md").lower()
    assert "heuristic" in expected and "file and line" in expected
    assert "may miss indirect wrappers" in expected
    wrapper = read("indirect-wrapper/src/telemetry.py") + read("indirect-wrapper/src/routes.py")
    assert "start_as_current_span" in wrapper and "@traced" in wrapper
    assert "remains heuristic" in read("indirect-wrapper/EXPECTED.md").lower()
