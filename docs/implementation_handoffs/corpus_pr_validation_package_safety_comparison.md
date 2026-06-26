# Corpus PR Validation Package-Safety Implementation Handoff

## Role

Codex C: Module Implementer for Mythic-Edge-Corpus issue #15.

## Source Artifact

- `docs/contracts/corpus_pr_validation_package_safety.md`
- GitHub issue #15, which authorizes implementation after the local preview command from issue #14.

## Comparison Summary

The contract required deterministic report-only PR package-safety validation that depends on the local package preview command, fails closed on unsafe package states, avoids contributor branch mutation, avoids durable artifact writes, and keeps downstream publishing, dispatch, ratchet, and baseline PR workflows out of scope.

Current repo state already had the issue #14 local package preview command. This implementation adds a thin PR validation layer over that preview output instead of duplicating package parsing.

## Live State Verification

- `git fetch --prune origin` completed before validation.
- Local `main`, `origin/main`, and `HEAD` were verified at `d650781ca9dd05a0f263f5347994f466600ba5d3`.
- `main` and `origin/main` both contain PR #22 merge commit `d650781ca9dd05a0f263f5347994f466600ba5d3`.
- Tracker #13 is open.
- Issue #14 is closed.
- Issue #15 is open.
- PR #22 is merged to `main`.

## Changes Made

- Added `tools/corpus_pr_validate_package_safety.py`.
  - Builds `corpus_pr_validation_package_safety.v1` reports.
  - Loads the local preview builder in-process.
  - Returns `passed_report_only` only when preview status is `preview_report_only`.
  - Maps missing, blocked, failed, or malformed preview states to symbolic blocked statuses.
  - Validates PR refs and requested paths before preview execution.
  - Emits no-write guard flags and explicit non-claims.
  - Supports deterministic text and JSON stdout output.
- Added `tests/test_corpus_pr_validation_package_safety.py`.
  - Covers clean package proposals, missing preview command, preview failures, malformed preview output, unsafe refs/paths, forbidden markers, package artifacts, CLI output, nonzero blocked exits, and deterministic ordering.

## Protected Boundaries Preserved

- No contributor branch writeback, sanitization, deletion, push, issue, PR, label, comment, review, status check, or durable validation artifact write was added.
- No package archive, release asset, dispatch payload, ratchet report, or baseline PR artifact creation was added.
- No private logs, raw corpus evidence, external corpus content, source repo files, generated local artifacts, or secret material were introduced.
- No claims were made for parser truth, fixture promotion, corpus readiness, release readiness, deploy readiness, production readiness, ratchet success, baseline approval, analytics truth, AI truth, coaching truth, privacy assurance, security assurance, or full corpus parity.

## Validation Run

- `python3 -m pytest -q tests/test_corpus_pr_validation_package_safety.py` passed: 13 tests after Codex D rebound regression coverage.
- `python3 -m pytest -q tests/test_corpus_package_preview.py tests/test_corpus_pr_validation_package_safety.py` passed: 25 tests after Codex D rebound regression coverage.
- `python3 tools/corpus_pr_validate_package_safety.py --base-ref origin/main --head-ref HEAD --package-root corpus --manifest corpus/manifest.v1.json --session-ledger corpus/session_ledger.v1.json` passed with `passed_report_only`.
- `python3 tools/corpus_pr_validate_package_safety.py --base-ref origin/main --head-ref HEAD --package-root corpus --manifest corpus/manifest.v1.json --session-ledger corpus/session_ledger.v1.json --format json` passed with `passed_report_only`.
- `python3 -m pytest -q` passed: 25 tests after Codex D rebound regression coverage.
- `python3 -m ruff check tools tests` passed.
- `python3 -m py_compile tools/corpus_pr_validate_package_safety.py tests/test_corpus_pr_validation_package_safety.py` passed.
- `python3 -m json.tool corpus/manifest.v1.json >/dev/null` passed.
- `python3 -m json.tool corpus/session_ledger.v1.json >/dev/null` passed.
- `git diff --check` passed for tracked diff state; files were intentionally not staged.
- Focused changed-file scan covered the new untracked files and passed for local paths, raw log literals, credential-shaped values, SQLite artifacts, whitespace, and final newlines.

