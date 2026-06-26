from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RELEASE_PATH = ROOT / "tools/corpus_release_package.py"
SOURCE_COMMIT = "1e1c0bfbd9451ee60ee8c423a48d56202f8c7b64"
OTHER_COMMIT = "d650781ca9dd05a0f263f5347994f466600ba5d3"


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, RELEASE_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Unable to load module: {RELEASE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_package(root: Path, *, session_text: str | None = None) -> None:
    package = root / "corpus"
    (package / "sessions").mkdir(parents=True)
    (package / "README.md").write_text("Public-safe package notes.\n", encoding="utf-8")
    (package / "sessions/bootstrap_public_session.json").write_text(
        session_text
        or json.dumps(
            {
                "contains_private_data": False,
                "contains_raw_log": False,
                "fixture_id": "bootstrap_public_session_v1",
                "object": "mythic_edge_public_corpus_preview_fixture",
                "schema_version": "mythic_edge_public_corpus_preview_fixture.v1",
                "source_kind": "synthetic_public_metadata",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    manifest = {
        "entries": [
            {
                "path": "corpus/README.md",
                "public_safe": True,
                "role": "package_notes",
                "session_id": None,
            },
            {
                "path": "corpus/manifest.v1.json",
                "public_safe": True,
                "role": "package_manifest",
                "session_id": None,
            },
            {
                "path": "corpus/session_ledger.v1.json",
                "public_safe": True,
                "role": "session_ledger",
                "session_id": None,
            },
            {
                "path": "corpus/sessions/bootstrap_public_session.json",
                "public_safe": True,
                "role": "public_safe_synthetic_session_metadata",
                "session_id": "bootstrap-public-session-v1",
            },
        ],
        "object": "mythic_edge_corpus_package_manifest",
        "package_id": "test-package",
        "package_root": "corpus",
        "package_version": "0.0.0-preview",
        "schema_version": "mythic_edge_corpus_package_manifest.v1",
    }
    ledger = {
        "entries": [
            {
                "paths": ["corpus/sessions/bootstrap_public_session.json"],
                "public_safe": True,
                "session_id": "bootstrap-public-session-v1",
                "source_kind": "synthetic_public_metadata",
            }
        ],
        "ledger_id": "test-ledger",
        "object": "mythic_edge_corpus_session_ledger",
        "schema_version": "mythic_edge_corpus_session_ledger.v1",
    }
    write_json(package / "manifest.v1.json", manifest)
    write_json(package / "session_ledger.v1.json", ledger)


def clean_args(root: Path | None = None) -> dict[str, Any]:
    return {
        "package_root": "corpus",
        "manifest_path": "corpus/manifest.v1.json",
        "session_ledger_path": "corpus/session_ledger.v1.json",
        "package_version": "0.0.0-preview",
        "source_commit": SOURCE_COMMIT,
        "preview_source_commit": SOURCE_COMMIT,
        "pr_validation_source_commit": SOURCE_COMMIT,
        "repo_root": ROOT if root is None else root,
        "review_approved": True,
        "reviewed_by": "codex-e",
        "review_ref": "issue-16-review",
        "dry_run": True,
        "clean_worktree_confirmed": True,
    }


def build_report(module, root: Path | None = None, **overrides):
    args = clean_args(root)
    args.update(overrides)
    return module.build_release_report(**args)


class CorpusReleasePackageTests(unittest.TestCase):
    def test_committed_bootstrap_package_builds_reviewed_dry_run_metadata(self) -> None:
        module = load_module("corpus_release_committed_test")

        report = build_report(module)
        rendered = json.dumps(report, sort_keys=True)

        self.assertEqual(report["object"], "corpus_release_package_dry_run")
        self.assertEqual(report["schema_version"], "corpus_release_package_dry_run.v1")
        self.assertEqual(report["status"], "release_candidate_report_only")
        self.assertTrue(report["dry_run"])
        self.assertFalse(report["publish_requested"])
        self.assertEqual(report["release_tag"], "corpus-package-v0.0.0-preview")
        self.assertEqual(report["release_metadata"]["object"], "corpus_release_package_metadata")
        self.assertEqual(report["release_metadata"]["source_commit"], SOURCE_COMMIT)
        self.assertEqual(report["included_files_summary"]["total_included_files"], 4)
        self.assertEqual([asset["written"] for asset in report["planned_assets"]], [False, False, False])
        self.assertEqual([asset["published"] for asset in report["planned_assets"]], [False, False, False])
        self.assertTrue(all(value is False for value in report["no_write_guards"].values()))
        self.assertIn("not_parser_truth", report["non_claims"])
        self.assertNotIn(str(ROOT), rendered)

    def test_predecessor_refs_do_not_echo_extra_private_fields(self) -> None:
        module = load_module("corpus_release_predecessor_ref_safety_test")
        private_value = "/Us" + "ers/example/private/" + "Player" + ".log"

        preview = _passing_preview(module)()
        preview["manifest_ref"] = {
            "path": "corpus/manifest.v1.json",
            "private_source": private_value,
        }
        preview["session_ledger_ref"] = {
            "path": "corpus/session_ledger.v1.json",
            "private_source": private_value,
        }
        preview["private_source"] = private_value
        pr_validation = _passing_pr_validation(module)()
        pr_validation["private_source"] = private_value

        report = build_report(
            module,
            preview_builder=lambda **_kwargs: preview,
            pr_validation_builder=lambda **_kwargs: pr_validation,
        )
        rendered = json.dumps(report, sort_keys=True)

        self.assertEqual(report["status"], "release_candidate_report_only")
        self.assertEqual(
            report["release_metadata"]["manifest_ref"],
            {"path": "corpus/manifest.v1.json"},
        )
        self.assertEqual(
            report["release_metadata"]["session_ledger_ref"],
            {"path": "corpus/session_ledger.v1.json"},
        )
        self.assertEqual(
            report["release_metadata"]["package_preview_ref"],
            {
                "object": module.PREVIEW_OBJECT,
                "schema_version": module.PREVIEW_SCHEMA_VERSION,
                "status": module.PREVIEW_PASSED_STATUS,
                "source_commit": SOURCE_COMMIT,
            },
        )
        self.assertEqual(
            report["release_metadata"]["pr_validation_ref"],
            {
                "object": module.PR_VALIDATION_OBJECT,
                "schema_version": module.PR_VALIDATION_SCHEMA_VERSION,
                "status": module.PR_VALIDATION_PASSED_STATUS,
                "source_commit": SOURCE_COMMIT,
            },
        )
        self.assertNotIn(private_value, rendered)
        self.assertNotIn("Player" + ".log", rendered)

    def test_cli_json_output_is_dry_run_and_stdout_only(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "tools/corpus_release_package.py",
                "--package-root",
                "corpus",
                "--manifest",
                "corpus/manifest.v1.json",
                "--session-ledger",
                "corpus/session_ledger.v1.json",
                "--package-version",
                "0.0.0-preview",
                "--source-commit",
                SOURCE_COMMIT,
                "--preview-source-commit",
                SOURCE_COMMIT,
                "--pr-validation-source-commit",
                SOURCE_COMMIT,
                "--reviewed-by",
                "codex-e",
                "--review-ref",
                "issue-16-review",
                "--dry-run",
                "--clean-worktree-confirmed",
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
        self.assertEqual(report["status"], "release_candidate_report_only")
        self.assertEqual(report["blocked_reason_codes"], [])
        self.assertEqual(result.stderr, "")

    def test_missing_preview_and_preview_failure_fail_closed(self) -> None:
        module = load_module("corpus_release_preview_blocks_test")

        missing = build_report(module, preview_builder=None)
        self.assertEqual(missing["status"], "blocked_missing_preview_command")
        self.assertEqual(missing["blocked_reason_codes"], ["preview_command_missing"])

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_package(root)
            (root / "corpus/manifest.v1.json").unlink()

            failed = build_report(module, root)

        self.assertEqual(failed["status"], "blocked_preview_failed")
        self.assertEqual(failed["blocked_reason_codes"], ["preview_status_blocked_missing_manifest"])

    def test_missing_and_failed_pr_validation_fail_closed(self) -> None:
        module = load_module("corpus_release_pr_blocks_test")

        missing = build_report(module, pr_validation_builder=None)
        self.assertEqual(missing["status"], "blocked_missing_pr_validation")
        self.assertEqual(missing["blocked_reason_codes"], ["pr_validation_missing"])

        failed = build_report(
            module,
            pr_validation_builder=lambda **_kwargs: {
                "changed_package_files": [],
                "object": module.PR_VALIDATION_OBJECT,
                "schema_version": module.PR_VALIDATION_SCHEMA_VERSION,
                "status": "blocked_unsafe_path",
            },
        )
        self.assertEqual(failed["status"], "blocked_pr_validation_failed")
        self.assertEqual(failed["blocked_reason_codes"], ["pr_validation_status_blocked_unsafe_path"])

    def test_stale_predecessor_source_commit_fails_closed(self) -> None:
        module = load_module("corpus_release_stale_commit_test")

        report = build_report(module, preview_source_commit=OTHER_COMMIT)

        self.assertEqual(report["status"], "blocked_invalid_metadata")
        self.assertEqual(report["blocked_reason_codes"], ["predecessor_source_commit_mismatch"])

    def test_unreviewed_non_default_and_unclean_candidates_fail_closed(self) -> None:
        module = load_module("corpus_release_review_branch_clean_test")

        unreviewed = build_report(module, review_approved=False, reviewed_by=None, review_ref=None)
        self.assertEqual(unreviewed["status"], "blocked_unreviewed_candidate")
        self.assertEqual(unreviewed["blocked_reason_codes"], ["human_review_missing"])

        missing_reviewer = build_report(module, reviewed_by=None, review_ref="issue-16-review")
        self.assertEqual(missing_reviewer["status"], "blocked_unreviewed_candidate")
        self.assertEqual(missing_reviewer["blocked_reason_codes"], ["reviewer_missing"])

        missing_review_ref = build_report(module, reviewed_by="codex-e", review_ref=None)
        self.assertEqual(missing_review_ref["status"], "blocked_unreviewed_candidate")
        self.assertEqual(missing_review_ref["blocked_reason_codes"], ["review_ref_missing"])

        non_default = build_report(module, source_branch="feature/test")
        self.assertEqual(non_default["status"], "blocked_non_default_branch")

        unclean = build_report(module, clean_worktree_confirmed=False)
        self.assertEqual(unclean["status"], "blocked_invalid_metadata")
        self.assertEqual(unclean["blocked_reason_codes"], ["clean_worktree_not_confirmed"])

    def test_existing_tag_existing_asset_and_checksum_mismatch_fail_closed(self) -> None:
        module = load_module("corpus_release_identity_blocks_test")

        existing_tag = build_report(module, existing_tags=("corpus-package-v0.0.0-preview",))
        self.assertEqual(existing_tag["status"], "blocked_existing_tag")

        existing_asset = build_report(
            module,
            existing_assets=("mythic-edge-corpus-0.0.0-preview.metadata.json",),
        )
        self.assertEqual(existing_asset["status"], "blocked_existing_asset")

        mismatch = build_report(
            module,
            expected_asset_checksums={
                "mythic-edge-corpus-0.0.0-preview.tar.gz": "0" * 64,
            },
        )
        self.assertEqual(mismatch["status"], "blocked_invalid_metadata")
        self.assertEqual(mismatch["blocked_reason_codes"], ["asset_checksum_mismatch"])

    def test_cli_invalid_expected_checksum_fails_closed_without_ignoring_value(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "tools/corpus_release_package.py",
                "--package-root",
                "corpus",
                "--manifest",
                "corpus/manifest.v1.json",
                "--session-ledger",
                "corpus/session_ledger.v1.json",
                "--package-version",
                "0.0.0-preview",
                "--source-commit",
                SOURCE_COMMIT,
                "--preview-source-commit",
                SOURCE_COMMIT,
                "--pr-validation-source-commit",
                SOURCE_COMMIT,
                "--reviewed-by",
                "codex-e",
                "--review-ref",
                "issue-16-review",
                "--dry-run",
                "--clean-worktree-confirmed",
                "--expected-asset-checksum",
                "mythic-edge-corpus-0.0.0-preview.tar.gz=not-a-sha",
                "--format",
                "json",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stderr, "")
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "blocked_invalid_metadata")
        self.assertEqual(report["blocked_reason_codes"], ["expected_asset_checksum_value_invalid"])

    def test_cli_partial_review_metadata_fails_closed_with_specific_reason(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "tools/corpus_release_package.py",
                "--package-root",
                "corpus",
                "--manifest",
                "corpus/manifest.v1.json",
                "--session-ledger",
                "corpus/session_ledger.v1.json",
                "--package-version",
                "0.0.0-preview",
                "--source-commit",
                SOURCE_COMMIT,
                "--preview-source-commit",
                SOURCE_COMMIT,
                "--pr-validation-source-commit",
                SOURCE_COMMIT,
                "--reviewed-by",
                "codex-e",
                "--dry-run",
                "--clean-worktree-confirmed",
                "--format",
                "json",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stderr, "")
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "blocked_unreviewed_candidate")
        self.assertEqual(report["blocked_reason_codes"], ["review_ref_missing"])

    def test_release_scan_blocks_unsafe_package_contents_without_echo(self) -> None:
        module = load_module("corpus_release_content_scan_test")
        forbidden = "unsafe " + "Player" + ".log marker"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_package(root, session_text=forbidden)

            report = build_report(
                module,
                root,
                preview_builder=_passing_preview(module),
                pr_validation_builder=_passing_pr_validation(module),
            )
            rendered = json.dumps(report, sort_keys=True)

        self.assertEqual(report["status"], "blocked_forbidden_content")
        self.assertEqual(report["blocked_reason_codes"], ["blocked_forbidden_content"])
        self.assertNotIn(forbidden, rendered)

    def test_publish_and_downstream_requests_are_unsupported_or_blocked(self) -> None:
        module = load_module("corpus_release_downstream_blocks_test")

        publish = build_report(module, publish=True)
        self.assertEqual(publish["status"], "unsupported")
        self.assertEqual(publish["blocked_reason_codes"], ["publish_mode_requires_separate_authorization"])

        dispatch = build_report(module, dispatch_requested=True)
        self.assertEqual(dispatch["status"], "blocked_dispatch_requested")

        ratchet = build_report(module, ratchet_requested=True)
        self.assertEqual(ratchet["status"], "blocked_ratchet_requested")

        baseline = build_report(module, baseline_pr_requested=True)
        self.assertEqual(baseline["status"], "blocked_baseline_pr_requested")

    def test_dry_run_output_is_deterministic(self) -> None:
        module = load_module("corpus_release_deterministic_test")

        first = build_report(module)
        second = build_report(module)

        self.assertEqual(first, second)


def _passing_preview(module):
    def build(**_kwargs):
        return {
            "blocked_reason_codes": [],
            "inventory": [
                {"path": "corpus/README.md", "session_id": None},
                {"path": "corpus/manifest.v1.json", "session_id": None},
                {"path": "corpus/session_ledger.v1.json", "session_id": None},
                {"path": "corpus/sessions/bootstrap_public_session.json", "session_id": "bootstrap"},
            ],
            "manifest_ref": {"path": "corpus/manifest.v1.json"},
            "object": module.PREVIEW_OBJECT,
            "package_id": "test-package",
            "package_version": "0.0.0-preview",
            "schema_version": module.PREVIEW_SCHEMA_VERSION,
            "session_ledger_ref": {"path": "corpus/session_ledger.v1.json"},
            "status": module.PREVIEW_PASSED_STATUS,
            "summary": {
                "total_declared_manifest_entries": 4,
                "total_session_ledger_entries": 1,
            },
        }

    return build


def _passing_pr_validation(module):
    def build(**_kwargs):
        return {
            "changed_package_files": [
                "corpus/README.md",
                "corpus/manifest.v1.json",
                "corpus/session_ledger.v1.json",
                "corpus/sessions/bootstrap_public_session.json",
            ],
            "object": module.PR_VALIDATION_OBJECT,
            "schema_version": module.PR_VALIDATION_SCHEMA_VERSION,
            "status": module.PR_VALIDATION_PASSED_STATUS,
        }

    return build


if __name__ == "__main__":
    unittest.main()
