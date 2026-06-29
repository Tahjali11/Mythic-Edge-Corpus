# Corpus Public-Safe End-To-End Dry Run Implementation Handoff

## Role

Codex C: Module Implementer / dry-run validation implementer for
Mythic-Edge-Corpus issue #20, with a Codex D fixer addendum for
CORPUS-DRYRUN-E-001.

## Source Artifact

- Repository: `Tahjali11/Mythic-Edge-Corpus`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge-Corpus`
- Tracker: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13
- Issue: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/20
- Previous issue: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/19
- Previous PR: https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/27
- Previous merge commit:
  `e2b2325ccccf6cd470d38beb7e42e0080b927546`
- Source contracts:
  - `docs/contracts/corpus_local_package_preview_command.md`
  - `docs/contracts/corpus_pr_validation_package_safety.md`
  - `docs/contracts/corpus_release_publishing_reviewed_packages.md`
  - `docs/contracts/corpus_repository_dispatch_into_mythic_edge.md`
  - `docs/contracts/corpus_ratchet_comparison_for_mythic_edge_corpus_releases.md`
  - `docs/contracts/corpus_baseline_pr_proposal_after_ratchet_comparison.md`
- Report artifact:
  `docs/contract_test_reports/corpus_public_safe_end_to_end_dry_run.md`

## Comparison Summary

Issue #20 asks for a public-safe no-external-action dry run of the implemented
Corpus automation loop. The implementation composes the six reviewed local
surfaces in memory:

1. local package preview;
2. PR package-safety validation;
3. release package dry run;
4. repository dispatch no-send payload validation;
5. ratchet comparison report construction from synthetic/public-safe
   comparison inputs;
6. no-write baseline proposal preview.

Implemented:

- `tools/corpus_public_safe_dry_run.py` as a report-only orchestration helper;
- focused tests in `tests/test_corpus_public_safe_dry_run.py`;
- a release dry-run integrity fix that keeps release metadata
  non-self-referential while exposing complete planned asset checksum evidence
  through a separate top-level surface required by dispatch and ratchet
  validators;
- release regression assertions for the final metadata JSON checksum and
  complete planned asset checksums;
- `docs/contract_test_reports/corpus_public_safe_end_to_end_dry_run.md`;
- this implementation handoff.

Not implemented:

- package archive writes;
- release metadata file writes;
- checksum file writes;
- GitHub release creation;
- release asset uploads;
- repository dispatch sends;
- ratchet execution;
- parser output generation;
- baseline mutation;
- baseline PR creation;
- Mythic Edge checkout inspection or mutation;
- raw corpus import;
- private log reads;
- readiness, truth, assurance, or full-parity claims.

## Codex D Fixer Addendum

CORPUS-DRYRUN-E-001 exposed a dry-run integrity representation mismatch:

- `tools/corpus_release_package.py` produced three planned assets in memory:
  package archive, release metadata, and checksum manifest.
- The planned release metadata asset checksum was computed before the metadata
  object's checksum surface was finalized.
- That made the planned `release_metadata` asset checksum stale relative to
  the final canonical JSON bytes returned in `report["release_metadata"]`.

Fix:

- `tools/corpus_release_package.py` now leaves
  `release_metadata.asset_checksums` intentionally non-self-referential: it
  records the package archive checksum only.
- The returned release report now exposes complete planned asset checksum
  evidence through top-level `planned_asset_checksums`.
- The planned `release_metadata` asset checksum now matches the final canonical
  JSON bytes of `report["release_metadata"]`.
- Dispatch and ratchet validators now validate the complete planned checksum
  evidence from `planned_asset_checksums`, while release metadata validates
  only the non-self-referential archive checksum.
- Test helpers no longer patch release metadata into the old self-referential
  shape.

This remains in-memory dry-run metadata only. It does not write release assets,
publish releases, send dispatch, run ratchets, or create baseline PRs.

## Files Changed

- `tools/corpus_release_package.py`
- `tools/corpus_repository_dispatch.py`
- `tools/corpus_ratchet_comparison_report.py`
- `tools/corpus_public_safe_dry_run.py`
- `tests/test_corpus_release_package.py`
- `tests/test_corpus_repository_dispatch.py`
- `tests/test_corpus_ratchet_comparison_report.py`
- `tests/test_corpus_baseline_pr_proposal.py`
- `tests/test_corpus_public_safe_dry_run.py`
- `docs/contract_test_reports/corpus_public_safe_end_to_end_dry_run.md`
- `docs/implementation_handoffs/corpus_public_safe_end_to_end_dry_run_comparison.md`

## Validation Run

Passed:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/test_corpus_release_package.py tests/test_corpus_repository_dispatch.py tests/test_corpus_ratchet_comparison_report.py tests/test_corpus_public_safe_dry_run.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/test_corpus_baseline_pr_proposal.py
python3 tools/corpus_public_safe_dry_run.py --source-commit e2b2325ccccf6cd470d38beb7e42e0080b927546 --mythic-edge-commit 0000000000000000000000000000000000000000 --format json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
python3 -m json.tool corpus/manifest.v1.json >/dev/null
python3 -m json.tool corpus/session_ledger.v1.json >/dev/null
python3 -m json.tool corpus/sessions/bootstrap_public_session.json >/dev/null
python3 -m py_compile tools/*.py tests/test_corpus_release_package.py tests/test_corpus_repository_dispatch.py tests/test_corpus_ratchet_comparison_report.py tests/test_corpus_public_safe_dry_run.py
python3 -m ruff check tools tests
git diff --check
focused public-artifact marker scan
```

