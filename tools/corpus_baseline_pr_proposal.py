#!/usr/bin/env python3
"""No-write baseline PR proposal preview after corpus ratchet comparison."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

try:
    from corpus_ratchet_comparison_report import validate_ratchet_report
except ModuleNotFoundError:  # pragma: no cover - import style depends on caller
    import importlib.util

    _RATCHET_MODULE_PATH = Path(__file__).with_name("corpus_ratchet_comparison_report.py")
    _RATCHET_SPEC = importlib.util.spec_from_file_location(
        "corpus_ratchet_comparison_report",
        _RATCHET_MODULE_PATH,
    )
    if _RATCHET_SPEC is not None and _RATCHET_SPEC.loader is not None:
        _RATCHET_MODULE = importlib.util.module_from_spec(_RATCHET_SPEC)
        _RATCHET_SPEC.loader.exec_module(_RATCHET_MODULE)
        validate_ratchet_report = _RATCHET_MODULE.validate_ratchet_report
    else:
        validate_ratchet_report = None

OBJECT_TYPE = "corpus_baseline_pr_proposal"
SCHEMA_VERSION = "corpus_baseline_pr_proposal.v1"
SOURCE_REPOSITORY = "Tahjali11/Mythic-Edge-Corpus"
SOURCE_REPOSITORY_URL = "https://github.com/Tahjali11/Mythic-Edge-Corpus"
TARGET_REPOSITORY = "Tahjali11/Mythic-Edge"
TARGET_REPOSITORY_URL = "https://github.com/Tahjali11/Mythic-Edge"
TARGET_BASE_BRANCH = "main"
RELEASE_CHANNEL = "reviewed"

ELIGIBLE_RATCHET_STATUSES = {
    "comparison_report_ready_for_review",
    "comparison_completed_with_deltas",
    "comparison_completed_with_no_deltas",
}
READY_PROPOSAL_STATUSES = {
    "proposal_preview_ready_for_review",
    "proposal_preview_no_deltas",
    "proposal_preview_degraded",
}
PROPOSAL_STATUSES = READY_PROPOSAL_STATUSES | {
    "contract_only",
    "proposal_blocked_missing_ratchet_report",
    "proposal_blocked_ineligible_ratchet_status",
    "proposal_blocked_missing_integrity_metadata",
    "proposal_blocked_checksum_or_release_mismatch",
    "proposal_blocked_stale_report",
    "proposal_blocked_forbidden_content",
    "proposal_blocked_raw_or_private_input",
    "proposal_blocked_source_action_requested",
    "proposal_blocked_baseline_mutation_requested",
    "proposal_blocked_ratchet_execution_requested",
    "proposal_blocked_release_or_dispatch_requested",
    "proposal_blocked_missing_human_review",
    "review_required",
    "unsupported",
    "invalid",
}
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
    "not_security_assurance",
    "not_privacy_assurance",
    "not_full_corpus_parity",
    "not_source_repo_action",
    "not_baseline_mutation",
    "not_ratchet_execution",
)
NO_WRITE_GUARDS = {
    "baseline_mutated": False,
    "baseline_pr_created": False,
    "source_branch_created": False,
    "source_commit_created": False,
    "source_pr_created": False,
    "source_comment_created": False,
    "source_status_check_created": False,
    "source_review_created": False,
    "source_label_created": False,
    "ratchet_executed": False,
    "release_published": False,
    "repository_dispatch_sent": False,
    "mythic_edge_mutated": False,
}
REQUIRED_PROPOSAL_KEYS = {
    "object",
    "schema_version",
    "proposal_id",
    "proposal_status",
    "source_repository",
    "source_repository_url",
    "target_repository",
    "target_repository_url",
    "package_id",
    "package_version",
    "release_tag",
    "release_url",
    "release_source_commit",
    "release_channel",
    "release_metadata_ref",
    "checksum_ref",
    "asset_checksums_verified",
    "ratchet_report_id",
    "ratchet_report_ref",
    "ratchet_report_status",
    "mythic_edge_commit",
    "mythic_edge_base_branch",
    "mythic_edge_candidate_branch_name",
    "draft_pr_title",
    "draft_pr_body_sections",
    "changed_output_summary",
    "validation_summary",
    "review_gate_refs",
    "blocked_reason_codes",
    "no_write_guards",
    "non_claims",
}
SUMMARY_KEYS = {
    "total_cases",
    "matched_expected_output",
    "new_passes",
    "new_failures",
    "changed_outputs",
    "missing_families",
    "missing_cases",
    "extra_outputs",
    "degraded_evidence",
    "unsupported",
    "review_required",
}
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9._/@{}:+-]+$")
PACKAGE_VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")
GITHUB_RELEASE_URL_RE = re.compile(
    r"^https://github\.com/Tahjali11/Mythic-Edge-Corpus/releases/"
    r"(?:tag|download)/[A-Za-z0-9._+/-]+$",
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
SOURCE_PATCH_MARKER_RE = re.compile(
    r"(diff --git|@@\s|^\+\+\+\s|^---\s|source patch|source snippet)",
    re.IGNORECASE | re.MULTILINE,
)
STRONG_CLAIM_RE = re.compile(
    r"\b("
    r"parser truth|fixture promotion|baseline approved|baseline approval|"
    r"corpus ready|release ready|deploy ready|production ready|"
    r"full corpus parity|security assurance|privacy assurance"
    r")\b",
    re.IGNORECASE,
)
ACTION_REQUEST_REASONS = (
    (
        re.compile(r"\b(source[_ -]?branch|branch).*\b(creat|open|request|push|write)", re.IGNORECASE),
        "proposal_requests_source_branch",
    ),
    (
        re.compile(r"\b(creat|open|request|push|write).*\b(source[_ -]?branch|branch)", re.IGNORECASE),
        "proposal_requests_source_branch",
    ),
    (
        re.compile(r"\b(source[_ -]?commit|commit).*\b(creat|push|write|request)", re.IGNORECASE),
        "proposal_requests_source_commit",
    ),
    (
        re.compile(r"\b(creat|push|write|request).*\b(source[_ -]?commit|commit)", re.IGNORECASE),
        "proposal_requests_source_commit",
    ),
    (
        re.compile(r"\b(source[_ -]?pr|pull request|pr).*\b(creat|open|request)", re.IGNORECASE),
        "proposal_requests_source_pr",
    ),
    (
        re.compile(r"\b(creat|open|request).*\b(source[_ -]?pr|pull request|pr)", re.IGNORECASE),
        "proposal_requests_source_pr",
    ),
    (
        re.compile(r"\b(comment).*\b(creat|post|add|request)", re.IGNORECASE),
        "proposal_requests_source_comment",
    ),
    (
        re.compile(r"\b(creat|post|add|request).*\b(comment)", re.IGNORECASE),
        "proposal_requests_source_comment",
    ),
    (
        re.compile(r"\b(status[_ -]?check).*\b(creat|post|set|request)", re.IGNORECASE),
        "proposal_requests_source_status_check",
    ),
    (
        re.compile(r"\b(creat|post|set|request).*\b(status[_ -]?check)", re.IGNORECASE),
        "proposal_requests_source_status_check",
    ),
    (
        re.compile(r"\b(review).*\b(creat|submit|request)", re.IGNORECASE),
        "proposal_requests_source_review",
    ),
    (
        re.compile(r"\b(creat|submit|request).*\b(review)", re.IGNORECASE),
        "proposal_requests_source_review",
    ),
    (
        re.compile(r"\b(label).*\b(creat|add|apply|request)", re.IGNORECASE),
        "proposal_requests_source_label",
    ),
    (
        re.compile(r"\b(creat|add|apply|request).*\b(label)", re.IGNORECASE),
        "proposal_requests_source_label",
    ),
    (
        re.compile(r"\b(baseline).*\b(mutat|modify|update|write|request|apply)", re.IGNORECASE),
        "proposal_requests_baseline_mutation",
    ),
    (
        re.compile(r"\b(mutat|modify|update|write|request|apply).*\b(baseline)", re.IGNORECASE),
        "proposal_requests_baseline_mutation",
    ),
    (
        re.compile(r"\b(ratchet).*\b(run|execute|request)", re.IGNORECASE),
        "proposal_requests_ratchet_execution",
    ),
    (
        re.compile(r"\b(run|execute|request).*\b(ratchet)", re.IGNORECASE),
        "proposal_requests_ratchet_execution",
    ),
    (
        re.compile(r"\b(release).*\b(publish|request)", re.IGNORECASE),
        "proposal_requests_release_publishing",
    ),
    (
        re.compile(r"\b(publish|request).*\b(release)", re.IGNORECASE),
        "proposal_requests_release_publishing",
    ),
    (
        re.compile(r"\b(repository[_ -]?dispatch|dispatch).*\b(send|request)", re.IGNORECASE),
        "proposal_requests_repository_dispatch",
    ),
    (
        re.compile(r"\b(send|request).*\b(repository[_ -]?dispatch|dispatch)", re.IGNORECASE),
        "proposal_requests_repository_dispatch",
    ),
)
ACTION_KEY_REASONS = (
    (
        re.compile(r"\b(source_repo_)?source_branch_(created|requested)$|\bsource_repo_branch_(created|requested)$"),
        "proposal_requests_source_branch",
    ),
    (
        re.compile(r"\b(source_repo_)?source_commit_(created|requested)$|\bsource_repo_mutation_(created|requested)$"),
        "proposal_requests_source_commit",
    ),
    (
        re.compile(r"\b(source_repo_)?source_pr_(created|requested)$|\b(source_repo_)?pr_(created|requested)$|\bbaseline_pr_(created|requested)$"),
        "proposal_requests_source_pr",
    ),
    (
        re.compile(r"\b(source_repo_)?source_comment_(created|requested)$|\b(source_repo_)?comment_(created|requested)$"),
        "proposal_requests_source_comment",
    ),
    (
        re.compile(r"\b(source_repo_)?source_status_check_(created|requested)$|\b(source_repo_)?status_check_(created|requested)$"),
        "proposal_requests_source_status_check",
    ),
    (
        re.compile(r"\b(source_repo_)?source_review_(created|requested)$|\b(source_repo_)?review_(created|requested)$"),
        "proposal_requests_source_review",
    ),
    (
        re.compile(r"\b(source_repo_)?source_label_(created|requested)$|\b(source_repo_)?label_(created|requested)$"),
        "proposal_requests_source_label",
    ),
    (re.compile(r"\bbaseline_(mutated|mutation_requested)$"), "proposal_requests_baseline_mutation"),
    (re.compile(r"\bratchet_(executed|execution_requested)$"), "proposal_requests_ratchet_execution"),
    (re.compile(r"\brelease_(published|publishing_requested)$"), "proposal_requests_release_publishing"),
    (re.compile(r"\brepository_dispatch_(sent|requested)$"), "proposal_requests_repository_dispatch"),
    (re.compile(r"\bmythic_edge_mutated$"), "proposal_requests_source_commit"),
)
ALLOWED_KEY_TEXT = (
    REQUIRED_PROPOSAL_KEYS
    | SUMMARY_KEYS
    | set(NO_WRITE_GUARDS)
    | set(NON_CLAIMS)
    | PROPOSAL_STATUSES
    | ELIGIBLE_RATCHET_STATUSES
)
ALLOWED_SYMBOLIC_TEXT = ALLOWED_KEY_TEXT | {
    "blocked_baseline_mutation_requested",
    "blocked_baseline_pr_requested",
    "blocked_source_mutation_requested",
    "blocked_release_or_dispatch_requested",
    "baseline_mutation_requested",
    "baseline_pr_requested",
    "source_mutation_requested",
    "release_or_dispatch_requested",
    "ratchet_execution_requested",
}


def build_baseline_pr_proposal(
    *,
    ratchet_report: Mapping[str, Any] | None,
    ratchet_report_ref: str | None = None,
    package_preview_ref: Mapping[str, Any] | None = None,
    pr_validation_ref: Mapping[str, Any] | None = None,
    release_review_ref: Mapping[str, Any] | None = None,
    dispatch_or_manual_selection_ref: Mapping[str, Any] | None = None,
    human_proposal_review_ref: Mapping[str, Any] | None = None,
    expected_package_version: str | None = None,
    expected_release_tag: str | None = None,
    expected_release_source_commit: str | None = None,
    expected_mythic_edge_commit: str | None = None,
    baseline_mutation_requested: bool = False,
    baseline_pr_requested: bool = False,
    source_action_requested: bool = False,
    ratchet_execution_requested: bool = False,
    release_or_dispatch_requested: bool = False,
) -> dict[str, Any]:
    """Build a public-safe no-write baseline proposal preview."""

    action_block = _requested_action_block(
        baseline_mutation_requested=baseline_mutation_requested,
        baseline_pr_requested=baseline_pr_requested,
        source_action_requested=source_action_requested,
        ratchet_execution_requested=ratchet_execution_requested,
        release_or_dispatch_requested=release_or_dispatch_requested,
    )
    if action_block:
        return _base_proposal(status=action_block[0], blocked_reason_codes=[action_block[1]])
    if ratchet_report is None:
        return _base_proposal(
            status="proposal_blocked_missing_ratchet_report",
            blocked_reason_codes=["missing_ratchet_report"],
        )

    safety_reason = _public_safety_reason(ratchet_report)
    if safety_reason:
        return _base_proposal(
            status="proposal_blocked_forbidden_content",
            blocked_reason_codes=[safety_reason],
        )

    schema_errors = _validate_ratchet_input(ratchet_report)
    if schema_errors:
        return _base_proposal(status="invalid", blocked_reason_codes=[schema_errors[0]])

    ratchet_status = str(ratchet_report.get("comparison_status"))
    if ratchet_status not in ELIGIBLE_RATCHET_STATUSES:
        return _base_proposal(
            status="proposal_blocked_ineligible_ratchet_status",
            ratchet_report=ratchet_report,
            ratchet_report_ref=ratchet_report_ref,
            blocked_reason_codes=["ratchet_report_status_ineligible"],
        )

    integrity_reason = _integrity_reason(
        ratchet_report,
        ratchet_report_ref=ratchet_report_ref,
        expected_package_version=expected_package_version,
        expected_release_tag=expected_release_tag,
        expected_release_source_commit=expected_release_source_commit,
        expected_mythic_edge_commit=expected_mythic_edge_commit,
    )
    if integrity_reason:
        return _base_proposal(
            status=_integrity_status(integrity_reason),
            ratchet_report=ratchet_report,
            ratchet_report_ref=ratchet_report_ref,
            blocked_reason_codes=[integrity_reason],
        )

    predecessor_reason = _predecessor_reason(
        package_preview_ref=package_preview_ref,
        pr_validation_ref=pr_validation_ref,
        release_review_ref=release_review_ref,
        dispatch_or_manual_selection_ref=dispatch_or_manual_selection_ref,
        human_proposal_review_ref=human_proposal_review_ref,
    )
    if predecessor_reason:
        return _base_proposal(
            status=_predecessor_status(predecessor_reason),
            ratchet_report=ratchet_report,
            ratchet_report_ref=ratchet_report_ref,
            blocked_reason_codes=[predecessor_reason],
        )

    proposal_status = _ready_status(ratchet_report)
    return _base_proposal(
        status=proposal_status,
        ratchet_report=ratchet_report,
        ratchet_report_ref=ratchet_report_ref,
        review_gate_refs=[
            str(package_preview_ref["ref"]),
            str(pr_validation_ref["ref"]),
            str(release_review_ref["ref"]),
            str(dispatch_or_manual_selection_ref["ref"]),
            str(human_proposal_review_ref["ref"]),
        ],
        validation_summary={
            "ratchet_report_validation": "passed",
            "package_preview": str(package_preview_ref["status"]),
            "pr_validation": str(pr_validation_ref["status"]),
            "release_review": "approved",
            "dispatch_or_manual_selection": str(dispatch_or_manual_selection_ref["status"]),
            "human_proposal_review": "approved",
        },
    )


def validate_baseline_pr_proposal(proposal: Mapping[str, Any]) -> list[str]:
    """Return symbolic validation reason codes for a proposal object."""

    if not isinstance(proposal, Mapping):
        return ["proposal_schema_invalid"]
    if _public_safety_reason(proposal):
        return [_public_safety_reason(proposal) or "proposal_contains_forbidden_content"]
    if set(proposal) != REQUIRED_PROPOSAL_KEYS:
        return ["proposal_schema_invalid"]
    if proposal.get("object") != OBJECT_TYPE or proposal.get("schema_version") != SCHEMA_VERSION:
        return ["proposal_schema_invalid"]
    if proposal.get("source_repository") != SOURCE_REPOSITORY:
        return ["proposal_schema_invalid"]
    if proposal.get("source_repository_url") != SOURCE_REPOSITORY_URL:
        return ["proposal_schema_invalid"]
    if proposal.get("target_repository") != TARGET_REPOSITORY:
        return ["proposal_schema_invalid"]
    if proposal.get("target_repository_url") != TARGET_REPOSITORY_URL:
        return ["proposal_schema_invalid"]
    if proposal.get("proposal_status") not in PROPOSAL_STATUSES:
        return ["proposal_schema_invalid"]
    if proposal.get("non_claims") != list(NON_CLAIMS):
        return ["proposal_schema_invalid"]
    if proposal.get("no_write_guards") != NO_WRITE_GUARDS:
        return ["proposal_schema_invalid"]
    if not isinstance(proposal.get("blocked_reason_codes"), list):
        return ["proposal_schema_invalid"]
    if not all(_is_reason_code(item) for item in proposal["blocked_reason_codes"]):
        return ["proposal_schema_invalid"]
    if not isinstance(proposal.get("changed_output_summary"), Mapping):
        return ["proposal_schema_invalid"]
    if set(proposal["changed_output_summary"]) != SUMMARY_KEYS:
        return ["proposal_schema_invalid"]
    if not all(isinstance(value, int) and value >= 0 for value in proposal["changed_output_summary"].values()):
        return ["proposal_schema_invalid"]
    if proposal["proposal_status"] in READY_PROPOSAL_STATUSES:
        ready_problem = _ready_proposal_problem(proposal)
        if ready_problem:
            return [ready_problem]
    else:
        blocked_problem = _blocked_proposal_problem(proposal)
        if blocked_problem:
            return [blocked_problem]
    return []


def format_text(proposal: Mapping[str, Any]) -> str:
    """Render a deterministic text summary."""

    lines = [
        "Corpus Baseline PR Proposal Preview",
        f"schema_version: {proposal['schema_version']}",
        f"status: {proposal['proposal_status']}",
        f"package_version: {proposal.get('package_version') or 'unknown'}",
        f"ratchet_report_status: {proposal.get('ratchet_report_status') or 'unknown'}",
        "blocked_reason_codes:",
    ]
    if proposal["blocked_reason_codes"]:
        lines.extend(f"- {reason}" for reason in proposal["blocked_reason_codes"])
    else:
        lines.append("- none")
    lines.append("no_write_guards:")
    lines.extend(f"- {key}: {str(value).lower()}" for key, value in sorted(proposal["no_write_guards"].items()))
    lines.append("non_claims:")
    lines.extend(f"- {claim}" for claim in proposal["non_claims"])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a no-write corpus baseline PR proposal preview.")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--proposal", required=True)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    if not args.validate_only:
        proposal = _base_proposal(status="unsupported", blocked_reason_codes=["unsupported"])
    else:
        try:
            proposal = _load_proposal(args.proposal)
        except ValueError as exc:
            proposal = _base_proposal(status="invalid", blocked_reason_codes=[str(exc)])
        else:
            problems = validate_baseline_pr_proposal(proposal)
            if problems:
                proposal = _base_proposal(status="invalid", blocked_reason_codes=[problems[0]])

    if args.format == "json":
        print(json.dumps(proposal, indent=2, sort_keys=True))
    else:
        print(format_text(proposal), end="")
    return 0 if proposal["proposal_status"] in READY_PROPOSAL_STATUSES else 2


def _base_proposal(
    *,
    status: str,
    ratchet_report: Mapping[str, Any] | None = None,
    ratchet_report_ref: str | None = None,
    blocked_reason_codes: Sequence[str] = (),
    review_gate_refs: Sequence[str] = (),
    validation_summary: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    report = ratchet_report or {}
    package_version = _safe_optional(report.get("package_version"))
    report_id = _safe_optional(report.get("report_id"))
    has_draft = status in {
        "proposal_preview_ready_for_review",
        "proposal_preview_degraded",
    }
    branch_name = _branch_name(package_version, report_id) if has_draft else None
    title = _draft_title(package_version, report_id, status) if has_draft else None
    summary = _changed_output_summary(report.get("summary"))
    return {
        "object": OBJECT_TYPE,
        "schema_version": SCHEMA_VERSION,
        "proposal_id": _proposal_id(package_version, report_id),
        "proposal_status": status,
        "source_repository": SOURCE_REPOSITORY,
        "source_repository_url": SOURCE_REPOSITORY_URL,
        "target_repository": TARGET_REPOSITORY,
        "target_repository_url": TARGET_REPOSITORY_URL,
        "package_id": _safe_optional(report.get("package_id")),
        "package_version": package_version,
        "release_tag": _safe_optional(report.get("release_tag")),
        "release_url": _safe_optional(report.get("release_url")),
        "release_source_commit": _safe_optional(report.get("release_source_commit")),
        "release_channel": _safe_optional(report.get("release_channel")),
        "release_metadata_ref": _safe_optional(report.get("release_metadata_ref")),
        "checksum_ref": _safe_optional(report.get("checksum_ref")),
        "asset_checksums_verified": bool(report.get("asset_checksums_verified") is True),
        "ratchet_report_id": report_id,
        "ratchet_report_ref": ratchet_report_ref,
        "ratchet_report_status": _safe_optional(report.get("comparison_status")),
        "mythic_edge_commit": _safe_optional(report.get("mythic_edge_commit")),
        "mythic_edge_base_branch": TARGET_BASE_BRANCH,
        "mythic_edge_candidate_branch_name": branch_name,
        "draft_pr_title": title,
        "draft_pr_body_sections": _draft_body_sections(report, summary) if has_draft else [],
        "changed_output_summary": summary,
        "validation_summary": dict(validation_summary or {}),
        "review_gate_refs": list(review_gate_refs),
        "blocked_reason_codes": list(blocked_reason_codes),
        "no_write_guards": dict(NO_WRITE_GUARDS),
        "non_claims": list(NON_CLAIMS),
    }


def _requested_action_block(
    *,
    baseline_mutation_requested: bool,
    baseline_pr_requested: bool,
    source_action_requested: bool,
    ratchet_execution_requested: bool,
    release_or_dispatch_requested: bool,
) -> tuple[str, str] | None:
    if baseline_mutation_requested:
        return ("proposal_blocked_baseline_mutation_requested", "proposal_requests_baseline_mutation")
    if baseline_pr_requested or source_action_requested:
        return ("proposal_blocked_source_action_requested", "proposal_requests_source_pr")
    if ratchet_execution_requested:
        return ("proposal_blocked_ratchet_execution_requested", "proposal_requests_ratchet_execution")
    if release_or_dispatch_requested:
        return ("proposal_blocked_release_or_dispatch_requested", "proposal_requests_release_publishing")
    return None


def _validate_ratchet_input(report: Mapping[str, Any]) -> list[str]:
    if validate_ratchet_report is None:
        return []
    problems = validate_ratchet_report(report)
    if problems:
        if problems[0] == "payload_or_metadata_contains_forbidden_content":
            return ["proposal_contains_forbidden_content"]
        return ["ratchet_report_schema_invalid"]
    return []


def _integrity_reason(
    report: Mapping[str, Any],
    *,
    ratchet_report_ref: str | None,
    expected_package_version: str | None,
    expected_release_tag: str | None,
    expected_release_source_commit: str | None,
    expected_mythic_edge_commit: str | None,
) -> str | None:
    if not _is_public_ref(ratchet_report_ref):
        return "missing_ratchet_report"
    if not _is_package_version(report.get("package_version")):
        return "package_version_mismatch"
    if not _is_public_ref(report.get("release_metadata_ref")):
        return "missing_release_metadata"
    if not _is_public_ref(report.get("checksum_ref")):
        return "missing_checksum_metadata"
    if report.get("asset_checksums_verified") is not True:
        return "checksum_mismatch"
    if not _is_github_release_url(report.get("release_url")):
        return "missing_release_metadata"
    if report.get("release_channel") != RELEASE_CHANNEL:
        return "missing_release_metadata"
    package_version = str(report["package_version"])
    expected_tag = expected_release_tag or f"corpus-package-v{package_version}"
    if report.get("release_tag") != expected_tag:
        return "release_tag_mismatch"
    if expected_package_version and package_version != expected_package_version:
        return "package_version_mismatch"
    if not _is_commit(report.get("release_source_commit")):
        return "release_source_commit_mismatch"
    if expected_release_source_commit and report.get("release_source_commit") != expected_release_source_commit:
        return "release_source_commit_mismatch"
    if not _is_commit(report.get("mythic_edge_commit")):
        return "mythic_edge_commit_missing"
    if expected_mythic_edge_commit and report.get("mythic_edge_commit") != expected_mythic_edge_commit:
        return "ratchet_report_stale"
    return None


def _integrity_status(reason: str) -> str:
    if reason in {"checksum_mismatch", "release_tag_mismatch", "package_version_mismatch"}:
        return "proposal_blocked_checksum_or_release_mismatch"
    if reason in {"ratchet_report_stale", "release_source_commit_mismatch"}:
        return "proposal_blocked_stale_report"
    return "proposal_blocked_missing_integrity_metadata"


def _predecessor_reason(
    *,
    package_preview_ref: Mapping[str, Any] | None,
    pr_validation_ref: Mapping[str, Any] | None,
    release_review_ref: Mapping[str, Any] | None,
    dispatch_or_manual_selection_ref: Mapping[str, Any] | None,
    human_proposal_review_ref: Mapping[str, Any] | None,
) -> str | None:
    if not _evidence_status_ref(package_preview_ref, "passed"):
        return "missing_predecessor_preview_evidence"
    if not _evidence_status_ref(pr_validation_ref, "passed"):
        return "missing_predecessor_pr_validation_evidence"
    if not _approved_ref(release_review_ref):
        return "missing_release_review"
    if not _evidence_status_ref(dispatch_or_manual_selection_ref, "manual_selection_recorded"):
        return "missing_dispatch_or_manual_selection_ref"
    if not _approved_ref(human_proposal_review_ref):
        return "missing_human_proposal_review"
    return None


def _predecessor_status(reason: str) -> str:
    if reason == "missing_human_proposal_review":
        return "proposal_blocked_missing_human_review"
    return "proposal_blocked_missing_integrity_metadata"


def _ready_status(report: Mapping[str, Any]) -> str:
    status = report.get("comparison_status")
    summary = _changed_output_summary(report.get("summary"))
    if status == "comparison_completed_with_no_deltas":
        return "proposal_preview_no_deltas"
    if status == "comparison_report_ready_for_review":
        return "proposal_preview_degraded"
    if summary["review_required"] or summary["degraded_evidence"] or summary["unsupported"]:
        return "proposal_preview_degraded"
    return "proposal_preview_ready_for_review"


def _changed_output_summary(summary: Any) -> dict[str, int]:
    if not isinstance(summary, Mapping):
        return {key: 0 for key in sorted(SUMMARY_KEYS)}
    return {
        "total_cases": _non_negative_int(summary.get("total_cases")),
        "matched_expected_output": _non_negative_int(summary.get("matched_expected_output")),
        "new_passes": _non_negative_int(summary.get("new_passes")),
        "new_failures": _non_negative_int(summary.get("new_failures")),
        "changed_outputs": _non_negative_int(summary.get("changed_outputs")),
        "missing_families": _non_negative_int(summary.get("missing_families")),
        "missing_cases": _non_negative_int(summary.get("missing_cases")),
        "extra_outputs": _non_negative_int(summary.get("extra_outputs")),
        "degraded_evidence": _non_negative_int(summary.get("degraded_evidence")),
        "unsupported": _non_negative_int(summary.get("unsupported")),
        "review_required": _non_negative_int(summary.get("review_required")),
    }


def _draft_body_sections(report: Mapping[str, Any], summary: Mapping[str, int]) -> list[dict[str, Any]]:
    return [
        {
            "heading": "Refs",
            "lines": [
                f"Corpus release tag: {report.get('release_tag')}",
                f"Ratchet report: {report.get('report_id')}",
            ],
        },
        {
            "heading": "Package Provenance",
            "lines": [
                f"Package version: {report.get('package_version')}",
                f"Release source commit: {report.get('release_source_commit')}",
                f"Mythic Edge comparison commit: {report.get('mythic_edge_commit')}",
            ],
        },
        {
            "heading": "Changed Output Summary",
            "lines": [f"{key}: {value}" for key, value in sorted(summary.items())],
        },
        {
            "heading": "Review Required Before Merge",
            "lines": [
                "A human reviewer must inspect this no-write proposal before any source-repo action.",
            ],
        },
        {
            "heading": "Non-Claims",
            "lines": list(NON_CLAIMS),
        },
    ]


def _draft_title(package_version: str | None, report_id: str | None, status: str) -> str:
    label = package_version or report_id or "unknown"
    if status == "proposal_preview_no_deltas":
        return f"[draft proposal] Corpus baseline review no deltas for {label}"
    return f"[draft proposal] Corpus baseline review for {label}"


def _proposal_id(package_version: str | None, report_id: str | None) -> str:
    parts = ["corpus-baseline-proposal"]
    if package_version:
        parts.append(package_version)
    if report_id:
        parts.append(_short_ref(report_id))
    return "-".join(parts)


def _branch_name(package_version: str | None, report_id: str | None) -> str:
    label = package_version or "unknown"
    return f"codex/corpus-baseline-proposal-{label}-{_short_ref(report_id or 'report')}"


def _short_ref(value: str) -> str:
    clean = re.sub(r"[^A-Za-z0-9._+-]+", "-", value).strip("-")
    return clean[:24] or "unknown"


def _ready_proposal_problem(proposal: Mapping[str, Any]) -> str | None:
    if proposal.get("blocked_reason_codes") != []:
        return "proposal_schema_invalid"
    if not _is_public_ref(proposal.get("ratchet_report_ref")):
        return "missing_ratchet_report"
    if not _is_package_version(proposal.get("package_version")):
        return "package_version_mismatch"
    if not _is_commit(proposal.get("release_source_commit")):
        return "release_source_commit_mismatch"
    if not _is_commit(proposal.get("mythic_edge_commit")):
        return "mythic_edge_commit_missing"
    if proposal.get("proposal_status") == "proposal_preview_no_deltas":
        return _blocked_proposal_problem(proposal)
    if not _is_public_ref(proposal.get("mythic_edge_candidate_branch_name")):
        return "proposal_contains_forbidden_content"
    if not isinstance(proposal.get("draft_pr_title"), str) or not proposal["draft_pr_title"]:
        return "proposal_schema_invalid"
    if not isinstance(proposal.get("draft_pr_body_sections"), list) or not proposal["draft_pr_body_sections"]:
        return "proposal_schema_invalid"
    if not isinstance(proposal.get("review_gate_refs"), list) or not proposal["review_gate_refs"]:
        return "missing_human_proposal_review"
    return None


def _blocked_proposal_problem(proposal: Mapping[str, Any]) -> str | None:
    if proposal.get("mythic_edge_candidate_branch_name") is not None:
        return "proposal_schema_invalid"
    if proposal.get("draft_pr_title") is not None:
        return "proposal_schema_invalid"
    if proposal.get("draft_pr_body_sections") != []:
        return "proposal_schema_invalid"
    return None


def _evidence_status_ref(value: Mapping[str, Any] | None, expected_status: str) -> bool:
    return (
        isinstance(value, Mapping)
        and value.get("status") == expected_status
        and _is_public_ref(value.get("ref"))
    )


def _approved_ref(value: Mapping[str, Any] | None) -> bool:
    return isinstance(value, Mapping) and value.get("approved") is True and _is_public_ref(value.get("ref"))


def _public_safety_reason(value: Any) -> str | None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key)
            key_reason = _unsafe_key_reason(key_text)
            if key_reason:
                return key_reason
            reason = _public_safety_reason(item)
            if reason:
                return reason
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for item in value:
            reason = _public_safety_reason(item)
            if reason:
                return reason
    elif isinstance(value, str):
        if _unsafe_text(value):
            return _unsafe_reason(value)
    return None


def _unsafe_text(value: str) -> bool:
    return _unsafe_reason(value) is not None


def _unsafe_key_reason(value: str) -> str | None:
    if value in ALLOWED_KEY_TEXT:
        return None
    action_reason = _action_key_reason(value)
    if action_reason:
        return action_reason
    return _unsafe_reason(value)


def _unsafe_reason(value: str) -> str | None:
    if value in ALLOWED_SYMBOLIC_TEXT:
        return None
    if SOURCE_PATCH_MARKER_RE.search(value):
        return "proposal_contains_source_patch"
    action_reason = _action_text_reason(value)
    if action_reason:
        return action_reason
    claim_reason = _claim_reason(value)
    if claim_reason:
        return claim_reason
    if LOCAL_OR_SECRET_MARKER_RE.search(value):
        return "proposal_contains_forbidden_content"
    return None


def _action_key_reason(value: str) -> str | None:
    normalized = _normalized_label(value)
    for pattern, reason in ACTION_KEY_REASONS:
        if pattern.search(normalized):
            return reason
    return None


def _action_text_reason(value: str) -> str | None:
    normalized = _normalized_label(value).replace("_", " ")
    for pattern, reason in ACTION_REQUEST_REASONS:
        if pattern.search(normalized):
            return reason
    return None


def _claim_reason(value: str) -> str | None:
    normalized = _normalized_label(value).replace("_", " ")
    if re.search(r"\bparser truth\b", normalized, re.IGNORECASE):
        return "proposal_claims_parser_truth"
    if re.search(r"\bfixture promotion\b", normalized, re.IGNORECASE):
        return "proposal_claims_fixture_promotion"
    if re.search(r"\bbaseline (approved|approval|confirmed)\b", normalized, re.IGNORECASE):
        return "proposal_claims_baseline_approval"
    if re.search(
        r"\b(corpus|release|deploy|production) readiness\b|\bfull corpus parity\b|"
        r"\b(security|privacy) assurance\b",
        normalized,
        re.IGNORECASE,
    ):
        return "proposal_claims_readiness"
    if STRONG_CLAIM_RE.search(value):
        return "proposal_claims_readiness"
    return None


def _normalized_label(value: str) -> str:
    camel_spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    return re.sub(r"[^A-Za-z0-9]+", "_", camel_spaced).strip("_").lower()


def _is_public_ref(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and bool(SAFE_ID_RE.fullmatch(value)) and not _unsafe_text(value)


def _is_reason_code(value: Any) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"[a-z0-9_]+", value))


def _is_package_version(value: Any) -> bool:
    return isinstance(value, str) and bool(PACKAGE_VERSION_RE.fullmatch(value))


def _is_commit(value: Any) -> bool:
    return isinstance(value, str) and bool(COMMIT_RE.fullmatch(value))


def _is_github_release_url(value: Any) -> bool:
    return isinstance(value, str) and bool(GITHUB_RELEASE_URL_RE.fullmatch(value))


def _non_negative_int(value: Any) -> int:
    return value if isinstance(value, int) and value >= 0 else 0


def _safe_optional(value: Any) -> str | None:
    return value if isinstance(value, str) and not _unsafe_text(value) else None


def _load_proposal(path_value: str) -> Mapping[str, Any]:
    if _unsafe_text(path_value):
        raise ValueError("proposal_contains_forbidden_content")
    path = Path(path_value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("proposal_contains_forbidden_content")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("proposal_schema_invalid") from exc


if __name__ == "__main__":
    raise SystemExit(main())
