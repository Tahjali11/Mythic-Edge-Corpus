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
RATCHET_PATH = ROOT / "tools/corpus_ratchet_comparison_report.py"
RELEASE_PATH = ROOT / "tools/corpus_release_package.py"
SOURCE_COMMIT = "1e1c0bfbd9451ee60ee8c423a48d56202f8c7b64"
OTHER_COMMIT = "d650781ca9dd05a0f263f5347994f466600ba5d3"
RECEIVER_CONTRACT = "docs/contracts/mythic_edge_corpus_release_receiver.md"
COMPARISON_SURFACE = "public_safe_parser_summary"
RELEASE_URL = "https://github.com/Tahjali11/Mythic-Edge-Corpus/releases/tag/corpus-package-v0.0.0-preview"
DEFAULT_RELEASE = object()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Unable to load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def release_report() -> dict[str, Any]:
    release = load_module("corpus_release_for_ratchet_test", RELEASE_PATH)
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
    report["release_metadata"]["asset_checksums"] = [
        {
            "algorithm": "sha256",
            "asset_name": asset["asset_name"],
            "sha256": asset["sha256"],
        }
        for asset in report["planned_assets"]
    ]
    return report


def comparison_result(category: str, *, case_id: str = "case-1", review_required: bool = False) -> dict[str, Any]:
    module = load_module("corpus_ratchet_result_shape_test", RATCHET_PATH)
    return {
        "actual_ref": "actual-summary-ref" if category != "missing_case" else "missing",
        "case_id": case_id,
        "comparison_confidence": "bounded",
        "evidence_status": "observed_public_summary",
        "expected_ref": "expected-summary-ref",
        "family_id": "family-public",
        "freshness": "current_public_release",
        "non_claims": list(module.NON_CLAIMS),
        "reason_codes": ["review_required"] if review_required else [],
        "result_category": category,
        "review_required": review_required,
    }


def build_report(module, release: dict[str, Any] | None | object = DEFAULT_RELEASE, **overrides):
    selected_release = release_report() if release is DEFAULT_RELEASE else release
    args = {
        "release_report": selected_release,
        "release_url": RELEASE_URL,
        "release_metadata_ref": "release-metadata-ref",
        "checksum_ref": "checksum-ref",
        "asset_checksums_verified": True,
        "expected_asset_checksums": {
            asset["asset_name"]: asset["sha256"]
            for asset in release_report()["planned_assets"]
        },
        "mythic_edge_commit": OTHER_COMMIT,
        "mythic_edge_comparison_contract_ref": RECEIVER_CONTRACT,
        "comparison_surface": COMPARISON_SURFACE,
        "comparison_results": [
            comparison_result("matched_expected_output", case_id="case-match"),
            comparison_result("new_pass", case_id="case-pass"),
            comparison_result("new_failure", case_id="case-fail", review_required=True),
            comparison_result("changed_output", case_id="case-changed", review_required=True),
            comparison_result("missing_family", case_id="case-missing-family", review_required=True),
            comparison_result("missing_case", case_id="case-missing-case", review_required=True),
            comparison_result("extra_output", case_id="case-extra", review_required=True),
            comparison_result("degraded_evidence", case_id="case-degraded", review_required=True),
        ],
        "validation_refs": ["issue-18-review"],
    }
    args.update(overrides)
    return module.build_ratchet_report(**args)


def checksum_entries_for(release: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "algorithm": "sha256",
            "asset_name": asset["asset_name"],
            "sha256": asset["sha256"],
        }
        for asset in release["planned_assets"]
    ]


def expected_checksums_for(release: dict[str, Any]) -> dict[str, str]:
    return {
        asset["asset_name"]: asset["sha256"]
        for asset in release["planned_assets"]
    }


