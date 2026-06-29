from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from unittest import mock
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DISPATCH_PATH = ROOT / "tools/corpus_repository_dispatch.py"
RELEASE_PATH = ROOT / "tools/corpus_release_package.py"
SOURCE_COMMIT = "1e1c0bfbd9451ee60ee8c423a48d56202f8c7b64"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Unable to load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def release_report() -> dict[str, Any]:
    release = load_module("corpus_release_for_dispatch_test", RELEASE_PATH)
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


def build_report(module, release: dict[str, Any] | None = None, **overrides):
    args = {"release_report": release_report() if release is None else release}
    args.update(overrides)
    return module.build_dispatch_report(**args)


class CorpusRepositoryDispatchTests(unittest.TestCase):
    def test_release_report_builds_payload_only_dry_run_notification(self) -> None:
        module = load_module("corpus_repository_dispatch_happy_test", DISPATCH_PATH)

        report = build_report(module)
        rendered = json.dumps(report, sort_keys=True)
        payload = report["payload"]

        self.assertEqual(report["object"], "corpus_repository_dispatch_no_send_validation")
        self.assertEqual(report["schema_version"], "corpus_repository_dispatch_no_send.v1")
        self.assertEqual(report["status"], "dry_run_payload_ready")
        self.assertEqual(report["event_name"], module.DRY_RUN_EVENT_NAME)
        self.assertTrue(report["payload_only"])
        self.assertFalse(report["send_requested"])
        self.assertFalse(report["repository_dispatch_sent"])
        self.assertTrue(all(value is False for value in report["no_send_guards"].values()))
        self.assertEqual(report["blocked_reason_codes"], [])
        self.assertEqual(report["non_claims"], list(module.NON_CLAIMS))
        self.assertNotIn(str(ROOT), rendered)

        self.assertEqual(payload["schema_version"], module.PAYLOAD_SCHEMA_VERSION)
        self.assertEqual(payload["source_repository"], module.REPOSITORY)
        self.assertEqual(payload["target_repository"], module.TARGET_REPOSITORY)
        self.assertEqual(payload["package_id"], module.PACKAGE_ID)
        self.assertEqual(payload["package_version"], "0.0.0-preview")
        self.assertEqual(payload["release_tag"], "corpus-package-v0.0.0-preview")
        self.assertEqual(payload["release_source_commit"], SOURCE_COMMIT)
        self.assertEqual(payload["release_channel"], "reviewed")
        self.assertEqual(module.validate_dispatch_payload(payload), [])
        self.assertEqual(
            {
                payload["package_asset_name"],
                payload["release_metadata_asset_name"],
                payload["checksum_asset_name"],
            },
            {item["asset_name"] for item in payload["asset_checksums"]},
        )

    def test_cli_json_output_is_payload_only_and_stdout_only(self) -> None:
        release_path = Path("tests") / ".tmp_dispatch_release_report.json"
        try:
            (ROOT / release_path).write_text(
                json.dumps(release_report(), indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "tools/corpus_repository_dispatch.py",
                    "--release-report",
                    str(release_path),
                    "--package-version",
                    "0.0.0-preview",
                    "--payload-only",
                    "--format",
                    "json",
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
        finally:
            (ROOT / release_path).unlink(missing_ok=True)

        self.assertEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "dry_run_payload_ready")
        self.assertFalse(report["repository_dispatch_sent"])
        self.assertEqual(result.stderr, "")
        self.assertNotIn(str(ROOT), result.stdout)

    def test_unsafe_release_report_path_is_rejected_before_filesystem_access(self) -> None:
        module = load_module("corpus_repository_dispatch_path_preflight_test", DISPATCH_PATH)

        unsafe_paths = (
            "/" + "Users" + "/example/release_report.json",
            "release_" + "api_" + "key" + ".json",
            "private-" + "Player" + ".log",
        )
        for unsafe_path in unsafe_paths:
            with self.subTest(unsafe_path=unsafe_path):
                with (
                    mock.patch.object(Path, "exists", side_effect=AssertionError("exists called")),
                    mock.patch.object(Path, "read_text", side_effect=AssertionError("read_text called")),
                ):
                    with self.assertRaises(ValueError) as context:
                        module._load_release_report(unsafe_path)

                self.assertEqual(str(context.exception), "payload_contains_forbidden_content")
                self.assertNotIn(unsafe_path, str(context.exception))

    def test_cli_unsafe_release_report_path_is_symbolic_and_not_echoed(self) -> None:
        unsafe_path = "/" + "Users" + "/example/release_report.json"

        result = subprocess.run(
            [
                sys.executable,
                "tools/corpus_repository_dispatch.py",
                "--release-report",
                unsafe_path,
                "--payload-only",
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
        self.assertIn("payload_contains_forbidden_content", rendered)
        self.assertNotIn(unsafe_path, rendered)
        self.assertNotIn("/" + "Users" + "/", rendered)

    def test_missing_release_report_and_failed_release_status_fail_closed(self) -> None:
        module = load_module("corpus_repository_dispatch_missing_release_test", DISPATCH_PATH)

        missing = module.build_dispatch_report(release_report=None)
        self.assertEqual(missing["status"], "blocked_release_not_published")
        self.assertEqual(missing["blocked_reason_codes"], ["missing_release_metadata"])

        failed_release = release_report()
        failed_release["status"] = "blocked_preview_failed"
        failed = build_report(module, failed_release)
        self.assertEqual(failed["status"], "blocked_release_validation_failed")
        self.assertEqual(failed["blocked_reason_codes"], ["blocked_release_validation_failed"])
        self.assertIsNone(failed["payload"])

    def test_missing_assets_and_checksum_mismatch_fail_closed(self) -> None:
        module = load_module("corpus_repository_dispatch_asset_test", DISPATCH_PATH)
        report_without_package = release_report()
        report_without_package["planned_assets"] = [
            item for item in report_without_package["planned_assets"] if item["role"] != "package_archive"
        ]

        missing_asset = build_report(module, report_without_package)
        self.assertEqual(missing_asset["status"], "blocked_release_validation_failed")
        self.assertEqual(missing_asset["blocked_reason_codes"], ["missing_release_asset"])

        report_without_checksum = release_report()
        report_without_checksum["planned_assets"] = [
            item for item in report_without_checksum["planned_assets"] if item["role"] != "checksum_manifest"
        ]
        missing_checksum = build_report(module, report_without_checksum)
        self.assertEqual(missing_checksum["blocked_reason_codes"], ["missing_checksum_asset"])

        mismatch = build_report(
            module,
            expected_asset_checksums={
                "mythic-edge-corpus-0.0.0-preview.tar.gz": "0" * 64,
            },
        )
        self.assertEqual(mismatch["status"], "blocked_release_validation_failed")
        self.assertEqual(mismatch["blocked_reason_codes"], ["checksum_mismatch"])

    def test_payload_forbidden_content_is_symbolic_and_not_echoed(self) -> None:
        module = load_module("corpus_repository_dispatch_forbidden_test", DISPATCH_PATH)
        release = release_report()
        forbidden = "/" + "Users" + "/example/" + "Player" + ".log/" + "api_" + "key"
        release["release_metadata"]["private_source"] = forbidden

        report = build_report(module, release)
        rendered = json.dumps(report, sort_keys=True)

        self.assertEqual(report["status"], "blocked_payload_forbidden_content")
        self.assertEqual(report["blocked_reason_codes"], ["payload_contains_forbidden_content"])
        self.assertIsNone(report["payload"])
        self.assertNotIn(forbidden, rendered)
        self.assertNotIn("Player" + ".log", rendered)

    def test_event_names_send_and_downstream_actions_are_refused(self) -> None:
        module = load_module("corpus_repository_dispatch_action_test", DISPATCH_PATH)

        unknown = build_report(module, event_name="run_ratchet")
        self.assertEqual(unknown["status"], "blocked_missing_receiver_allowlist")
        self.assertEqual(unknown["blocked_reason_codes"], ["event_name_not_allowlisted"])

        non_dry = build_report(module, event_name=module.EVENT_NAME)
        self.assertEqual(non_dry["status"], "unsupported")
        self.assertEqual(non_dry["blocked_reason_codes"], ["non_dry_run_event_requires_separate_authorization"])

        send = build_report(module, send_requested=True)
        self.assertEqual(send["status"], "blocked_missing_token")
        self.assertEqual(send["blocked_reason_codes"], ["credential_missing"])

        ratchet = build_report(module, ratchet_requested=True)
        self.assertEqual(ratchet["status"], "blocked_ratchet_requested")
        self.assertEqual(ratchet["blocked_reason_codes"], ["payload_requests_ratchet"])

        baseline = build_report(module, baseline_pr_requested=True)
        self.assertEqual(baseline["status"], "blocked_baseline_pr_requested")
        self.assertEqual(baseline["blocked_reason_codes"], ["payload_requests_baseline_pr"])

        mutation = build_report(module, source_mutation_requested=True)
        self.assertEqual(mutation["status"], "blocked_source_mutation_requested")
        self.assertEqual(mutation["blocked_reason_codes"], ["payload_requests_source_mutation"])

        asset_creation = build_report(module, release_or_asset_creation_requested=True)
        self.assertEqual(asset_creation["status"], "blocked_release_or_asset_creation_requested")
        self.assertEqual(asset_creation["blocked_reason_codes"], ["release_or_asset_creation_requested"])

    def test_version_tag_and_source_commit_mismatches_fail_closed(self) -> None:
        module = load_module("corpus_repository_dispatch_identity_test", DISPATCH_PATH)

        tag_mismatch = release_report()
        tag_mismatch["release_tag"] = "corpus-package-v0.0.1"
        tag_result = build_report(module, tag_mismatch)
        self.assertEqual(tag_result["status"], "blocked_release_validation_failed")
        self.assertEqual(tag_result["blocked_reason_codes"], ["release_tag_mismatch"])

        version_mismatch = release_report()
        version_mismatch["package_version"] = "0.0.0/unsafe"
        version_result = build_report(module, version_mismatch)
        self.assertEqual(version_result["status"], "blocked_release_validation_failed")
        self.assertEqual(version_result["blocked_reason_codes"], ["package_version_mismatch"])

        commit_mismatch = release_report()
        commit_mismatch["source_commit"] = "abc1234"
        commit_result = build_report(module, commit_mismatch)
        self.assertEqual(commit_result["status"], "blocked_release_validation_failed")
        self.assertEqual(commit_result["blocked_reason_codes"], ["source_commit_mismatch"])

    def test_payload_schema_allowlist_blocks_extra_payload_keys(self) -> None:
        module = load_module("corpus_repository_dispatch_payload_schema_test", DISPATCH_PATH)
        report = build_report(module)
        payload = copy.deepcopy(report["payload"])
        payload["run_ratchet"] = True

        self.assertEqual(module.validate_dispatch_payload(payload), ["payload_contains_forbidden_content"])

        payload = copy.deepcopy(report["payload"])
        payload["package_asset_url"] = "https://example.com/package.tar.gz"
        self.assertEqual(module.validate_dispatch_payload(payload), ["payload_schema_invalid"])

        payload = copy.deepcopy(report["payload"])
        payload["non_claims"] = ["notification_only"]
        self.assertEqual(module.validate_dispatch_payload(payload), ["payload_schema_invalid"])

    def test_direct_payload_forbidden_extra_keys_fail_closed(self) -> None:
        module = load_module("corpus_repository_dispatch_direct_payload_key_test", DISPATCH_PATH)
        report = build_report(module)

        for forbidden_key in (
            "parser" + "_truth_claimed",
            "repository" + "_dispatch_sent",
            "raw" + "_corpus_payload",
            "fixture" + "_promotion_claimed",
        ):
            with self.subTest(forbidden_key=forbidden_key):
                payload = copy.deepcopy(report["payload"])
                payload[forbidden_key] = "synthetic-public-value"

                self.assertEqual(module.validate_dispatch_payload(payload), ["payload_contains_forbidden_content"])

    def test_payload_checksum_items_fail_closed_on_forbidden_or_unexpected_keys(self) -> None:
        module = load_module("corpus_repository_dispatch_checksum_key_test", DISPATCH_PATH)
        report = build_report(module)
        payload = copy.deepcopy(report["payload"])
        forbidden_key = "parser" + "_truth_claimed"
        payload["asset_checksums"][0][forbidden_key] = True

        self.assertEqual(module.validate_dispatch_payload(payload), ["payload_contains_forbidden_content"])

        payload = copy.deepcopy(report["payload"])
        payload["asset_checksums"][0]["unexpected"] = "synthetic-public-value"
        self.assertEqual(module.validate_dispatch_payload(payload), ["payload_contains_forbidden_content"])

    def test_release_planned_assets_fail_closed_on_forbidden_or_unexpected_keys(self) -> None:
        module = load_module("corpus_repository_dispatch_release_asset_key_test", DISPATCH_PATH)
        release = release_report()
        forbidden_key = "raw" + "_corpus_payload"
        release["planned_assets"][0][forbidden_key] = "synthetic-public-value"

        forbidden = build_report(module, release)
        self.assertEqual(forbidden["status"], "blocked_release_validation_failed")
        self.assertEqual(forbidden["blocked_reason_codes"], ["payload_contains_forbidden_content"])
        self.assertIsNone(forbidden["payload"])

        release = release_report()
        release["planned_assets"][0]["unexpected"] = "synthetic-public-value"
        unexpected = build_report(module, release)
        self.assertEqual(unexpected["status"], "blocked_release_validation_failed")
        self.assertEqual(unexpected["blocked_reason_codes"], ["payload_schema_invalid"])
        self.assertIsNone(unexpected["payload"])

    def test_release_report_top_level_extra_keys_fail_closed(self) -> None:
        module = load_module("corpus_repository_dispatch_release_top_key_test", DISPATCH_PATH)
        release = release_report()
        forbidden_key = "repository" + "_dispatch_sent"
        release[forbidden_key] = True

        forbidden = build_report(module, release)
        self.assertEqual(forbidden["status"], "blocked_release_validation_failed")
        self.assertEqual(forbidden["blocked_reason_codes"], ["payload_contains_forbidden_content"])
        self.assertIsNone(forbidden["payload"])

        release = release_report()
        release["unexpected"] = "synthetic-public-value"
        unexpected = build_report(module, release)
        self.assertEqual(unexpected["status"], "blocked_release_validation_failed")
        self.assertEqual(unexpected["blocked_reason_codes"], ["payload_schema_invalid"])
        self.assertIsNone(unexpected["payload"])

    def test_release_metadata_extra_keys_fail_closed(self) -> None:
        module = load_module("corpus_repository_dispatch_release_metadata_key_test", DISPATCH_PATH)
        release = release_report()
        forbidden_key = "parser" + "_truth_claimed"
        release["release_metadata"][forbidden_key] = True

        forbidden = build_report(module, release)
        self.assertEqual(forbidden["status"], "blocked_release_validation_failed")
        self.assertEqual(forbidden["blocked_reason_codes"], ["payload_contains_forbidden_content"])
        self.assertIsNone(forbidden["payload"])

        release = release_report()
        release["release_metadata"]["unexpected"] = "synthetic-public-value"
        unexpected = build_report(module, release)
        self.assertEqual(unexpected["status"], "blocked_release_validation_failed")
        self.assertEqual(unexpected["blocked_reason_codes"], ["payload_schema_invalid"])
        self.assertIsNone(unexpected["payload"])

    def test_release_reference_nested_extra_keys_fail_closed(self) -> None:
        module = load_module("corpus_repository_dispatch_release_ref_key_test", DISPATCH_PATH)
        release = release_report()
        forbidden_key = "raw" + "_corpus_payload"
        release["manifest_ref"][forbidden_key] = "synthetic-public-value"

        forbidden = build_report(module, release)
        self.assertEqual(forbidden["status"], "blocked_release_validation_failed")
        self.assertEqual(forbidden["blocked_reason_codes"], ["payload_contains_forbidden_content"])
        self.assertIsNone(forbidden["payload"])

        release = release_report()
        release["package_preview_ref"]["unexpected"] = "synthetic-public-value"
        unexpected = build_report(module, release)
        self.assertEqual(unexpected["status"], "blocked_release_validation_failed")
        self.assertEqual(unexpected["blocked_reason_codes"], ["payload_schema_invalid"])
        self.assertIsNone(unexpected["payload"])

        release = release_report()
        release["review_ref"]["source" + "_mutation_requested"] = False
        action = build_report(module, release)
        self.assertEqual(action["status"], "blocked_release_validation_failed")
        self.assertEqual(action["blocked_reason_codes"], ["payload_contains_forbidden_content"])
        self.assertIsNone(action["payload"])

    def test_release_metadata_nested_extra_keys_fail_closed(self) -> None:
        module = load_module("corpus_repository_dispatch_release_metadata_nested_test", DISPATCH_PATH)
        release = release_report()
        forbidden_key = "parser" + "_truth_claimed"
        release["release_metadata"]["asset_checksums"][0][forbidden_key] = "synthetic-public-value"

        forbidden = build_report(module, release)
        self.assertEqual(forbidden["status"], "blocked_release_validation_failed")
        self.assertEqual(forbidden["blocked_reason_codes"], ["payload_contains_forbidden_content"])
        self.assertIsNone(forbidden["payload"])

        release = release_report()
        release["release_metadata"]["manifest_ref"]["unexpected"] = "synthetic-public-value"
        unexpected = build_report(module, release)
        self.assertEqual(unexpected["status"], "blocked_release_validation_failed")
        self.assertEqual(unexpected["blocked_reason_codes"], ["payload_schema_invalid"])
        self.assertIsNone(unexpected["payload"])

    def test_release_metadata_identity_mismatch_fails_closed(self) -> None:
        module = load_module("corpus_repository_dispatch_release_metadata_identity_test", DISPATCH_PATH)
        release = release_report()
        release["release_metadata"]["package_version"] = "0.0.1-preview"

        result = build_report(module, release)

        self.assertEqual(result["status"], "blocked_release_validation_failed")
        self.assertEqual(result["blocked_reason_codes"], ["payload_schema_invalid"])
        self.assertIsNone(result["payload"])

    def test_included_file_summary_paths_must_stay_in_corpus_package(self) -> None:
        module = load_module("corpus_repository_dispatch_included_path_test", DISPATCH_PATH)
        release = release_report()
        release["included_files_summary"]["paths"] = ["docs/public.json"]

        outside_top = build_report(module, release)
        self.assertEqual(outside_top["status"], "blocked_release_validation_failed")
        self.assertEqual(outside_top["blocked_reason_codes"], ["payload_schema_invalid"])
        self.assertIsNone(outside_top["payload"])

        release = release_report()
        release["release_metadata"]["included_files_summary"]["paths"] = ["corpus/../manifest.v1.json"]
        traversal_metadata = build_report(module, release)
        self.assertEqual(traversal_metadata["status"], "blocked_release_validation_failed")
        self.assertEqual(traversal_metadata["blocked_reason_codes"], ["payload_schema_invalid"])
        self.assertIsNone(traversal_metadata["payload"])

    def test_planned_assets_extra_and_duplicate_records_fail_closed(self) -> None:
        module = load_module("corpus_repository_dispatch_planned_asset_list_test", DISPATCH_PATH)
        release = release_report()
        release["planned_assets"].append(
            {
                "role": "ignored_role",
                "raw" + "_corpus_payload": "synthetic-public-value",
            }
        )

        forbidden_extra = build_report(module, release)
        self.assertEqual(forbidden_extra["status"], "blocked_release_validation_failed")
        self.assertEqual(forbidden_extra["blocked_reason_codes"], ["payload_contains_forbidden_content"])
        self.assertIsNone(forbidden_extra["payload"])

        release = release_report()
        release["planned_assets"].append(dict(release["planned_assets"][0]))
        duplicate_role = build_report(module, release)
        self.assertEqual(duplicate_role["status"], "blocked_release_validation_failed")
        self.assertEqual(duplicate_role["blocked_reason_codes"], ["payload_schema_invalid"])
        self.assertIsNone(duplicate_role["payload"])

        release = release_report()
        release["planned_assets"].append(
            {
                "algorithm": "sha256",
                "asset_name": "mythic-edge-corpus-extra.txt",
                "byte_count": 1,
                "published": False,
                "role": "unexpected_role",
                "sha256": "1" * 64,
                "written": False,
            }
        )
        unexpected_role = build_report(module, release)
        self.assertEqual(unexpected_role["status"], "blocked_release_validation_failed")
        self.assertEqual(unexpected_role["blocked_reason_codes"], ["payload_schema_invalid"])
        self.assertIsNone(unexpected_role["payload"])

    def test_release_metadata_checksums_must_reference_planned_assets(self) -> None:
        module = load_module("corpus_repository_dispatch_metadata_checksum_match_test", DISPATCH_PATH)
        release = release_report()
        release["release_metadata"]["asset_checksums"] = release["release_metadata"]["asset_checksums"][:-1]

        missing = build_report(module, release)
        self.assertEqual(missing["status"], "blocked_release_validation_failed")
        self.assertEqual(missing["blocked_reason_codes"], ["checksum_mismatch"])
        self.assertIsNone(missing["payload"])

        release = release_report()
        release["release_metadata"]["asset_checksums"].append(dict(release["release_metadata"]["asset_checksums"][0]))

        duplicate = build_report(module, release)
        self.assertEqual(duplicate["status"], "blocked_release_validation_failed")
        self.assertEqual(duplicate["blocked_reason_codes"], ["checksum_mismatch"])
        self.assertIsNone(duplicate["payload"])

        release = release_report()
        release["release_metadata"]["asset_checksums"].append(
            {
                "algorithm": "sha256",
                "asset_name": "mythic-edge-corpus-extra.txt",
                "sha256": "1" * 64,
            }
        )
        extra = build_report(module, release)
        self.assertEqual(extra["status"], "blocked_release_validation_failed")
        self.assertEqual(extra["blocked_reason_codes"], ["checksum_mismatch"])
        self.assertIsNone(extra["payload"])

        release = release_report()
        release["release_metadata"]["asset_checksums"][0]["sha256"] = "2" * 64
        mismatch = build_report(module, release)
        self.assertEqual(mismatch["status"], "blocked_release_validation_failed")
        self.assertEqual(mismatch["blocked_reason_codes"], ["checksum_mismatch"])
        self.assertIsNone(mismatch["payload"])

    def test_no_write_guard_extra_keys_fail_closed(self) -> None:
        module = load_module("corpus_repository_dispatch_no_write_guard_key_test", DISPATCH_PATH)
        release = release_report()
        forbidden_key = "fixture" + "_promotion_claimed"
        release["no_write_guards"][forbidden_key] = False

        forbidden = build_report(module, release)
        self.assertEqual(forbidden["status"], "blocked_release_validation_failed")
        self.assertEqual(forbidden["blocked_reason_codes"], ["payload_contains_forbidden_content"])
        self.assertIsNone(forbidden["payload"])

        release = release_report()
        release["no_write_guards"]["unexpected"] = False
        unexpected = build_report(module, release)
        self.assertEqual(unexpected["status"], "blocked_release_validation_failed")
        self.assertEqual(unexpected["blocked_reason_codes"], ["payload_schema_invalid"])
        self.assertIsNone(unexpected["payload"])

        release = release_report()
        release["no_write_guards"] = {}
        empty = build_report(module, release)
        self.assertEqual(empty["status"], "blocked_release_validation_failed")
        self.assertEqual(empty["blocked_reason_codes"], ["payload_schema_invalid"])
        self.assertIsNone(empty["payload"])

        release = release_report()
        release["no_write_guards"].pop("repository_dispatch_sent")
        missing = build_report(module, release)
        self.assertEqual(missing["status"], "blocked_release_validation_failed")
        self.assertEqual(missing["blocked_reason_codes"], ["payload_schema_invalid"])
        self.assertIsNone(missing["payload"])

        release = release_report()
        release["no_write_guards"]["repository_dispatch_sent"] = {"value": False}
        nested = build_report(module, release)
        self.assertEqual(nested["status"], "blocked_release_validation_failed")
        self.assertEqual(nested["blocked_reason_codes"], ["payload_schema_invalid"])
        self.assertIsNone(nested["payload"])


if __name__ == "__main__":
    unittest.main()
