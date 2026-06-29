from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL_PATH = ROOT / "tools/corpus_baseline_pr_proposal.py"
RATCHET_PATH = ROOT / "tools/corpus_ratchet_comparison_report.py"
RELEASE_PATH = ROOT / "tools/corpus_release_package.py"
SOURCE_COMMIT = "1e1c0bfbd9451ee60ee8c423a48d56202f8c7b64"
MYTHIC_EDGE_COMMIT = "d650781ca9dd05a0f263f5347994f466600ba5d3"
RECEIVER_CONTRACT = "docs/contracts/mythic_edge_corpus_release_receiver.md"
COMPARISON_SURFACE = "public_safe_parser_summary"
RELEASE_URL = "https://github.com/Tahjali11/Mythic-Edge-Corpus/releases/tag/corpus-package-v0.0.0-preview"
DEFAULT_REPORT = object()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Unable to load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def release_report() -> dict[str, Any]:
    release = load_module("corpus_release_for_baseline_proposal_test", RELEASE_PATH)
    report = release.build_release_report(
        package_root="corpus",
        manifest_path="corpus/manifest.v1.json",
        session_ledger_path="corpus/session_ledger.v1.json",
        package_version="0.0.0-preview",
        source_commit=SOURCE_COMMIT,
        preview_source_commit=SOURCE_COMMIT,
        pr_validation_source_commit=SOURCE_COMMIT,
        repo_root=ROOT,
        review_approved=True,
        reviewed_by="codex-e",
        review_ref="issue-16-review",
        dry_run=True,
        clean_worktree_confirmed=True,
    )
    return report


def comparison_result(
    category: str,
    *,
    case_id: str = "case-1",
    review_required: bool = False,
) -> dict[str, Any]:
    ratchet = load_module("corpus_ratchet_result_for_baseline_proposal_test", RATCHET_PATH)
    return {
        "actual_ref": "actual-summary-ref" if category != "missing_case" else "missing",
        "case_id": case_id,
        "comparison_confidence": "bounded",
        "evidence_status": "observed_public_summary",
        "expected_ref": "expected-summary-ref",
        "family_id": "family-public",
        "freshness": "current_public_release",
        "non_claims": list(ratchet.NON_CLAIMS),
        "reason_codes": ["review_required"] if review_required else [],
        "result_category": category,
        "review_required": review_required,
    }


def expected_checksums_for(release: dict[str, Any]) -> dict[str, str]:
    return {asset["asset_name"]: asset["sha256"] for asset in release["planned_assets"]}


def ratchet_report(*, results: list[dict[str, Any]] | None = None, **overrides) -> dict[str, Any]:
    ratchet = load_module("corpus_ratchet_for_baseline_proposal_test", RATCHET_PATH)
    release = release_report()
    args = {
        "release_report": release,
        "release_url": RELEASE_URL,
        "release_metadata_ref": "release-metadata-ref",
        "checksum_ref": "checksum-ref",
        "asset_checksums_verified": True,
        "expected_asset_checksums": expected_checksums_for(release),
        "mythic_edge_commit": MYTHIC_EDGE_COMMIT,
        "mythic_edge_comparison_contract_ref": RECEIVER_CONTRACT,
        "comparison_surface": COMPARISON_SURFACE,
        "comparison_results": results
        if results is not None
        else [
            comparison_result("matched_expected_output", case_id="case-match"),
            comparison_result("new_pass", case_id="case-pass"),
            comparison_result("changed_output", case_id="case-changed"),
        ],
        "validation_refs": ["issue-18-review"],
    }
    args.update(overrides)
    return ratchet.build_ratchet_report(**args)


def predecessor_refs() -> dict[str, dict[str, Any]]:
    return {
        "package_preview_ref": {"status": "passed", "ref": "issue-14-preview"},
        "pr_validation_ref": {"status": "passed", "ref": "issue-15-pr-validation"},
        "release_review_ref": {"approved": True, "ref": "issue-16-release-review"},
        "dispatch_or_manual_selection_ref": {
            "status": "manual_selection_recorded",
            "ref": "issue-17-manual-selection",
        },
        "human_proposal_review_ref": {"approved": True, "ref": "issue-19-review-gate"},
    }


