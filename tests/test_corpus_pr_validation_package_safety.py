from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "tools/corpus_pr_validate_package_safety.py"


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Unable to load module: {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_package(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    package = root / "corpus"
    (package / "sessions").mkdir(parents=True)
    (package / "README.md").write_text("Public-safe package notes.\n", encoding="utf-8")
    (package / "sessions/bootstrap_public_session.json").write_text(
        json.dumps(
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
        "package_version": "0.0.0-test",
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
    return manifest, ledger


def build_report(module, root: Path, **overrides):
    args = {
        "base_ref": "origin/main",
        "head_ref": "HEAD",
        "package_root": "corpus",
        "manifest_path": "corpus/manifest.v1.json",
        "session_ledger_path": "corpus/session_ledger.v1.json",
        "repo_root": root,
    }
    args.update(overrides)
    return module.build_validation_report(**args)


class CorpusPrValidationPackageSafetyTests(unittest.TestCase):
    def test_committed_bootstrap_package_passes_report_only(self) -> None:
        module = load_module("corpus_pr_validation_committed_test")

        report = build_report(module, ROOT)
        rendered = json.dumps(report, sort_keys=True)

        self.assertEqual(report["object"], "corpus_pr_validation_package_safety")
        self.assertEqual(report["schema_version"], "corpus_pr_validation_package_safety.v1")
        self.assertEqual(report["status"], "passed_report_only")
        self.assertEqual(report["package_preview_ref"]["status"], "preview_report_only")
        self.assertEqual(report["blocked_reason_codes"], [])
        self.assertEqual(report["inventory_summary"]["total_included_files"], 4)
        self.assertEqual(report["manifest_session_summary"]["total_manifest_entries"], 4)
        self.assertTrue(all(value is False for value in report["no_write_guards"].values()))
        self.assertIn("not_parser_truth", report["non_claims"])
        self.assertNotIn(str(ROOT), rendered)

    def test_cli_text_and_json_output_are_report_only_and_stdout_only(self) -> None:
        text_result = subprocess.run(
            [
                sys.executable,
                "tools/corpus_pr_validate_package_safety.py",
                "--base-ref",
                "origin/main",
                "--head-ref",
                "HEAD",
                "--package-root",
                "corpus",
                "--manifest",
                "corpus/manifest.v1.json",
                "--session-ledger",
                "corpus/session_ledger.v1.json",
                "--format",
                "text",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(text_result.returncode, 0)
        self.assertIn("schema_version: corpus_pr_validation_package_safety.v1", text_result.stdout)
        self.assertIn("status: passed_report_only", text_result.stdout)
        self.assertIn("not_fixture_promotion", text_result.stdout)
        self.assertEqual(text_result.stderr, "")

        json_result = subprocess.run(
            [
                sys.executable,
                "tools/corpus_pr_validate_package_safety.py",
                "--base-ref",
                "origin/main",
                "--head-ref",
                "HEAD",
                "--package-root",
                "corpus",
                "--manifest",
                "corpus/manifest.v1.json",
                "--session-ledger",
                "corpus/session_ledger.v1.json",
                "--format",
                "json",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(json_result.returncode, 0)
        parsed = json.loads(json_result.stdout)
        self.assertEqual(parsed["status"], "passed_report_only")
        self.assertEqual(json_result.stderr, "")

    def test_main_returns_nonzero_for_blocked_state(self) -> None:
        module = load_module("corpus_pr_validation_main_blocked_test")
        stdout = io.StringIO()

        with redirect_stdout(stdout):
            code = module.main(
                [
                    "--base-ref",
                    "origin/main",
                    "--head-ref",
                    "HEAD",
                    "--package-root",
                    "corpus",
                    "--manifest",
                    "corpus/missing_manifest.v1.json",
                    "--session-ledger",
                    "corpus/session_ledger.v1.json",
                    "--format",
                    "json",
                ]
            )

        self.assertEqual(code, 2)
        report = json.loads(stdout.getvalue())
        self.assertEqual(report["status"], "blocked_missing_manifest")

    def test_missing_preview_command_fails_closed(self) -> None:
        module = load_module("corpus_pr_validation_missing_preview_test")

        report = build_report(module, ROOT, preview_builder=None)

        self.assertEqual(report["status"], "blocked_missing_preview_command")
        self.assertEqual(report["package_preview_ref"]["status"], "preview_missing")
        self.assertEqual(report["blocked_reason_codes"], ["preview_command_missing"])

    def test_preview_failure_and_invalid_output_fail_closed(self) -> None:
        module = load_module("corpus_pr_validation_preview_failure_test")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_package(root)
            (root / "corpus/manifest.v1.json").unlink()

            report = build_report(module, root)

        self.assertEqual(report["status"], "blocked_missing_manifest")
        self.assertEqual(report["package_preview_ref"]["status"], "blocked_missing_manifest")
        self.assertEqual(report["blocked_reason_codes"], ["manifest_missing"])

        malformed_report = build_report(
            module,
            ROOT,
            preview_builder=lambda **_kwargs: {"object": "unexpected", "status": "ok"},
        )
        self.assertEqual(malformed_report["status"], "blocked_preview_invalid_output")
        self.assertEqual(malformed_report["blocked_reason_codes"], ["preview_object_unsupported"])

    def test_unsafe_paths_and_ref_labels_fail_before_preview_without_echo(self) -> None:
        module = load_module("corpus_pr_validation_unsafe_input_test")

        unsafe_path = str(ROOT / "corpus/manifest.v1.json")
        report = build_report(module, ROOT, manifest_path=unsafe_path)
        rendered = json.dumps(report, sort_keys=True)

        self.assertEqual(report["status"], "blocked_unsafe_path")
        self.assertEqual(report["blocked_reason_codes"], ["path_contains_local_or_secret_marker"])
        self.assertNotIn(unsafe_path, rendered)

        unsafe_ref = str(ROOT)
        ref_report = build_report(module, ROOT, head_ref=unsafe_ref)
        ref_rendered = json.dumps(ref_report, sort_keys=True)

        self.assertEqual(ref_report["status"], "blocked_unsafe_path")
        self.assertEqual(ref_report["blocked_reason_codes"], ["head_ref_unsafe"])
        self.assertNotIn(unsafe_ref, ref_rendered)

    def test_forbidden_marker_and_package_artifact_map_to_symbolic_status(self) -> None:
        module = load_module("corpus_pr_validation_marker_artifact_test")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_package(root)
            forbidden = "unsafe " + "Player" + ".log marker"
            (root / "corpus/sessions/bootstrap_public_session.json").write_text(
                forbidden,
                encoding="utf-8",
            )

            report = build_report(module, root)
            rendered = json.dumps(report, sort_keys=True)

        self.assertEqual(report["status"], "blocked_forbidden_content")
        self.assertEqual(report["blocked_reason_codes"], ["forbidden_content_marker"])
        self.assertNotIn(forbidden, rendered)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest, _ledger = write_package(root)
            (root / "corpus/package.zip").write_text("archive placeholder\n", encoding="utf-8")
            manifest["entries"].append(
                {
                    "path": "corpus/package.zip",
                    "public_safe": True,
                    "role": "package_archive",
                    "session_id": None,
                }
            )
            write_json(root / "corpus/manifest.v1.json", manifest)

            artifact_report = build_report(module, root)

        self.assertEqual(artifact_report["status"], "blocked_package_artifact")
        self.assertEqual(artifact_report["blocked_reason_codes"], ["package_artifact_suffix"])

    def test_preview_output_metadata_values_fail_closed_without_echo(self) -> None:
        module = load_module("corpus_pr_validation_preview_metadata_sanitized_test")
        forbidden = "/" + "Users" + "/example/" + "api_" + "key"

        report = build_report(
            module,
            ROOT,
            preview_builder=lambda **_kwargs: {
                "object": module.PREVIEW_OBJECT,
                "schema_version": module.PREVIEW_SCHEMA_VERSION,
                "status": module.PREVIEW_PASSED_STATUS,
                "package_id": forbidden,
                "package_version": "0.0.0-test",
                "inventory": [{"path": "corpus/README.md", "session_id": None}],
                "summary": {
                    "total_declared_manifest_entries": 1,
                    "total_session_ledger_entries": 0,
                },
                "blocked_reason_codes": [],
            },
        )
        rendered = json.dumps(report, sort_keys=True)

        self.assertEqual(report["status"], "blocked_preview_invalid_output")
        self.assertEqual(report["package_preview_ref"]["status"], "preview_report_only")
        self.assertEqual(report["blocked_reason_codes"], ["preview_package_id_unsafe"])
        self.assertNotIn(forbidden, rendered)

    def test_preview_output_inventory_paths_fail_closed_without_echo(self) -> None:
        module = load_module("corpus_pr_validation_preview_inventory_sanitized_test")
        forbidden = "/" + "Users" + "/example/private.json"

        report = build_report(
            module,
            ROOT,
            preview_builder=lambda **_kwargs: {
                "object": module.PREVIEW_OBJECT,
                "schema_version": module.PREVIEW_SCHEMA_VERSION,
                "status": module.PREVIEW_PASSED_STATUS,
                "package_id": "test-package",
                "package_version": "0.0.0-test",
                "inventory": [
                    {"path": "corpus/README.md", "session_id": None},
                    {"path": forbidden, "session_id": None},
                ],
                "summary": {
                    "total_declared_manifest_entries": 2,
                    "total_session_ledger_entries": 0,
                },
                "blocked_reason_codes": [],
            },
        )
        rendered = json.dumps(report, sort_keys=True)

        self.assertEqual(report["status"], "blocked_preview_invalid_output")
        self.assertEqual(report["blocked_reason_codes"], ["preview_inventory_path_unsafe"])
        self.assertEqual(report["changed_package_files"], [])
        self.assertNotIn(forbidden, rendered)

    def test_preview_output_inventory_paths_outside_package_root_fail_closed(self) -> None:
        module = load_module("corpus_pr_validation_preview_inventory_root_test")

        report = build_report(
            module,
            ROOT,
            preview_builder=lambda **_kwargs: {
                "object": module.PREVIEW_OBJECT,
                "schema_version": module.PREVIEW_SCHEMA_VERSION,
                "status": module.PREVIEW_PASSED_STATUS,
                "package_id": "test-package",
                "package_version": "0.0.0-test",
                "inventory": [
                    {"path": "corpus/README.md", "session_id": None},
                    {"path": "docs/outside-package.json", "session_id": None},
                ],
                "summary": {
                    "total_declared_manifest_entries": 2,
                    "total_session_ledger_entries": 0,
                },
                "blocked_reason_codes": [],
            },
        )

        self.assertEqual(report["status"], "blocked_preview_invalid_output")
        self.assertEqual(
            report["blocked_reason_codes"],
            ["preview_inventory_path_outside_package_root"],
        )
        self.assertEqual(report["changed_package_files"], [])
        self.assertEqual(report["inventory_summary"]["paths"], [])

    def test_preview_output_session_ids_and_summary_counts_fail_closed_without_echo(self) -> None:
        module = load_module("corpus_pr_validation_preview_summary_sanitized_test")
        forbidden = "/" + "Users" + "/example/" + "credential"

        session_report = build_report(
            module,
            ROOT,
            preview_builder=lambda **_kwargs: {
                "object": module.PREVIEW_OBJECT,
                "schema_version": module.PREVIEW_SCHEMA_VERSION,
                "status": module.PREVIEW_PASSED_STATUS,
                "package_id": "test-package",
                "package_version": "0.0.0-test",
                "inventory": [{"path": "corpus/README.md", "session_id": forbidden}],
                "summary": {
                    "total_declared_manifest_entries": 1,
                    "total_session_ledger_entries": 1,
                },
                "blocked_reason_codes": [],
            },
        )
        session_rendered = json.dumps(session_report, sort_keys=True)

        self.assertEqual(session_report["status"], "blocked_preview_invalid_output")
        self.assertEqual(
            session_report["blocked_reason_codes"],
            ["preview_inventory_session_id_unsafe"],
        )
        self.assertNotIn(forbidden, session_rendered)

        count_report = build_report(
            module,
            ROOT,
            preview_builder=lambda **_kwargs: {
                "object": module.PREVIEW_OBJECT,
                "schema_version": module.PREVIEW_SCHEMA_VERSION,
                "status": module.PREVIEW_PASSED_STATUS,
                "package_id": "test-package",
                "package_version": "0.0.0-test",
                "inventory": [{"path": "corpus/README.md", "session_id": None}],
                "summary": {
                    "total_declared_manifest_entries": forbidden,
                    "total_session_ledger_entries": 0,
                },
                "blocked_reason_codes": [],
            },
        )
        count_rendered = json.dumps(count_report, sort_keys=True)

        self.assertEqual(count_report["status"], "blocked_preview_invalid_output")
        self.assertEqual(
            count_report["blocked_reason_codes"],
            ["preview_summary_total_declared_manifest_entries_invalid"],
        )
        self.assertNotIn(forbidden, count_rendered)

    def test_preview_output_reason_codes_fail_closed_without_echo(self) -> None:
        module = load_module("corpus_pr_validation_preview_reason_sanitized_test")
        forbidden = "/" + "Users" + "/example/" + "token"

        report = build_report(
            module,
            ROOT,
            preview_builder=lambda **_kwargs: {
                "object": module.PREVIEW_OBJECT,
                "schema_version": module.PREVIEW_SCHEMA_VERSION,
                "status": "blocked_unsafe_path",
                "package_id": "test-package",
                "package_version": "0.0.0-test",
                "inventory": [],
                "summary": {
                    "total_declared_manifest_entries": 0,
                    "total_session_ledger_entries": 0,
                },
                "blocked_reason_codes": [forbidden],
            },
        )
        rendered = json.dumps(report, sort_keys=True)

        self.assertEqual(report["status"], "blocked_preview_invalid_output")
        self.assertEqual(report["blocked_reason_codes"], ["preview_blocked_reason_unsafe"])
        self.assertNotIn(forbidden, rendered)

    def test_invalid_preview_status_is_sanitized_without_echo(self) -> None:
        module = load_module("corpus_pr_validation_preview_status_sanitized_test")
        forbidden = "/" + "Users" + "/example/" + "token"

        report = build_report(
            module,
            ROOT,
            preview_builder=lambda **_kwargs: {
                "object": module.PREVIEW_OBJECT,
                "schema_version": module.PREVIEW_SCHEMA_VERSION,
                "status": forbidden,
                "inventory": [],
                "summary": {},
                "blocked_reason_codes": [],
            },
        )
        rendered = json.dumps(report, sort_keys=True)

        self.assertEqual(report["status"], "blocked_preview_invalid_output")
        self.assertEqual(report["package_preview_ref"]["status"], "invalid")
        self.assertEqual(report["blocked_reason_codes"], ["preview_status_unsupported"])
        self.assertNotIn(forbidden, rendered)

    def test_deterministic_ordering_for_clean_package_proposal(self) -> None:
        module = load_module("corpus_pr_validation_ordering_test")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest, _ledger = write_package(root)
            (root / "corpus/a_notes.md").write_text("A notes.\n", encoding="utf-8")
            manifest["entries"].append(
                {
                    "path": "corpus/a_notes.md",
                    "public_safe": True,
                    "role": "package_notes",
                    "session_id": None,
                }
            )
            manifest["entries"] = list(reversed(manifest["entries"]))
            write_json(root / "corpus/manifest.v1.json", manifest)

            first = build_report(module, root)
            second = build_report(module, root)

        self.assertEqual(first, second)
        self.assertEqual(first["status"], "passed_report_only")
        self.assertEqual(
            first["changed_package_files"],
            [
                "corpus/README.md",
                "corpus/a_notes.md",
                "corpus/manifest.v1.json",
                "corpus/session_ledger.v1.json",
                "corpus/sessions/bootstrap_public_session.json",
            ],
        )


if __name__ == "__main__":
    unittest.main()