Observed results:

- Focused CORPUS-DRYRUN-E-001 regression bundle: 56 passed.
- Focused baseline proposal compatibility tests: 16 passed.
- Dry-run CLI status: `public_safe_dry_run_complete`.
- Full Corpus test suite: 98 passed.
- Corpus manifest, session ledger, and bootstrap public session JSON validation
  passed.
- `tools/*.py` compile check passed.
- `python3 -m ruff check tools tests` passed.
- `git diff --check` and the focused public-artifact marker scan passed.

## Remaining Risks And Non-Claims

- The Mythic Edge comparison commit in the dry-run command is synthetic by
  design. Issue #20 does not authorize Mythic Edge source inspection or
  ratchet execution.
- No package, release, dispatch, ratchet, or baseline PR artifact was created.
- The baseline proposal stage completed as `proposal_preview_no_deltas`, which
  intentionally emits no draft PR title/body/branch.
- This does not claim parser truth, fixture promotion, baseline approval,
  corpus readiness, release readiness, deploy readiness, production readiness,
  ratchet success, analytics truth, AI truth, coaching truth, privacy
  assurance, security assurance, or full corpus parity.

## Recommended Next Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge-Corpus issue #20.

Repository:
Tahjali11/Mythic-Edge-Corpus

Repository URL:
https://github.com/Tahjali11/Mythic-Edge-Corpus

Tracker:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13

Issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/20

Previous issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/19

Previous PR:
https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/27

Previous merge commit:
e2b2325ccccf6cd470d38beb7e42e0080b927546

Implementation handoff:
docs/implementation_handoffs/corpus_public_safe_end_to_end_dry_run_comparison.md

Contract-test report:
docs/contract_test_reports/corpus_public_safe_end_to_end_dry_run.md

Review scope:
- tools/corpus_release_package.py
- tools/corpus_repository_dispatch.py
- tools/corpus_ratchet_comparison_report.py
- tools/corpus_public_safe_dry_run.py
- tests/test_corpus_release_package.py
- tests/test_corpus_repository_dispatch.py
- tests/test_corpus_ratchet_comparison_report.py
- tests/test_corpus_baseline_pr_proposal.py
- tests/test_corpus_public_safe_dry_run.py
- docs/contract_test_reports/corpus_public_safe_end_to_end_dry_run.md
- docs/implementation_handoffs/corpus_public_safe_end_to_end_dry_run_comparison.md

