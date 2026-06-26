#!/usr/bin/env python3
"""Dry-run release package metadata for reviewed public-safe corpus packages."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import io
import json
import re
import tarfile
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

OBJECT_TYPE = "corpus_release_package_dry_run"
SCHEMA_VERSION = "corpus_release_package_dry_run.v1"
METADATA_OBJECT = "corpus_release_package_metadata"
METADATA_SCHEMA_VERSION = "corpus_release_package_metadata.v1"
REPOSITORY = "Tahjali11/Mythic-Edge-Corpus"
REPOSITORY_URL = "https://github.com/Tahjali11/Mythic-Edge-Corpus"
DEFAULT_SOURCE_BRANCH = "main"
RELEASE_CHANNEL = "reviewed"

RELEASE_CANDIDATE_REPORT_ONLY_STATUS = "release_candidate_report_only"
PREVIEW_PASSED_STATUS = "preview_report_only"
PR_VALIDATION_PASSED_STATUS = "passed_report_only"
PREVIEW_OBJECT = "corpus_local_package_preview"
PREVIEW_SCHEMA_VERSION = "corpus_local_package_preview.v1"
PR_VALIDATION_OBJECT = "corpus_pr_validation_package_safety"
PR_VALIDATION_SCHEMA_VERSION = "corpus_pr_validation_package_safety.v1"

SAFETY_CHECKS = (
    "preview_command_required",
    "pr_validation_required",
    "default_branch_only",
    "clean_worktree_required",
    "repo_relative_paths_only",
    "no_path_traversal",
    "package_root_only",
    "manifest_declared_files_only",
    "session_ledger_reconciled",
    "human_review_required",
    "immutable_release_tag",
    "no_existing_asset_overwrite",
    "no_raw_corpus_evidence",
    "no_private_logs",
    "no_generated_local_artifacts",
    "no_secret_or_connection_material",
    "no_dispatch_payloads",
    "no_ratchet_reports",
    "no_baseline_pr_artifacts",
    "no_source_repo_files",
    "no_external_corpus_contents",
    "no_repository_dispatch",
    "no_ratchet_execution",
    "no_baseline_pr_creation",
    "release_non_claims_present",
)
NON_CLAIMS = (
    "not_parser_truth",
    "not_fixture_promotion",
    "not_corpus_readiness",
    "not_release_readiness",
    "not_deploy_readiness",
    "not_production_readiness",
    "not_ratchet_success",
    "not_baseline_approval",
    "not_analytics_truth",
    "not_ai_truth",
    "not_coaching_truth",
    "not_privacy_assurance",
    "not_security_assurance",
    "not_full_corpus_parity",
)
NO_WRITE_GUARDS = {
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

ALLOWED_PACKAGE_SUFFIXES = {".json", ".md", ".txt"}
PACKAGE_VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")
COMMIT_RE = re.compile(r"^[0-9a-f]{7,64}$")
REF_LABEL_RE = re.compile(r"^[A-Za-z0-9._/@{}:+-]+$")
LOCAL_OR_SECRET_MARKER_RE = re.compile(
    "|".join(
        (
            r"(^|/)(Users|home|var|tmp|private)(/|$)",
            r"[A-Za-z]:/",
            re.escape("Player" + ".log"),
            re.escape("UTC" + "_Log"),
            "Bearer" + r"\s+\S+",
            "web" + "hook[_ -]?url",
            r"api[_ -]?" + "key",
            "sec" + "ret",
            "cred" + "ential",
            "tok" + "en",
        )
    ),
    re.IGNORECASE,
)
FORBIDDEN_CONTENT_RE = re.compile(
    "|".join(
        (
            re.escape("Player" + ".log"),
            re.escape("UTC" + "_Log"),
            "Bearer" + r"\s+\S+",
            "web" + "hook[_ -]?url",
            r"api[_ -]?" + "key",
            "sec" + "ret",
            "cred" + "ential",
            "tok" + "en",
        )
    ),
    re.IGNORECASE,
)

DEFAULT_PREVIEW_BUILDER = object()
DEFAULT_PR_VALIDATION_BUILDER = object()
PreviewBuilder = Callable[..., Mapping[str, Any]]
PrValidationBuilder = Callable[..., Mapping[str, Any]]


def build_release_report(
    *,
    package_root: str | Path,
    manifest_path: str | Path,
    session_ledger_path: str | Path,
    package_version: str,
    source_commit: str,
    preview_source_commit: str | None = None,
    pr_validation_source_commit: str | None = None,
    source_branch: str = DEFAULT_SOURCE_BRANCH,
    repo_root: str | Path | None = None,
    review_approved: bool = False,
    reviewed_by: str | None = None,
    review_ref: str | None = None,
    dry_run: bool = True,
    publish: bool = False,
    clean_worktree_confirmed: bool = False,
    existing_tags: Sequence[str] = (),
    existing_assets: Sequence[str] = (),
    expected_asset_checksums: Mapping[str, str] | None = None,
    dispatch_requested: bool = False,
    ratchet_requested: bool = False,
    baseline_pr_requested: bool = False,
    preview_builder: PreviewBuilder | None | object = DEFAULT_PREVIEW_BUILDER,
    pr_validation_builder: PrValidationBuilder | None | object = DEFAULT_PR_VALIDATION_BUILDER,
) -> dict[str, Any]:
    """Build a deterministic no-write release candidate report."""

    root = Path.cwd() if repo_root is None else Path(repo_root)
    input_problem = _validate_release_inputs(
        package_root=package_root,
        manifest_path=manifest_path,
        session_ledger_path=session_ledger_path,
        package_version=package_version,
        source_commit=source_commit,
        source_branch=source_branch,
    )
    if input_problem:
        return _blocked_report(
            status="blocked_invalid_metadata",
            reason=input_problem,
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
        )
    if publish:
        return _blocked_report(
            status="unsupported",
            reason="publish_mode_requires_separate_authorization",
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
        )
    if not dry_run:
        return _blocked_report(
            status="unsupported",
            reason="non_dry_run_mode_requires_separate_authorization",
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
        )
    if source_branch != DEFAULT_SOURCE_BRANCH:
        return _blocked_report(
            status="blocked_non_default_branch",
            reason="source_branch_not_default",
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
        )
    if not clean_worktree_confirmed:
        return _blocked_report(
            status="blocked_invalid_metadata",
            reason="clean_worktree_not_confirmed",
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
        )
    downstream_block = _downstream_request_block(
        dispatch_requested=dispatch_requested,
        ratchet_requested=ratchet_requested,
        baseline_pr_requested=baseline_pr_requested,
        package_root=package_root,
        manifest_path=manifest_path,
        session_ledger_path=session_ledger_path,
        package_version=package_version,
        source_commit=source_commit,
        source_branch=source_branch,
    )
    if downstream_block:
        return downstream_block

    preview_report = _run_preview_builder(
        builder=preview_builder,
        package_root=package_root,
        manifest_path=manifest_path,
        session_ledger_path=session_ledger_path,
        repo_root=root,
    )
    if preview_report is None:
        return _blocked_report(
            status="blocked_missing_preview_command",
            reason="preview_command_missing",
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
        )
    preview_problem = _validate_preview_report(preview_report)
    if preview_problem or preview_report.get("status") != PREVIEW_PASSED_STATUS:
        return _blocked_report(
            status="blocked_preview_failed",
            reason=preview_problem or f"preview_status_{_safe_value(preview_report.get('status'))}",
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
            preview_report=preview_report,
        )

    pr_report = _run_pr_validation_builder(
        builder=pr_validation_builder,
        source_commit=source_commit,
        package_root=package_root,
        manifest_path=manifest_path,
        session_ledger_path=session_ledger_path,
        repo_root=root,
    )
    if pr_report is None:
        return _blocked_report(
            status="blocked_missing_pr_validation",
            reason="pr_validation_missing",
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
            preview_report=preview_report,
        )
    pr_problem = _validate_pr_validation_report(pr_report)
    if pr_problem or pr_report.get("status") != PR_VALIDATION_PASSED_STATUS:
        return _blocked_report(
            status="blocked_pr_validation_failed",
            reason=pr_problem or f"pr_validation_status_{_safe_value(pr_report.get('status'))}",
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
            preview_report=preview_report,
            pr_validation_report=pr_report,
        )

    commit_problem = _validate_predecessor_commits(
        source_commit=source_commit,
        preview_source_commit=preview_source_commit or _optional_source_commit(preview_report),
        pr_validation_source_commit=pr_validation_source_commit or _optional_source_commit(pr_report),
    )
    if commit_problem:
        return _blocked_report(
            status="blocked_invalid_metadata",
            reason=commit_problem,
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
            preview_report=preview_report,
            pr_validation_report=pr_report,
        )

    if not review_approved:
        return _blocked_report(
            status="blocked_unreviewed_candidate",
            reason="human_review_missing",
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
            preview_report=preview_report,
            pr_validation_report=pr_report,
        )
    review_problem = _validate_review_metadata(reviewed_by, review_ref)
    if review_problem:
        return _blocked_report(
            status="blocked_unreviewed_candidate",
            reason=review_problem,
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
            preview_report=preview_report,
            pr_validation_report=pr_report,
        )

    release_tag = _release_tag(package_version)
    asset_names = _asset_names(package_version)
    if release_tag in set(existing_tags):
        return _blocked_report(
            status="blocked_existing_tag",
            reason="release_tag_already_exists",
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
            preview_report=preview_report,
            pr_validation_report=pr_report,
        )
    asset_collision = sorted(set(asset_names.values()) & set(existing_assets))
    if asset_collision:
        return _blocked_report(
            status="blocked_existing_asset",
            reason="release_asset_already_exists",
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
            preview_report=preview_report,
            pr_validation_report=pr_report,
        )

    file_paths = _candidate_file_paths(preview_report, pr_report, package_root)
    try:
        archive_bytes = _build_deterministic_archive(root, file_paths)
    except ValueError as exc:
        return _blocked_report(
            status=str(exc),
            reason=str(exc),
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
            preview_report=preview_report,
            pr_validation_report=pr_report,
        )

    archive_checksum = _sha256(archive_bytes)
    release_metadata = _release_metadata(
        package_version=package_version,
        source_commit=source_commit,
        source_branch=source_branch,
        release_tag=release_tag,
        preview_report=preview_report,
        pr_validation_report=pr_report,
        reviewed_by=reviewed_by or "reviewed-human",
        review_ref=review_ref or "manual-review",
        included_files=file_paths,
        archive_asset_name=asset_names["archive"],
        archive_checksum=archive_checksum,
    )
    metadata_bytes = _json_bytes(release_metadata)
    checksums_text = _checksums_text(
        (
            (asset_names["archive"], archive_checksum),
            (asset_names["metadata"], _sha256(metadata_bytes)),
        )
    )
    planned_assets = [
        _asset(asset_names["archive"], "package_archive", archive_bytes),
        _asset(asset_names["metadata"], "release_metadata", metadata_bytes),
        _asset(asset_names["checksums"], "checksum_manifest", checksums_text.encode("utf-8")),
    ]
    checksum_problem = _validate_expected_checksums(planned_assets, expected_asset_checksums or {})
    if checksum_problem:
        return _blocked_report(
            status="blocked_invalid_metadata",
            reason=checksum_problem,
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
            preview_report=preview_report,
            pr_validation_report=pr_report,
        )

    return {
        "object": OBJECT_TYPE,
        "schema_version": SCHEMA_VERSION,
        "repository": REPOSITORY,
        "repository_url": REPOSITORY_URL,
        "status": RELEASE_CANDIDATE_REPORT_ONLY_STATUS,
        "dry_run": True,
        "publish_requested": False,
        "package_id": _safe_value(preview_report.get("package_id")),
        "package_version": package_version,
        "release_tag": release_tag,
        "release_name": f"Mythic Edge Corpus {package_version}",
        "release_channel": RELEASE_CHANNEL,
        "source_commit": source_commit,
        "source_branch": source_branch,
        "manifest_ref": {"path": _safe_path(manifest_path)},
        "session_ledger_ref": {"path": _safe_path(session_ledger_path)},
        "package_preview_ref": _predecessor_ref(preview_report, preview_source_commit or source_commit),
        "pr_validation_ref": _predecessor_ref(pr_report, pr_validation_source_commit or source_commit),
        "review_ref": {
            "approved": True,
            "reviewed_by": reviewed_by or "reviewed-human",
            "ref": review_ref or "manual-review",
        },
        "included_files_summary": {
            "total_included_files": len(file_paths),
            "paths": list(file_paths),
        },
        "release_metadata": release_metadata,
        "planned_assets": planned_assets,
        "safety_checks": _safety_checks(failed=False),
        "blocked_reason_codes": [],
        "no_write_guards": dict(NO_WRITE_GUARDS),
        "non_claims": list(NON_CLAIMS),
    }


def format_text(report: Mapping[str, Any]) -> str:
    """Render a deterministic text release dry-run report."""

    lines = [
        "Corpus Release Package Dry Run",
        f"schema_version: {report['schema_version']}",
        f"repository: {report['repository']}",
        f"status: {report['status']}",
        f"dry_run: {str(report['dry_run']).lower()}",
        f"package_version: {report.get('package_version') or 'unknown'}",
        f"release_tag: {report.get('release_tag') or 'unknown'}",
        f"source_commit: {report.get('source_commit') or 'unknown'}",
        f"source_branch: {report.get('source_branch') or 'unknown'}",
        "planned_assets:",
    ]
    assets = report.get("planned_assets", [])
    if assets:
        lines.extend(
            f"- {asset['asset_name']} | {asset['role']} | sha256={asset['sha256']}"
            for asset in assets
        )
    else:
        lines.append("- none")
    lines.append("blocked_reason_codes:")
    if report["blocked_reason_codes"]:
        lines.extend(f"- {reason}" for reason in report["blocked_reason_codes"])
    else:
        lines.append("- none")
    lines.append("non_claims:")
    lines.extend(f"- {claim}" for claim in report["non_claims"])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build reviewed corpus release package metadata in dry-run mode.",
    )
    parser.add_argument("--package-root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--session-ledger", required=True)
    parser.add_argument("--package-version", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--preview-source-commit", required=True)
    parser.add_argument("--pr-validation-source-commit", required=True)
    parser.add_argument("--source-branch", default=DEFAULT_SOURCE_BRANCH)
    parser.add_argument("--reviewed-by")
    parser.add_argument("--review-ref")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--clean-worktree-confirmed", action="store_true")
    parser.add_argument("--existing-tag", action="append", default=[])
    parser.add_argument("--existing-asset", action="append", default=[])
    parser.add_argument("--expected-asset-checksum", action="append", default=[])
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    try:
        expected_asset_checksums = _parse_expected_checksums(args.expected_asset_checksum)
    except ValueError as exc:
        report = _blocked_report(
            status="blocked_invalid_metadata",
            reason=str(exc),
            package_root=args.package_root,
            manifest_path=args.manifest,
            session_ledger_path=args.session_ledger,
            package_version=args.package_version,
            source_commit=args.source_commit,
            source_branch=args.source_branch,
        )
    else:
        report = build_release_report(
            package_root=args.package_root,
            manifest_path=args.manifest,
            session_ledger_path=args.session_ledger,
            package_version=args.package_version,
            source_commit=args.source_commit,
            preview_source_commit=args.preview_source_commit,
            pr_validation_source_commit=args.pr_validation_source_commit,
            source_branch=args.source_branch,
            review_approved=bool(args.reviewed_by or args.review_ref),
            reviewed_by=args.reviewed_by,
            review_ref=args.review_ref,
            dry_run=args.dry_run,
            publish=args.publish,
            clean_worktree_confirmed=args.clean_worktree_confirmed,
            existing_tags=tuple(args.existing_tag),
            existing_assets=tuple(args.existing_asset),
            expected_asset_checksums=expected_asset_checksums,
        )
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report), end="")
    return 0 if report["status"] == RELEASE_CANDIDATE_REPORT_ONLY_STATUS else 2


def _blocked_report(
    *,
    status: str,
    reason: str,
    package_root: str | Path,
    manifest_path: str | Path,
    session_ledger_path: str | Path,
    package_version: str,
    source_commit: str,
    source_branch: str,
    preview_report: Mapping[str, Any] | None = None,
    pr_validation_report: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "object": OBJECT_TYPE,
        "schema_version": SCHEMA_VERSION,
        "repository": REPOSITORY,
        "repository_url": REPOSITORY_URL,
        "status": status,
        "dry_run": True,
        "publish_requested": False,
        "package_id": _safe_value((preview_report or {}).get("package_id")),
        "package_version": _safe_value(package_version) or "invalid",
        "release_tag": _safe_release_tag(package_version),
        "release_name": f"Mythic Edge Corpus {_safe_value(package_version) or 'invalid'}",
        "release_channel": RELEASE_CHANNEL,
        "source_commit": _safe_commit(source_commit),
        "source_branch": _safe_label(source_branch),
        "manifest_ref": {"path": _safe_path(manifest_path)},
        "session_ledger_ref": {"path": _safe_path(session_ledger_path)},
        "package_preview_ref": _predecessor_ref(preview_report, None),
        "pr_validation_ref": _predecessor_ref(pr_validation_report, None),
        "review_ref": {"approved": False, "reviewed_by": None, "ref": None},
        "included_files_summary": {"total_included_files": 0, "paths": []},
        "release_metadata": None,
        "planned_assets": [],
        "safety_checks": _safety_checks(failed=True),
        "blocked_reason_codes": [_safe_reason(reason)],
        "no_write_guards": dict(NO_WRITE_GUARDS),
        "non_claims": list(NON_CLAIMS),
    }


def _validate_release_inputs(
    *,
    package_root: str | Path,
    manifest_path: str | Path,
    session_ledger_path: str | Path,
    package_version: str,
    source_commit: str,
    source_branch: str,
) -> str | None:
    try:
        package_rel = _clean_repo_relative_path(package_root)
        manifest_rel = _clean_repo_relative_path(manifest_path)
        ledger_rel = _clean_repo_relative_path(session_ledger_path)
    except ValueError as exc:
        return str(exc)
    package_text = package_rel.as_posix()
    if not manifest_rel.as_posix().startswith(package_text + "/"):
        return "manifest_outside_package_root"
    if not ledger_rel.as_posix().startswith(package_text + "/"):
        return "session_ledger_outside_package_root"
    if not _is_safe_package_version(package_version):
        return "package_version_invalid"
    if not _is_commit(source_commit):
        return "source_commit_invalid"
    if not _is_safe_label(source_branch):
        return "source_branch_invalid"
    return None


def _downstream_request_block(
    *,
    dispatch_requested: bool,
    ratchet_requested: bool,
    baseline_pr_requested: bool,
    package_root: str | Path,
    manifest_path: str | Path,
    session_ledger_path: str | Path,
    package_version: str,
    source_commit: str,
    source_branch: str,
) -> dict[str, Any] | None:
    if dispatch_requested:
        return _blocked_report(
            status="blocked_dispatch_requested",
            reason="repository_dispatch_requested",
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
        )
    if ratchet_requested:
        return _blocked_report(
            status="blocked_ratchet_requested",
            reason="ratchet_requested",
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
        )
    if baseline_pr_requested:
        return _blocked_report(
            status="blocked_baseline_pr_requested",
            reason="baseline_pr_requested",
            package_root=package_root,
            manifest_path=manifest_path,
            session_ledger_path=session_ledger_path,
            package_version=package_version,
            source_commit=source_commit,
            source_branch=source_branch,
        )
    return None


def _run_preview_builder(
    *,
    builder: PreviewBuilder | None | object,
    package_root: str | Path,
    manifest_path: str | Path,
    session_ledger_path: str | Path,
    repo_root: Path,
) -> Mapping[str, Any] | None:
    if builder is DEFAULT_PREVIEW_BUILDER:
        builder = _load_builder("corpus_package_preview.py", "build_preview")
    if builder is None:
        return None
    try:
        return dict(
            builder(
                package_root=package_root,
                manifest_path=manifest_path,
                session_ledger_path=session_ledger_path,
                repo_root=repo_root,
            )
        )
    except Exception:  # noqa: BLE001 - fail closed without echoing values.
        return {"object": PREVIEW_OBJECT, "schema_version": PREVIEW_SCHEMA_VERSION, "status": "preview_failed"}


def _run_pr_validation_builder(
    *,
    builder: PrValidationBuilder | None | object,
    source_commit: str,
    package_root: str | Path,
    manifest_path: str | Path,
    session_ledger_path: str | Path,
    repo_root: Path,
) -> Mapping[str, Any] | None:
    if builder is DEFAULT_PR_VALIDATION_BUILDER:
        builder = _load_builder("corpus_pr_validate_package_safety.py", "build_validation_report")
    if builder is None:
        return None
    try:
        return dict(
            builder(
                base_ref="origin/main",
                head_ref=source_commit,
                package_root=package_root,
                manifest_path=manifest_path,
                session_ledger_path=session_ledger_path,
                repo_root=repo_root,
            )
        )
    except Exception:  # noqa: BLE001 - fail closed without echoing values.
        return {
            "object": PR_VALIDATION_OBJECT,
            "schema_version": PR_VALIDATION_SCHEMA_VERSION,
            "status": "pr_validation_failed",
        }


def _load_builder(filename: str, function_name: str) -> Callable[..., Mapping[str, Any]] | None:
    path = Path(__file__).resolve().with_name(filename)
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(f"{path.stem}_for_release_package", path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    builder = getattr(module, function_name, None)
    if not callable(builder):
        return None
    return builder


def _validate_preview_report(report: Mapping[str, Any]) -> str | None:
    if report.get("object") != PREVIEW_OBJECT:
        return "preview_object_unsupported"
    if report.get("schema_version") != PREVIEW_SCHEMA_VERSION:
        return "preview_schema_version_unsupported"
    if not isinstance(report.get("status"), str):
        return "preview_status_missing"
    if not isinstance(report.get("inventory"), list):
        return "preview_inventory_missing"
    if not isinstance(report.get("summary"), Mapping):
        return "preview_summary_missing"
    return None


def _validate_pr_validation_report(report: Mapping[str, Any]) -> str | None:
    if report.get("object") != PR_VALIDATION_OBJECT:
        return "pr_validation_object_unsupported"
    if report.get("schema_version") != PR_VALIDATION_SCHEMA_VERSION:
        return "pr_validation_schema_version_unsupported"
    if not isinstance(report.get("status"), str):
        return "pr_validation_status_missing"
    if not isinstance(report.get("changed_package_files"), list):
        return "pr_validation_changed_files_missing"
    return None


def _validate_predecessor_commits(
    *,
    source_commit: str,
    preview_source_commit: str | None,
    pr_validation_source_commit: str | None,
) -> str | None:
    if not preview_source_commit or not _is_commit(preview_source_commit):
        return "preview_source_commit_missing_or_invalid"
    if not pr_validation_source_commit or not _is_commit(pr_validation_source_commit):
        return "pr_validation_source_commit_missing_or_invalid"
    if preview_source_commit != source_commit or pr_validation_source_commit != source_commit:
        return "predecessor_source_commit_mismatch"
    return None


def _optional_source_commit(report: Mapping[str, Any]) -> str | None:
    value = report.get("source_commit")
    return value if isinstance(value, str) else None


def _validate_review_metadata(reviewed_by: str | None, review_ref: str | None) -> str | None:
    if not reviewed_by and not review_ref:
        return "human_review_missing"
    if not reviewed_by:
        return "reviewer_missing"
    if not review_ref:
        return "review_ref_missing"
    if reviewed_by is not None and not _is_safe_label(reviewed_by):
        return "reviewer_unsafe"
    if review_ref is not None and not _is_safe_label(review_ref):
        return "review_ref_unsafe"
    return None


def _candidate_file_paths(
    preview_report: Mapping[str, Any],
    pr_report: Mapping[str, Any],
    package_root: str | Path,
) -> tuple[str, ...]:
    package_rel = _clean_repo_relative_path(package_root)
    pr_paths = [_safe_path(path) for path in pr_report.get("changed_package_files", [])]
    preview_paths = [
        _safe_path(item.get("path"))
        for item in preview_report.get("inventory", [])
        if isinstance(item, Mapping)
    ]
    paths = sorted({path for path in (*pr_paths, *preview_paths) if path != "invalid"})
    package_text = package_rel.as_posix()
    if not paths:
        raise ValueError("blocked_invalid_metadata")
    for path in paths:
        if not (path == package_text or path.startswith(package_text + "/")):
            raise ValueError("blocked_unsafe_path")
    return tuple(paths)


def _build_deterministic_archive(root: Path, rel_paths: Sequence[str]) -> bytes:
    archive = io.BytesIO()
    with gzip.GzipFile(fileobj=archive, mode="wb", mtime=0) as gzip_file:
        with tarfile.open(fileobj=gzip_file, mode="w") as tar:
            for rel_path in rel_paths:
                path = root / rel_path
                if not path.exists() or not path.is_file():
                    raise ValueError("blocked_invalid_metadata")
                if path.suffix not in ALLOWED_PACKAGE_SUFFIXES:
                    raise ValueError("blocked_raw_or_private_input")
                data = path.read_bytes()
                if FORBIDDEN_CONTENT_RE.search(data.decode("utf-8", errors="ignore")):
                    raise ValueError("blocked_forbidden_content")
                info = tarfile.TarInfo(rel_path)
                info.size = len(data)
                info.mtime = 0
                info.mode = 0o644
                info.uid = 0
                info.gid = 0
                info.uname = ""
                info.gname = ""
                tar.addfile(info, io.BytesIO(data))
    return archive.getvalue()


def _release_metadata(
    *,
    package_version: str,
    source_commit: str,
    source_branch: str,
    release_tag: str,
    preview_report: Mapping[str, Any],
    pr_validation_report: Mapping[str, Any],
    reviewed_by: str,
    review_ref: str,
    included_files: Sequence[str],
    archive_asset_name: str,
    archive_checksum: str,
) -> dict[str, Any]:
    return {
        "object": METADATA_OBJECT,
        "schema_version": METADATA_SCHEMA_VERSION,
        "repository": REPOSITORY,
        "repository_url": REPOSITORY_URL,
        "package_id": _safe_value(preview_report.get("package_id")),
        "package_version": package_version,
        "release_tag": release_tag,
        "release_channel": RELEASE_CHANNEL,
        "source_commit": source_commit,
        "source_branch": source_branch,
        "manifest_ref": _path_ref(preview_report.get("manifest_ref")),
        "session_ledger_ref": _path_ref(preview_report.get("session_ledger_ref")),
        "package_preview_ref": _predecessor_ref(preview_report, source_commit),
        "pr_validation_ref": _predecessor_ref(pr_validation_report, source_commit),
        "review_ref": {"approved": True, "reviewed_by": reviewed_by, "ref": review_ref},
        "included_files_summary": {
            "total_included_files": len(included_files),
            "paths": list(included_files),
        },
        "asset_checksums": [
            {
                "asset_name": archive_asset_name,
                "algorithm": "sha256",
                "sha256": archive_checksum,
            }
        ],
        "safety_checks": _safety_checks(failed=False),
        "blocked_reason_codes": [],
        "non_claims": list(NON_CLAIMS),
    }


def _asset(asset_name: str, role: str, payload: bytes) -> dict[str, Any]:
    return {
        "asset_name": asset_name,
        "role": role,
        "algorithm": "sha256",
        "sha256": _sha256(payload),
        "byte_count": len(payload),
        "written": False,
        "published": False,
    }


def _checksums_text(entries: Sequence[tuple[str, str]]) -> str:
    return "".join(f"{checksum}  {asset_name}\n" for asset_name, checksum in entries)


def _validate_expected_checksums(
    planned_assets: Sequence[Mapping[str, Any]],
    expected_asset_checksums: Mapping[str, str],
) -> str | None:
    planned = {str(asset["asset_name"]): str(asset["sha256"]) for asset in planned_assets}
    for asset_name, expected in expected_asset_checksums.items():
        if asset_name not in planned:
            return "expected_asset_checksum_unknown"
        if planned[asset_name] != expected:
            return "asset_checksum_mismatch"
    return None


def _parse_expected_checksums(values: Sequence[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError("expected_asset_checksum_invalid")
        asset_name, checksum = value.split("=", 1)
        if not _is_safe_label(asset_name):
            raise ValueError("expected_asset_checksum_asset_name_invalid")
        if not re.fullmatch(r"[0-9a-f]{64}", checksum):
            raise ValueError("expected_asset_checksum_value_invalid")
        parsed[asset_name] = checksum
    return parsed


def _predecessor_ref(report: Mapping[str, Any] | None, source_commit: str | None) -> dict[str, Any]:
    if not report:
        return {"object": None, "schema_version": None, "status": "not_run", "source_commit": None}
    return {
        "object": _safe_value(report.get("object")),
        "schema_version": _safe_value(report.get("schema_version")),
        "status": _safe_value(report.get("status")),
        "source_commit": _safe_commit(source_commit or _optional_source_commit(report) or ""),
    }


def _path_ref(value: Any) -> dict[str, str]:
    if not isinstance(value, Mapping):
        return {"path": "invalid"}
    return {"path": _safe_path(value.get("path"))}


def _release_tag(package_version: str) -> str:
    return f"corpus-package-v{package_version}"


def _safe_release_tag(package_version: str) -> str:
    if not _is_safe_package_version(package_version):
        return "invalid"
    return _release_tag(package_version)


def _asset_names(package_version: str) -> dict[str, str]:
    prefix = f"mythic-edge-corpus-{package_version}"
    return {
        "archive": f"{prefix}.tar.gz",
        "metadata": f"{prefix}.metadata.json",
        "checksums": f"{prefix}.checksums.txt",
    }


def _json_bytes(payload: Mapping[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _clean_repo_relative_path(value: str | Path) -> Path:
    if not isinstance(value, (str, Path)):
        raise ValueError("path_not_string")
    text = str(value).replace("\\", "/")
    if LOCAL_OR_SECRET_MARKER_RE.search(text):
        raise ValueError("path_contains_local_or_secret_marker")
    path = Path(text)
    if path.is_absolute():
        raise ValueError("absolute_path")
    if any(part in ("", ".", "..") for part in path.parts):
        raise ValueError("path_traversal_or_empty_part")
    if any(part.startswith(".") for part in path.parts):
        raise ValueError("hidden_path")
    return Path(path.as_posix())


def _safe_path(value: Any) -> str:
    try:
        return _clean_repo_relative_path(value).as_posix()
    except ValueError:
        return "invalid"


def _safe_label(value: str | None) -> str:
    if value is None or not _is_safe_label(value):
        return "invalid"
    return value


def _is_safe_label(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and bool(REF_LABEL_RE.fullmatch(value)) and not LOCAL_OR_SECRET_MARKER_RE.search(value)


def _safe_reason(value: Any) -> str:
    if not _is_safe_label(value):
        return "invalid_reason"
    return str(value)


def _safe_value(value: Any) -> str | None:
    if value is None:
        return None
    if not _is_safe_label(value):
        return "invalid"
    return str(value)


def _safe_commit(value: str) -> str:
    return value if _is_commit(value) else "invalid"


def _is_commit(value: Any) -> bool:
    return isinstance(value, str) and bool(COMMIT_RE.fullmatch(value))


def _is_safe_package_version(value: Any) -> bool:
    return isinstance(value, str) and bool(PACKAGE_VERSION_RE.fullmatch(value)) and not LOCAL_OR_SECRET_MARKER_RE.search(value)


def _safety_checks(failed: bool) -> list[dict[str, str]]:
    status = "blocked" if failed else "passed"
    return [{"check": check, "status": status} for check in SAFETY_CHECKS]


if __name__ == "__main__":
    raise SystemExit(main())
