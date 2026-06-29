#!/usr/bin/env python3
"""No-send repository_dispatch payload validation for reviewed corpus releases."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

OBJECT_TYPE = "corpus_repository_dispatch_no_send_validation"
SCHEMA_VERSION = "corpus_repository_dispatch_no_send.v1"
PAYLOAD_SCHEMA_VERSION = "corpus_repository_dispatch_payload.v1"
RELEASE_OBJECT = "corpus_release_package_dry_run"
RELEASE_SCHEMA_VERSION = "corpus_release_package_dry_run.v1"
RELEASE_METADATA_OBJECT = "corpus_release_package_metadata"
RELEASE_METADATA_SCHEMA_VERSION = "corpus_release_package_metadata.v1"
RELEASE_READY_STATUS = "release_candidate_report_only"
REPOSITORY = "Tahjali11/Mythic-Edge-Corpus"
REPOSITORY_URL = "https://github.com/Tahjali11/Mythic-Edge-Corpus"
TARGET_REPOSITORY = "Tahjali11/Mythic-Edge"
TARGET_REPOSITORY_URL = "https://github.com/Tahjali11/Mythic-Edge"
PACKAGE_ID = "mythic-edge-corpus"
RELEASE_CHANNEL = "reviewed"
DISPATCH_CONTRACT_REF = "docs/contracts/corpus_repository_dispatch_into_mythic_edge.md"
RELEASE_CONTRACT_REF = "docs/contracts/corpus_release_publishing_reviewed_packages.md"
EVENT_NAME = "mythic_edge_corpus.reviewed_package_published.v1"
DRY_RUN_EVENT_NAME = "mythic_edge_corpus.reviewed_package_published.dry_run.v1"
DRY_RUN_PAYLOAD_READY_STATUS = "dry_run_payload_ready"

NON_CLAIMS = (
    "notification_only",
    "no_parser_truth_claim",
    "no_fixture_promotion_claim",
    "no_ratchet_claim",
    "no_baseline_pr_claim",
    "no_readiness_claim",
    "no_release_readiness_claim",
    "no_deploy_readiness_claim",
    "no_production_readiness_claim",
    "no_analytics_truth_claim",
    "no_ai_truth_claim",
    "no_coaching_truth_claim",
    "no_privacy_assurance_claim",
    "no_security_assurance_claim",
    "no_full_corpus_parity_claim",
)
NO_SEND_GUARDS = {
    "repository_dispatch_sent": False,
    "github_release_created": False,
    "release_asset_uploaded": False,
    "package_artifact_created": False,
    "ratchet_executed": False,
    "baseline_pr_created": False,
    "mythic_edge_mutated": False,
    "source_repo_issue_created": False,
    "source_repo_pr_created": False,
}
ALLOWED_EVENT_NAMES = {DRY_RUN_EVENT_NAME}
KNOWN_EVENT_NAMES = {EVENT_NAME, DRY_RUN_EVENT_NAME}
ALLOWED_PAYLOAD_KEYS = {
    "schema_version",
    "event_name",
    "source_repository",
    "source_repository_url",
    "target_repository",
    "target_repository_url",
    "package_id",
    "package_version",
    "release_tag",
    "release_url",
    "release_metadata_asset_name",
    "release_metadata_asset_url",
    "package_asset_name",
    "package_asset_url",
    "checksum_asset_name",
    "checksum_asset_url",
    "asset_checksums",
    "release_source_commit",
    "release_channel",
    "release_contract_ref",
    "preview_validation_ref",
    "pr_validation_ref",
    "human_review_ref",
    "dispatch_contract_ref",
    "non_claims",
}
ASSET_ROLES = {
    "package_archive": ("package_asset_name", "package_asset_url"),
    "release_metadata": ("release_metadata_asset_name", "release_metadata_asset_url"),
    "checksum_manifest": ("checksum_asset_name", "checksum_asset_url"),
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
PAYLOAD_CHECKSUM_KEYS = {
    "algorithm",
    "asset_name",
    "checksum",
}
RELEASE_METADATA_CHECKSUM_KEYS = {
    "algorithm",
    "asset_name",
    "sha256",
}
PATH_REF_KEYS = {
    "path",
}
PREDECESSOR_REF_KEYS = {
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
NO_WRITE_GUARD_KEYS = {
    "baseline_pr_created",
    "checksum_file_written",
    "github_release_created",
    "mythic_edge_mutated",
    "package_archive_written",
    "ratchet_executed",
    "release_asset_uploaded",
    "release_metadata_written",
    "repository_dispatch_sent",
}
INCLUDED_FILES_SUMMARY_KEYS = {
    "paths",
    "total_included_files",
}
SAFETY_CHECK_KEYS = {
    "check",
    "status",
}

PACKAGE_VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SAFE_LABEL_RE = re.compile(r"^[A-Za-z0-9._/@{}:+-]+$")
ASSET_NAME_RE = re.compile(r"^[A-Za-z0-9._+-]+$")
GITHUB_RELEASE_URL_RE = re.compile(
    r"^https://github\.com/Tahjali11/Mythic-Edge-Corpus/releases/(?:tag|download)/[A-Za-z0-9._+/-]+$"
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
REASON_RE = re.compile(r"^[a-z0-9_]+$")
RAW_OR_PRIVATE_MARKER_RE = re.compile(
    "|".join(
        (
            "raw corpus",
            "private " + "log",
            "external corpus",
            "runtime artifact",
            "ratchet output",
            "run ratchet",
            "baseline pr",
            "open baseline pr",
            "source patch",
            "source snippet",
            "repository dispatch sent",
            "promote fixtures",
            "source mutation",
            "deploy",
            "parser truth",
            "fixture promotion",
            "corpus readiness",
            "release readiness",
            "deploy readiness",
            "production readiness",
        )
    ),
    re.IGNORECASE,
)


def build_dispatch_report(
    *,
    release_report: Mapping[str, Any] | None,
    event_name: str = DRY_RUN_EVENT_NAME,
    payload_only: bool = True,
    send_requested: bool = False,
    dispatch_execution_authorized: bool = False,
    expected_asset_checksums: Mapping[str, str] | None = None,
    ratchet_requested: bool = False,
    baseline_pr_requested: bool = False,
    source_mutation_requested: bool = False,
    release_or_asset_creation_requested: bool = False,
) -> dict[str, Any]:
    """Build and validate a dry-run dispatch payload without sending it."""

    unsupported_reason = _unsupported_request_reason(
        event_name=event_name,
        payload_only=payload_only,
        send_requested=send_requested,
        dispatch_execution_authorized=dispatch_execution_authorized,
        ratchet_requested=ratchet_requested,
        baseline_pr_requested=baseline_pr_requested,
        source_mutation_requested=source_mutation_requested,
        release_or_asset_creation_requested=release_or_asset_creation_requested,
    )
    if unsupported_reason:
        return _blocked_report(status=unsupported_reason[0], reason=unsupported_reason[1])
    if release_report is None:
        return _blocked_report(status="blocked_release_not_published", reason="missing_release_metadata")

    public_safety_reason = _public_safety_reason(release_report)
    if public_safety_reason:
        return _blocked_report(status="blocked_payload_forbidden_content", reason=public_safety_reason)

    release_problem = _validate_release_report(release_report)
    if release_problem:
        return _blocked_report(
            status=_release_problem_status(release_problem),
            reason=release_problem,
            package_version=_safe_package_version(release_report.get("package_version")),
            release_tag=_safe_release_tag(release_report.get("release_tag")),
            source_commit=_safe_commit(release_report.get("source_commit")),
        )

    assets = _assets_by_role(release_report.get("planned_assets"))
    checksum_problem = _validate_expected_checksums(assets, expected_asset_checksums or {})
    if checksum_problem:
        return _blocked_report(
            status="blocked_release_validation_failed",
            reason=checksum_problem,
            package_version=str(release_report["package_version"]),
            release_tag=str(release_report["release_tag"]),
            source_commit=str(release_report["source_commit"]),
        )

    payload = _payload_from_release_report(release_report, assets, event_name=event_name)
    payload_problems = validate_dispatch_payload(payload)
    if payload_problems:
        return _blocked_report(
            status="blocked_payload_schema",
            reason=payload_problems[0],
            package_version=str(release_report["package_version"]),
            release_tag=str(release_report["release_tag"]),
            source_commit=str(release_report["source_commit"]),
        )

    return _report(
        status=DRY_RUN_PAYLOAD_READY_STATUS,
        event_name=event_name,
        package_version=str(release_report["package_version"]),
        release_tag=str(release_report["release_tag"]),
        source_commit=str(release_report["source_commit"]),
        payload=payload,
        blocked_reason_codes=[],
    )


def validate_dispatch_payload(payload: Mapping[str, Any]) -> list[str]:
    """Return symbolic payload validation reason codes."""

    if not isinstance(payload, Mapping):
        return ["payload_schema_invalid"]
    keys = set(payload)
    shape_reason = _unexpected_key_reason(payload, allowed_keys=ALLOWED_PAYLOAD_KEYS)
    if shape_reason:
        return [shape_reason]
    if keys != ALLOWED_PAYLOAD_KEYS:
        return ["payload_schema_invalid"]
    public_safety_reason = _public_safety_reason(payload)
    if public_safety_reason:
        return [public_safety_reason]
    if payload.get("schema_version") != PAYLOAD_SCHEMA_VERSION:
        return ["payload_schema_invalid"]
    if payload.get("event_name") not in ALLOWED_EVENT_NAMES:
        return ["event_name_not_allowlisted"]
    if payload.get("source_repository") != REPOSITORY or payload.get("source_repository_url") != REPOSITORY_URL:
        return ["receiver_not_allowlisted"]
    if payload.get("target_repository") != TARGET_REPOSITORY or payload.get("target_repository_url") != TARGET_REPOSITORY_URL:
        return ["receiver_not_allowlisted"]
    if payload.get("package_id") != PACKAGE_ID:
        return ["payload_schema_invalid"]
    package_version = payload.get("package_version")
    release_tag = payload.get("release_tag")
    if not _is_package_version(package_version):
        return ["package_version_mismatch"]
    if release_tag != _release_tag(str(package_version)):
        return ["release_tag_mismatch"]
    if payload.get("release_channel") != RELEASE_CHANNEL:
        return ["payload_schema_invalid"]
    if payload.get("release_contract_ref") != RELEASE_CONTRACT_REF:
        return ["payload_schema_invalid"]
    if payload.get("dispatch_contract_ref") != DISPATCH_CONTRACT_REF:
        return ["payload_schema_invalid"]
    if not _is_commit(payload.get("release_source_commit")):
        return ["source_commit_mismatch"]
    for key in (
        "release_url",
        "release_metadata_asset_url",
        "package_asset_url",
        "checksum_asset_url",
    ):
        if not _is_github_release_url(payload.get(key)):
            return ["payload_schema_invalid"]
    for key in (
        "release_metadata_asset_name",
        "package_asset_name",
        "checksum_asset_name",
        "preview_validation_ref",
        "pr_validation_ref",
        "human_review_ref",
    ):
        if not _is_safe_label(payload.get(key)):
            return ["payload_schema_invalid"]
    checksum_problem = _validate_payload_checksums(
        payload.get("asset_checksums"),
        required_asset_names={
            str(payload["release_metadata_asset_name"]),
            str(payload["package_asset_name"]),
            str(payload["checksum_asset_name"]),
        },
    )
    if checksum_problem:
        return [checksum_problem]
    if payload.get("non_claims") != list(NON_CLAIMS):
        return ["payload_schema_invalid"]
    return []


def format_text(report: Mapping[str, Any]) -> str:
    """Render a deterministic no-send validation summary."""

    lines = [
        "Corpus Repository Dispatch No-Send Validation",
        f"schema_version: {report['schema_version']}",
        f"status: {report['status']}",
        f"event_name: {report['event_name']}",
        f"package_version: {report.get('package_version') or 'unknown'}",
        f"release_tag: {report.get('release_tag') or 'unknown'}",
        f"release_source_commit: {report.get('release_source_commit') or 'unknown'}",
        "blocked_reason_codes:",
    ]
    if report["blocked_reason_codes"]:
        lines.extend(f"- {reason}" for reason in report["blocked_reason_codes"])
    else:
        lines.append("- none")
    lines.append("no_send_guards:")
    lines.extend(f"- {key}: {str(value).lower()}" for key, value in sorted(report["no_send_guards"].items()))
    lines.append("non_claims:")
    lines.extend(f"- {claim}" for claim in report["non_claims"])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a no-send repository_dispatch payload for a reviewed corpus release.",
    )
    parser.add_argument("--release-report")
    parser.add_argument("--package-version")
    parser.add_argument("--event-name", default=DRY_RUN_EVENT_NAME)
    parser.add_argument("--payload-only", action="store_true")
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--expected-asset-checksum", action="append", default=[])
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    try:
        release_report = _load_release_report(args.release_report)
        expected_checksums = _parse_expected_checksums(args.expected_asset_checksum)
    except ValueError as exc:
        report = _blocked_report(status="invalid", reason=str(exc), package_version=args.package_version)
    else:
        report = build_dispatch_report(
            release_report=release_report,
            event_name=args.event_name,
            payload_only=args.payload_only,
            send_requested=args.send,
            expected_asset_checksums=expected_checksums,
        )
        if (
            args.package_version
            and report["status"] == DRY_RUN_PAYLOAD_READY_STATUS
            and report.get("package_version") != args.package_version
        ):
            report = _blocked_report(
                status="blocked_release_validation_failed",
                reason="package_version_mismatch",
                package_version=args.package_version,
                release_tag=report.get("release_tag"),
                source_commit=report.get("release_source_commit"),
            )

    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report), end="")
    return 0 if report["status"] == DRY_RUN_PAYLOAD_READY_STATUS else 2


def _unsupported_request_reason(
    *,
    event_name: str,
    payload_only: bool,
    send_requested: bool,
    dispatch_execution_authorized: bool,
    ratchet_requested: bool,
    baseline_pr_requested: bool,
    source_mutation_requested: bool,
    release_or_asset_creation_requested: bool,
) -> tuple[str, str] | None:
    if event_name not in KNOWN_EVENT_NAMES:
        return ("blocked_missing_receiver_allowlist", "event_name_not_allowlisted")
    if event_name != DRY_RUN_EVENT_NAME:
        return ("unsupported", "non_dry_run_event_requires_separate_authorization")
    if not payload_only:
        return ("unsupported", "payload_only_required")
    if send_requested or dispatch_execution_authorized:
        return ("blocked_missing_token", "credential_missing")
    if ratchet_requested:
        return ("blocked_ratchet_requested", "payload_requests_ratchet")
    if baseline_pr_requested:
        return ("blocked_baseline_pr_requested", "payload_requests_baseline_pr")
    if source_mutation_requested:
        return ("blocked_source_mutation_requested", "payload_requests_source_mutation")
    if release_or_asset_creation_requested:
        return ("blocked_release_or_asset_creation_requested", "release_or_asset_creation_requested")
    return None


def _validate_release_report(report: Mapping[str, Any]) -> str | None:
    if report.get("object") != RELEASE_OBJECT:
        return "missing_release_metadata"
    if report.get("schema_version") != RELEASE_SCHEMA_VERSION:
        return "payload_schema_invalid"
    shape_reason = _unexpected_key_reason(report, allowed_keys=RELEASE_REPORT_KEYS)
    if shape_reason:
        return shape_reason
    if report.get("status") != RELEASE_READY_STATUS:
        return "blocked_release_validation_failed"
    if report.get("dry_run") is not True or report.get("publish_requested") is not False:
        return "blocked_release_validation_failed"
    if report.get("repository") != REPOSITORY or report.get("repository_url") != REPOSITORY_URL:
        return "payload_schema_invalid"
    package_version = report.get("package_version")
    if not _is_package_version(package_version):
        return "package_version_mismatch"
    if report.get("release_tag") != _release_tag(str(package_version)):
        return "release_tag_mismatch"
    if not _is_commit(report.get("source_commit")):
        return "source_commit_mismatch"
    if report.get("release_channel") != RELEASE_CHANNEL:
        return "blocked_release_validation_failed"
    if report.get("blocked_reason_codes") != []:
        return "blocked_release_validation_failed"
    release_metadata = report.get("release_metadata")
    if not isinstance(release_metadata, Mapping):
        return "missing_release_metadata"
    shape_reason = _validate_release_metadata(release_metadata, release_report=report)
    if shape_reason:
        return shape_reason
    shape_reason = _validate_path_ref(report.get("manifest_ref"))
    if shape_reason:
        return shape_reason
    shape_reason = _validate_path_ref(report.get("session_ledger_ref"))
    if shape_reason:
        return shape_reason
    shape_reason = _validate_included_files_summary(report.get("included_files_summary"))
    if shape_reason:
        return shape_reason
    shape_reason = _validate_safety_checks(report.get("safety_checks"))
    if shape_reason:
        return shape_reason
    shape_reason = _validate_no_write_guards(report.get("no_write_guards"))
    if shape_reason:
        return shape_reason
    shape_reason = _validate_review_ref(report.get("review_ref"))
    if shape_reason:
        return shape_reason
    shape_reason = _validate_predecessor_ref(
        report.get("package_preview_ref"),
        "corpus_local_package_preview",
        "preview_report_only",
        "missing_predecessor_preview_evidence",
    )
    if shape_reason:
        return shape_reason
    shape_reason = _validate_predecessor_ref(
        report.get("pr_validation_ref"),
        "corpus_pr_validation_package_safety",
        "passed_report_only",
        "missing_predecessor_pr_validation_evidence",
    )
    if shape_reason:
        return shape_reason
    if any(bool(value) for value in _bool_values(report.get("no_write_guards"))):
        return "blocked_source_mutation_requested"
    assets_problem = _validate_assets(report.get("planned_assets"))
    if assets_problem:
        return assets_problem
    assets = _assets_by_role(report.get("planned_assets"))
    planned_checksums = {
        str(asset["asset_name"]): str(asset["sha256"])
        for asset in assets.values()
    }
    checksum_problem = _validate_release_metadata_checksums(
        release_metadata.get("asset_checksums"),
        required_checksums=planned_checksums,
    )
    if checksum_problem:
        return checksum_problem
    return None


def _validate_release_metadata(value: Mapping[str, Any], *, release_report: Mapping[str, Any]) -> str | None:
    shape_reason = _unexpected_key_reason(value, allowed_keys=RELEASE_METADATA_KEYS)
    if shape_reason:
        return shape_reason
    if value.get("object") != RELEASE_METADATA_OBJECT:
        return "missing_release_metadata"
    if value.get("schema_version") != RELEASE_METADATA_SCHEMA_VERSION:
        return "payload_schema_invalid"
    for key in (
        "blocked_reason_codes",
        "package_version",
        "release_channel",
        "release_tag",
        "repository",
        "repository_url",
        "source_branch",
        "source_commit",
    ):
        if value.get(key) != release_report.get(key):
            return "payload_schema_invalid"
    if not _is_safe_label(value.get("package_id")):
        return "payload_schema_invalid"
    if not isinstance(value.get("non_claims"), list) or not all(_is_safe_label(item) for item in value["non_claims"]):
        return "payload_schema_invalid"
    shape_reason = _validate_path_ref(value.get("manifest_ref"))
    if shape_reason:
        return shape_reason
    shape_reason = _validate_path_ref(value.get("session_ledger_ref"))
    if shape_reason:
        return shape_reason
    shape_reason = _validate_included_files_summary(value.get("included_files_summary"))
    if shape_reason:
        return shape_reason
    shape_reason = _validate_safety_checks(value.get("safety_checks"))
    if shape_reason:
        return shape_reason
    shape_reason = _validate_review_ref(value.get("review_ref"))
    if shape_reason:
        return shape_reason
    shape_reason = _validate_predecessor_ref(
        value.get("package_preview_ref"),
        "corpus_local_package_preview",
        "preview_report_only",
        "missing_predecessor_preview_evidence",
    )
    if shape_reason:
        return shape_reason
    shape_reason = _validate_predecessor_ref(
        value.get("pr_validation_ref"),
        "corpus_pr_validation_package_safety",
        "passed_report_only",
        "missing_predecessor_pr_validation_evidence",
    )
    if shape_reason:
        return shape_reason
    return _validate_release_metadata_checksums(value.get("asset_checksums"))


def _validate_path_ref(value: Any) -> str | None:
    if not isinstance(value, Mapping):
        return "payload_schema_invalid"
    shape_reason = _unexpected_key_reason(value, allowed_keys=PATH_REF_KEYS)
    if shape_reason:
        return shape_reason
    path = value.get("path")
    if not _is_corpus_path(path):
        return "payload_schema_invalid"
    return None


def _validate_predecessor_ref(
    value: Any,
    expected_object: str,
    expected_status: str,
    missing_reason: str,
) -> str | None:
    if not isinstance(value, Mapping):
        return missing_reason
    shape_reason = _unexpected_key_reason(value, allowed_keys=PREDECESSOR_REF_KEYS)
    if shape_reason:
        return shape_reason
    if not _predecessor_ref_passed(value, expected_object, expected_status):
        return missing_reason
    return None


def _validate_review_ref(value: Any) -> str | None:
    if not isinstance(value, Mapping):
        return "missing_human_review"
    shape_reason = _unexpected_key_reason(value, allowed_keys=REVIEW_REF_KEYS)
    if shape_reason:
        return shape_reason
    if not _review_ref_is_approved(value):
        return "missing_human_review"
    return None


def _validate_release_metadata_checksums(
    value: Any,
    *,
    required_checksums: Mapping[str, str] | None = None,
) -> str | None:
    if not isinstance(value, list) or not value:
        return "missing_checksum_asset"
    seen_checksums: dict[str, str] = {}
    for item in value:
        if not isinstance(item, Mapping):
            return "checksum_mismatch"
        shape_reason = _unexpected_key_reason(item, allowed_keys=RELEASE_METADATA_CHECKSUM_KEYS)
        if shape_reason:
            return shape_reason
        asset_name = item.get("asset_name")
        if not _is_asset_name(asset_name):
            return "missing_release_asset"
        sha256 = item.get("sha256")
        if item.get("algorithm") != "sha256" or not _is_sha256(sha256):
            return "checksum_mismatch"
        if str(asset_name) in seen_checksums:
            return "checksum_mismatch"
        seen_checksums[str(asset_name)] = str(sha256)
    if len(seen_checksums) != len(value):
        return "checksum_mismatch"
    if required_checksums is not None and seen_checksums != dict(required_checksums):
        return "checksum_mismatch"
    return None


def _validate_included_files_summary(value: Any) -> str | None:
    if not isinstance(value, Mapping):
        return "payload_schema_invalid"
    shape_reason = _unexpected_key_reason(value, allowed_keys=INCLUDED_FILES_SUMMARY_KEYS)
    if shape_reason:
        return shape_reason
    paths = value.get("paths")
    if not isinstance(paths, list) or not all(_is_corpus_path(path) for path in paths):
        return "payload_schema_invalid"
    if not isinstance(value.get("total_included_files"), int) or value["total_included_files"] < 0:
        return "payload_schema_invalid"
    return None


def _validate_safety_checks(value: Any) -> str | None:
    if not isinstance(value, list) or not value:
        return "payload_schema_invalid"
    for item in value:
        if not isinstance(item, Mapping):
            return "payload_schema_invalid"
        shape_reason = _unexpected_key_reason(item, allowed_keys=SAFETY_CHECK_KEYS)
        if shape_reason:
            return shape_reason
        if not _is_safe_label(item.get("check")) or item.get("status") != "passed":
            return "payload_schema_invalid"
    return None


def _validate_no_write_guards(value: Any) -> str | None:
    if not isinstance(value, Mapping):
        return "payload_schema_invalid"
    shape_reason = _unexpected_key_reason(value, allowed_keys=NO_WRITE_GUARD_KEYS)
    if shape_reason:
        return shape_reason
    if set(value) != NO_WRITE_GUARD_KEYS:
        return "payload_schema_invalid"
    if not all(isinstance(item, bool) for item in value.values()):
        return "payload_schema_invalid"
    return None


def _validate_assets(value: Any) -> str | None:
    if not isinstance(value, list):
        return "missing_release_asset"
    assets: dict[str, Mapping[str, Any]] = {}
    for item in value:
        if not isinstance(item, Mapping):
            return "payload_schema_invalid"
        shape_reason = _unexpected_key_reason(item, allowed_keys=RELEASE_ASSET_KEYS)
        if shape_reason:
            return shape_reason
        role = item.get("role")
        if not isinstance(role, str) or role not in ASSET_ROLES:
            return "payload_schema_invalid"
        if role in assets:
            return "payload_schema_invalid"
        if not _is_asset_name(item.get("asset_name")):
            return "missing_release_asset"
        if item.get("algorithm") != "sha256" or not _is_sha256(item.get("sha256")):
            return "checksum_mismatch"
        if item.get("written") is not False or item.get("published") is not False:
            return "blocked_release_or_asset_creation_requested"
        if not isinstance(item.get("byte_count"), int) or item["byte_count"] < 0:
            return "payload_schema_invalid"
        assets[role] = item
    missing_roles = set(ASSET_ROLES) - set(assets)
    if "checksum_manifest" in missing_roles:
        return "missing_checksum_asset"
    if missing_roles:
        return "missing_release_asset"
    return None


def _assets_by_role(value: Any) -> dict[str, Mapping[str, Any]]:
    if not isinstance(value, list):
        return {}
    assets: dict[str, Mapping[str, Any]] = {}
    for item in value:
        if not isinstance(item, Mapping):
            continue
        role = item.get("role")
        if isinstance(role, str) and role in ASSET_ROLES:
            assets[role] = item
    return assets


def _payload_from_release_report(
    release_report: Mapping[str, Any],
    assets: Mapping[str, Mapping[str, Any]],
    *,
    event_name: str,
) -> dict[str, Any]:
    package_version = str(release_report["package_version"])
    release_tag = str(release_report["release_tag"])
    payload: dict[str, Any] = {
        "schema_version": PAYLOAD_SCHEMA_VERSION,
        "event_name": event_name,
        "source_repository": REPOSITORY,
        "source_repository_url": REPOSITORY_URL,
        "target_repository": TARGET_REPOSITORY,
        "target_repository_url": TARGET_REPOSITORY_URL,
        "package_id": PACKAGE_ID,
        "package_version": package_version,
        "release_tag": release_tag,
        "release_url": _release_url(release_tag),
        "asset_checksums": _asset_checksums(assets),
        "release_source_commit": str(release_report["source_commit"]),
        "release_channel": RELEASE_CHANNEL,
        "release_contract_ref": RELEASE_CONTRACT_REF,
        "preview_validation_ref": _predecessor_public_ref(release_report.get("package_preview_ref")),
        "pr_validation_ref": _predecessor_public_ref(release_report.get("pr_validation_ref")),
        "human_review_ref": _human_review_ref(release_report.get("review_ref")),
        "dispatch_contract_ref": DISPATCH_CONTRACT_REF,
        "non_claims": list(NON_CLAIMS),
    }
    for role, (name_key, url_key) in ASSET_ROLES.items():
        asset_name = str(assets[role]["asset_name"])
        payload[name_key] = asset_name
        payload[url_key] = _asset_url(release_tag, asset_name)
    return payload


def _asset_checksums(assets: Mapping[str, Mapping[str, Any]]) -> list[dict[str, str]]:
    checksums = []
    for role in sorted(assets):
        asset = assets[role]
        checksums.append(
            {
                "asset_name": str(asset["asset_name"]),
                "algorithm": "sha256",
                "checksum": str(asset["sha256"]),
            }
        )
    return checksums


def _validate_expected_checksums(
    assets: Mapping[str, Mapping[str, Any]],
    expected_checksums: Mapping[str, str],
) -> str | None:
    planned = {str(asset["asset_name"]): str(asset["sha256"]) for asset in assets.values()}
    for asset_name, expected in expected_checksums.items():
        if not _is_asset_name(asset_name) or not _is_sha256(expected):
            return "checksum_mismatch"
        if asset_name not in planned:
            return "missing_release_asset"
        if planned[asset_name] != expected:
            return "checksum_mismatch"
    return None


def _validate_payload_checksums(value: Any, *, required_asset_names: set[str]) -> str | None:
    if not isinstance(value, list) or not value:
        return "missing_checksum_asset"
    seen_assets: set[str] = set()
    for item in value:
        if not isinstance(item, Mapping):
            return "checksum_mismatch"
        if set(item) != PAYLOAD_CHECKSUM_KEYS:
            return "payload_contains_forbidden_content"
        asset_name = item.get("asset_name")
        if not _is_asset_name(asset_name):
            return "missing_release_asset"
        if item.get("algorithm") != "sha256" or not _is_sha256(item.get("checksum")):
            return "checksum_mismatch"
        seen_assets.add(str(asset_name))
    if seen_assets != required_asset_names:
        return "checksum_mismatch"
    return None


def _release_problem_status(reason: str) -> str:
    if reason == "missing_release_metadata":
        return "blocked_release_not_published"
    if reason in {
        "missing_release_asset",
        "missing_checksum_asset",
        "checksum_mismatch",
        "release_tag_mismatch",
        "package_version_mismatch",
        "source_commit_mismatch",
        "missing_predecessor_preview_evidence",
        "missing_predecessor_pr_validation_evidence",
        "missing_human_review",
    }:
        return "blocked_release_validation_failed"
    if reason == "blocked_release_or_asset_creation_requested":
        return "blocked_release_or_asset_creation_requested"
    if reason == "blocked_source_mutation_requested":
        return "blocked_source_mutation_requested"
    return "blocked_release_validation_failed"


def _report(
    *,
    status: str,
    event_name: str,
    package_version: str | None,
    release_tag: str | None,
    source_commit: str | None,
    payload: Mapping[str, Any] | None,
    blocked_reason_codes: Sequence[str],
) -> dict[str, Any]:
    return {
        "object": OBJECT_TYPE,
        "schema_version": SCHEMA_VERSION,
        "repository": REPOSITORY,
        "repository_url": REPOSITORY_URL,
        "target_repository": TARGET_REPOSITORY,
        "target_repository_url": TARGET_REPOSITORY_URL,
        "status": status,
        "event_name": event_name,
        "payload_only": True,
        "send_requested": False,
        "repository_dispatch_sent": False,
        "package_version": package_version,
        "release_tag": release_tag,
        "release_source_commit": source_commit,
        "payload": dict(payload) if payload is not None else None,
        "blocked_reason_codes": list(blocked_reason_codes),
        "no_send_guards": dict(NO_SEND_GUARDS),
        "non_claims": list(NON_CLAIMS),
    }


def _blocked_report(
    *,
    status: str,
    reason: str,
    package_version: Any = None,
    release_tag: Any = None,
    source_commit: Any = None,
) -> dict[str, Any]:
    return _report(
        status=status,
        event_name=DRY_RUN_EVENT_NAME,
        package_version=_safe_package_version(package_version),
        release_tag=_safe_release_tag(release_tag),
        source_commit=_safe_commit(source_commit),
        payload=None,
        blocked_reason_codes=[_safe_reason(reason)],
    )


def _public_safety_reason(value: Any) -> str | None:
    for text in _string_values_from(value):
        if LOCAL_OR_SECRET_MARKER_RE.search(text):
            return "payload_contains_forbidden_content"
        if _raw_or_private_marker_present(text):
            return "payload_contains_forbidden_content"
    return None


def _string_values_from(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, Mapping):
        strings: list[str] = []
        for item in value.values():
            strings.extend(_string_values_from(item))
        return strings
    if isinstance(value, list | tuple):
        strings = []
        for item in value:
            strings.extend(_string_values_from(item))
        return strings
    return []


def _marker_text(text: str) -> str:
    return re.sub(r"[_-]+", " ", text)


def _raw_or_private_marker_present(text: str) -> bool:
    normalized = _marker_text(text).lower()
    if normalized.startswith(("no ", "not ")):
        return False
    return bool(RAW_OR_PRIVATE_MARKER_RE.search(normalized))


def _unexpected_key_reason(value: Mapping[str, Any], *, allowed_keys: set[str]) -> str | None:
    unexpected = set(value) - allowed_keys
    if not unexpected:
        return None
    if any(
        not isinstance(key, str)
        or LOCAL_OR_SECRET_MARKER_RE.search(key)
        or _raw_or_private_marker_present(key)
        for key in unexpected
    ):
        return "payload_contains_forbidden_content"
    return "payload_schema_invalid"


def _load_release_report(path: str | None) -> dict[str, Any] | None:
    if path is None:
        return None
    clean_path = _clean_local_input_path(path)
    try:
        return json.loads(clean_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("missing_release_metadata") from exc


def _parse_expected_checksums(values: Sequence[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError("checksum_mismatch")
        asset_name, checksum = value.split("=", 1)
        if not _is_asset_name(asset_name) or not _is_sha256(checksum):
            raise ValueError("checksum_mismatch")
        parsed[asset_name] = checksum
    return parsed


def _clean_local_input_path(value: str) -> Path:
    safety_reason = _input_path_safety_reason(value)
    if safety_reason:
        raise ValueError(safety_reason)
    path = Path(value)
    if not path.exists() or not path.is_file():
        raise ValueError("missing_release_metadata")
    return path


def _input_path_safety_reason(value: str) -> str | None:
    if not isinstance(value, str) or not value:
        return "missing_release_metadata"
    path = Path(value)
    if path.is_absolute() or LOCAL_OR_SECRET_MARKER_RE.search(value) or _raw_or_private_marker_present(value):
        return "payload_contains_forbidden_content"
    parts = path.parts
    if any(part in {"", ".", ".."} for part in parts):
        return "payload_contains_forbidden_content"
    return None


def _predecessor_ref_passed(value: Any, expected_object: str, expected_status: str) -> bool:
    return (
        isinstance(value, Mapping)
        and value.get("object") == expected_object
        and isinstance(value.get("schema_version"), str)
        and value.get("status") == expected_status
        and _is_commit(value.get("source_commit"))
    )


def _review_ref_is_approved(value: Any) -> bool:
    return (
        isinstance(value, Mapping)
        and value.get("approved") is True
        and _is_safe_label(value.get("reviewed_by"))
        and _is_safe_label(value.get("ref"))
    )


def _predecessor_public_ref(value: Any) -> str:
    if not isinstance(value, Mapping):
        return "invalid"
    parts = [
        value.get("object"),
        value.get("schema_version"),
        value.get("status"),
        value.get("source_commit"),
    ]
    if not all(_is_safe_label(part) for part in parts):
        return "invalid"
    return "@".join(str(part) for part in parts)


def _human_review_ref(value: Any) -> str:
    if not isinstance(value, Mapping) or value.get("approved") is not True:
        return "invalid"
    reviewer = value.get("reviewed_by")
    ref = value.get("ref")
    if not _is_safe_label(reviewer) or not _is_safe_label(ref):
        return "invalid"
    return f"{reviewer}@{ref}"


def _bool_values(value: Any) -> list[bool]:
    if not isinstance(value, Mapping):
        return [True]
    return [item for item in value.values() if isinstance(item, bool)]


def _release_tag(package_version: str) -> str:
    return f"corpus-package-v{package_version}"


def _release_url(release_tag: str) -> str:
    return f"{REPOSITORY_URL}/releases/tag/{release_tag}"


def _asset_url(release_tag: str, asset_name: str) -> str:
    return f"{REPOSITORY_URL}/releases/download/{release_tag}/{asset_name}"


def _is_github_release_url(value: Any) -> bool:
    return isinstance(value, str) and bool(GITHUB_RELEASE_URL_RE.fullmatch(value))


def _is_safe_label(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and bool(SAFE_LABEL_RE.fullmatch(value)) and not LOCAL_OR_SECRET_MARKER_RE.search(value)


def _is_package_version(value: Any) -> bool:
    return isinstance(value, str) and bool(PACKAGE_VERSION_RE.fullmatch(value)) and not LOCAL_OR_SECRET_MARKER_RE.search(value)


def _is_commit(value: Any) -> bool:
    return isinstance(value, str) and bool(COMMIT_RE.fullmatch(value))


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and bool(SHA256_RE.fullmatch(value))


def _is_asset_name(value: Any) -> bool:
    return isinstance(value, str) and bool(ASSET_NAME_RE.fullmatch(value)) and not LOCAL_OR_SECRET_MARKER_RE.search(value)


def _is_corpus_path(value: Any) -> bool:
    if not _is_safe_label(value) or not str(value).startswith("corpus/"):
        return False
    parts = str(value).split("/")
    return all(part not in {"", ".", ".."} for part in parts)


def _safe_package_version(value: Any) -> str | None:
    return value if _is_package_version(value) else None


def _safe_release_tag(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    return value if _is_safe_label(value) and value.startswith("corpus-package-v") else None


def _safe_commit(value: Any) -> str | None:
    return value if _is_commit(value) else None


def _safe_reason(value: Any) -> str:
    return str(value) if isinstance(value, str) and bool(REASON_RE.fullmatch(value)) else "invalid"


if __name__ == "__main__":
    raise SystemExit(main())
