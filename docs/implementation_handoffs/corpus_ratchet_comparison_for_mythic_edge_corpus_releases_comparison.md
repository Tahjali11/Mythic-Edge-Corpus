# Codex C/D Handoff: Corpus Ratchet Comparison Report

## Role

Codex C: Module Implementer for Mythic-Edge-Corpus issue #18.

Codex D: Module Fixer for Codex E findings `CORPUS-RATCHET-E-001` and
`CORPUS-RATCHET-E-002`.

## Source Artifacts

- Repository: `Tahjali11/Mythic-Edge-Corpus`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge-Corpus`
- Tracker: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13
- Issue: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/18
- Previous issue: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/17
- Previous PR: https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/25
- Latest verified commit:
  `c74d559639a1d7e4ad325d0c96e4a1635a436dc7`
- Source contract:
  `docs/contracts/corpus_ratchet_comparison_for_mythic_edge_corpus_releases.md`

## Artifact Produced

- `tools/corpus_ratchet_comparison_report.py`
- `tests/test_corpus_ratchet_comparison_report.py`
- `docs/implementation_handoffs/corpus_ratchet_comparison_for_mythic_edge_corpus_releases_comparison.md`

## Comparison Summary

The implementation adds bounded Corpus-side ratchet comparison report support.
It builds and validates public-safe diagnostic report objects from supplied
release dry-run metadata and supplied comparison summaries. It does not run
ratchets, generate parser output, publish releases, create package artifacts,
send `repository_dispatch`, mutate baselines, open baseline PRs, or mutate
`Tahjali11/Mythic-Edge`.

Confirmed contract matches:

- Defines a report object:
  `corpus_ratchet_comparison_report.v1`.
- Validates reviewed release package identity, release tag/version pairing,
  source commit shape, release channel, planned release assets, SHA-256
  checksum metadata, public release URL shape, release metadata ref, checksum
  ref, and no-write guards.
- Supports report-only comparison categories including matched output, new
  passes, new failures, changed outputs, missing family, missing case, extra
  output, degraded evidence, unsupported categories, not comparable, review
  required, and invalid.
- Produces summary counts for total cases, matched outputs, new passes, new
  failures, changed outputs, missing families, missing cases, degraded
  evidence, unsupported rows, and review-required rows.
- Fails closed for missing release metadata, missing receiver contract, missing
  parser comparison surface, checksum mismatch, release/tag mismatch, stale
  source commit, malformed comparison rows, forbidden public content, baseline
  mutation requests, baseline PR requests, source mutation requests,
  ratchet-execution requests, and release or dispatch requests.
- Emits symbolic reason codes and avoids echoing unsafe raw values.
- Adds a validate-only CLI for already-built public-safe report JSON:
  `python3 tools/corpus_ratchet_comparison_report.py --validate-only --report <public_safe_report.json>`.
- Preserves explicit non-claims for parser truth, fixture promotion, baseline
  approval, corpus readiness, release readiness, deploy readiness, production
  readiness, analytics truth, AI truth, coaching truth, privacy assurance,
  security assurance, and full corpus parity.

Mismatches fixed:

- No ratchet comparison report builder, validator, CLI, or focused tests
  existed before this pass.
- The contract's Codex B-era status was `contract_only`; issue #18's current
  reconciliation authorized only this bounded report-only implementation.

## Validation Run

Passed:

- `python3 -m unittest discover -s tests -p 'test_corpus_ratchet_comparison_report.py'`
  - 18 tests passed after Codex D rebound regression coverage.
- `python3 -m unittest discover -s tests`
  - 79 tests passed.
- `python3 -m py_compile tools/corpus_ratchet_comparison_report.py tests/test_corpus_ratchet_comparison_report.py`
- `python3 -m ruff check tools tests`
- `git diff --check`
- focused changed-file public-safety scan for local absolute paths, raw log
  markers, private markers, credential-shaped strings, generated artifact
  references, and positive readiness or assurance claims
- changed-file whitespace and final-newline scan

## Codex D Fixer Addendum

Codex D addressed the fail-closed blockers from Codex E:

- Release dry-run `no_write_guards` now must match the exact expected guard
  key set with boolean `false` values. Missing, empty, extra, nested, or
  non-boolean guard shapes fail closed as invalid, and any true guard fails as
  a source-mutation request.
- Release metadata checksum entries now must exactly match the planned asset
  names and SHA-256 values. Missing, duplicate, extra, or mismatched checksum
  entries fail closed.
- Supplied expected checksum evidence now must exactly match the planned asset
  names and SHA-256 values. Missing, extra, or mismatched expected checksum
  entries fail closed.
- `asset_checksums_verified` now must be the literal boolean `true`. Truthy
  string or integer values fail closed as checksum mismatches and are not
  reflected as verified in blocked reports.
- Planned release asset names now must match the package-version-derived
  release identity exactly. Path-like names, wrong public-looking names, and
  duplicate/collapsed planned asset names fail closed instead of being accepted
  through matching checksum maps.
- Release dry-run status fields now fail closed when they indicate write or
  publish behavior, even if the `no_write_guards` object still contains false
  values.
- Release report, release metadata, and planned asset objects now use exact
  schema key sets so extra write flags or external asset URL fields cannot
  bypass the guard/checksum containers.
- Focused regression coverage was added for the guard-shape, checksum evidence,
  literal verification flag, release asset identity, dry-run write/publish
  flags, and extra release/asset metadata probes.

## Codex D Rebound Fixer Addendum

Codex E reported that `CORPUS-RATCHET-E-001` and
`CORPUS-RATCHET-E-002` still reproduced. The remaining gap was not only in the
first-order guard/checksum containers; release provenance containers could be
mutated while the top-level dry-run status still looked clean.

The rebound D pass now fails closed when:

- `package_preview_ref` is missing, malformed, stale, or mismatched between
  the top-level release report and nested release metadata;
- `pr_validation_ref` is missing, malformed, stale, or mismatched between the
  top-level release report and nested release metadata;
- `review_ref` is missing, malformed, not approved, unsafe, or mismatched
  between the top-level release report and nested release metadata;
- `manifest_ref` or `session_ledger_ref` is missing, malformed, path-unsafe,
  or mismatched between the top-level release report and nested release
  metadata;
- `included_files_summary` is missing, empty, count-mismatched, path-unsafe,
  or mismatched between the top-level release report and nested release
  metadata;
- `safety_checks` is missing, empty, duplicated, malformed, non-passing, or
  mismatched between the top-level release report and nested release metadata.

Focused regression coverage was added for the reproduced missing/mismatched
predecessor evidence, human-review evidence, path-ref evidence, safety-check
evidence, and included-file evidence cases.

Direct probes that previously returned `comparison_completed_with_deltas` now
return fail-closed statuses and symbolic reason codes:

- missing preview evidence -> `blocked_missing_release_metadata` /
  `missing_predecessor_preview_evidence`;
- missing PR-validation evidence -> `blocked_missing_release_metadata` /
  `missing_predecessor_pr_validation_evidence`;
- missing human review -> `blocked_missing_release_metadata` /
  `missing_human_review`;
- missing manifest/session ledger, failed safety checks, and empty included
  file summaries -> `blocked_missing_release_metadata` /
  `missing_release_metadata`.

No ratchet was run, no baseline was mutated, no baseline PR was created, no
package or release artifact was created, no release was published, no dispatch
was sent, and `Tahjali11/Mythic-Edge` was not mutated.

## Remaining Risks And Non-Claims

- No real ratchet was run.
- No parser output was generated.
- No receiving-side Mythic Edge ratchet implementation was created.
- No baseline was mutated.
- No baseline PR was opened or prepared.
- No package or release artifact was created.
- No release was published.
- No `repository_dispatch` was sent.
- No raw corpus, private logs, local app data, secrets, credentials, tokens,
  transport endpoint URLs, or generated local artifacts were read.
- This does not claim parser truth, fixture promotion, baseline approval,
  corpus readiness, release readiness, deploy readiness, production readiness,
  analytics truth, AI truth, coaching truth, privacy assurance, security
  assurance, or full corpus parity.

## Recommended Next Role

Recommended next role: Codex E review.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge-Corpus issue #18.

Repository:
Tahjali11/Mythic-Edge-Corpus

Repository URL:
https://github.com/Tahjali11/Mythic-Edge-Corpus

Tracker:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13

Issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/18

Previous issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/17

Previous PR:
https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/25

Latest verified commit:
c74d559639a1d7e4ad325d0c96e4a1635a436dc7

Source contract:
docs/contracts/corpus_ratchet_comparison_for_mythic_edge_corpus_releases.md

Implementation handoff:
docs/implementation_handoffs/corpus_ratchet_comparison_for_mythic_edge_corpus_releases_comparison.md

Goal:
Review the Codex D rebound fixer pass for `CORPUS-RATCHET-E-001` and
`CORPUS-RATCHET-E-002`. Lead with findings if any. Verify that the helper
builds and validates public-safe diagnostic report objects only, fails closed
for malformed no-write guard metadata, checksum evidence drift, non-literal
checksum verification flags, release asset identity drift, dry-run write or
publish flags, extra release/asset metadata fields, missing or mismatched
predecessor preview evidence, missing or mismatched PR-validation evidence,
missing or unapproved human-review evidence, unsafe or mismatched manifest and
session-ledger refs, failed safety checks, and malformed included-file
summaries, while preserving no-ratchet, no-baseline-mutation, no-baseline-PR,
no-dispatch, no-release-publishing, no-package-artifact,
no-Mythic-Edge-mutation, and no-truth/readiness/assurance boundaries.

Suggested validation:
- python3 -m unittest discover -s tests -p 'test_corpus_ratchet_comparison_report.py'
- python3 -m unittest discover -s tests
- python3 -m py_compile tools/corpus_ratchet_comparison_report.py tests/test_corpus_ratchet_comparison_report.py
- python3 -m ruff check tools tests
- git diff --check

Do not run real ratchets.
Do not mutate baselines.
Do not open baseline PRs.
Do not publish releases or create package artifacts.
Do not send repository_dispatch.
Do not mutate Tahjali11/Mythic-Edge.
Do not read private logs, raw corpus/private files, secrets, private paths, or generated local artifacts.
Do not claim parser truth, fixture promotion, baseline approval, corpus readiness, release readiness, deploy readiness, production readiness, security assurance, privacy assurance, analytics truth, AI truth, coaching truth, or full corpus parity.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge-Corpus"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge-Corpus"
  issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/18"
  tracker: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/17"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/25"
  latest_verified_commit: "c74d559639a1d7e4ad325d0c96e4a1635a436dc7"
  completed_thread: "D"
  next_thread: "E"
  verdict: "ratchet_comparison_report_fail_closed_rebound_blockers_fixed_ready_for_review"
  risk_tier: "High"
  source_artifact: "docs/contracts/corpus_ratchet_comparison_for_mythic_edge_corpus_releases.md"
  target_artifact: "docs/implementation_handoffs/corpus_ratchet_comparison_for_mythic_edge_corpus_releases_comparison.md"
  ratchet_execution_authorized: false
  baseline_pr_creation_authorized: false
  baseline_mutation_authorized: false
  release_publishing_authorized: false
  repository_dispatch_authorized: false
  package_artifact_creation_authorized: false
  mythic_edge_mutation_authorized: false
  raw_corpus_import_authorized: false
  private_log_read_authorized: false
  validation:
    - "python3 -m unittest discover -s tests -p 'test_corpus_ratchet_comparison_report.py' -> 18 passed"
    - "python3 -m unittest discover -s tests -> 79 passed"
    - "python3 -m py_compile tools/corpus_ratchet_comparison_report.py tests/test_corpus_ratchet_comparison_report.py"
    - "python3 -m ruff check tools tests"
    - "git diff --check"
    - "focused changed-file public-safety scan"
    - "changed-file whitespace and final-newline scan"
```
