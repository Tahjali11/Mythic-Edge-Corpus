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

ROOT = Path(__file__).resolve().parents[1]
PREVIEW_PATH = ROOT / "tools/corpus_package_preview.py"


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, PREVIEW_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Unable to load module: {PREVIEW_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_package(root: Path) -> tuple[dict, dict]:
    package = root / "corpus"
    (package / "sessions").mkdir(parents=True)
    (package / "README.md").write_text("Public-safe package notes.\n", encoding="utf-8")
    (package / "sessions/bootstrap_public_session.json").write_text(
        json.dumps(
            {
                "object": "mythic_edge_public_corpus_preview_fixture",
                "schema_version": "mythic_edge_public_corpus_preview_fixture.v1",
                "fixture_id": "bootstrap_public_session_v1",
                "source_kind": "synthetic_public_metadata",
                "contains_raw_log": False,
                "contains_private_data": False,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    manifest = {
        "object": "mythic_edge_corpus_package_manifest",
        "schema_version": "mythic_edge_corpus_package_manifest.v1",
        "package_id": "test-package",
        "package_version": "0.0.0-test",
        "package_root": "corpus",
        "entries": [
            {
                "path": "corpus/README.md",
                "role": "package_notes",
                "public_safe": True,
                "session_id": None,
            },
            {
                "path": "corpus/manifest.v1.json",
                "role": "package_manifest",
                "public_safe": True,
                "session_id": None,
            },
            {
                "path": "corpus/session_ledger.v1.json",
                "role": "session_ledger",
                "public_safe": True,
                "session_id": None,
            },
            {
                "path": "corpus/sessions/bootstrap_public_session.json",
                "role": "public_safe_synthetic_session_metadata",
                "public_safe": True,
                "session_id": "bootstrap-public-session-v1",
            },
        ],
    }
    ledger = {
        "object": "mythic_edge_corpus_session_ledger",
        "schema_version": "mythic_edge_corpus_session_ledger.v1",
        "ledger_id": "test-ledger",
        "entries": [
            {
                "session_id": "bootstrap-public-session-v1",
                "paths": ["corpus/sessions/bootstrap_public_session.json"],
                "source_kind": "synthetic_public_metadata",
                "public_safe": True,
            }
        ],
    }
    write_json(package / "manifest.v1.json", manifest)
    write_json(package / "session_ledger.v1.json", ledger)
    return manifest, ledger


def build_preview(module, root: Path) -> dict:
    return module.build_preview(
        package_root="corpus",
        manifest_path="corpus/manifest.v1.json",
        session_ledger_path="corpus/session_ledger.v1.json",
        repo_root=root,
    )


class CorpusPackagePreviewTests(unittest.TestCase):
    def test_committed_bootstrap_preview_is_report_only_and_public_safe(self) -> None:
        module = load_module("corpus_package_preview_committed_test")

        report = build_preview(module, ROOT)
        rendered = json.dumps(report, sort_keys=True)

        self.assertEqual(report["object"], "corpus_local_package_preview")
        self.assertEqual(report["schema_version"], "corpus_local_package_preview.v1")
        self.assertEqual(report["status"], "preview_report_only")
        self.assertEqual(report["package_id"], "mythic-edge-corpus-preview-bootstrap")
        self.assertEqual(report["summary"]["total_included_files"], 4)
        self.assertEqual(report["blocked_reason_codes"], [])
        self.assertEqual(report["non_claims"], list(module.NON_CLAIMS))
        self.assertNotIn(str(ROOT), rendered)
        self.assertEqual(
            [item["path"] for item in report["inventory"]],
            [
                "corpus/README.md",
                "corpus/manifest.v1.json",
                "corpus/session_ledger.v1.json",
                "corpus/sessions/bootstrap_public_session.json",
            ],
        )

    def test_cli_text_and_json_output_are_stdout_only(self) -> None:
        text_result = subprocess.run(
            [
                sys.executable,
                "tools/corpus_package_preview.py",
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
        self.assertIn("schema_version: corpus_local_package_preview.v1", text_result.stdout)
        self.assertIn("status: preview_report_only", text_result.stdout)
        self.assertIn("not_parser_truth", text_result.stdout)
        self.assertEqual(text_result.stderr, "")

        json_result = subprocess.run(
            [
                sys.executable,
                "tools/corpus_package_preview.py",
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
        self.assertEqual(parsed["status"], "preview_report_only")
        self.assertEqual(json_result.stderr, "")

    def test_main_returns_nonzero_for_blocked_state(self) -> None:
        module = load_module("corpus_package_preview_main_blocked_test")
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            code = module.main(
                [
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

    def test_missing_manifest_and_missing_session_ledger_fail_closed(self) -> None:
        module = load_module("corpus_package_preview_missing_test")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_package(root)
            (root / "corpus/manifest.v1.json").unlink()
            report = build_preview(module, root)
            self.assertEqual(report["status"], "blocked_missing_manifest")
            self.assertEqual(report["blocked_reason_codes"], ["manifest_missing"])

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_package(root)
            (root / "corpus/session_ledger.v1.json").unlink()
            report = build_preview(module, root)
            self.assertEqual(report["status"], "blocked_missing_session_ledger")
            self.assertEqual(report["blocked_reason_codes"], ["session_ledger_missing"])

    def test_malformed_manifest_and_session_ledger_fail_closed(self) -> None:
        module = load_module("corpus_package_preview_malformed_test")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_package(root)
            (root / "corpus/manifest.v1.json").write_text("{not json", encoding="utf-8")
            report = build_preview(module, root)
            self.assertEqual(report["status"], "blocked_invalid_metadata")
            self.assertEqual(report["blocked_reason_codes"], ["manifest_malformed"])

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_package(root)
            (root / "corpus/session_ledger.v1.json").write_text("{not json", encoding="utf-8")
            report = build_preview(module, root)
            self.assertEqual(report["status"], "blocked_invalid_metadata")
            self.assertEqual(report["blocked_reason_codes"], ["session_ledger_malformed"])

    def test_manifest_entry_missing_from_disk_and_undeclared_file_fail_closed(self) -> None:
        module = load_module("corpus_package_preview_inventory_test")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_package(root)
            (root / "corpus/sessions/bootstrap_public_session.json").unlink()
            report = build_preview(module, root)
            self.assertEqual(report["status"], "blocked_manifest_ledger_mismatch")
            self.assertEqual(report["blocked_reason_codes"], ["manifest_entry_missing_from_disk"])

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_package(root)
            (root / "corpus/extra.json").write_text("{}\n", encoding="utf-8")
            report = build_preview(module, root)
            self.assertEqual(report["status"], "blocked_manifest_ledger_mismatch")
            self.assertEqual(report["blocked_reason_codes"], ["package_file_missing_from_manifest"])

    def test_manifest_session_ledger_mismatch_fails_closed(self) -> None:
        module = load_module("corpus_package_preview_mismatch_test")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _manifest, ledger = write_package(root)
            ledger["entries"][0]["paths"] = ["corpus/README.md"]
            write_json(root / "corpus/session_ledger.v1.json", ledger)

            report = build_preview(module, root)

            self.assertEqual(report["status"], "blocked_manifest_ledger_mismatch")
            self.assertEqual(report["blocked_reason_codes"], ["manifest_path_missing_from_ledger"])

    def test_path_traversal_and_absolute_paths_fail_without_echo(self) -> None:
        module = load_module("corpus_package_preview_path_test")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest, _ledger = write_package(root)
            forbidden_absolute = str(root / "corpus/absolute.json")
            manifest["entries"][0]["path"] = forbidden_absolute
            write_json(root / "corpus/manifest.v1.json", manifest)

            report = build_preview(module, root)
            rendered = json.dumps(report, sort_keys=True)

            self.assertEqual(report["status"], "blocked_unsafe_path")
            self.assertEqual(report["blocked_reason_codes"], ["absolute_path"])
            self.assertNotIn(forbidden_absolute, rendered)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest, _ledger = write_package(root)
            manifest["entries"][0]["path"] = "corpus/../outside.json"
            write_json(root / "corpus/manifest.v1.json", manifest)

            report = build_preview(module, root)

            self.assertEqual(report["status"], "blocked_unsafe_path")
            self.assertEqual(report["blocked_reason_codes"], ["path_traversal_or_empty_part"])

    def test_generated_runtime_cache_paths_and_archives_fail_closed(self) -> None:
        module = load_module("corpus_package_preview_artifact_test")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest, _ledger = write_package(root)
            (root / "corpus/__pycache__").mkdir()
            (root / "corpus/__pycache__/cached.json").write_text("{}\n", encoding="utf-8")
            manifest["entries"].append(
                {
                    "path": "corpus/__pycache__/cached.json",
                    "role": "generated_cache",
                    "public_safe": True,
                    "session_id": None,
                }
            )
            write_json(root / "corpus/manifest.v1.json", manifest)

            report = build_preview(module, root)

            self.assertEqual(report["status"], "blocked_unsafe_path")
            self.assertEqual(report["blocked_reason_codes"], ["generated_runtime_or_cache_path"])

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest, _ledger = write_package(root)
            (root / "corpus/package.zip").write_text("archive placeholder\n", encoding="utf-8")
            manifest["entries"].append(
                {
                    "path": "corpus/package.zip",
                    "role": "package_archive",
                    "public_safe": True,
                    "session_id": None,
                }
            )
            write_json(root / "corpus/manifest.v1.json", manifest)

            report = build_preview(module, root)

            self.assertEqual(report["status"], "blocked_package_artifact")
            self.assertEqual(report["blocked_reason_codes"], ["package_artifact_suffix"])

    def test_forbidden_private_marker_blocks_without_echoing_content(self) -> None:
        module = load_module("corpus_package_preview_marker_test")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_package(root)
            forbidden = "unsafe " + "Player" + ".log marker"
            (root / "corpus/sessions/bootstrap_public_session.json").write_text(
                forbidden,
                encoding="utf-8",
            )

            report = build_preview(module, root)
            rendered = json.dumps(report, sort_keys=True)

            self.assertEqual(report["status"], "blocked_forbidden_content")
            self.assertEqual(report["blocked_reason_codes"], ["forbidden_content_marker"])
            self.assertNotIn(forbidden, rendered)

    def test_inventory_ordering_is_deterministic(self) -> None:
        module = load_module("corpus_package_preview_order_test")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest, _ledger = write_package(root)
            (root / "corpus/a_notes.md").write_text("A notes.\n", encoding="utf-8")
            manifest["entries"].append(
                {
                    "path": "corpus/a_notes.md",
                    "role": "package_notes",
                    "public_safe": True,
                    "session_id": None,
                }
            )
            manifest["entries"] = list(reversed(manifest["entries"]))
            write_json(root / "corpus/manifest.v1.json", manifest)

            first = build_preview(module, root)
            second = build_preview(module, root)

            self.assertEqual(first, second)
            self.assertEqual(
                [item["path"] for item in first["inventory"]],
                [
                    "corpus/README.md",
                    "corpus/a_notes.md",
                    "corpus/manifest.v1.json",
                    "corpus/session_ledger.v1.json",
                    "corpus/sessions/bootstrap_public_session.json",
                ],
            )

    def test_status_remains_report_only_not_preview_ready(self) -> None:
        module = load_module("corpus_package_preview_status_test")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_package(root)
            report = build_preview(module, root)

        self.assertEqual(report["status"], "preview_report_only")
        self.assertNotEqual(report["status"], "preview_ready")


if __name__ == "__main__":
    unittest.main()
