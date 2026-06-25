# Codex C Implementation Handoff: Corpus Local Package Preview Command

## Role

Codex C: Module Implementer for Mythic-Edge-Corpus issue #14.

## Source Artifact

- Repository: `Tahjali11/Mythic-Edge-Corpus`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge-Corpus`
- Tracker: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13
- Issue: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/14
- Source contract: `docs/contracts/corpus_local_package_preview_command.md`
- Base branch: `main`
- Latest verified commit:
  `9d37e0ee5332c3cf44d02c86d455248b5cc9fc79`

## Comparison Summary

The contract authorizes a local report-only preview command for committed,
public-safe corpus metadata. It does not authorize package publication,
release artifacts, repository dispatch, ratchets, baseline PRs, raw/private
corpus import, mutation of `Tahjali11/Mythic-Edge`, parser truth, fixture
promotion, readiness claims, analytics truth, AI truth, coaching truth,
privacy assurance, security assurance, or full corpus parity.

Implemented:

- `tools/corpus_package_preview.py` local CLI.
- `--package-root`, `--manifest`, `--session-ledger`, and `--format text|json`
  command arguments.
- stdout-only text and JSON report output.
- deterministic inventory ordering.
- manifest/session-ledger relationship checks.
- fail-closed statuses for missing metadata, malformed metadata, path issues,
  manifest/ledger mismatches, forbidden content markers, raw/local artifact
  suffixes, generated/cache paths, and package archive suffixes.
- explicit report-only non-claims in both output formats.
- tiny public-safe bootstrap metadata under `corpus/`.
- focused tests for happy-path CLI output and contract-required blocked states.

Not implemented:

- package archives or release assets;
- repository dispatch;
- ratchet reports;
- baseline PR artifacts;
- report file writes;
- raw/private corpus import;
- source repository mutation;
- parser behavior changes;
- fixture promotion or readiness claims.

## Files Changed

- `tools/corpus_package_preview.py`
- `tests/test_corpus_package_preview.py`
- `corpus/README.md`
- `corpus/manifest.v1.json`
- `corpus/session_ledger.v1.json`
- `corpus/sessions/bootstrap_public_session.json`
- `docs/implementation_handoffs/corpus_local_package_preview_command_comparison.md`

## Bootstrap Metadata

The new `corpus/` directory is intentionally tiny. It contains only public-safe
metadata needed for the command to validate a committed package shape:

- package notes;
- the package manifest;
- the session ledger;
- one synthetic public-safe session metadata JSON file.

The bootstrap metadata is not raw evidence and does not claim parser truth,
fixture promotion, corpus readiness, release readiness, production readiness,
analytics truth, AI truth, coaching truth, privacy assurance, security
assurance, or full corpus parity.

## Validation Run

Passed:

```bash
python3 -m pytest -q tests/test_corpus_package_preview.py
python3 -m pytest -q
python3 tools/corpus_package_preview.py --package-root corpus --manifest corpus/manifest.v1.json --session-ledger corpus/session_ledger.v1.json --format text
python3 tools/corpus_package_preview.py --package-root corpus --manifest corpus/manifest.v1.json --session-ledger corpus/session_ledger.v1.json --format json | python3 -m json.tool >/dev/null
for f in corpus/manifest.v1.json corpus/session_ledger.v1.json corpus/sessions/bootstrap_public_session.json; do python3 -m json.tool "$f" >/dev/null; done
python3 -m ruff check tools tests
python3 -m py_compile tools/corpus_package_preview.py tests/test_corpus_package_preview.py
git diff --check
```

Results:

- Focused tests: 12 passed.
- Repo pytest suite: 12 passed.
- CLI text mode returned status `preview_report_only`.
- CLI text mode now includes
  `schema_version: corpus_local_package_preview.v1`.
- CLI JSON mode produced valid JSON.
- Bootstrap JSON fixtures validated.
- Ruff passed for `tools` and `tests`.
- Py-compile passed for the new command and tests.
- `git diff --check`: passed.
- Focused public-artifact marker scan over changed files: passed.
- Changed-file whitespace/final-newline scan: passed.
- Generated Python cache directories were removed after validation.

## Codex D Fixer Addendum

Codex D addressed `CORPUS-PREVIEW-E-001`: text output omitted the preview
report schema version required by the output-shape contract.

Fix applied:

- `format_text()` now emits
  `schema_version: corpus_local_package_preview.v1`;
- the CLI text-output test now asserts the schema-version line is present.

No package artifact was created. No release was published. No
`repository_dispatch` event was sent. No ratchet was run. No baseline PR was
created. No `Tahjali11/Mythic-Edge` mutation, parser-truth claim, fixture
promotion, corpus-readiness claim, release-readiness claim, privacy assurance,
or security assurance was performed or authorized.

## Remaining Risks And Non-Claims

- The preview command validates local committed metadata only.
- It does not publish packages or create release artifacts.
- It does not send repository dispatch.
- It does not run ratchets.
- It does not open baseline PRs.
- It does not mutate `Tahjali11/Mythic-Edge`.
- It does not import raw/private corpus files.
- It does not claim parser truth, fixture promotion, corpus readiness, release
  readiness, deploy readiness, production readiness, analytics truth, AI truth,
  coaching truth, privacy assurance, security assurance, or full corpus parity.

## Recommended Next Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge-Corpus issue #14.

Repository:
Tahjali11/Mythic-Edge-Corpus

Repository URL:
https://github.com/Tahjali11/Mythic-Edge-Corpus

Operating repo/worktree:
Use the checked-out Mythic-Edge-Corpus repo.

Tracker:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13

Issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/14

Source contract:
docs/contracts/corpus_local_package_preview_command.md

Implementation handoff:
docs/implementation_handoffs/corpus_local_package_preview_command_comparison.md

Review scope:
- tools/corpus_package_preview.py
- tests/test_corpus_package_preview.py
- corpus/README.md
- corpus/manifest.v1.json
- corpus/session_ledger.v1.json
- corpus/sessions/bootstrap_public_session.json
- docs/implementation_handoffs/corpus_local_package_preview_command_comparison.md

Goal:
Review the local report-only corpus package preview command against the
contract. Lead with findings ordered by severity. Verify that the command is
stdout-only, deterministic, public-safe, fail-closed, limited to committed
repo-relative metadata, and does not publish packages, create release
artifacts, dispatch events, run ratchets, open baseline PRs, read raw/private
corpus inputs, mutate Tahjali11/Mythic-Edge, or claim parser truth, fixture
promotion, readiness, analytics truth, AI truth, coaching truth, privacy
assurance, security assurance, or full corpus parity.

Validation:
- python3 -m pytest -q tests/test_corpus_package_preview.py
- python3 tools/corpus_package_preview.py --package-root corpus --manifest corpus/manifest.v1.json --session-ledger corpus/session_ledger.v1.json --format text
- python3 tools/corpus_package_preview.py --package-root corpus --manifest corpus/manifest.v1.json --session-ledger corpus/session_ledger.v1.json --format json | python3 -m json.tool >/dev/null
- for f in corpus/manifest.v1.json corpus/session_ledger.v1.json corpus/sessions/bootstrap_public_session.json; do python3 -m json.tool "$f" >/dev/null; done
- python3 -m ruff check tools tests
- git diff --check
- focused public-artifact marker scan over changed files

Expected output:
- findings first, if any
- review verdict
- validation evidence
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge-Corpus"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge-Corpus"
  tracker: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13"
  issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/14"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/corpus_local_package_preview_command.md"
  target_artifact: "docs/implementation_handoffs/corpus_local_package_preview_command_comparison.md"
  verdict: "corpus_local_package_preview_command_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  latest_verified_commit: "9d37e0ee5332c3cf44d02c86d455248b5cc9fc79"
  package_preview_command_implemented: true
  package_artifact_creation_authorized: false
  release_publishing_authorized: false
  repository_dispatch_authorized: false
  ratchet_execution_authorized: false
  baseline_pr_creation_authorized: false
  raw_corpus_import_authorized: false
  private_log_read_authorized: false
  mythic_edge_mutation_authorized: false
  parser_truth_claimed: false
  corpus_readiness_claimed: false
  release_readiness_claimed: false
  production_readiness_claimed: false
  privacy_assurance_claimed: false
  security_assurance_claimed: false
```
