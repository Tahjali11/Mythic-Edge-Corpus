#!/usr/bin/env python3
"""Local report-only preview for public-safe corpus package metadata."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

OBJECT_TYPE = "corpus_local_package_preview"
SCHEMA_VERSION = "corpus_local_package_preview.v1"
REPOSITORY = "Tahjali11/Mythic-Edge-Corpus"
REPOSITORY_URL = "https://github.com/Tahjali11/Mythic-Edge-Corpus"
MANIFEST_SCHEMA_VERSION = "mythic_edge_corpus_package_manifest.v1"
SESSION_LEDGER_SCHEMA_VERSION = "mythic_edge_corpus_session_ledger.v1"

PREVIEW_REPORT_ONLY_STATUS = "preview_report_only"
NON_CLAIMS = (
    "not_parser_truth",
    "not_fixture_promotion",
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
SAFETY_CHECKS = (
    "repo_relative_paths_only",
    "no_path_traversal",
    "package_root_only",
    "manifest_declared_files_only",
    "session_ledger_reconciled",
    "no_raw_corpus_evidence",
    "no_private_logs",
    "no_generated_local_artifacts",
    "no_secrets_or_connection_material",
    "no_release_artifacts",
    "no_dispatch_payloads",
    "no_ratchet_reports",
    "no_baseline_pr_artifacts",
    "no_source_repo_files",
    "no_external_corpus_contents",
    "stdout_only",
    "report_only_non_claims_present",
)
ALLOWED_SUFFIXES = {".json", ".md", ".txt"}
PACKAGE_ARTIFACT_SUFFIXES = {
    ".zip",
    ".tar",
    ".tgz",
    ".whl",
    ".gz",
    ".bz2",
    ".xz",
}
RAW_OR_LOCAL_SUFFIXES = {
    ".log",
    ".jsonl",
    ".sqlite",
    ".sqlite3",
    ".db",
    ".wal",
    ".shm",
}
GENERATED_OR_RUNTIME_PARTS = {
    "__pycache__",
    ".pytest_cache",
    "build",
    "dist",
    "runtime",
    "runtime_logs",
    "failed_posts",
    "status",
    "tmp",
    "temp",
}
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


class PreviewError(ValueError):
    """Fail-closed preview error with a symbolic status and reason code."""

    def __init__(self, status: str, reason_code: str) -> None:
        super().__init__(reason_code)
        self.status = status
        self.reason_code = reason_code


def build_preview(
    *,
    package_root: str | Path,
    manifest_path: str | Path,
    session_ledger_path: str | Path,
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    """Build a deterministic report-only preview object."""

    root = Path.cwd() if repo_root is None else Path(repo_root)
    try:
        package_rel = _clean_repo_relative_path(package_root)
        manifest_rel = _clean_repo_relative_path(manifest_path)
        ledger_rel = _clean_repo_relative_path(session_ledger_path)
        package_abs = _resolve_inside(root, package_rel)
        manifest_abs = _resolve_inside(root, manifest_rel)
        ledger_abs = _resolve_inside(root, ledger_rel)
        if not package_abs.exists() or not package_abs.is_dir():
            raise PreviewError("blocked_unsafe_path", "package_root_missing_or_not_directory")
        if not manifest_abs.exists():
            raise PreviewError("blocked_missing_manifest", "manifest_missing")
        if not ledger_abs.exists():
            raise PreviewError("blocked_missing_session_ledger", "session_ledger_missing")
        if not _is_relative_to(manifest_abs, package_abs) or not _is_relative_to(ledger_abs, package_abs):
            raise PreviewError("blocked_unsafe_path", "metadata_paths_must_be_inside_package_root")

        manifest = _load_json(manifest_abs, "manifest")
        ledger = _load_json(ledger_abs, "session_ledger")
        manifest_entries = _validate_manifest(manifest, package_rel)
        ledger_entries = _validate_session_ledger(ledger)
        inventory_paths = _inventory_paths(package_abs, root)

        _validate_declared_paths(
            declared_paths={entry["path"] for entry in manifest_entries},
            inventory_paths=set(inventory_paths),
        )
        _validate_manifest_ledger_relationship(manifest_entries, ledger_entries)
        inventory = _build_inventory(manifest_entries, ledger_entries)

        for rel_path in inventory_paths:
            _scan_public_safe_content(root / rel_path)

        return _report(
            status=PREVIEW_REPORT_ONLY_STATUS,
            package_id=str(manifest["package_id"]),
            package_version=str(manifest["package_version"]),
            manifest_path=str(manifest_rel),
            manifest_schema_version=str(manifest["schema_version"]),
            ledger_path=str(ledger_rel),
            ledger_schema_version=str(ledger["schema_version"]),
            package_root=str(package_rel),
            inventory=inventory,
            blocked_reason_codes=[],
        )
    except PreviewError as error:
        return _report(
            status=error.status,
            package_id=None,
            package_version=None,
            manifest_path=_safe_report_path(manifest_path),
            manifest_schema_version=None,
            ledger_path=_safe_report_path(session_ledger_path),
            ledger_schema_version=None,
            package_root=_safe_report_path(package_root),
            inventory=[],
            blocked_reason_codes=[error.reason_code],
        )


def format_text(report: Mapping[str, Any]) -> str:
    """Render a deterministic text preview."""

    lines = [
        "Corpus Package Preview",
        f"schema_version: {report['schema_version']}",
        f"status: {report['status']}",
        f"package_id: {report.get('package_id') or 'unknown'}",
        f"package_version: {report.get('package_version') or 'unknown'}",
        f"manifest: {report['manifest_ref']['path']}",
        f"session_ledger: {report['session_ledger_ref']['path']}",
        f"package_root: {report['package_root']}",
        f"total_included_files: {report['summary']['total_included_files']}",
        f"total_declared_manifest_entries: {report['summary']['total_declared_manifest_entries']}",
        f"total_session_ledger_entries: {report['summary']['total_session_ledger_entries']}",
        "safety_checks:",
    ]
    lines.extend(f"- {check['check']}: {check['status']}" for check in report["safety_checks"])
    lines.append("inventory:")
    if report["inventory"]:
        for item in report["inventory"]:
            session_id = item.get("session_id") or "-"
            lines.append(f"- {item['path']} | {item['role']} | session={session_id}")
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
    parser = argparse.ArgumentParser(description="Preview a local public-safe corpus package.")
    parser.add_argument("--package-root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--session-ledger", required=True)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    report = build_preview(
        package_root=args.package_root,
        manifest_path=args.manifest,
        session_ledger_path=args.session_ledger,
    )
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report), end="")
    return 0 if report["status"] == PREVIEW_REPORT_ONLY_STATUS else 2


def _report(
    *,
    status: str,
    package_id: str | None,
    package_version: str | None,
    manifest_path: str | None,
    manifest_schema_version: str | None,
    ledger_path: str | None,
    ledger_schema_version: str | None,
    package_root: str | None,
    inventory: list[dict[str, Any]],
    blocked_reason_codes: list[str],
) -> dict[str, Any]:
    return {
        "object": OBJECT_TYPE,
        "schema_version": SCHEMA_VERSION,
        "repository": REPOSITORY,
        "repository_url": REPOSITORY_URL,
        "package_id": package_id,
        "package_version": package_version,
        "manifest_ref": {
            "path": manifest_path or "invalid",
            "schema_version": manifest_schema_version,
        },
        "session_ledger_ref": {
            "path": ledger_path or "invalid",
            "schema_version": ledger_schema_version,
        },
        "package_root": package_root or "invalid",
        "status": status,
        "summary": {
            "total_included_files": len(inventory),
            "total_declared_manifest_entries": len(inventory),
            "total_session_ledger_entries": len(
                {item["session_id"] for item in inventory if item.get("session_id")}
            ),
        },
        "inventory": inventory,
        "safety_checks": _safety_checks(status),
        "blocked_reason_codes": blocked_reason_codes,
        "non_claims": list(NON_CLAIMS),
    }


def _safety_checks(status: str) -> list[dict[str, str]]:
    check_status = "passed" if status == PREVIEW_REPORT_ONLY_STATUS else "blocked"
    return [{"check": check, "status": check_status} for check in SAFETY_CHECKS]


def _load_json(path: Path, label: str) -> dict[str, Any]:
    if path.suffix != ".json":
        raise PreviewError("blocked_invalid_metadata", f"{label}_must_be_json")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PreviewError("blocked_invalid_metadata", f"{label}_malformed") from exc
    if not isinstance(data, dict):
        raise PreviewError("blocked_invalid_metadata", f"{label}_not_object")
    return data


def _validate_manifest(manifest: Mapping[str, Any], package_root: Path) -> list[dict[str, Any]]:
    required = {"object", "schema_version", "package_id", "package_version", "package_root", "entries"}
    if not required.issubset(manifest):
        raise PreviewError("blocked_invalid_metadata", "manifest_missing_required_fields")
    if manifest["schema_version"] != MANIFEST_SCHEMA_VERSION:
        raise PreviewError("blocked_invalid_metadata", "manifest_schema_version_unsupported")
    if manifest["package_root"] != str(package_root):
        raise PreviewError("blocked_invalid_metadata", "manifest_package_root_mismatch")
    entries = manifest["entries"]
    if not isinstance(entries, list) or not entries:
        raise PreviewError("blocked_invalid_metadata", "manifest_entries_not_non_empty_list")

    normalized_entries: list[dict[str, Any]] = []
    seen_paths: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise PreviewError("blocked_invalid_metadata", "manifest_entry_not_object")
        for field in ("path", "role", "public_safe"):
            if field not in entry:
                raise PreviewError("blocked_invalid_metadata", "manifest_entry_missing_required_field")
        rel_path = _clean_repo_relative_path(entry["path"])
        if not str(rel_path).startswith(str(package_root) + "/"):
            raise PreviewError("blocked_unsafe_path", "manifest_entry_outside_package_root")
        _validate_allowed_package_path(rel_path)
        if rel_path.as_posix() in seen_paths:
            raise PreviewError("blocked_invalid_metadata", "manifest_duplicate_entry_path")
        seen_paths.add(rel_path.as_posix())
        if entry["public_safe"] is not True:
            raise PreviewError("blocked_raw_or_private_input", "manifest_entry_not_public_safe")
        normalized_entries.append(
            {
                "path": rel_path.as_posix(),
                "role": str(entry["role"]),
                "public_safe": True,
                "session_id": entry.get("session_id"),
            }
        )
    return sorted(normalized_entries, key=lambda item: item["path"])


def _validate_session_ledger(ledger: Mapping[str, Any]) -> dict[str, set[str]]:
    required = {"object", "schema_version", "ledger_id", "entries"}
    if not required.issubset(ledger):
        raise PreviewError("blocked_invalid_metadata", "session_ledger_missing_required_fields")
    if ledger["schema_version"] != SESSION_LEDGER_SCHEMA_VERSION:
        raise PreviewError("blocked_invalid_metadata", "session_ledger_schema_version_unsupported")
    entries = ledger["entries"]
    if not isinstance(entries, list):
        raise PreviewError("blocked_invalid_metadata", "session_ledger_entries_not_list")

    by_session: dict[str, set[str]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise PreviewError("blocked_invalid_metadata", "session_ledger_entry_not_object")
        if not entry.get("public_safe"):
            raise PreviewError("blocked_raw_or_private_input", "session_ledger_entry_not_public_safe")
        session_id = entry.get("session_id")
        paths = entry.get("paths")
        if not isinstance(session_id, str) or not session_id:
            raise PreviewError("blocked_invalid_metadata", "session_ledger_entry_missing_session_id")
        if not isinstance(paths, list) or not paths:
            raise PreviewError("blocked_invalid_metadata", "session_ledger_entry_missing_paths")
        normalized_paths: set[str] = set()
        for path in paths:
            rel_path = _clean_repo_relative_path(path)
            _validate_allowed_package_path(rel_path)
            normalized_paths.add(rel_path.as_posix())
        if session_id in by_session:
            raise PreviewError("blocked_invalid_metadata", "session_ledger_duplicate_session_id")
        by_session[session_id] = normalized_paths
    return by_session


def _validate_manifest_ledger_relationship(
    manifest_entries: Sequence[Mapping[str, Any]],
    ledger_entries: Mapping[str, set[str]],
) -> None:
    manifest_session_paths = {
        entry["path"]: entry["session_id"] for entry in manifest_entries if entry.get("session_id")
    }
    for path, session_id in manifest_session_paths.items():
        if session_id not in ledger_entries:
            raise PreviewError("blocked_manifest_ledger_mismatch", "manifest_session_missing_from_ledger")
        if path not in ledger_entries[session_id]:
            raise PreviewError("blocked_manifest_ledger_mismatch", "manifest_path_missing_from_ledger")
    manifest_paths = {entry["path"] for entry in manifest_entries}
    for session_id, paths in ledger_entries.items():
        if not paths & manifest_paths:
            raise PreviewError("blocked_manifest_ledger_mismatch", "ledger_entry_not_in_manifest")
        for path in paths:
            if path not in manifest_paths:
                raise PreviewError("blocked_manifest_ledger_mismatch", "ledger_path_not_in_manifest")
            if manifest_session_paths.get(path) != session_id:
                raise PreviewError("blocked_manifest_ledger_mismatch", "ledger_session_path_conflict")


def _validate_declared_paths(*, declared_paths: set[str], inventory_paths: set[Path]) -> None:
    inventory = {path.as_posix() for path in inventory_paths}
    if missing := sorted(declared_paths - inventory):
        _raise_path_set_error(missing, "blocked_manifest_ledger_mismatch", "manifest_entry_missing_from_disk")
    if undeclared := sorted(inventory - declared_paths):
        _raise_path_set_error(undeclared, "blocked_manifest_ledger_mismatch", "package_file_missing_from_manifest")


def _raise_path_set_error(paths: list[str], status: str, reason: str) -> None:
    for path in paths:
        _validate_allowed_package_path(Path(path))
    raise PreviewError(status, reason)


def _inventory_paths(package_abs: Path, repo_root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in sorted(package_abs.rglob("*")):
        if not path.is_file():
            continue
        if path.is_symlink():
            raise PreviewError("blocked_unsafe_path", "symlink_package_file")
        resolved = path.resolve()
        if not _is_relative_to(resolved, repo_root.resolve()):
            raise PreviewError("blocked_unsafe_path", "package_file_outside_repo")
        rel_path = Path(resolved.relative_to(repo_root.resolve()).as_posix())
        _validate_allowed_package_path(rel_path)
        paths.append(rel_path)
    return sorted(paths, key=lambda item: item.as_posix())


def _build_inventory(
    manifest_entries: Sequence[Mapping[str, Any]],
    ledger_entries: Mapping[str, set[str]],
) -> list[dict[str, Any]]:
    session_by_path = {
        path: session_id for session_id, paths in ledger_entries.items() for path in paths
    }
    return [
        {
            "path": entry["path"],
            "role": entry["role"],
            "public_safe": True,
            "session_id": entry.get("session_id"),
            "ledger_entry_present": entry["path"] in session_by_path,
        }
        for entry in sorted(manifest_entries, key=lambda item: item["path"])
    ]


def _scan_public_safe_content(path: Path) -> None:
    if path.suffix not in ALLOWED_SUFFIXES:
        raise PreviewError("blocked_unsafe_path", "unsupported_file_suffix")
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise PreviewError("blocked_raw_or_private_input", "non_text_file") from exc
    if FORBIDDEN_CONTENT_RE.search(text):
        raise PreviewError("blocked_forbidden_content", "forbidden_content_marker")


def _clean_repo_relative_path(value: str | Path) -> Path:
    if not isinstance(value, (str, Path)):
        raise PreviewError("blocked_unsafe_path", "path_not_string")
    text = str(value).replace("\\", "/")
    path = Path(text)
    if path.is_absolute():
        raise PreviewError("blocked_unsafe_path", "absolute_path")
    if any(part in ("", ".", "..") for part in path.parts):
        raise PreviewError("blocked_unsafe_path", "path_traversal_or_empty_part")
    if any(part.startswith(".") for part in path.parts):
        raise PreviewError("blocked_unsafe_path", "hidden_path")
    return Path(path.as_posix())


def _resolve_inside(repo_root: Path, rel_path: Path) -> Path:
    resolved_root = repo_root.resolve()
    resolved = (resolved_root / rel_path).resolve()
    if not _is_relative_to(resolved, resolved_root):
        raise PreviewError("blocked_unsafe_path", "path_outside_repo")
    return resolved


def _validate_allowed_package_path(path: Path) -> None:
    path = _clean_repo_relative_path(path)
    parts = set(path.parts)
    if parts & GENERATED_OR_RUNTIME_PARTS:
        raise PreviewError("blocked_unsafe_path", "generated_runtime_or_cache_path")
    suffix = path.suffix.lower()
    if suffix in PACKAGE_ARTIFACT_SUFFIXES:
        raise PreviewError("blocked_package_artifact", "package_artifact_suffix")
    if suffix in RAW_OR_LOCAL_SUFFIXES:
        raise PreviewError("blocked_raw_or_private_input", "raw_or_local_artifact_suffix")
    if suffix not in ALLOWED_SUFFIXES:
        raise PreviewError("blocked_unsafe_path", "unsupported_file_suffix")


def _safe_report_path(value: str | Path) -> str | None:
    try:
        return _clean_repo_relative_path(value).as_posix()
    except PreviewError:
        return "invalid"


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _iter_scalar_values(value: Any) -> Iterable[Any]:
    if isinstance(value, dict):
        for item in value.values():
            yield from _iter_scalar_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from _iter_scalar_values(item)
    else:
        yield value


if __name__ == "__main__":
    raise SystemExit(main())