def build_proposal(module, report: dict[str, Any] | None | object = DEFAULT_REPORT, **overrides):
    args = {
        "ratchet_report": ratchet_report() if report is DEFAULT_REPORT else report,
        "ratchet_report_ref": "issue-18-ratchet-report",
        **predecessor_refs(),
    }
    args.update(overrides)
    return module.build_baseline_pr_proposal(**args)


class CorpusBaselinePrProposalTests(unittest.TestCase):
    def test_public_safe_delta_report_builds_review_only_proposal(self) -> None:
        module = load_module("corpus_baseline_proposal_happy_test", PROPOSAL_PATH)

        proposal = build_proposal(module)
        rendered = json.dumps(proposal, sort_keys=True)

        self.assertEqual(proposal["object"], "corpus_baseline_pr_proposal")
        self.assertEqual(proposal["schema_version"], "corpus_baseline_pr_proposal.v1")
        self.assertEqual(proposal["proposal_status"], "proposal_preview_ready_for_review")
        self.assertEqual(proposal["package_version"], "0.0.0-preview")
        self.assertEqual(proposal["release_tag"], "corpus-package-v0.0.0-preview")
        self.assertEqual(proposal["release_source_commit"], SOURCE_COMMIT)
        self.assertEqual(proposal["mythic_edge_commit"], MYTHIC_EDGE_COMMIT)
        self.assertEqual(proposal["changed_output_summary"]["new_passes"], 1)
        self.assertEqual(proposal["changed_output_summary"]["changed_outputs"], 1)
        self.assertEqual(proposal["blocked_reason_codes"], [])
        self.assertTrue(all(value is False for value in proposal["no_write_guards"].values()))
        self.assertIn("not_parser_truth", proposal["non_claims"])
        self.assertIn("not_baseline_mutation", proposal["non_claims"])
        self.assertTrue(proposal["draft_pr_title"].startswith("[draft proposal]"))
        self.assertIn("Refs", [section["heading"] for section in proposal["draft_pr_body_sections"]])
        self.assertNotIn("Closes", rendered)
        self.assertEqual(module.validate_baseline_pr_proposal(proposal), [])

    def test_no_delta_report_builds_non_actionable_noop_summary(self) -> None:
        module = load_module("corpus_baseline_proposal_no_delta_test", PROPOSAL_PATH)
        report = ratchet_report(
            results=[comparison_result("matched_expected_output", case_id="case-match")]
        )

        proposal = build_proposal(module, report=report)

        self.assertEqual(proposal["proposal_status"], "proposal_preview_no_deltas")
        self.assertIsNone(proposal["mythic_edge_candidate_branch_name"])
        self.assertIsNone(proposal["draft_pr_title"])
        self.assertEqual(proposal["draft_pr_body_sections"], [])
        self.assertEqual(module.validate_baseline_pr_proposal(proposal), [])

    def test_review_required_or_degraded_deltas_mark_proposal_degraded(self) -> None:
        module = load_module("corpus_baseline_proposal_degraded_test", PROPOSAL_PATH)
        report = ratchet_report(
            results=[
                comparison_result("matched_expected_output", case_id="case-match"),
                comparison_result(
                    "degraded_evidence",
                    case_id="case-degraded",
                    review_required=True,
                ),
            ]
        )

        proposal = build_proposal(module, report=report)

        self.assertEqual(proposal["proposal_status"], "proposal_preview_degraded")
        self.assertEqual(proposal["changed_output_summary"]["degraded_evidence"], 1)
        self.assertEqual(proposal["changed_output_summary"]["review_required"], 1)
        self.assertEqual(module.validate_baseline_pr_proposal(proposal), [])

    def test_missing_ratchet_report_fails_closed_without_draft_text(self) -> None:
        module = load_module("corpus_baseline_proposal_missing_ratchet_test", PROPOSAL_PATH)

        proposal = build_proposal(module, report=None)

        self.assertEqual(proposal["proposal_status"], "proposal_blocked_missing_ratchet_report")
        self.assertEqual(proposal["blocked_reason_codes"], ["missing_ratchet_report"])
        self.assertIsNone(proposal["draft_pr_title"])
        self.assertEqual(proposal["draft_pr_body_sections"], [])
        self.assertEqual(module.validate_baseline_pr_proposal(proposal), [])

    def test_ineligible_ratchet_status_fails_closed(self) -> None:
        module = load_module("corpus_baseline_proposal_ineligible_status_test", PROPOSAL_PATH)
        report = ratchet_report(baseline_mutation_requested=True)

        proposal = build_proposal(module, report=report)

        self.assertEqual(proposal["proposal_status"], "proposal_blocked_ineligible_ratchet_status")
        self.assertEqual(proposal["blocked_reason_codes"], ["ratchet_report_status_ineligible"])
        self.assertIsNone(proposal["draft_pr_title"])

    def test_integrity_and_staleness_gates_fail_closed(self) -> None:
        module = load_module("corpus_baseline_proposal_integrity_test", PROPOSAL_PATH)

        missing_ref = build_proposal(module, ratchet_report_ref=None)
        self.assertEqual(missing_ref["proposal_status"], "proposal_blocked_missing_integrity_metadata")
        self.assertEqual(missing_ref["blocked_reason_codes"], ["missing_ratchet_report"])

        checksum = ratchet_report()
        checksum["asset_checksums_verified"] = False
        checksum_problem = build_proposal(module, report=checksum)
        self.assertEqual(
            checksum_problem["proposal_status"],
            "proposal_blocked_checksum_or_release_mismatch",
        )
        self.assertEqual(checksum_problem["blocked_reason_codes"], ["checksum_mismatch"])

        stale = build_proposal(module, expected_mythic_edge_commit="0" * 40)
        self.assertEqual(stale["proposal_status"], "proposal_blocked_stale_report")
        self.assertEqual(stale["blocked_reason_codes"], ["ratchet_report_stale"])

        tag_mismatch = build_proposal(module, expected_release_tag="corpus-package-v0.0.1-preview")
        self.assertEqual(
            tag_mismatch["proposal_status"],
            "proposal_blocked_checksum_or_release_mismatch",
        )
        self.assertEqual(tag_mismatch["blocked_reason_codes"], ["release_tag_mismatch"])

    def test_predecessor_evidence_and_human_review_are_required(self) -> None:
        module = load_module("corpus_baseline_proposal_predecessor_test", PROPOSAL_PATH)

        missing_preview = build_proposal(module, package_preview_ref=None)
        self.assertEqual(
            missing_preview["proposal_status"],
            "proposal_blocked_missing_integrity_metadata",
        )
        self.assertEqual(
            missing_preview["blocked_reason_codes"],
            ["missing_predecessor_preview_evidence"],
        )

        missing_pr_validation = build_proposal(module, pr_validation_ref=None)
        self.assertEqual(
            missing_pr_validation["blocked_reason_codes"],
            ["missing_predecessor_pr_validation_evidence"],
        )

        missing_release_review = build_proposal(module, release_review_ref={"approved": False, "ref": "review"})
        self.assertEqual(missing_release_review["blocked_reason_codes"], ["missing_release_review"])

        missing_dispatch = build_proposal(module, dispatch_or_manual_selection_ref=None)
        self.assertEqual(
            missing_dispatch["blocked_reason_codes"],
            ["missing_dispatch_or_manual_selection_ref"],
        )

        missing_human = build_proposal(module, human_proposal_review_ref=None)
        self.assertEqual(missing_human["proposal_status"], "proposal_blocked_missing_human_review")
        self.assertEqual(missing_human["blocked_reason_codes"], ["missing_human_proposal_review"])

    def test_out_of_scope_actions_are_refused_without_mutating_guards(self) -> None:
        module = load_module("corpus_baseline_proposal_action_test", PROPOSAL_PATH)

        checks = [
            (
                "baseline_mutation_requested",
                "proposal_blocked_baseline_mutation_requested",
                "proposal_requests_baseline_mutation",
            ),
            (
                "baseline_pr_requested",
                "proposal_blocked_source_action_requested",
                "proposal_requests_source_pr",
            ),
            (
                "source_action_requested",
                "proposal_blocked_source_action_requested",
                "proposal_requests_source_pr",
            ),
            (
                "ratchet_execution_requested",
                "proposal_blocked_ratchet_execution_requested",
                "proposal_requests_ratchet_execution",
            ),
            (
                "release_or_dispatch_requested",
                "proposal_blocked_release_or_dispatch_requested",
                "proposal_requests_release_publishing",
            ),
        ]
        for flag, status, reason in checks:
            with self.subTest(flag=flag):
                proposal = build_proposal(module, **{flag: True})
                self.assertEqual(proposal["proposal_status"], status)
                self.assertEqual(proposal["blocked_reason_codes"], [reason])
                self.assertTrue(all(value is False for value in proposal["no_write_guards"].values()))
                self.assertIsNone(proposal["draft_pr_title"])

    def test_forbidden_content_is_symbolic_and_does_not_echo_values(self) -> None:
        module = load_module("corpus_baseline_proposal_forbidden_test", PROPOSAL_PATH)
        forbidden_value = (
            "/" + "Users" + "/example/" + "private" + "/" + "Player" + ".log/" + "api_" + "key"
        )
        report = copy.deepcopy(ratchet_report())
        report["results"][0]["actual_ref"] = forbidden_value

        proposal = build_proposal(module, report=report)
        rendered = json.dumps(proposal, sort_keys=True)

        self.assertEqual(proposal["proposal_status"], "proposal_blocked_forbidden_content")
        self.assertEqual(
            proposal["blocked_reason_codes"],
            ["proposal_contains_forbidden_content"],
        )
        self.assertNotIn(forbidden_value, rendered)
        self.assertNotIn("Player" + ".log", rendered)
        self.assertNotIn("api_" + "key", rendered)

    def test_validate_rejects_mutated_guards_and_actionable_blocked_text(self) -> None:
        module = load_module("corpus_baseline_proposal_validate_guard_test", PROPOSAL_PATH)
        proposal = build_proposal(module)
        mutated = copy.deepcopy(proposal)
        mutated["no_write_guards"]["baseline_pr_created"] = True

        self.assertEqual(module.validate_baseline_pr_proposal(mutated), ["proposal_schema_invalid"])

        blocked = build_proposal(module, report=None)
        blocked["draft_pr_title"] = "[draft proposal] should not exist"
        self.assertEqual(module.validate_baseline_pr_proposal(blocked), ["proposal_schema_invalid"])

    def test_validate_rejects_direct_source_action_text_with_symbolic_codes(self) -> None:
        module = load_module("corpus_baseline_proposal_action_text_test", PROPOSAL_PATH)
        checks = [
            ("Create a source branch for this proposal.", "proposal_requests_source_branch"),
            ("Create a source commit for this proposal.", "proposal_requests_source_commit"),
            ("Open a PR in Mythic Edge now.", "proposal_requests_source_pr"),
            ("Post a source comment after validation.", "proposal_requests_source_comment"),
            ("Create a source status check for the baseline.", "proposal_requests_source_status_check"),
            ("Submit a source review as approved.", "proposal_requests_source_review"),
            ("Add a source label for this proposal.", "proposal_requests_source_label"),
            ("Update the baseline after validation.", "proposal_requests_baseline_mutation"),
            ("Run the ratchet after this preview.", "proposal_requests_ratchet_execution"),
            ("Publish the release after validation.", "proposal_requests_release_publishing"),
            ("Send repository_dispatch after validation.", "proposal_requests_repository_dispatch"),
        ]
        for unsafe_line, reason in checks:
            with self.subTest(reason=reason):
                proposal = build_proposal(module)
                proposal["draft_pr_body_sections"][0]["lines"].append(unsafe_line)

                self.assertEqual(module.validate_baseline_pr_proposal(proposal), [reason])

    def test_validate_rejects_truth_and_approval_claims_with_specific_codes(self) -> None:
        module = load_module("corpus_baseline_proposal_claim_text_test", PROPOSAL_PATH)
        checks = [
            ("This establishes parser truth.", "proposal_claims_parser_truth"),
            ("Fixture promotion is approved.", "proposal_claims_fixture_promotion"),
            ("Baseline approved by this proposal.", "proposal_claims_baseline_approval"),
            ("Production ready after this proposal.", "proposal_claims_readiness"),
        ]
        for unsafe_line, reason in checks:
            with self.subTest(reason=reason):
                proposal = build_proposal(module)
                proposal["draft_pr_body_sections"][0]["lines"].append(unsafe_line)

                self.assertEqual(module.validate_baseline_pr_proposal(proposal), [reason])

    def test_action_key_shapes_fail_closed_before_public_preview_without_echo(self) -> None:
        module = load_module("corpus_baseline_proposal_action_key_test", PROPOSAL_PATH)
        checks = [
            ("sourceRepoPrCreated", "proposal_requests_source_pr"),
            ("baselineMutationRequested", "proposal_requests_baseline_mutation"),
            ("repositoryDispatchSent", "proposal_requests_repository_dispatch"),
        ]
        for unsafe_key, reason in checks:
            with self.subTest(key=unsafe_key):
                report = copy.deepcopy(ratchet_report())
                report[unsafe_key] = True

                proposal = build_proposal(module, report=report)
                rendered = json.dumps(proposal, sort_keys=True)

                self.assertEqual(proposal["proposal_status"], "proposal_blocked_forbidden_content")
                self.assertEqual(proposal["blocked_reason_codes"], [reason])
                self.assertNotIn(unsafe_key, rendered)

    def test_validate_only_cli_accepts_public_safe_proposal(self) -> None:
        module = load_module("corpus_baseline_proposal_cli_test", PROPOSAL_PATH)
        proposal_path = Path("tests") / ".tmp_baseline_pr_proposal.json"
        try:
            (ROOT / proposal_path).write_text(
                json.dumps(build_proposal(module), indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "tools/corpus_baseline_pr_proposal.py",
                    "--validate-only",
                    "--proposal",
                    str(proposal_path),
                    "--format",
                    "json",
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
        finally:
            (ROOT / proposal_path).unlink(missing_ok=True)

        self.assertEqual(result.returncode, 0)
        proposal = json.loads(result.stdout)
        self.assertEqual(proposal["proposal_status"], "proposal_preview_ready_for_review")
        self.assertEqual(result.stderr, "")
        self.assertNotIn(str(ROOT), result.stdout)

    def test_validate_only_cli_rejects_unsafe_path_before_reading(self) -> None:
        unsafe_path = "/" + "Users" + "/example/" + "private" + "/" + "Player" + ".log"

        result = subprocess.run(
            [
                sys.executable,
                "tools/corpus_baseline_pr_proposal.py",
                "--validate-only",
                "--proposal",
                unsafe_path,
                "--format",
                "json",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        rendered = result.stdout + result.stderr
        self.assertEqual(result.returncode, 2)
        self.assertIn("proposal_contains_forbidden_content", rendered)
        self.assertNotIn(unsafe_path, rendered)
        self.assertNotIn("Player" + ".log", rendered)

    def test_validate_only_cli_rejects_action_text_without_echo(self) -> None:
        module = load_module("corpus_baseline_proposal_cli_action_text_test", PROPOSAL_PATH)
        unsafe_line = "Open a PR in Mythic Edge now."
        proposal = build_proposal(module)
        proposal["draft_pr_body_sections"][0]["lines"].append(unsafe_line)
        proposal_path = Path("tests") / ".tmp_baseline_pr_proposal_unsafe_action.json"
        try:
            (ROOT / proposal_path).write_text(
                json.dumps(proposal, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "tools/corpus_baseline_pr_proposal.py",
                    "--validate-only",
                    "--proposal",
                    str(proposal_path),
                    "--format",
                    "json",
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
        finally:
            (ROOT / proposal_path).unlink(missing_ok=True)

        rendered = result.stdout + result.stderr
        self.assertEqual(result.returncode, 2)
        self.assertIn("proposal_requests_source_pr", rendered)
        self.assertNotIn(unsafe_line, rendered)


if __name__ == "__main__":
    unittest.main()
