#!/usr/bin/env python3
"""Public-safe end-to-end dry-run report for corpus automation gates."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

OBJECT_TYPE = "corpus_public_safe_end_to_end_dry_run"
SCHEMA_VERSION = "corpus_public_safe_end_to_end_dry_run.v1"
REPOSITORY = "Tahjali11/Mythic-Edge-Corpus"
REPOSITORY_URL = "https://github.com/Tahjali11/Mythic-Edge-Corpus"
TARGET_REPOSITORY = "Tahjali11/Mythic-Edge"
TARGET_REPOSITORY_URL = "https://github.com/Tahjali11/Mythic-Edge"

COMPLETE_STATUS = "public_safe_dry_run_complete"
BLOCKED_STATUS = "public_safe_dry_run_blocked"
PACKAGE_VERSION = "0.0.0-preview"
PACKAGE_ROOT = "corpus"
MANIFEST_PATH = "corpus/manifest.v1.json"
SESSION_LEDGER_PATH = "corpus/session_ledger.v1.json"
RELEASE_URL = (
    "https://github.com/Tahjali11/Mythic-Edge-Corpus/releases/"
    "tag/corpus-package-v0.0.0-preview"
)
RECEIVER_CONTRACT_REF = "docs/contracts/mythic_edge_corpus_release_receiver.md"
COMPARISON_SURFACE = "public_safe_parser_summary"

NON_CLAIMS = (
    "not_parser_truth",
    "not_fixture_promotion",
    "not_baseline_approval",
    "not_corpus_readiness",
    "not_release_readiness",
    "not_deploy_readiness",
    "not_production_readiness",
    "not_ratchet_success",
    "not_analytics_truth",
    "not_ai_truth",
    "not_coaching_truth",
    "not_privacy_assurance",
    "not_security_assurance",
    "not_full_corpus_parity",
    "not_external_action",
    "not_mythic_edge_mutation",
)
NO_EXTERNAL_ACTION_GUARDS = {
    "package_artifact_created": False,
    "release_published": False,
    "repository_dispatch_sent": False,
    "ratchet_executed": False,
    "baseline_pr_created": False,
    "baseline_mutated": False,
    "mythic_edge_mutated": False,
    "raw_corpus_imported": False,
    "private_log_read": False,
}

EXPECTED_STAGE_STATUSES = {
    "package_preview": {"preview_report_only"},
    "pr_validation": {"passed_report_only"},
    "release_dry_run": {"release_candidate_report_only"},
    "dispatch_no_send": {"dry_run_payload_ready"},
    "ratchet_report": {
        "comparison_report_ready_for_review",
        "comparison_completed_with_no_deltas",
        "comparison_completed_with_deltas",
    },
    "baseline_proposal": {
        "proposal_preview_ready_for_review",
        "proposal_preview_no_deltas",
        "proposal_preview_degraded",
    },
}

COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SAFE_VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")


def build_public_safe_dry_run_report(
    *,
    repo_root: str | Path | None = None,
    source_commit: str,
    mythic_edge_commit: str,
    package_version: str = PACKAGE_VERSION,
    comparison_results: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a deterministic report-only dry run across corpus automation gates."""

    root = Path.cwd() if repo_root is None else Path(repo_root)
    input_problem = _validate_inputs(
        source_commit=source_commit,
        mythic_edge_commit=mythic_edge_commit,
        package_version=package_version,
    )
    if input_problem:
        return _report(
            status=BLOCKED_STATUS,
            source_commit=_safe_commit(source_commit),
            mythic_edge_commit=_safe_commit(mythic_edge_commit),
            package_version=_safe_version(package_version),
            stages=[],
            blocked_reason_codes=[input_problem],
            release_assets=[],
        )

    preview_mod = _load_tool_module("corpus_package_preview")
    pr_mod = _load_tool_module("corpus_pr_validate_package_safety")
    release_mod = _load_tool_module("corpus_release_package")
    dispatch_mod = _load_tool_module("corpus_repository_dispatch")
    ratchet_mod = _load_tool_module("corpus_ratchet_comparison_report")
    proposal_mod = _load_tool_module("corpus_baseline_pr_proposal")

    preview_report = preview_mod.build_preview(
        package_root=PACKAGE_ROOT,
        manifest_path=MANIFEST_PATH,
        session_ledger_path=SESSION_LEDGER_PATH,
        repo_root=root,
    )
    pr_report = pr_mod.build_validation_report(
        base_ref="origin/main",
        head_ref="HEAD",
        package_root=PACKAGE_ROOT,
        manifest_path=MANIFEST_PATH,
        session_ledger_path=SESSION_LEDGER_PATH,
        repo_root=root,
    )
    release_report = release_mod.build_release_report(
        package_root=PACKAGE_ROOT,
        manifest_path=MANIFEST_PATH,
        session_ledger_path=SESSION_LEDGER_PATH,
        package_version=package_version,
        source_commit=source_commit,
        preview_source_commit=source_commit,
        pr_validation_source_commit=source_commit,
        source_branch="main",
        repo_root=root,
        review_approved=True,
        reviewed_by="codex-c",
        review_ref="issue-20-public-safe-dry-run",
        dry_run=True,
        clean_worktree_confirmed=True,
    )
    expected_checksums = _asset_checksums(release_report)
    dispatch_report = dispatch_mod.build_dispatch_report(
        release_report=release_report,
        payload_only=True,
        send_requested=False,
        expected_asset_checksums=expected_checksums,
    )
    ratchet_report = ratchet_mod.build_ratchet_report(
        release_report=release_report,
        release_url=RELEASE_URL,
        release_metadata_ref="issue-20-release-metadata-ref",
        checksum_ref="issue-20-checksum-ref",
        asset_checksums_verified=True,
        expected_asset_checksums=expected_checksums,
        expected_release_source_commit=source_commit,
        mythic_edge_commit=mythic_edge_commit,
        mythic_edge_comparison_contract_ref=RECEIVER_CONTRACT_REF,
        comparison_surface=COMPARISON_SURFACE,
        comparison_results=list(comparison_results)
        if comparison_results is not None
        else [_matched_expected_output_result(ratchet_mod)],
        validation_refs=["issue-20-public-safe-dry-run"],
    )
    proposal_report = proposal_mod.build_baseline_pr_proposal(
        ratchet_report=ratchet_report,
        ratchet_report_ref="issue-20-ratchet-report",
        package_preview_ref={"status": "passed", "ref": "issue-14-preview"},
        pr_validation_ref={"status": "passed", "ref": "issue-15-pr-validation"},
        release_review_ref={"approved": True, "ref": "issue-16-release-review"},
        dispatch_or_manual_selection_ref={
            "status": "manual_selection_recorded",
            "ref": "issue-20-dispatch-dry-run",
        },
        human_proposal_review_ref={
            "approved": True,
            "ref": "issue-20-human-review-gate",
        },
    )

    stages = [
        _stage("package_preview", preview_report, "status"),
        _stage("pr_validation", pr_report, "status"),
        _stage("release_dry_run", release_report, "status"),
        _stage("dispatch_no_send", dispatch_report, "status"),
        _stage("ratchet_report", ratchet_report, "comparison_status"),
        _stage("baseline_proposal", proposal_report, "proposal_status"),
    ]
    blocked = _blocked_reason_codes(stages)
    return _report(
        status=COMPLETE_STATUS if not blocked else BLOCKED_STATUS,
        source_commit=source_commit,
        mythic_edge_commit=mythic_edge_commit,
        package_version=package_version,
        stages=stages,
        blocked_reason_codes=blocked,
        release_assets=_release_asset_summary(release_report),
    )


