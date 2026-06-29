#!/usr/bin/env python3
"""Report-only ratchet comparison validation for reviewed corpus releases."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

OBJECT_TYPE = "corpus_ratchet_comparison_report"
SCHEMA_VERSION = "corpus_ratchet_comparison_report.v1"
RELEASE_OBJECT = "corpus_release_package_dry_run"
RELEASE_SCHEMA_VERSION = "corpus_release_package_dry_run.v1"
RELEASE_READY_STATUS = "release_candidate_report_only"
REPOSITORY = "Tahjali11/Mythic-Edge-Corpus"
REPOSITORY_URL = "https://github.com/Tahjali11/Mythic-Edge-Corpus"
TARGET_REPOSITORY = "Tahjali11/Mythic-Edge"
TARGET_REPOSITORY_URL = "https://github.com/Tahjali11/Mythic-Edge"
RELEASE_CHANNEL = "reviewed"

READY_STATUSES = {
    "comparison_report_ready_for_review",
    "comparison_completed_with_no_deltas",
    "comparison_completed_with_deltas",
}
RESULT_CATEGORIES = {
    "not_evaluated",
    "matched_expected_output",
    "new_pass",
    "new_failure",
    "changed_output",
    "missing_family",
    "missing_case",
    "extra_output",
    "degraded_evidence",
    "unsupported_package",
    "unsupported_parser_surface",
    "checksum_or_integrity_failure",
    "forbidden_content_blocked",
    "not_comparable",
    "review_required",
    "invalid",
}
DELTA_CATEGORIES = {
    "new_pass",
    "new_failure",
    "changed_output",
    "missing_family",
    "missing_case",
    "extra_output",
    "degraded_evidence",
    "unsupported_package",
    "unsupported_parser_surface",
    "checksum_or_integrity_failure",
    "forbidden_content_blocked",
    "not_comparable",
    "review_required",
    "invalid",
}
REQUIRED_RESULT_KEYS = {
    "case_id",
    "family_id",
    "result_category",
    "expected_ref",
    "actual_ref",
    "evidence_status",
    "comparison_confidence",
    "freshness",
    "reason_codes",
    "review_required",
    "non_claims",
}
RELEASE_ASSET_ROLES = {"package_archive", "release_metadata", "checksum_manifest"}
NON_CLAIMS = (
    "not_parser_truth",
    "not_fixture_promotion",
    "not_baseline_approval",
    "not_corpus_readiness",
    "not_release_readiness",
    "not_deploy_readiness",
    "not_production_readiness",
    "not_analytics_truth",
    "not_ai_truth",
    "not_coaching_truth",
    "not_privacy_assurance",
    "not_security_assurance",
    "not_full_corpus_parity",
)
NO_WRITE_GUARDS = {
    "ratchet_executed": False,
    "parser_output_generated": False,
    "baseline_mutated": False,
    "baseline_pr_created": False,
    "repository_dispatch_sent": False,
    "release_published": False,
    "package_artifact_created": False,
    "mythic_edge_mutated": False,
}
RELEASE_NO_WRITE_GUARDS = {
    "package_archive_written": False,
    "release_metadata_written": False,
    "checksum_file_written": False,
    "github_release_created": False,
    "release_asset_uploaded": False,
    "repository_dispatch_sent": False,
    "ratchet_executed": False,
    "baseline_pr_created": False,
    "mythic_edge_mutated": False,
}
RELEASE_METADATA_CHECKSUM_KEYS = {
    "algorithm",
    "asset_name",
    "sha256",
}
PREVIEW_REF_KEYS = {
    "object",
    "schema_version",
    "source_commit",
    "status",
}
PR_VALIDATION_REF_KEYS = {
    "object",
    "schema_version",
    "source_commit",
    "status",
}
REVIEW_REF_KEYS = {
    "approved",
    "ref",
    "reviewed_by",
}
PATH_REF_KEYS = {"path"}
INCLUDED_FILES_SUMMARY_KEYS = {"paths", "total_included_files"}
SAFETY_CHECK_KEYS = {"check", "status"}
RELEASE_REPORT_KEYS = {
    "blocked_reason_codes",
    "dry_run",
    "included_files_summary",
    "manifest_ref",
    "no_write_guards",
    "non_claims",
    "object",
    "package_id",
    "package_preview_ref",
    "package_version",
    "planned_asset_checksums",
    "planned_assets",
    "pr_validation_ref",
    "publish_requested",
    "release_channel",
    "release_metadata",
    "release_name",
    "release_tag",
    "repository",
    "repository_url",
    "review_ref",
    "safety_checks",
    "schema_version",
    "session_ledger_ref",
    "source_branch",
    "source_commit",
    "status",
}
RELEASE_METADATA_KEYS = {
    "asset_checksums",
    "blocked_reason_codes",
    "included_files_summary",
    "manifest_ref",
    "non_claims",
    "object",
    "package_id",
    "package_preview_ref",
    "package_version",
    "pr_validation_ref",
    "release_channel",
    "release_tag",
    "repository",
    "repository_url",
    "review_ref",
    "safety_checks",
    "schema_version",
    "session_ledger_ref",
    "source_branch",
    "source_commit",
}
RELEASE_ASSET_KEYS = {
    "algorithm",
    "asset_name",
    "byte_count",
    "published",
    "role",
    "sha256",
    "written",
}
ALLOWED_ACTION_GUARD_KEYS = set(NO_WRITE_GUARDS) | set(RELEASE_NO_WRITE_GUARDS)

COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9._/@{}:+-]+$")
PACKAGE_VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")
ASSET_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")
GITHUB_RELEASE_URL_RE = re.compile(
    r"^https://github\.com/Tahjali11/Mythic-Edge-Corpus/releases/(?:tag|download)/[A-Za-z0-9._+/-]+$",
)
LOCAL_OR_SECRET_MARKER_RE = re.compile(
    "|".join(
        (
            r"(^|/)(Users|home|var|tmp|private)(/|$)",
            r"(^|[\s\"'])[A-Za-z]:[\\/]",
            re.escape("Player" + ".log"),
            re.escape("UTC" + "_Log"),
            "Bearer" + r"\s+\S+",
            "web" + "hook[_ -]?url",
            r"api[_ -]?" + "key",
            r"\bsec" + "ret" + r"\b",
            r"\bcred" + "ential" + r"s?\b",
            r"\btok" + "en" + r"s?\b",
        )
    ),
    re.IGNORECASE,
)
FORBIDDEN_KEY_RE = re.compile(
    "|".join(
        (
            "raw",
            "private",
            "secret",
            "credential",
            "token",
            "parser_truth",
            "fixture_promotion",
            "baseline_mutation",
            "baseline_pr",
            "repository_dispatch_sent",
            "mythic_edge_mutated",
            "release_published",
            "ratchet_executed",
        )
    ),
    re.IGNORECASE,
)


def build_ratchet_report(
    *,
    release_report: Mapping[str, Any] | None,
    release_url: str | None = None,
    release_metadata_ref: str | None = None,
    checksum_ref: str | None = None,
    asset_checksums_verified: bool = False,
    expected_asset_checksums: Mapping[str, str] | None = None,
    expected_release_source_commit: str | None = None,
    mythic_edge_commit: str = "unknown",
    mythic_edge_comparison_contract_ref: str | None = None,
    comparison_surface: str = "unknown",
    comparison_results: Sequence[Mapping[str, Any]] | None = None,
    validation_refs: Sequence[str] = (),
    ratchet_execution_requested: bool = False,
    baseline_mutation_requested: bool = False,
    baseline_pr_requested: bool = False,
    source_mutation_requested: bool = False,
    release_or_dispatch_requested: bool = False,
) -> dict[str, Any]:
    """Build a public-safe diagnostic report without running ratchets."""

    request_block = _out_of_scope_request_reason(
        ratchet_execution_requested=ratchet_execution_requested,
        baseline_mutation_requested=baseline_mutation_requested,
        baseline_pr_requested=baseline_pr_requested,
        source_mutation_requested=source_mutation_requested,
        release_or_dispatch_requested=release_or_dispatch_requested,
    )
    if request_block:
        return _blocked_report(status=request_block[0], reason=request_block[1])
    if release_report is None:
        return _blocked_report(status="blocked_missing_release", reason="missing_release_metadata")

    public_safety_reason = _public_safety_reason(release_report)
    if public_safety_reason:
        return _blocked_report(status="blocked_forbidden_content", reason=public_safety_reason)

    release_problem = _validate_release_report(release_report)
    if release_problem:
        return _blocked_report(status=_release_problem_status(release_problem), reason=release_problem)

    if expected_release_source_commit and release_report.get("source_commit") != expected_release_source_commit:
        return _base_report(
            status="review_required",
            release_report=release_report,
            release_url=release_url,
            release_metadata_ref=release_metadata_ref,
            checksum_ref=checksum_ref,
            asset_checksums_verified=asset_checksums_verified,
            mythic_edge_commit=mythic_edge_commit,
            mythic_edge_comparison_contract_ref=mythic_edge_comparison_contract_ref,
            comparison_surface=comparison_surface,
            results=[],
            blocked_reason_codes=["source_commit_mismatch"],
            validation_refs=validation_refs,
        )

    checksum_problem = _validate_release_integrity(
        release_report,
        release_url=release_url,
        release_metadata_ref=release_metadata_ref,
        checksum_ref=checksum_ref,
        asset_checksums_verified=asset_checksums_verified,
        expected_asset_checksums=expected_asset_checksums or {},
    )
    if checksum_problem:
        return _blocked_report(
            status=_release_problem_status(checksum_problem),
            reason=checksum_problem,
            release_report=release_report,
            release_url=release_url,
            release_metadata_ref=release_metadata_ref,
            checksum_ref=checksum_ref,
            asset_checksums_verified=asset_checksums_verified,
            mythic_edge_commit=mythic_edge_commit,
            mythic_edge_comparison_contract_ref=mythic_edge_comparison_contract_ref,
            comparison_surface=comparison_surface,
            validation_refs=validation_refs,
        )

    if not _is_public_ref(mythic_edge_comparison_contract_ref):
        return _blocked_report(
            status="blocked_missing_receiver_contract",
            reason="missing_receiver_contract",
            release_report=release_report,
            release_url=release_url,
            release_metadata_ref=release_metadata_ref,
            checksum_ref=checksum_ref,
            asset_checksums_verified=asset_checksums_verified,
            mythic_edge_commit=mythic_edge_commit,
            comparison_surface=comparison_surface,
            validation_refs=validation_refs,
        )
    if not _is_public_ref(comparison_surface) or comparison_surface == "unknown":
        return _blocked_report(
            status="blocked_missing_parser_surface",
            reason="missing_parser_comparison_surface",
            release_report=release_report,
            release_url=release_url,
            release_metadata_ref=release_metadata_ref,
            checksum_ref=checksum_ref,
            asset_checksums_verified=asset_checksums_verified,
            mythic_edge_commit=mythic_edge_commit,
            mythic_edge_comparison_contract_ref=mythic_edge_comparison_contract_ref,
            comparison_surface=comparison_surface,
            validation_refs=validation_refs,
        )
    if mythic_edge_commit != "unknown" and not _is_commit(mythic_edge_commit):
        return _blocked_report(status="invalid", reason="mythic_edge_commit_invalid")

    result_problem = _validate_results(comparison_results)
    if result_problem:
        status = "blocked_forbidden_content" if result_problem == "payload_or_metadata_contains_forbidden_content" else "invalid"
        return _blocked_report(
            status=status,
            reason=result_problem,
            release_report=release_report,
            release_url=release_url,
            release_metadata_ref=release_metadata_ref,
            checksum_ref=checksum_ref,
            asset_checksums_verified=asset_checksums_verified,
            mythic_edge_commit=mythic_edge_commit,
            mythic_edge_comparison_contract_ref=mythic_edge_comparison_contract_ref,
            comparison_surface=comparison_surface,
            validation_refs=validation_refs,
        )

    results = [_sanitize_result(result) for result in comparison_results or ()]
    if not results:
        status = "review_required"
        blocked_reason_codes = ["comparison_output_missing"]
    elif any(result["result_category"] in DELTA_CATEGORIES or result["review_required"] for result in results):
        status = "comparison_completed_with_deltas"
        blocked_reason_codes = []
    else:
        status = "comparison_completed_with_no_deltas"
        blocked_reason_codes = []

    return _base_report(
        status=status,
        release_report=release_report,
        release_url=release_url,
        release_metadata_ref=release_metadata_ref,
        checksum_ref=checksum_ref,
        asset_checksums_verified=asset_checksums_verified,
        mythic_edge_commit=mythic_edge_commit,
        mythic_edge_comparison_contract_ref=mythic_edge_comparison_contract_ref,
        comparison_surface=comparison_surface,
        results=results,
        blocked_reason_codes=blocked_reason_codes,
        validation_refs=validation_refs,
    )


def validate_ratchet_report(report: Mapping[str, Any]) -> list[str]:
    """Return symbolic validation reason codes for a ratchet report."""

    if not isinstance(report, Mapping):
        return ["report_schema_invalid"]
    public_safety_reason = _public_safety_reason(report)
    if public_safety_reason:
        return [public_safety_reason]
    required_keys = {
        "asset_checksums_verified",
        "blocked_reason_codes",
        "checksum_ref",
        "comparison_status",
        "comparison_surface",
        "completed_at_utc",
        "mythic_edge_commit",
        "mythic_edge_comparison_contract_ref",
        "no_write_guards",
        "non_claims",
        "object",
        "package_id",
        "package_version",
        "release_channel",
        "release_metadata_ref",
        "release_source_commit",
        "release_tag",
        "release_url",
        "report_id",
        "results",
        "schema_version",
        "source_repository",
        "source_repository_url",
        "started_at_utc",
        "summary",
        "target_repository",
        "target_repository_url",
        "validation_refs",
    }
    if set(report) != required_keys:
        return ["report_schema_invalid"]
    if report.get("object") != OBJECT_TYPE or report.get("schema_version") != SCHEMA_VERSION:
        return ["report_schema_invalid"]
    if report.get("source_repository") != REPOSITORY or report.get("source_repository_url") != REPOSITORY_URL:
        return ["report_schema_invalid"]
    if report.get("target_repository") != TARGET_REPOSITORY or report.get("target_repository_url") != TARGET_REPOSITORY_URL:
        return ["report_schema_invalid"]
    if report.get("comparison_status") not in _known_statuses():
        return ["report_schema_invalid"]
    if not isinstance(report.get("asset_checksums_verified"), bool):
        return ["report_schema_invalid"]
    if report.get("non_claims") != list(NON_CLAIMS):
        return ["report_schema_invalid"]
    if report.get("no_write_guards") != NO_WRITE_GUARDS:
        return ["report_schema_invalid"]
    if not isinstance(report.get("blocked_reason_codes"), list) or not all(
        _is_reason_code(item) for item in report["blocked_reason_codes"]
    ):
        return ["report_schema_invalid"]
    if not isinstance(report.get("results"), list):
        return ["report_schema_invalid"]
    result_problem = _validate_results(report["results"])
    if result_problem:
        return [result_problem]
    if not _summary_matches(report.get("summary"), report["results"]):
        return ["report_schema_invalid"]
    return []


def format_text(report: Mapping[str, Any]) -> str:
    """Render a deterministic text summary."""

    lines = [
        "Corpus Ratchet Comparison Report",
        f"schema_version: {report['schema_version']}",
        f"status: {report['comparison_status']}",
        f"package_version: {report.get('package_version') or 'unknown'}",
        f"release_tag: {report.get('release_tag') or 'unknown'}",
        f"release_source_commit: {report.get('release_source_commit') or 'unknown'}",
        f"mythic_edge_commit: {report.get('mythic_edge_commit') or 'unknown'}",
        f"total_cases: {report['summary']['total_cases']}",
        "blocked_reason_codes:",
    ]
    if report["blocked_reason_codes"]:
        lines.extend(f"- {reason}" for reason in report["blocked_reason_codes"])
    else:
        lines.append("- none")
    lines.append("no_write_guards:")
    lines.extend(f"- {key}: {str(value).lower()}" for key, value in sorted(report["no_write_guards"].items()))
    lines.append("non_claims:")
    lines.extend(f"- {claim}" for claim in report["non_claims"])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a public-safe corpus ratchet comparison report.")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--report", required=True)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    if not args.validate_only:
        report = _blocked_report(status="unsupported", reason="validate_only_required")
    else:
        try:
            report = _load_report(args.report)
        except ValueError as exc:
            report = _blocked_report(status="invalid", reason=str(exc))
        else:
            problems = validate_ratchet_report(report)
            if problems:
                report = _blocked_report(status="invalid", reason=problems[0])

    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report), end="")
    return 0 if report["comparison_status"] in READY_STATUSES else 2


def _out_of_scope_request_reason(
    *,
    ratchet_execution_requested: bool,
    baseline_mutation_requested: bool,
    baseline_pr_requested: bool,
    source_mutation_requested: bool,
    release_or_dispatch_requested: bool,
) -> tuple[str, str] | None:
    if ratchet_execution_requested:
        return ("unsupported", "ratchet_execution_requested")
    if baseline_mutation_requested:
        return ("blocked_baseline_mutation_requested", "baseline_mutation_requested")
    if baseline_pr_requested:
        return ("blocked_baseline_pr_requested", "baseline_pr_requested")
    if source_mutation_requested:
        return ("blocked_source_mutation_requested", "source_mutation_requested")
    if release_or_dispatch_requested:
        return ("blocked_release_or_dispatch_requested", "release_or_dispatch_requested")
    return None


def _validate_release_report(report: Mapping[str, Any]) -> str | None:
    if report.get("object") != RELEASE_OBJECT or report.get("schema_version") != RELEASE_SCHEMA_VERSION:
        return "missing_release_metadata"
    if report.get("status") != RELEASE_READY_STATUS:
        return "missing_release_metadata"
    if set(report) != RELEASE_REPORT_KEYS:
        return "report_schema_invalid"
    if report.get("dry_run") is not True or report.get("publish_requested") is not False:
        return "release_or_dispatch_requested"
    if report.get("repository") != REPOSITORY or report.get("repository_url") != REPOSITORY_URL:
        return "unsupported_package_schema"
    version = report.get("package_version")
    if not _is_package_version(version):
        return "package_version_mismatch"
    if report.get("release_tag") != _release_tag(str(version)):
        return "release_tag_mismatch"
    if report.get("release_channel") != RELEASE_CHANNEL:
        return "unsupported_release_channel"
    if not _is_commit(report.get("source_commit")):
        return "source_commit_mismatch"
    if report.get("blocked_reason_codes") != []:
        return "missing_release_metadata"
    guard_problem = _validate_release_no_write_guards(report.get("no_write_guards"))
    if guard_problem:
        return guard_problem
    if not _safe_non_claims(report.get("non_claims")):
        return "report_schema_invalid"
    assets_problem = _validate_release_assets(report.get("planned_assets"), package_version=str(version))
    if assets_problem:
        return assets_problem
    release_metadata = report.get("release_metadata")
    if not isinstance(release_metadata, Mapping):
        return "missing_release_metadata"
    if set(release_metadata) != RELEASE_METADATA_KEYS:
        return "report_schema_invalid"
    if release_metadata.get("object") != "corpus_release_package_metadata":
        return "missing_release_metadata"
    if release_metadata.get("schema_version") != "corpus_release_package_metadata.v1":
        return "unsupported_package_schema"
    if release_metadata.get("repository") != REPOSITORY or release_metadata.get("repository_url") != REPOSITORY_URL:
        return "unsupported_package_schema"
    if release_metadata.get("package_version") != version or release_metadata.get("release_tag") != report.get("release_tag"):
        return "package_version_mismatch"
    if release_metadata.get("source_commit") != report.get("source_commit"):
        return "source_commit_mismatch"
    if release_metadata.get("release_channel") != RELEASE_CHANNEL:
        return "unsupported_release_channel"
    evidence_problem = _validate_release_evidence_refs(report, release_metadata=release_metadata)
    if evidence_problem:
        return evidence_problem
    summary_problem = _validate_release_summary_and_safety(report, release_metadata=release_metadata)
    if summary_problem:
        return summary_problem
    if not _safe_non_claims(release_metadata.get("non_claims")):
        return "report_schema_invalid"
    checksum_problem = _validate_release_metadata_checksums(
        release_metadata.get("asset_checksums"),
        required_checksums=_non_self_referential_asset_checksums(report.get("planned_assets")),
    )
    if checksum_problem:
        return checksum_problem
    checksum_problem = _validate_release_metadata_checksums(
        report.get("planned_asset_checksums"),
        required_checksums=_planned_asset_checksums(report.get("planned_assets")),
    )
    if checksum_problem:
        return checksum_problem
    return None


def _validate_release_integrity(
    release_report: Mapping[str, Any],
    *,
    release_url: str | None,
    release_metadata_ref: str | None,
    checksum_ref: str | None,
    asset_checksums_verified: bool,
    expected_asset_checksums: Mapping[str, str],
) -> str | None:
    if not _is_github_release_url(release_url):
        return "missing_package_asset"
    if not _is_public_ref(release_metadata_ref):
        return "missing_release_metadata"
    if not _is_public_ref(checksum_ref):
        return "missing_checksum_asset"
    if asset_checksums_verified is not True:
        return "checksum_mismatch"
    planned = _planned_asset_checksums(release_report.get("planned_assets"))
    expected_problem = _validate_expected_asset_checksums(
        expected_asset_checksums,
        required_checksums=planned,
    )
    if expected_problem:
        return expected_problem
    return None


def _validate_release_assets(value: Any, *, package_version: str) -> str | None:
    if not isinstance(value, list):
        return "missing_package_asset"
    roles: set[str] = set()
    expected_names = _release_asset_names(package_version)
    for item in value:
        if not isinstance(item, Mapping):
            return "unsupported_package_schema"
        if _public_safety_reason(item):
            return "payload_or_metadata_contains_forbidden_content"
        if set(item) != RELEASE_ASSET_KEYS:
            return "report_schema_invalid"
        role = item.get("role")
        if role not in RELEASE_ASSET_ROLES or role in roles:
            return "missing_package_asset"
        roles.add(str(role))
        if item.get("algorithm") != "sha256" or not _is_sha256(item.get("sha256")):
            return "checksum_mismatch"
        if not _is_asset_name(item.get("asset_name")) or item.get("asset_name") != expected_names.get(str(role)):
            return "missing_package_asset"
        if item.get("written") is not False or item.get("published") is not False:
            return "release_or_dispatch_requested"
    if roles != RELEASE_ASSET_ROLES:
        return "missing_package_asset"
    return None


def _validate_results(results: Sequence[Mapping[str, Any]] | Any) -> str | None:
    if results is None:
        return None
    if not isinstance(results, Sequence) or isinstance(results, (str, bytes)):
        return "comparison_output_invalid"
    for result in results:
        if not isinstance(result, Mapping):
            return "comparison_output_invalid"
        if _public_safety_reason(result):
            return "payload_or_metadata_contains_forbidden_content"
        if set(result) != REQUIRED_RESULT_KEYS:
            return "comparison_output_invalid"
        if result.get("result_category") not in RESULT_CATEGORIES:
            return "comparison_output_invalid"
        if not _is_public_ref(result.get("case_id")) or not _is_public_ref(result.get("family_id")):
            return "comparison_output_invalid"
        if not _is_public_ref(result.get("expected_ref")):
            return "comparison_output_invalid"
        actual_ref = result.get("actual_ref")
        if actual_ref != "missing" and not _is_public_ref(actual_ref):
            return "comparison_output_invalid"
        if not _is_public_ref(result.get("evidence_status")):
            return "comparison_output_invalid"
        if not _is_public_ref(result.get("comparison_confidence")):
            return "comparison_output_invalid"
        if not _is_public_ref(result.get("freshness")):
            return "comparison_output_invalid"
        if not isinstance(result.get("review_required"), bool):
            return "comparison_output_invalid"
        if not _safe_reason_codes(result.get("reason_codes")):
            return "comparison_output_invalid"
        if result.get("non_claims") != list(NON_CLAIMS):
            return "comparison_output_invalid"
    return None


def _sanitize_result(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "actual_ref": str(result["actual_ref"]),
        "case_id": str(result["case_id"]),
        "comparison_confidence": str(result["comparison_confidence"]),
        "evidence_status": str(result["evidence_status"]),
        "expected_ref": str(result["expected_ref"]),
        "family_id": str(result["family_id"]),
        "freshness": str(result["freshness"]),
        "non_claims": list(NON_CLAIMS),
        "reason_codes": sorted(str(item) for item in result["reason_codes"]),
        "result_category": str(result["result_category"]),
        "review_required": bool(result["review_required"]),
    }


def _base_report(
    *,
    status: str,
    release_report: Mapping[str, Any],
    release_url: str | None,
    release_metadata_ref: str | None,
    checksum_ref: str | None,
    asset_checksums_verified: bool,
    mythic_edge_commit: str,
    mythic_edge_comparison_contract_ref: str | None,
    comparison_surface: str,
    results: list[dict[str, Any]],
    blocked_reason_codes: Sequence[str],
    validation_refs: Sequence[str],
) -> dict[str, Any]:
    package_version = _safe_value(release_report.get("package_version")) or "unknown"
    release_tag = _safe_value(release_report.get("release_tag")) or "unknown"
    source_commit = _safe_value(release_report.get("source_commit")) or "unknown"
    return {
        "asset_checksums_verified": asset_checksums_verified is True,
        "blocked_reason_codes": sorted(str(reason) for reason in blocked_reason_codes),
        "checksum_ref": _safe_value(checksum_ref) or "missing",
        "comparison_status": status,
        "comparison_surface": _safe_value(comparison_surface) or "unknown",
        "completed_at_utc": "omitted",
        "mythic_edge_commit": _safe_value(mythic_edge_commit) or "unknown",
        "mythic_edge_comparison_contract_ref": _safe_value(mythic_edge_comparison_contract_ref) or "missing",
        "no_write_guards": dict(NO_WRITE_GUARDS),
        "non_claims": list(NON_CLAIMS),
        "object": OBJECT_TYPE,
        "package_id": _safe_value(release_report.get("package_id")) or "unknown",
        "package_version": package_version,
        "release_channel": _safe_value(release_report.get("release_channel")) or "unknown",
        "release_metadata_ref": _safe_value(release_metadata_ref) or "missing",
        "release_source_commit": source_commit,
        "release_tag": release_tag,
        "release_url": _safe_value(release_url) or "missing",
        "report_id": f"ratchet-comparison-{package_version}",
        "results": results,
        "schema_version": SCHEMA_VERSION,
        "source_repository": REPOSITORY,
        "source_repository_url": REPOSITORY_URL,
        "started_at_utc": "omitted",
        "summary": _summary(results),
        "target_repository": TARGET_REPOSITORY,
        "target_repository_url": TARGET_REPOSITORY_URL,
        "validation_refs": [_safe_value(ref) for ref in validation_refs if _is_public_ref(ref)],
    }


def _blocked_report(
    *,
    status: str,
    reason: str,
    release_report: Mapping[str, Any] | None = None,
    release_url: str | None = None,
    release_metadata_ref: str | None = None,
    checksum_ref: str | None = None,
    asset_checksums_verified: bool = False,
    mythic_edge_commit: str = "unknown",
    mythic_edge_comparison_contract_ref: str | None = None,
    comparison_surface: str = "unknown",
    validation_refs: Sequence[str] = (),
) -> dict[str, Any]:
    safe_release = release_report if isinstance(release_report, Mapping) else {}
    return _base_report(
        status=status,
        release_report=safe_release,
        release_url=release_url,
        release_metadata_ref=release_metadata_ref,
        checksum_ref=checksum_ref,
        asset_checksums_verified=asset_checksums_verified,
        mythic_edge_commit=mythic_edge_commit,
        mythic_edge_comparison_contract_ref=mythic_edge_comparison_contract_ref,
        comparison_surface=comparison_surface,
        results=[],
        blocked_reason_codes=[reason],
        validation_refs=validation_refs,
    )


def _summary(results: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    counts = Counter(str(result["result_category"]) for result in results)
    return {
        "changed_outputs": counts["changed_output"],
        "degraded_evidence": counts["degraded_evidence"],
        "matched_expected_output": counts["matched_expected_output"],
        "missing_cases": counts["missing_case"],
        "missing_families": counts["missing_family"],
        "new_failures": counts["new_failure"],
        "new_passes": counts["new_pass"],
        "review_required": sum(1 for result in results if bool(result["review_required"])),
        "total_cases": len(results),
        "unsupported": counts["unsupported_package"] + counts["unsupported_parser_surface"],
    }


def _summary_matches(summary: Any, results: Sequence[Mapping[str, Any]]) -> bool:
    return isinstance(summary, Mapping) and dict(summary) == _summary(results)


def _release_problem_status(reason: str) -> str:
    return {
        "missing_release_metadata": "blocked_missing_release_metadata",
        "missing_package_asset": "blocked_missing_release",
        "missing_checksum_asset": "blocked_missing_checksum",
        "checksum_mismatch": "blocked_checksum_mismatch",
        "unsupported_package_schema": "blocked_unsupported_package",
        "unsupported_release_channel": "blocked_unsupported_package",
        "payload_or_metadata_contains_forbidden_content": "blocked_forbidden_content",
        "source_mutation_requested": "blocked_source_mutation_requested",
        "release_or_dispatch_requested": "blocked_release_or_dispatch_requested",
        "missing_predecessor_preview_evidence": "blocked_missing_release_metadata",
        "missing_predecessor_pr_validation_evidence": "blocked_missing_release_metadata",
        "missing_human_review": "blocked_missing_release_metadata",
    }.get(reason, "invalid")


def _known_statuses() -> set[str]:
    return {
        "blocked_missing_release",
        "blocked_missing_release_metadata",
        "blocked_missing_checksum",
        "blocked_checksum_mismatch",
        "blocked_unsupported_package",
        "blocked_missing_receiver_contract",
        "blocked_missing_parser_surface",
        "blocked_forbidden_content",
        "blocked_private_input",
        "blocked_baseline_mutation_requested",
        "blocked_baseline_pr_requested",
        "blocked_source_mutation_requested",
        "blocked_release_or_dispatch_requested",
        "comparison_report_ready_for_review",
        "comparison_completed_with_no_deltas",
        "comparison_completed_with_deltas",
        "review_required",
        "unsupported",
        "invalid",
    }


def _load_report(report_path: str | Path) -> dict[str, Any]:
    safe_path = _clean_repo_relative_path(report_path)
    path = Path.cwd() / safe_path
    if not path.exists() or not path.is_file():
        raise ValueError("report_missing")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("report_schema_invalid") from exc
    if not isinstance(data, Mapping):
        raise ValueError("report_schema_invalid")
    return dict(data)


def _clean_repo_relative_path(value: str | Path) -> Path:
    raw = str(value)
    if _public_safety_reason(raw):
        raise ValueError("payload_or_metadata_contains_forbidden_content")
    path = Path(raw)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("payload_or_metadata_contains_forbidden_content")
    return path


def _planned_asset_checksums(value: Any) -> dict[str, str]:
    if not isinstance(value, list):
        return {}
    checksums: dict[str, str] = {}
    for item in value:
        if isinstance(item, Mapping) and _is_asset_name(item.get("asset_name")) and _is_sha256(item.get("sha256")):
            checksums[str(item["asset_name"])] = str(item["sha256"])
    return checksums


def _non_self_referential_asset_checksums(value: Any) -> dict[str, str]:
    if not isinstance(value, list):
        return {}
    checksums: dict[str, str] = {}
    for item in value:
        if (
            isinstance(item, Mapping)
            and item.get("role") == "package_archive"
            and _is_asset_name(item.get("asset_name"))
            and _is_sha256(item.get("sha256"))
        ):
            checksums[str(item["asset_name"])] = str(item["sha256"])
    return checksums


def _validate_release_no_write_guards(value: Any) -> str | None:
    if not isinstance(value, Mapping):
        return "report_schema_invalid"
    if set(value) != set(RELEASE_NO_WRITE_GUARDS):
        return "report_schema_invalid"
    if not all(isinstance(item, bool) for item in value.values()):
        return "report_schema_invalid"
    if value != RELEASE_NO_WRITE_GUARDS:
        return "source_mutation_requested"
    return None


def _validate_release_evidence_refs(report: Mapping[str, Any], *, release_metadata: Mapping[str, Any]) -> str | None:
    source_commit = report.get("source_commit")
    for key in (
        "package_preview_ref",
        "pr_validation_ref",
        "review_ref",
        "manifest_ref",
        "session_ledger_ref",
    ):
        if report.get(key) != release_metadata.get(key):
            return _evidence_ref_reason(key)

    preview_problem = _validate_preview_ref(report.get("package_preview_ref"), source_commit=source_commit)
    if preview_problem:
        return preview_problem
    pr_validation_problem = _validate_pr_validation_ref(report.get("pr_validation_ref"), source_commit=source_commit)
    if pr_validation_problem:
        return pr_validation_problem
    review_problem = _validate_review_ref(report.get("review_ref"))
    if review_problem:
        return review_problem
    for key in ("manifest_ref", "session_ledger_ref"):
        if not _valid_path_ref(report.get(key)):
            return "missing_release_metadata"
    return None


def _validate_preview_ref(value: Any, *, source_commit: Any) -> str | None:
    if not isinstance(value, Mapping) or set(value) != PREVIEW_REF_KEYS:
        return "missing_predecessor_preview_evidence"
    if (
        value.get("object") != "corpus_local_package_preview"
        or value.get("schema_version") != "corpus_local_package_preview.v1"
        or value.get("status") != "preview_report_only"
        or value.get("source_commit") != source_commit
        or not _is_commit(value.get("source_commit"))
    ):
        return "missing_predecessor_preview_evidence"
    return None


def _validate_pr_validation_ref(value: Any, *, source_commit: Any) -> str | None:
    if not isinstance(value, Mapping) or set(value) != PR_VALIDATION_REF_KEYS:
        return "missing_predecessor_pr_validation_evidence"
    if (
        value.get("object") != "corpus_pr_validation_package_safety"
        or value.get("schema_version") != "corpus_pr_validation_package_safety.v1"
        or value.get("status") != "passed_report_only"
        or value.get("source_commit") != source_commit
        or not _is_commit(value.get("source_commit"))
    ):
        return "missing_predecessor_pr_validation_evidence"
    return None


def _validate_review_ref(value: Any) -> str | None:
    if not isinstance(value, Mapping) or set(value) != REVIEW_REF_KEYS:
        return "missing_human_review"
    if value.get("approved") is not True:
        return "missing_human_review"
    if not _is_public_ref(value.get("reviewed_by")) or not _is_public_ref(value.get("ref")):
        return "missing_human_review"
    return None


def _valid_path_ref(value: Any) -> bool:
    if not isinstance(value, Mapping) or set(value) != PATH_REF_KEYS:
        return False
    return _valid_repo_relative_path_text(value.get("path"))


def _validate_release_summary_and_safety(
    report: Mapping[str, Any],
    *,
    release_metadata: Mapping[str, Any],
) -> str | None:
    if report.get("included_files_summary") != release_metadata.get("included_files_summary"):
        return "missing_release_metadata"
    if not _valid_included_files_summary(report.get("included_files_summary")):
        return "missing_release_metadata"
    if report.get("safety_checks") != release_metadata.get("safety_checks"):
        return "missing_release_metadata"
    if not _valid_safety_checks(report.get("safety_checks")):
        return "missing_release_metadata"
    return None


def _valid_included_files_summary(value: Any) -> bool:
    if not isinstance(value, Mapping) or set(value) != INCLUDED_FILES_SUMMARY_KEYS:
        return False
    paths = value.get("paths")
    total = value.get("total_included_files")
    if isinstance(total, bool) or not isinstance(total, int) or total <= 0:
        return False
    if not isinstance(paths, list) or not paths or len(paths) != total:
        return False
    return all(_valid_repo_relative_path_text(path) for path in paths)


def _valid_safety_checks(value: Any) -> bool:
    if not isinstance(value, list) or not value:
        return False
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, Mapping) or set(item) != SAFETY_CHECK_KEYS:
            return False
        check = item.get("check")
        if not _is_public_ref(check) or str(check) in seen:
            return False
        seen.add(str(check))
        if item.get("status") != "passed":
            return False
    return True


def _valid_repo_relative_path_text(value: Any) -> bool:
    if not _is_public_ref(value):
        return False
    path_text = str(value).replace("\\", "/")
    if path_text.startswith(("/", "_review_", "data/")):
        return False
    if ":" in path_text:
        return False
    parts = path_text.split("/")
    return not any(part in {"", ".", ".."} for part in parts)


def _evidence_ref_reason(key: str) -> str:
    return {
        "package_preview_ref": "missing_predecessor_preview_evidence",
        "pr_validation_ref": "missing_predecessor_pr_validation_evidence",
        "review_ref": "missing_human_review",
    }.get(key, "missing_release_metadata")

def _validate_release_metadata_checksums(value: Any, *, required_checksums: Mapping[str, str]) -> str | None:
    if not isinstance(value, list) or not value:
        return "missing_checksum_asset"
    checksums: dict[str, str] = {}
    for item in value:
        if not isinstance(item, Mapping):
            return "checksum_mismatch"
        if _public_safety_reason(item):
            return "payload_or_metadata_contains_forbidden_content"
        if set(item) != RELEASE_METADATA_CHECKSUM_KEYS:
            return "report_schema_invalid"
        asset_name = item.get("asset_name")
        sha256 = item.get("sha256")
        if not _is_asset_name(asset_name):
            return "missing_package_asset"
        if item.get("algorithm") != "sha256" or not _is_sha256(sha256):
            return "checksum_mismatch"
        if str(asset_name) in checksums:
            return "checksum_mismatch"
        checksums[str(asset_name)] = str(sha256)
    if checksums != dict(required_checksums):
        return "checksum_mismatch"
    return None


def _validate_expected_asset_checksums(value: Any, *, required_checksums: Mapping[str, str]) -> str | None:
    if not isinstance(value, Mapping) or not value:
        return "missing_checksum_asset"
    checksums: dict[str, str] = {}
    for asset_name, sha256 in value.items():
        if not _is_asset_name(asset_name):
            return "missing_package_asset"
        if not _is_sha256(sha256):
            return "checksum_mismatch"
        checksums[str(asset_name)] = str(sha256)
    if checksums != dict(required_checksums):
        return "checksum_mismatch"
    return None


def _public_safety_reason(value: Any) -> str | None:
    for item in _strings_from(value):
        if LOCAL_OR_SECRET_MARKER_RE.search(item):
            return "payload_or_metadata_contains_forbidden_content"
    if isinstance(value, Mapping):
        for key in value:
            if isinstance(key, str) and key not in ALLOWED_ACTION_GUARD_KEYS and FORBIDDEN_KEY_RE.search(key):
                return "payload_or_metadata_contains_forbidden_content"
    return None


def _strings_from(value: Any) -> list[str]:
    strings: list[str] = []
    if isinstance(value, str):
        strings.append(value)
    elif isinstance(value, Mapping):
        for key, item in value.items():
            if isinstance(key, str):
                strings.append(key)
            strings.extend(_strings_from(item))
    elif isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        for item in value:
            strings.extend(_strings_from(item))
    return strings


def _bool_values(value: Any) -> list[bool]:
    if isinstance(value, bool):
        return [value]
    if isinstance(value, Mapping):
        result: list[bool] = []
        for item in value.values():
            result.extend(_bool_values(item))
        return result
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        result: list[bool] = []
        for item in value:
            result.extend(_bool_values(item))
        return result
    return []


def _safe_value(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    if _public_safety_reason(value):
        return None
    return value


def _safe_non_claims(value: Any) -> bool:
    return isinstance(value, list) and all(_is_public_ref(item) for item in value)


def _safe_reason_codes(value: Any) -> bool:
    return isinstance(value, list) and all(_is_reason_code(item) for item in value)


def _is_reason_code(value: Any) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"[a-z0-9_]+", value))


def _is_public_ref(value: Any) -> bool:
    return isinstance(value, str) and bool(SAFE_ID_RE.fullmatch(value)) and not _public_safety_reason(value)


def _is_asset_name(value: Any) -> bool:
    return isinstance(value, str) and bool(ASSET_NAME_RE.fullmatch(value)) and not _public_safety_reason(value)


def _is_package_version(value: Any) -> bool:
    return isinstance(value, str) and bool(PACKAGE_VERSION_RE.fullmatch(value))


def _is_commit(value: Any) -> bool:
    return isinstance(value, str) and bool(COMMIT_RE.fullmatch(value))


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and bool(SHA256_RE.fullmatch(value))


def _is_github_release_url(value: Any) -> bool:
    return isinstance(value, str) and bool(GITHUB_RELEASE_URL_RE.fullmatch(value))


def _release_tag(package_version: str) -> str:
    return f"corpus-package-v{package_version}"


def _release_asset_names(package_version: str) -> dict[str, str]:
    prefix = f"mythic-edge-corpus-{package_version}"
    return {
        "package_archive": f"{prefix}.tar.gz",
        "release_metadata": f"{prefix}.metadata.json",
        "checksum_manifest": f"{prefix}.checksums.txt",
    }


if __name__ == "__main__":
    raise SystemExit(main())