## Codex D Fixer Addendum

Codex D addressed the rebound form of `CORPUS-PRVAL-E-001`: preview-output
values must not merely be masked after the fact. A malformed or custom preview
builder containing local-path or credential-shaped values must fail closed as
`blocked_preview_invalid_output` before the PR validation report can pass.

Fix applied:

- preview package metadata values are checked for public-safe content before
  they are copied into `package_preview_ref`;
- preview inventory paths and optional session identifiers are checked before
  they can influence changed-file and inventory summaries;
- preview blocked reason codes are checked before they can be reported;
- preview summary counters must be non-negative integers, preventing unsafe
  value echoes and malformed-value crashes;
- invalid preview status values are sanitized in the blocked report;
- focused regressions prove unsafe preview package metadata, inventory paths,
  session IDs, summary counters, reason codes, and invalid status values fail
  closed without echoing the unsafe values.

The fix does not create package artifacts, publish releases, send
`repository_dispatch`, run ratchets, create baseline PRs, mutate
`Tahjali11/Mythic-Edge`, auto-sanitize contributor branches, or claim parser
truth, fixture promotion, corpus readiness, privacy assurance, or security
assurance.

## Remaining Risks

- The validator intentionally treats the existing checkout as the validation input. It does not fetch, checkout, or diff PR branches in V1.
- CI/GitHub Actions wiring remains out of scope.
- Package-safety validation is hygiene evidence only. It is not parser truth, corpus readiness, release readiness, privacy assurance, or security assurance.

## Recommended Next Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge-Corpus issue #15.

Repository:
Tahjali11/Mythic-Edge-Corpus

Repository URL:
https://github.com/Tahjali11/Mythic-Edge-Corpus

Issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/15

Tracker:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13

Source contract:
docs/contracts/corpus_pr_validation_package_safety.md

Implementation handoff:
docs/implementation_handoffs/corpus_pr_validation_package_safety_comparison.md

Goal:
Review the PR validation package-safety implementation against the contract. Lead with findings, if any. Verify that the implementation depends on the local preview command, fails closed on missing/failed/blocked/malformed preview states, emits only symbolic unsafe reasons, preserves no-write/no-auto-sanitization behavior, and keeps publishing, dispatch, ratchets, baseline PRs, parser truth, fixture promotion, readiness, privacy assurance, and security assurance out of scope.

Review files:
- tools/corpus_pr_validate_package_safety.py
- tests/test_corpus_pr_validation_package_safety.py
- docs/implementation_handoffs/corpus_pr_validation_package_safety_comparison.md

Suggested validation:
- python3 -m pytest -q tests/test_corpus_pr_validation_package_safety.py
- python3 -m pytest -q tests/test_corpus_package_preview.py tests/test_corpus_pr_validation_package_safety.py
- python3 tools/corpus_pr_validate_package_safety.py --base-ref origin/main --head-ref HEAD --package-root corpus --manifest corpus/manifest.v1.json --session-ledger corpus/session_ledger.v1.json
- python3 -m ruff check tools tests
- git diff --check

Do not implement code unless routing to Codex D for concrete findings.
Do not publish packages, create releases, send repository_dispatch, run ratchets, open baseline PRs, import raw corpus data, read private logs, or mutate Tahjali11/Mythic-Edge.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge-Corpus"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge-Corpus"
  issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/15"
  tracker: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/14"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/22"
  previous_merge_commit: "d650781ca9dd05a0f263f5347994f466600ba5d3"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/corpus_pr_validation_package_safety.md"
  target_artifact: "docs/implementation_handoffs/corpus_pr_validation_package_safety_comparison.md"
  verdict: "corpus_pr_validation_package_safety_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  package_artifact_creation_authorized: false
  release_publishing_authorized: false
  repository_dispatch_authorized: false
  ratchet_execution_authorized: false
  baseline_pr_creation_authorized: false
  source_repo_mutation_authorized: false
```