Goal:
Review the public-safe no-external-action dry-run implementation against
issue #20 and the six Corpus contracts. Lead with findings ordered by
severity. Verify that package preview, PR validation, release dry-run,
dispatch no-send validation, ratchet report construction, and baseline
proposal preview compose without writing package/release/checksum artifacts,
sending repository_dispatch, running ratchets, mutating baselines, creating
baseline PRs, inspecting/mutating Mythic Edge, reading private logs, or making
truth/readiness/assurance claims.

Suggested validation:
- PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/test_corpus_release_package.py tests/test_corpus_repository_dispatch.py tests/test_corpus_ratchet_comparison_report.py tests/test_corpus_public_safe_dry_run.py
- PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/test_corpus_baseline_pr_proposal.py
- python3 tools/corpus_public_safe_dry_run.py --source-commit e2b2325ccccf6cd470d38beb7e42e0080b927546 --mythic-edge-commit 0000000000000000000000000000000000000000 --format json
- PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
- python3 -m py_compile tools/*.py tests/test_corpus_release_package.py tests/test_corpus_repository_dispatch.py tests/test_corpus_ratchet_comparison_report.py tests/test_corpus_public_safe_dry_run.py
- python3 -m ruff check tools tests
- git diff --check
- focused public-artifact marker scan

Protected boundaries:
- Do not create package artifacts, release artifacts, GitHub releases, release
  assets, repository_dispatch events, ratchet outputs, baseline PRs, Mythic
  Edge branches, Mythic Edge commits, Mythic Edge PRs, comments, reviews,
  labels, or status checks.
- Do not mutate Tahjali11/Mythic-Edge.
- Do not read raw corpus/private files, private logs, local app data, secrets,
  private paths, generated local artifacts, or private reports.
- Do not claim parser truth, fixture promotion, baseline approval, corpus
  readiness, release readiness, deploy readiness, production readiness,
  ratchet success, analytics truth, AI truth, coaching truth, privacy
  assurance, security assurance, or full corpus parity.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge-Corpus"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge-Corpus"
  issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/20"
  tracker: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/19"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/27"
  previous_merge_commit: "e2b2325ccccf6cd470d38beb7e42e0080b927546"
  completed_thread: "D"
  next_thread: "E"
  finding_id: "CORPUS-DRYRUN-E-001"
  verdict: "public_safe_end_to_end_dry_run_checksum_integrity_fix_ready_for_review"
  risk_tier: "High"
  source_artifact: "docs/contract_test_reports/corpus_public_safe_end_to_end_dry_run.md"
  target_artifacts:
    - "docs/contract_test_reports/corpus_public_safe_end_to_end_dry_run.md"
    - "docs/implementation_handoffs/corpus_public_safe_end_to_end_dry_run_comparison.md"
  package_artifact_creation_authorized: false
  release_publishing_authorized: false
  repository_dispatch_authorized: false
  ratchet_execution_against_mythic_edge_authorized: false
  baseline_pr_creation_authorized: false
  baseline_mutation_authorized: false
  mythic_edge_mutation_authorized: false
  raw_corpus_import_authorized: false
  private_log_read_authorized: false
  validation:
    - "python3 -m unittest tests/test_corpus_public_safe_dry_run.py"
    - "python3 -m unittest tests/test_corpus_public_safe_dry_run.py tests/test_corpus_release_package.py tests/test_corpus_repository_dispatch.py tests/test_corpus_ratchet_comparison_report.py tests/test_corpus_baseline_pr_proposal.py"
    - "python3 tools/corpus_public_safe_dry_run.py --source-commit e2b2325ccccf6cd470d38beb7e42e0080b927546 --mythic-edge-commit 0000000000000000000000000000000000000000 --format json"
    - "python3 -m unittest discover -s tests"
    - "python3 -m json.tool corpus/manifest.v1.json >/dev/null"
    - "python3 -m json.tool corpus/session_ledger.v1.json >/dev/null"
    - "python3 -m json.tool corpus/sessions/bootstrap_public_session.json >/dev/null"
    - "python3 -m py_compile tools/*.py"
    - "git diff --check"
    - "focused public-artifact marker scan"
```
