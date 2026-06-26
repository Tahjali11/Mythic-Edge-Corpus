#!/usr/bin/env python3
"""Report-only PR package-safety validation for public-safe corpus packages."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

OBJECT_TYPE = "corpus_pr_validation_package_safety"
SCHEMA_VERSION = "corpus_pr_validation_package_safety.v1"
REPOSITORY = "Tahjali11/Mythic-Edge-Corpus"
REPOSITORY_URL = "https://github.com/Tahjali11/Mythic-Edge-Corpus"

PASSED_REPORT_ONLY_STATUS = "passed_report_only"
PREVIEW_PASSED_STATUS = "preview_report_only"
PREVIEW_OBJECT = "corpus_local_package_preview"
PREVIEW_SCHEMA_VERSION = "corpus_local_package_preview.v1"

SAFETY_CHECKS = (
    "preview_command_required",
    "repo_relative_paths_only",
    "no_path_traversal",
    "package_root_only",
    "manifest_declared_files_only",
    "session_ledger_reconciled",
    "changed_files_reviewed",
    "no_raw_corpus_evidence",
    "no_private_logs",
    "no_generated_local_artifacts",
    "no_secret_or_connection_material",
    "no_release_artifacts",
    "no_dispatch_payloads",
    "no_ratchet_reports",
    "no_baseline_pr_artifacts",
    "no_source_repo_files",
    "no_external_corpus_contents",
    "no_auto_sanitization",
    "no_contributor_branch_writeback",
    "report_only_non_claims_present",
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
    "contributor_branch_rewritten": False,
    "package_artifact_created": False,
    "release_artifact_created": False,
    "repository_dispatch_sent": False,
    "ratchet_executed": False,
    "baseline_pr_created": False,
    "durable_validation_artifact_written": False,
}

BLOCKED_PREVIEW_STATUSES = {
    "blocked_missing_manifest",
    "blocked_missing_session_ledger",
    "blocked_invalid_metadata",
    "blocked_manifest_ledger_mismatch",
    "blocked_unsafe_path",
    "blocked_forbidden_content",
    "blocked_raw_or_private_input",
    "blocked_package_artifact",
}
PREVIEW_STATUS_MAP = {
    "blocked_missing_manifest": "blocked_missing_manifest",
    "blocked_missing_session_ledger": "blocked_missing_session_ledger",
    "blocked_invalid_metadata": "blocked_invalid_metadata",
    "blocked_manifest_ledger_mismatch": "blocked_manifest_ledger_mismatch",
    "blocked_unsafe_path": "blocked_unsafe_path",
    "blocked_forbidden_content": "blocked_forbidden_content",
    "blocked_raw_or_private_input": "blocked_raw_or_private_input",
    "blocked_package_artifact": "blocked_package_artifact",
}
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
REF_LABEL_RE = re.compile(r"^[A-Za-z0-9._/@{}:+-]+$")

DEFAULT_PREVIEW_BUILDER = object()
PreviewBuilder = Callable[..., Mapping[str, Any]]


def build_validation_report(
    *,
    base_ref: str,
    head_ref: str,
    package_root: str | Path,
    manifest_path: str | Path,
    session_ledger_path: str | Path,
    repo_root: str | Path | None = None,
    preview_builder: PreviewBuilder | None | object = DEFAULT_PREVIEW_BUILDER,
) -> dict[str, Any]:
    """Build a deterministic no-write PR validation report."""

    root = Path.cwd() if repo_root is None else Path(repo_root)
    ref_problem = _validate_ref_labels(base_ref, head_ref)
    path_problem = _validate_requested_paths(package_root, manifest_path, session_ledger_path)
    if ref_problem or path_problem:
        reason = ref_problem or path_problem or "unsafe_input"
        return _report(
            base_ref=_safe_label(base_ref),
            head_ref=_safe_label(head_ref),
            package_root=_safe_report_path(package_root),
            manifest_path=_safe_report_path(manifest_path),
            session_ledger_path=_safe_report_path(session_ledger_path),
            status="blocked_unsafe_path",
            preview_status="not_run",
            preview_summary={},
            changed_package_files=[],
            inventory_summary=_empty_inventory_summary(),
            manifest_session_summary=_empty_manifest_session_summary(),
            blocked_reason_codes=[reason],
            review_notes=["validation stopped before package preview because an input label or path was unsafe"],
        )

    builder = preview_builder
    if builder is DEFAULT_PREVIEW_BUILDER:
        builder = _load_preview_builder()
    if builder is None:
        return _report(
            base_ref=base_ref,
            head_ref=head_ref,
            package_root=str(package_root),
            manifest_path=str(manifest_path),
            session_ledger_path=str(session_ledger_path),
            status="blocked_missing_preview_command",
            preview_status="preview_missing",
            preview_summary={},
            changed_package_files=[],
            inventory_summary=_empty_inventory_summary(),
            manifest_session_summary=_empty_manifest_session_summary(),
            blocked_reason_codes=["preview_command_missing"],
            review_notes=["package preview command is required before PR package-safety validation"],
        )

    try:
        preview_report = dict(
            builder(
                package_root=package_root,
                manifest_path=manifest_path,
                session_ledger_path=session_ledger_path,
                repo_root=root,
            )
        )
    except Exception:  # noqa: BLE001 - fail closed without echoing exception values.
        return _report(
            base_ref=base_ref,
            head_ref=head_ref,
            package_root=str(package_root),
            manifest_path=str(manifest_path),
            session_ledger_path=str(session_ledger_path),
            status="blocked_preview_failed",
            preview_status="preview_failed",
            preview_summary={},
            changed_package_files=[],
            inventory_summary=_empty_inventory_summary(),
            manifest_session_summary=_empty_manifest_session_summary(),
            blocked_reason_codes=["preview_builder_failed"],
            review_notes=["package preview builder failed closed"],
        )

    invalid_reason = _validate_preview_shape(preview_report)
    if invalid_reason is None:
        invalid_reason = _validate_preview_public_safe_values(preview_report, package_root)
    if invalid_reason:
        return _report(
            base_ref=base_ref,
            head_ref=head_ref,
            package_root=str(package_root),
            manifest_path=str(manifest_path),
            session_ledger_path=str(session_ledger_path),
            status="blocked_preview_invalid_output",
            preview_status=_safe_preview_value(preview_report.get("status")) or "preview_invalid_output",
            preview_summary={},
            changed_package_files=[],
            inventory_summary=_empty_inventory_summary(),
            manifest_session_summary=_empty_manifest_session_summary(),
            blocked_reason_codes=[invalid_reason],
            review_notes=["package preview output was malformed or unsupported"],
        )

    preview_status = str(preview_report["status"])
    inventory = list(preview_report.get("inventory", []))
    blocked_reasons = _string_list(preview_report.get("blocked_reason_codes", []))
    if preview_status != PREVIEW_PASSED_STATUS:
        validation_status = PREVIEW_STATUS_MAP.get(preview_status, "blocked_preview_failed")
        reason_codes = blocked_reasons or [f"preview_status_{preview_status}"]
        return _report(
            base_ref=base_ref,
            head_ref=head_ref,
            package_root=str(package_root),
            manifest_path=str(manifest_path),
            session_ledger_path=str(session_ledger_path),
            status=validation_status,
            preview_status=preview_status,
            preview_summary=_preview_summary(preview_report),
            changed_package_files=[],
            inventory_summary=_inventory_summary(inventory),
            manifest_session_summary=_manifest_session_summary(preview_report),
            blocked_reason_codes=reason_codes,
            review_notes=["package preview did not pass, so PR validation failed closed"],
        )

    changed_files = [
        safe_path
        for item in inventory
        if isinstance(item, Mapping) and "path" in item
        for safe_path in [_safe_preview_path(item["path"])]
        if safe_path != "invalid"
    ]
    return _report(
        base_ref=base_ref,
        head_ref=head_ref,
        package_root=str(package_root),
        manifest_path=str(manifest_path),
        session_ledger_path=str(session_ledger_path),
        status=PASSED_REPORT_ONLY_STATUS,
        preview_status=preview_status,
        preview_summary=_preview_summary(preview_report),
        changed_package_files=sorted(changed_files),
        inventory_summary=_inventory_summary(inventory),
        manifest_session_summary=_manifest_session_summary(preview_report),
        blocked_reason_codes=[],
        review_notes=["validation passed as report-only package hygiene evidence"],
    )


def format_text(report: Mapping[str, Any]) -> str:
    """Render a deterministic text validation summary."""

    lines = [
        "Corpus PR Package-Safety Validation",
        f"schema_version: {report['schema_version']}",
        f"repository: {report['repository']}",
        f"base_ref: {report['base_ref']}",
        f"head_ref: {report['head_ref']}",
        f"package_root: {report['package_root']}",
        f"manifest: {report['manifest_ref']['path']}",
        f"session_ledger: {report['session_ledger_ref']['path']}",
        f"package_preview_status: {report['package_preview_ref']['status']}",
        f"status: {report['status']}",
        f"total_changed_package_files: {len(report['changed_package_files'])}",
        f"total_included_files: {report['inventory_summary']['total_included_files']}",
        f"total_manifest_entries: {report['manifest_session_summary']['total_manifest_entries']}",
        f"total_session_ledger_entries: {report['manifest_session_summary']['total_session_ledger_entries']}",
        "safety_checks:",
    ]
    lines.extend(f"- {item['check']}: {item['status']}" for item in report["safety_checks"])
    lines.append("changed_package_files:")
    if report["changed_package_files"]:
        lines.extend(f"- {path}" for path in report["changed_package_files"])
    else:
        lines.append("- none")
    lines.append("blocked_reason_codes:")
    if report["blocked_reason_codes"]:
        lines.extend(f"- {reason}" for reason in report["blocked_reason_codes"])
    else:
        lines.append("- none")
    lines.append("review_notes:")
    lines.extend(f"- {note}" for note in report["review_notes"])
    lines.append("non_claims:")
    lines.extend(f"- {claim}" for claim in report["non_claims"])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate public-safe corpus package changes for PR review.",
    )
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--head-ref", required=True)
    parser.add_argument("--package-root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--session-ledger", required=True)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    report = build_validation_report(
        base_ref=args.base_ref,
        head_ref=args.head_ref,
        package_root=args.package_root,
        manifest_path=args.manifest,
        session_ledger_path=args.session_ledger,
    )
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report), end="")
    return 0 if report["status"] == PASSED_REPORT_ONLY_STATUS else 2


def _report(
    *,
    base_ref: str,
    head_ref: str,
    package_root: str,
    manifest_path: str,
    session_ledger_path: str,
    status: str,
    preview_status: str,
    preview_summary: Mapping[str, Any],
    changed_package_files: list[str],
    inventory_summary: Mapping[str, Any],
    manifest_session_summary: Mapping[str, Any],
    blocked_reason_codes: list[str],
    review_notes: list[str],
) -> dict[str, Any]:
    failed = status != PASSED_REPORT_ONLY_STATUS
    return {
        "object": OBJECT_TYPE,
        "schema_version": SCHEMA_VERSION,
        "repository": REPOSITORY,
        "repository_url": REPOSITORY_URL,
        "base_ref": base_ref,
        "head_ref": head_ref,
        "package_root": package_root,
        "manifest_ref": {"path": manifest_path},
        "session_ledger_ref": {"path": session_ledger_path},
        "package_preview_ref": {
            "object": preview_summary.get("object"),
            "schema_version": preview_summary.get("schema_version"),
            "status": preview_status,
            "package_id": preview_summary.get("package_id"),
            "package_version": preview_summary.get("package_version"),
        },
        "status": status,
        "changed_package_files": changed_package_files,
        "inventory_summary": dict(inventory_summary),
        "manifest_session_summary": dict(manifest_session_summary),
        "safety_checks": _safety_checks(failed),
        "blocked_reason_codes": blocked_reason_codes,
        "review_notes": review_notes,
        "no_write_guards": dict(NO_WRITE_GUARDS),
        "non_claims": list(NON_CLAIMS),
    }


def _load_preview_builder() -> PreviewBuilder | None:
    preview_path = Path(__file__).resolve().with_name("corpus_package_preview.py")
    if not preview_path.exists():
        return None
    spec = importlib.util.spec_from_file_location("corpus_package_preview_for_pr_validation", preview_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    builder = getattr(module, "build_preview", None)
    if not callable(builder):
        return None
    return builder


def _validate_preview_shape(preview_report: Mapping[str, Any]) -> str | None:
    if preview_report.get("object") != PREVIEW_OBJECT:
        return "preview_object_unsupported"
    if preview_report.get("schema_version") != PREVIEW_SCHEMA_VERSION:
        return "preview_schema_version_unsupported"
    status = preview_report.get("status")
    if not isinstance(status, str) or status not in BLOCKED_PREVIEW_STATUSES | {PREVIEW_PASSED_STATUS}:
        return "preview_status_unsupported"
    if not isinstance(preview_report.get("summary"), Mapping):
        return "preview_summary_missing"
    if not isinstance(preview_report.get("inventory"), list):
        return "preview_inventory_missing"
    if not isinstance(preview_report.get("blocked_reason_codes"), list):
        return "preview_blocked_reasons_missing"
    return None


def _validate_preview_public_safe_values(
    preview_report: Mapping[str, Any],
    package_root: str | Path,
) -> str | None:
    try:
        package_rel = _clean_repo_relative_path(package_root)
    except ValueError:
        return "preview_package_root_unsafe"

    for field in ("package_id", "package_version"):
        value = preview_report.get(field)
        if value is not None and not _is_public_safe_preview_value(value):
            return f"preview_{field}_unsafe"

    summary = preview_report.get("summary")
    if isinstance(summary, Mapping):
        for field in ("total_declared_manifest_entries", "total_session_ledger_entries"):
            value = summary.get(field)
            if value is None:
                continue
            if not isinstance(value, int) or value < 0:
                return f"preview_summary_{field}_invalid"

    for item in preview_report.get("inventory", []):
        if not isinstance(item, Mapping):
            return "preview_inventory_entry_not_object"
        safe_path = _safe_preview_path(item.get("path"))
        if safe_path == "invalid":
            return "preview_inventory_path_unsafe"
        if not _is_preview_path_inside_package_root(safe_path, package_rel):
            return "preview_inventory_path_outside_package_root"
        session_id = item.get("session_id")
        if session_id is not None and not _is_public_safe_preview_value(session_id):
            return "preview_inventory_session_id_unsafe"

    for reason in preview_report.get("blocked_reason_codes", []):
        if _safe_preview_reason(reason) == "invalid_reason":
            return "preview_blocked_reason_unsafe"

    return None


def _validate_ref_labels(base_ref: str, head_ref: str) -> str | None:
    for label, value in (("base_ref", base_ref), ("head_ref", head_ref)):
        if not isinstance(value, str) or not value:
            return f"{label}_missing"
        if not REF_LABEL_RE.fullmatch(value) or LOCAL_OR_SECRET_MARKER_RE.search(value):
            return f"{label}_unsafe"
    return None


def _validate_requested_paths(
    package_root: str | Path,
    manifest_path: str | Path,
    session_ledger_path: str | Path,
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
    return None


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


def _safe_report_path(value: str | Path) -> str:
    try:
        return _clean_repo_relative_path(value).as_posix()
    except ValueError:
        return "invalid"


def _safe_label(value: str) -> str:
    if not isinstance(value, str) or not value or LOCAL_OR_SECRET_MARKER_RE.search(value):
        return "invalid"
    if not REF_LABEL_RE.fullmatch(value):
        return "invalid"
    return value


def _preview_summary(preview_report: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "object": _safe_preview_value(preview_report.get("object")),
        "schema_version": _safe_preview_value(preview_report.get("schema_version")),
        "status": _safe_preview_value(preview_report.get("status")),
        "package_id": _safe_preview_value(preview_report.get("package_id")),
        "package_version": _safe_preview_value(preview_report.get("package_version")),
    }


def _inventory_summary(inventory: Sequence[Any]) -> dict[str, Any]:
    paths = [
        safe_path
        for item in inventory
        if isinstance(item, Mapping) and isinstance(item.get("path"), str)
        for safe_path in [_safe_preview_path(item["path"])]
        if safe_path != "invalid"
    ]
    session_ids = {
        str(item["session_id"])
        for item in inventory
        if isinstance(item, Mapping) and item.get("session_id")
    }
    return {
        "total_included_files": len(paths),
        "total_session_backed_files": len(session_ids),
        "paths": sorted(paths),
    }


def _manifest_session_summary(preview_report: Mapping[str, Any]) -> dict[str, Any]:
    summary = preview_report.get("summary")
    if not isinstance(summary, Mapping):
        return _empty_manifest_session_summary()
    return {
        "total_manifest_entries": int(summary.get("total_declared_manifest_entries") or 0),
        "total_session_ledger_entries": int(summary.get("total_session_ledger_entries") or 0),
    }


def _empty_inventory_summary() -> dict[str, Any]:
    return {"total_included_files": 0, "total_session_backed_files": 0, "paths": []}


def _empty_manifest_session_summary() -> dict[str, Any]:
    return {"total_manifest_entries": 0, "total_session_ledger_entries": 0}


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [_safe_preview_reason(item) for item in value]


def _safe_preview_value(value: Any) -> str | None:
    if value is None:
        return None
    if not _is_public_safe_preview_value(value):
        return "invalid"
    return value


def _safe_preview_path(value: Any) -> str:
    try:
        return _clean_repo_relative_path(value).as_posix()
    except ValueError:
        return "invalid"


def _is_preview_path_inside_package_root(path: str, package_root: Path) -> bool:
    package_text = package_root.as_posix()
    return path == package_text or path.startswith(package_text + "/")


def _safe_preview_reason(value: Any) -> str:
    if not isinstance(value, str):
        return "invalid_reason"
    if not REF_LABEL_RE.fullmatch(value) or LOCAL_OR_SECRET_MARKER_RE.search(value):
        return "invalid_reason"
    return value


def _is_public_safe_preview_value(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and not LOCAL_OR_SECRET_MARKER_RE.search(value)


def _safety_checks(failed: bool) -> list[dict[str, str]]:
    status = "blocked" if failed else "passed"
    return [{"check": check, "status": status} for check in SAFETY_CHECKS]


if __name__ == "__main__":
    raise SystemExit(main())