class CorpusRatchetComparisonReportTests(unittest.TestCase):
    def test_public_safe_release_and_deltas_build_report_only_summary(self) -> None:
        module = load_module("corpus_ratchet_happy_test", RATCHET_PATH)

        report = build_report(module)
        rendered = json.dumps(report, sort_keys=True)

        self.assertEqual(report["object"], "corpus_ratchet_comparison_report")
        self.assertEqual(report["schema_version"], "corpus_ratchet_comparison_report.v1")
        self.assertEqual(report["comparison_status"], "comparison_completed_with_deltas")
        self.assertEqual(report["package_version"], "0.0.0-preview")
        self.assertEqual(report["release_tag"], "corpus-package-v0.0.0-preview")
        self.assertEqual(report["release_source_commit"], SOURCE_COMMIT)
        self.assertEqual(report["mythic_edge_commit"], OTHER_COMMIT)
        self.assertEqual(report["summary"]["total_cases"], 8)
        self.assertEqual(report["summary"]["matched_expected_output"], 1)
        self.assertEqual(report["summary"]["new_passes"], 1)
        self.assertEqual(report["summary"]["new_failures"], 1)
        self.assertEqual(report["summary"]["changed_outputs"], 1)
        self.assertEqual(report["summary"]["missing_families"], 1)
        self.assertEqual(report["summary"]["missing_cases"], 1)
        self.assertEqual(report["summary"]["degraded_evidence"], 1)
        self.assertEqual(report["summary"]["review_required"], 6)
        self.assertEqual(report["blocked_reason_codes"], [])
        self.assertTrue(all(value is False for value in report["no_write_guards"].values()))
        self.assertEqual(report["non_claims"], list(module.NON_CLAIMS))
        self.assertEqual(module.validate_ratchet_report(report), [])
        self.assertNotIn(str(ROOT), rendered)

    def test_no_delta_results_get_no_delta_status(self) -> None:
        module = load_module("corpus_ratchet_no_delta_test", RATCHET_PATH)

        report = build_report(
            module,
            comparison_results=[comparison_result("matched_expected_output", case_id="case-match")],
        )

        self.assertEqual(report["comparison_status"], "comparison_completed_with_no_deltas")
        self.assertEqual(report["summary"]["total_cases"], 1)

    def test_missing_release_and_missing_receiver_contract_fail_closed(self) -> None:
        module = load_module("corpus_ratchet_missing_test", RATCHET_PATH)

        missing_release = build_report(module, release=None)
        self.assertEqual(missing_release["comparison_status"], "blocked_missing_release")
        self.assertEqual(missing_release["blocked_reason_codes"], ["missing_release_metadata"])

        missing_receiver = build_report(module, mythic_edge_comparison_contract_ref=None)
        self.assertEqual(missing_receiver["comparison_status"], "blocked_missing_receiver_contract")
        self.assertEqual(missing_receiver["blocked_reason_codes"], ["missing_receiver_contract"])

        missing_surface = build_report(module, comparison_surface="unknown")
        self.assertEqual(missing_surface["comparison_status"], "blocked_missing_parser_surface")
        self.assertEqual(missing_surface["blocked_reason_codes"], ["missing_parser_comparison_surface"])

    def test_checksum_mismatch_release_tag_and_stale_release_fail_closed_or_review(self) -> None:
        module = load_module("corpus_ratchet_integrity_test", RATCHET_PATH)

        mismatch = build_report(module, expected_asset_checksums={"mythic-edge-corpus-0.0.0-preview.tar.gz": "0" * 64})
        self.assertEqual(mismatch["comparison_status"], "blocked_checksum_mismatch")
        self.assertEqual(mismatch["blocked_reason_codes"], ["checksum_mismatch"])

        tag_mismatch = release_report()
        tag_mismatch["release_tag"] = "corpus-package-v0.0.1-preview"
        bad_tag = build_report(module, release=tag_mismatch)
        self.assertEqual(bad_tag["comparison_status"], "invalid")
        self.assertEqual(bad_tag["blocked_reason_codes"], ["release_tag_mismatch"])

        stale = build_report(module, expected_release_source_commit="0" * 40)
        self.assertEqual(stale["comparison_status"], "review_required")
        self.assertEqual(stale["blocked_reason_codes"], ["source_commit_mismatch"])

    def test_release_no_write_guards_must_match_exact_expected_shape(self) -> None:
        module = load_module("corpus_ratchet_release_guard_shape_test", RATCHET_PATH)

        malformed_guard_cases = [
            ("empty", {}),
            ("missing", {key: False for key in release_report()["no_write_guards"] if key != "ratchet_executed"}),
            ("extra", {**release_report()["no_write_guards"], "unexpected": False}),
            ("nested", {**release_report()["no_write_guards"], "ratchet_executed": {"value": False}}),
            ("non_bool", {**release_report()["no_write_guards"], "ratchet_executed": 0}),
        ]
        for name, guards in malformed_guard_cases:
            with self.subTest(name=name):
                release = release_report()
                release["no_write_guards"] = guards

                report = build_report(module, release=release)

                self.assertEqual(report["comparison_status"], "invalid")
                self.assertEqual(report["blocked_reason_codes"], ["report_schema_invalid"])

        release = release_report()
        release["no_write_guards"]["ratchet_executed"] = True
        report = build_report(module, release=release)

        self.assertEqual(report["comparison_status"], "blocked_source_mutation_requested")
        self.assertEqual(report["blocked_reason_codes"], ["source_mutation_requested"])

    def test_release_dry_run_flags_must_not_request_writes_or_publish(self) -> None:
        module = load_module("corpus_ratchet_dry_run_flag_test", RATCHET_PATH)

        cases = [
            ("dry_run_false", "dry_run", False),
            ("publish_requested_true", "publish_requested", True),
        ]
        for name, field, value in cases:
            with self.subTest(name=name):
                release = release_report()
                release[field] = value

                report = build_report(module, release=release)

                self.assertEqual(report["comparison_status"], "blocked_release_or_dispatch_requested")
                self.assertEqual(report["blocked_reason_codes"], ["release_or_dispatch_requested"])

    def test_release_schema_rejects_extra_write_or_asset_url_fields(self) -> None:
        module = load_module("corpus_ratchet_release_schema_shape_test", RATCHET_PATH)

        cases = [
            (
                "top_level_write_flag",
                lambda release: release.update({"package_archive_written": True}),
            ),
            (
                "planned_asset_upload_flag",
                lambda release: release["planned_assets"][0].update({"release_asset_uploaded": True}),
            ),
            (
                "planned_asset_external_url",
                lambda release: release["planned_assets"][0].update(
                    {"asset_url": "https://example.com/not-corpus.tar.gz"}
                ),
            ),
            (
                "release_metadata_upload_flag",
                lambda release: release["release_metadata"].update({"release_asset_uploaded": True}),
            ),
        ]
        for name, mutate in cases:
            with self.subTest(name=name):
                release = release_report()
                mutate(release)

                report = build_report(module, release=release)

                self.assertEqual(report["comparison_status"], "invalid")
                self.assertEqual(report["blocked_reason_codes"], ["report_schema_invalid"])

    def test_release_predecessor_and_review_evidence_must_be_present_and_matching(self) -> None:
        module = load_module("corpus_ratchet_predecessor_evidence_test", RATCHET_PATH)

        cases = [
            (
                "missing_preview_ref",
                lambda release: release.update({"package_preview_ref": {}}),
                "missing_predecessor_preview_evidence",
            ),
            (
                "metadata_preview_ref_mismatch",
                lambda release: release["release_metadata"].update({"package_preview_ref": {}}),
                "missing_predecessor_preview_evidence",
            ),
            (
                "preview_ref_wrong_source_commit",
                lambda release: release["package_preview_ref"].update({"source_commit": OTHER_COMMIT}),
                "missing_predecessor_preview_evidence",
            ),
            (
                "missing_pr_validation_ref",
                lambda release: release.update({"pr_validation_ref": {}}),
                "missing_predecessor_pr_validation_evidence",
            ),
            (
                "metadata_pr_validation_ref_mismatch",
                lambda release: release["release_metadata"].update({"pr_validation_ref": {}}),
                "missing_predecessor_pr_validation_evidence",
            ),
            (
                "human_review_not_approved",
                lambda release: release["review_ref"].update({"approved": False}),
                "missing_human_review",
            ),
            (
                "metadata_review_ref_mismatch",
                lambda release: release["release_metadata"].update({"review_ref": {}}),
                "missing_human_review",
            ),
            (
                "missing_manifest_ref",
                lambda release: release.update({"manifest_ref": {}}),
                "missing_release_metadata",
            ),
            (
                "session_ledger_path_traversal",
                lambda release: release["session_ledger_ref"].update({"path": "../corpus/session_ledger.v1.json"}),
                "missing_release_metadata",
            ),
        ]
        for name, mutate, reason in cases:
            with self.subTest(name=name):
                release = release_report()
                mutate(release)

                report = build_report(module, release=release)

                self.assertEqual(report["comparison_status"], "blocked_missing_release_metadata")
                self.assertEqual(report["blocked_reason_codes"], [reason])

    def test_release_summary_and_safety_evidence_must_be_present_and_passing(self) -> None:
        module = load_module("corpus_ratchet_summary_safety_evidence_test", RATCHET_PATH)

        cases = [
            (
                "top_level_failed_safety_check",
                lambda release: release["safety_checks"][0].update({"status": "failed"}),
            ),
            (
                "metadata_failed_safety_check",
                lambda release: release["release_metadata"]["safety_checks"][0].update({"status": "failed"}),
            ),
            (
                "safety_check_mismatch",
                lambda release: release["release_metadata"].update({"safety_checks": []}),
            ),
            (
                "empty_included_files_summary",
                lambda release: release.update({"included_files_summary": {}}),
            ),
            (
                "metadata_included_files_summary_mismatch",
                lambda release: release["release_metadata"].update({"included_files_summary": {}}),
            ),
            (
                "included_file_path_traversal",
                lambda release: release["included_files_summary"].update({"paths": ["../corpus/manifest.v1.json"]}),
            ),
            (
                "included_file_count_mismatch",
                lambda release: release["included_files_summary"].update({"total_included_files": 99}),
            ),
        ]
        for name, mutate in cases:
            with self.subTest(name=name):
                release = release_report()
                mutate(release)

                report = build_report(module, release=release)

                self.assertEqual(report["comparison_status"], "blocked_missing_release_metadata")
                self.assertEqual(report["blocked_reason_codes"], ["missing_release_metadata"])

    def test_release_metadata_checksums_must_match_planned_assets_exactly(self) -> None:
        module = load_module("corpus_ratchet_metadata_checksum_test", RATCHET_PATH)

        release = release_report()
        release["release_metadata"]["asset_checksums"][0]["sha256"] = "0" * 64
        mismatch = build_report(module, release=release)
        self.assertEqual(mismatch["comparison_status"], "blocked_checksum_mismatch")
        self.assertEqual(mismatch["blocked_reason_codes"], ["checksum_mismatch"])

        release = release_report()
        release["release_metadata"]["asset_checksums"].pop()
        missing = build_report(module, release=release)
        self.assertEqual(missing["comparison_status"], "blocked_checksum_mismatch")
        self.assertEqual(missing["blocked_reason_codes"], ["checksum_mismatch"])

        release = release_report()
        release["release_metadata"]["asset_checksums"].append(
            copy.deepcopy(release["release_metadata"]["asset_checksums"][0])
        )
        duplicate = build_report(module, release=release)
        self.assertEqual(duplicate["comparison_status"], "blocked_checksum_mismatch")
        self.assertEqual(duplicate["blocked_reason_codes"], ["checksum_mismatch"])

        release = release_report()
        release["release_metadata"]["asset_checksums"] = []
        empty = build_report(module, release=release)
        self.assertEqual(empty["comparison_status"], "blocked_missing_checksum")
        self.assertEqual(empty["blocked_reason_codes"], ["missing_checksum_asset"])

    def test_asset_checksum_verification_must_be_literal_true(self) -> None:
        module = load_module("corpus_ratchet_literal_checksum_verified_test", RATCHET_PATH)

        for value in ("true", "false", 1):
            with self.subTest(value=value):
                report = build_report(module, asset_checksums_verified=value)

                self.assertEqual(report["comparison_status"], "blocked_checksum_mismatch")
                self.assertEqual(report["blocked_reason_codes"], ["checksum_mismatch"])
                self.assertIs(report["asset_checksums_verified"], False)

        mutated = build_report(module)
        mutated["asset_checksums_verified"] = "true"
        self.assertEqual(module.validate_ratchet_report(mutated), ["report_schema_invalid"])

    def test_planned_asset_names_must_match_release_identity_exactly(self) -> None:
        module = load_module("corpus_ratchet_asset_name_identity_test", RATCHET_PATH)

        cases = [
            ("path_like_asset_name", "nested/mythic-edge-corpus-0.0.0-preview.tar.gz"),
            ("wrong_public_asset_name", "unexpected-public-asset.json"),
        ]
        for name, replacement in cases:
            with self.subTest(name=name):
                release = release_report()
                release["planned_assets"][0]["asset_name"] = replacement
                release["release_metadata"]["asset_checksums"] = checksum_entries_for(release)

                report = build_report(
                    module,
                    release=release,
                    expected_asset_checksums=expected_checksums_for(release),
                )

                self.assertEqual(report["comparison_status"], "blocked_missing_release")
                self.assertEqual(report["blocked_reason_codes"], ["missing_package_asset"])

        release = release_report()
        release["planned_assets"][1]["asset_name"] = release["planned_assets"][0]["asset_name"]
        collapsed = expected_checksums_for(release)
        release["release_metadata"]["asset_checksums"] = [
            {"algorithm": "sha256", "asset_name": asset_name, "sha256": sha256}
            for asset_name, sha256 in collapsed.items()
        ]

        duplicate = build_report(module, release=release, expected_asset_checksums=collapsed)

        self.assertEqual(duplicate["comparison_status"], "blocked_missing_release")
        self.assertEqual(duplicate["blocked_reason_codes"], ["missing_package_asset"])

    def test_expected_asset_checksums_must_match_planned_assets_exactly(self) -> None:
        module = load_module("corpus_ratchet_expected_checksum_test", RATCHET_PATH)
        expected = {
            asset["asset_name"]: asset["sha256"]
            for asset in release_report()["planned_assets"]
        }

        missing_evidence = build_report(module, expected_asset_checksums={})
        self.assertEqual(missing_evidence["comparison_status"], "blocked_missing_checksum")
        self.assertEqual(missing_evidence["blocked_reason_codes"], ["missing_checksum_asset"])

        missing_asset = build_report(
            module,
            expected_asset_checksums={
                name: checksum
                for name, checksum in expected.items()
                if name != "mythic-edge-corpus-0.0.0-preview.tar.gz"
            },
        )
        self.assertEqual(missing_asset["comparison_status"], "blocked_checksum_mismatch")
        self.assertEqual(missing_asset["blocked_reason_codes"], ["checksum_mismatch"])

        extra_asset = build_report(
            module,
            expected_asset_checksums={**expected, "unexpected-public-asset.json": "0" * 64},
        )
        self.assertEqual(extra_asset["comparison_status"], "blocked_checksum_mismatch")
        self.assertEqual(extra_asset["blocked_reason_codes"], ["checksum_mismatch"])

    def test_malformed_comparison_output_and_forbidden_values_are_symbolic(self) -> None:
        module = load_module("corpus_ratchet_malformed_test", RATCHET_PATH)

        malformed = build_report(
            module,
            comparison_results=[
                {
                    **comparison_result("matched_expected_output"),
                    "result_category": "parser_truth_confirmed",
                }
            ],
        )
        self.assertEqual(malformed["comparison_status"], "invalid")
        self.assertEqual(malformed["blocked_reason_codes"], ["comparison_output_invalid"])

        forbidden_value = "/" + "Users" + "/example/private/" + "Player" + ".log/" + "api_" + "key"
        forbidden_result = comparison_result("changed_output", review_required=True)
        forbidden_result["expected_ref"] = forbidden_value
        forbidden = build_report(module, comparison_results=[forbidden_result])
        rendered = json.dumps(forbidden, sort_keys=True)

        self.assertEqual(forbidden["comparison_status"], "blocked_forbidden_content")
        self.assertEqual(forbidden["blocked_reason_codes"], ["payload_or_metadata_contains_forbidden_content"])
        self.assertNotIn(forbidden_value, rendered)
        self.assertNotIn("Player" + ".log", rendered)

    def test_out_of_scope_actions_are_refused_with_no_write_guards_false(self) -> None:
        module = load_module("corpus_ratchet_action_test", RATCHET_PATH)

        checks = [
            ("ratchet_execution_requested", "unsupported", "ratchet_execution_requested"),
            ("baseline_mutation_requested", "blocked_baseline_mutation_requested", "baseline_mutation_requested"),
            ("baseline_pr_requested", "blocked_baseline_pr_requested", "baseline_pr_requested"),
            ("source_mutation_requested", "blocked_source_mutation_requested", "source_mutation_requested"),
            ("release_or_dispatch_requested", "blocked_release_or_dispatch_requested", "release_or_dispatch_requested"),
        ]
        for flag, status, reason in checks:
            with self.subTest(flag=flag):
                report = build_report(module, **{flag: True})
                self.assertEqual(report["comparison_status"], status)
                self.assertEqual(report["blocked_reason_codes"], [reason])
                self.assertTrue(all(value is False for value in report["no_write_guards"].values()))

    def test_validate_only_cli_accepts_public_safe_report(self) -> None:
        module = load_module("corpus_ratchet_cli_test", RATCHET_PATH)
        report_path = Path("tests") / ".tmp_ratchet_comparison_report.json"
        try:
            (ROOT / report_path).write_text(
                json.dumps(build_report(module), indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "tools/corpus_ratchet_comparison_report.py",
                    "--validate-only",
                    "--report",
                    str(report_path),
                    "--format",
                    "json",
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
        finally:
            (ROOT / report_path).unlink(missing_ok=True)

        self.assertEqual(result.returncode, 0)
        cli_report = json.loads(result.stdout)
        self.assertEqual(cli_report["comparison_status"], "comparison_completed_with_deltas")
        self.assertEqual(result.stderr, "")
        self.assertNotIn(str(ROOT), result.stdout)

    def test_validate_only_cli_rejects_unsafe_path_before_reading(self) -> None:
        unsafe_path = "/" + "Users" + "/example/private/" + "Player" + ".log"

        result = subprocess.run(
            [
                sys.executable,
                "tools/corpus_ratchet_comparison_report.py",
                "--validate-only",
                "--report",
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
        self.assertIn("payload_or_metadata_contains_forbidden_content", rendered)
        self.assertNotIn(unsafe_path, rendered)
        self.assertNotIn("Player" + ".log", rendered)

    def test_existing_report_validation_rejects_mutated_guards(self) -> None:
        module = load_module("corpus_ratchet_guard_validation_test", RATCHET_PATH)
        report = build_report(module)
        mutated = copy.deepcopy(report)
        mutated["no_write_guards"]["ratchet_executed"] = True

        self.assertEqual(module.validate_ratchet_report(mutated), ["report_schema_invalid"])


if __name__ == "__main__":
    unittest.main()
