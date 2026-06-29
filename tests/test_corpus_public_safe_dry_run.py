from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRY_RUN_PATH = ROOT / "tools/corpus_public_safe_dry_run.py"
SOURCE_COMMIT = "e2b2325ccccf6cd470d38beb7e42e0080b927546"
SYNTHETIC_MYTHIC_EDGE_COMMIT = "0" * 40


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, DRY_RUN_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Unable to load module: {DRY_RUN_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class CorpusPublicSafeDryRunTests(unittest.TestCase):
    def test_committed_bootstrap_package_completes_no_external_action_dry_run(
        self,
    ) -> None:
        module = load_module("corpus_public_safe_dry_run_happy_test")

        report = module.build_public_safe_dry_run_report(
            repo_root=ROOT,
            source_commit=SOURCE_COMMIT,
            mythic_edge_commit=SYNTHETIC_MYTHIC_EDGE_COMMIT,
        )
        rendered = json.dumps(report, sort_keys=True)

        self.assertEqual(report["object"], "corpus_public_safe_end_to_end_dry_run")
        self.assertEqual(
            report["schema_version"],
            "corpus_public_safe_end_to_end_dry_run.v1",
        )
        self.assertEqual(report["status"], "public_safe_dry_run_complete")
        self.assertEqual(
            {stage["name"]: stage["status"] for stage in report["stages"]},
            {
                "package_preview": "preview_report_only",
                "pr_validation": "passed_report_only",
                "release_dry_run": "release_candidate_report_only",
                "dispatch_no_send": "dry_run_payload_ready",
                "ratchet_report": "comparison_completed_with_no_deltas",
                "baseline_proposal": "proposal_preview_no_deltas",
            },
        )
        self.assertEqual(report["blocked_reason_codes"], [])
        self.assertEqual(len(report["release_assets"]), 3)
        self.assertTrue(
            all(value is False for value in report["no_external_action_guards"].values())
        )
        for stage in report["stages"]:
            self.assertTrue(
                all(value is False for value in stage["external_actions"].values())
            )
        self.assertFalse(report["ready_for_external_action"])
        self.assertFalse(report["ready_for_corpus_readiness_claim"])
        self.assertIn("not_parser_truth", report["non_claims"])
        self.assertNotIn(str(ROOT), rendered)

    def test_cli_json_output_is_report_only_and_stdout_only(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "tools/corpus_public_safe_dry_run.py",
                "--source-commit",
                SOURCE_COMMIT,
                "--mythic-edge-commit",
                SYNTHETIC_MYTHIC_EDGE_COMMIT,
                "--format",
                "json",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "public_safe_dry_run_complete")
        self.assertEqual(report["blocked_reason_codes"], [])
        self.assertEqual(result.stderr, "")

    def test_invalid_input_fails_closed_without_echoing_unsafe_values(self) -> None:
        module = load_module("corpus_public_safe_dry_run_invalid_input_test")
        unsafe_value = "/" + "Users/example/private/source"

        report = module.build_public_safe_dry_run_report(
            repo_root=ROOT,
            source_commit=unsafe_value,
            mythic_edge_commit=SYNTHETIC_MYTHIC_EDGE_COMMIT,
        )
        rendered = json.dumps(report, sort_keys=True)

        self.assertEqual(report["status"], "public_safe_dry_run_blocked")
        self.assertEqual(report["blocked_reason_codes"], ["source_commit_invalid"])
        self.assertNotIn(unsafe_value, rendered)


if __name__ == "__main__":
    unittest.main()