def format_text(report: Mapping[str, Any]) -> str:
    """Render a deterministic human-readable dry-run report."""

    lines = [
        "Corpus Public-Safe End-To-End Dry Run",
        f"schema_version: {report['schema_version']}",
        f"status: {report['status']}",
        f"package_version: {report['package_version']}",
        f"source_commit: {report['source_commit']}",
        f"mythic_edge_commit: {report['mythic_edge_commit']}",
        "stages:",
    ]
    lines.extend(
        f"- {stage['name']}: {stage['status']}"
        for stage in report["stages"]
    )
    lines.append("release_assets:")
    if report["release_assets"]:
        lines.extend(
            f"- {asset['asset_name']} | {asset['role']} | "
            f"written={str(asset['written']).lower()} | "
            f"published={str(asset['published']).lower()}"
            for asset in report["release_assets"]
        )
    else:
        lines.append("- none")
    lines.append("blocked_reason_codes:")
    if report["blocked_reason_codes"]:
        lines.extend(f"- {reason}" for reason in report["blocked_reason_codes"])
    else:
        lines.append("- none")
    lines.append("no_external_action_guards:")
    lines.extend(
        f"- {key}: {str(value).lower()}"
        for key, value in sorted(report["no_external_action_guards"].items())
    )
    lines.append("non_claims:")
    lines.extend(f"- {claim}" for claim in report["non_claims"])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the public-safe no-external-action corpus dry run.",
    )
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--mythic-edge-commit", default="0" * 40)
    parser.add_argument("--package-version", default=PACKAGE_VERSION)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    report = build_public_safe_dry_run_report(
        source_commit=args.source_commit,
        mythic_edge_commit=args.mythic_edge_commit,
        package_version=args.package_version,
    )
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report), end="")
    return 0 if report["status"] == COMPLETE_STATUS else 2


def _load_tool_module(name: str) -> Any:
    path = Path(__file__).with_name(f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("tool_module_missing")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _matched_expected_output_result(ratchet_mod: Any) -> dict[str, Any]:
    return {
        "actual_ref": "actual-summary-ref",
        "case_id": "issue-20-public-safe-no-delta",
        "comparison_confidence": "bounded",
        "evidence_status": "observed_public_summary",
        "expected_ref": "expected-summary-ref",
        "family_id": "bootstrap-public-family",
        "freshness": "current_public_release",
        "non_claims": list(ratchet_mod.NON_CLAIMS),
        "reason_codes": [],
        "result_category": "matched_expected_output",
        "review_required": False,
    }


def _stage(
    name: str,
    report: Mapping[str, Any],
    status_field: str,
) -> dict[str, Any]:
    status = str(report.get(status_field) or "invalid")
    return {
        "name": name,
        "object": str(report.get("object") or "invalid"),
        "status": status,
        "expected": status in EXPECTED_STAGE_STATUSES[name],
        "blocked_reason_codes": _string_list(report.get("blocked_reason_codes", [])),
        "external_actions": _external_action_summary(report),
    }


def _blocked_reason_codes(stages: Sequence[Mapping[str, Any]]) -> list[str]:
    reasons: list[str] = []
    for stage in stages:
        if not stage["expected"]:
            reasons.append(f"{stage['name']}_unexpected_status")
        reasons.extend(_string_list(stage.get("blocked_reason_codes", [])))
        for action_name, action_value in stage.get("external_actions", {}).items():
            if action_value:
                reasons.append(f"{stage['name']}_{action_name}_requested")
    return sorted(dict.fromkeys(reasons))


def _external_action_summary(report: Mapping[str, Any]) -> dict[str, bool]:
    keys = set(NO_EXTERNAL_ACTION_GUARDS)
    keys.update(str(key) for key in report.get("no_write_guards", {}))
    keys.update(str(key) for key in report.get("no_send_guards", {}))
    summary: dict[str, bool] = {}
    for key in sorted(keys):
        value = False
        if isinstance(report.get("no_write_guards"), Mapping):
            value = value or bool(report["no_write_guards"].get(key))
        if isinstance(report.get("no_send_guards"), Mapping):
            value = value or bool(report["no_send_guards"].get(key))
        value = value or bool(report.get(key, False))
        summary[key] = value
    return summary


def _asset_checksums(release_report: Mapping[str, Any]) -> dict[str, str]:
    return {
        str(asset["asset_name"]): str(asset["sha256"])
        for asset in release_report.get("planned_assets", [])
        if isinstance(asset, Mapping)
    }


def _release_asset_summary(release_report: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "asset_name": str(asset.get("asset_name")),
            "role": str(asset.get("role")),
            "sha256": str(asset.get("sha256")),
            "written": bool(asset.get("written")),
            "published": bool(asset.get("published")),
        }
        for asset in release_report.get("planned_assets", [])
        if isinstance(asset, Mapping)
    ]


def _report(
    *,
    status: str,
    source_commit: str | None,
    mythic_edge_commit: str | None,
    package_version: str | None,
    stages: list[dict[str, Any]],
    blocked_reason_codes: list[str],
    release_assets: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "object": OBJECT_TYPE,
        "schema_version": SCHEMA_VERSION,
        "repository": REPOSITORY,
        "repository_url": REPOSITORY_URL,
        "target_repository": TARGET_REPOSITORY,
        "target_repository_url": TARGET_REPOSITORY_URL,
        "status": status,
        "package_version": package_version or "invalid",
        "source_commit": source_commit or "invalid",
        "mythic_edge_commit": mythic_edge_commit or "synthetic_no_source_action",
        "stages": stages,
        "release_assets": release_assets,
        "blocked_reason_codes": blocked_reason_codes,
        "no_external_action_guards": dict(NO_EXTERNAL_ACTION_GUARDS),
        "ready_for_external_action": False,
        "ready_for_corpus_readiness_claim": False,
        "non_claims": list(NON_CLAIMS),
    }


def _validate_inputs(
    *,
    source_commit: str,
    mythic_edge_commit: str,
    package_version: str,
) -> str | None:
    if not COMMIT_RE.fullmatch(source_commit):
        return "source_commit_invalid"
    if not COMMIT_RE.fullmatch(mythic_edge_commit):
        return "mythic_edge_commit_invalid"
    if not SAFE_VERSION_RE.fullmatch(package_version):
        return "package_version_invalid"
    return None


def _safe_commit(value: Any) -> str | None:
    return value if isinstance(value, str) and COMMIT_RE.fullmatch(value) else None


def _safe_version(value: Any) -> str | None:
    return value if isinstance(value, str) and SAFE_VERSION_RE.fullmatch(value) else None


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return []
    return [item for item in value if isinstance(item, str)]


if __name__ == "__main__":
    raise SystemExit(main())
