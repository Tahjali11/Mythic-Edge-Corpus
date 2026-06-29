# Codex C Implementation Handoff: Corpus Repository Dispatch Payload Builder

## Role

Codex C: Implementer for Mythic-Edge-Corpus issue #17.

## Source Artifacts

- Tracker: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13
- Issue: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/17
- Previous issue: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/16
- Previous PR: https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/24
- Previous merge commit:
  `df882af26e090ca0b037877ebb16052f047b0e94`
- Source contract:
  `docs/contracts/corpus_repository_dispatch_into_mythic_edge.md`

## Artifact Produced

- `tools/corpus_repository_dispatch.py`
- `tests/test_corpus_repository_dispatch.py`
- `docs/implementation_handoffs/corpus_repository_dispatch_into_mythic_edge_comparison.md`

## Comparison Summary

The implementation adds a Corpus-side no-send repository-dispatch payload
builder and validator. It consumes the existing reviewed release dry-run report
from issue #16, builds only a bounded dry-run payload, and refuses unsafe or
out-of-scope states with symbolic reason codes.

Confirmed contract matches:

- Uses only the dry-run event:
  `mythic_edge_corpus.reviewed_package_published.dry_run.v1`.
- Keeps the non-dry-run event unsupported until separate send authorization
  exists.
- Requires a valid issue #16 release dry-run report with passed preview,
  PR-validation, review, no-write guard, asset, tag, version, source-commit,
  channel, and checksum evidence.
- Builds a small allowlisted payload with public GitHub release URLs, release
  asset names, SHA-256 checksums, predecessor refs, human review ref, contract
  refs, and non-claims.
- Validates payload schema, exact event name, source repository, target
  repository, package ID, release tag/version pair, release source commit,
  release URLs, asset checksums, and non-claims.
- Refuses send attempts, token-gated paths, ratchet requests, baseline PR
  requests, source mutation requests, and release/asset creation requests.
- Keeps all outputs no-send and report-only with `repository_dispatch_sent:
  false`.
- Uses symbolic failure output and avoids echoing forbidden payload values.

Mismatches fixed:

- No dispatch payload builder or focused tests existed before this pass.
- The initial forbidden-content scanner was too broad for safe non-claim labels
  and GitHub URLs. It was narrowed to actual local path, private marker, and
  credential-shaped values while schema allowlists continue to guard keys.
- Payload checksum validation now confirms that checksum entries match the
  three payload asset-name fields.

Codex D fixer addendum for `CORPUS-DISPATCH-E-001` and
`CORPUS-DISPATCH-E-002`:

- Nested release asset records now require the exact reviewed dry-run asset
  shape and reject extra keys before a dispatch payload can be produced.
- Nested payload checksum records now require the exact checksum shape and
  reject extra keys during direct payload validation.
- Raw/private marker detection normalizes underscores and hyphens in string
  values while preserving explicit `no_...` / `not_...` non-claim values.
- Focused regression coverage proves nested forbidden/unexpected keys fail
  closed without emitting a payload and without sending dispatch.

Codex D rebound addendum for still-reproducing `CORPUS-DISPATCH-E-001` and
`CORPUS-DISPATCH-E-002`:

- Top-level release reports now require the exact reviewed dry-run report shape
  before payload construction.
- Release metadata, no-write guards, safety check entries, and included-file
  summaries now require exact public-safe container shapes.
- Unexpected keys with raw/private/truth/action wording return
  `payload_contains_forbidden_content`; ordinary unexpected keys return
  `payload_schema_invalid`.
- Focused regression coverage proves extra top-level, release-metadata, and
  no-write guard keys fail closed without emitting a payload and without
  sending dispatch.

Codex D second rebound addendum for remaining `CORPUS-DISPATCH-E-001` and
`CORPUS-DISPATCH-E-002` fail-closed blockers:

- Direct payload validation now classifies forbidden extra keys with
  raw/private/truth/action wording as `payload_contains_forbidden_content`
  instead of a generic schema mismatch.
- Release report refs, predecessor refs, review refs, and release metadata
  checksum records now require exact public-safe nested shapes before payload
  construction.
- Release metadata copied from the release dry-run report must stay consistent
  with the outer report identity fields used to build the dispatch payload.
- Focused regression coverage proves these nested and direct-validation
  blocker probes fail closed without emitting a payload and without sending
  dispatch.

Codex D third rebound addendum for remaining `CORPUS-DISPATCH-E-001` and
`CORPUS-DISPATCH-E-002` fail-closed blockers:

- Included-file summaries now require repo-relative `corpus/` paths with no
  empty, current-directory, or parent-directory path segments.
- Planned release assets are validated item-by-item before role grouping, so
  malformed, duplicate, ignored, or forbidden extra asset records cannot be
  silently discarded before payload construction.
- Release metadata checksum entries must be unique and may reference only
  planned public-safe release assets.
- Focused regression coverage proves package-root escapes, ignored planned
  asset records, duplicate asset roles, unexpected asset roles, and release
  metadata checksum drift fail closed without emitting a payload and without
  sending dispatch.

Codex D fourth rebound addendum for remaining `CORPUS-DISPATCH-E-001`,
`CORPUS-DISPATCH-E-002`, and `CORPUS-DISPATCH-E-003` blockers:

- `--release-report` path strings are preflighted before `exists()` or
  `read_text()`, so raw/private/local/secret-shaped input paths fail closed
  with symbolic output and without echoing the unsafe path.
- No-write guards now require the exact expected no-write guard key set; empty,
  missing, extra, nested, or non-bool guard shapes fail closed with no payload.
- Release metadata checksum entries must exactly match planned release asset
  names and SHA-256 values; missing, extra, duplicate, or mismatched checksum
  entries fail closed with no payload.
- Focused regression coverage proves each remaining blocker fails closed
  without sending dispatch, mutating Mythic Edge, or emitting a payload.

## Files Changed

- Added/updated `tools/corpus_repository_dispatch.py`
- Added/updated `tests/test_corpus_repository_dispatch.py`
- Added/updated
  `docs/implementation_handoffs/corpus_repository_dispatch_into_mythic_edge_comparison.md`

## Validation Run

Passed:

- `python3 -m unittest discover -s tests -p 'test_corpus_repository_dispatch.py'`
  - 22 tests passed after Codex D fourth rebound coverage.
- `python3 -m unittest discover -s tests -p 'test_corpus_package_preview.py'`
  - 12 tests passed.
- `python3 -m unittest discover -s tests -p 'test_corpus_pr_validation_package_safety.py'`
  - 14 tests passed.
- `python3 -m unittest discover -s tests -p 'test_corpus_release_package.py'`
  - 13 tests passed.
- `python3 -m unittest discover -s tests`
  - 61 tests passed.
- direct probes for unsafe `--release-report` path preflight, exact
  `no_write_guards`, and exact release metadata checksum matching
  - passed.
- `python3 -m py_compile tools/corpus_repository_dispatch.py tests/test_corpus_repository_dispatch.py`
  - passed.
- `python3 -m ruff check tools tests`
  - passed.
- `git diff --check`
  - passed.
- changed-file whitespace/final-newline scan
  - passed.
- focused public-artifact marker scan for local paths, private markers,
  credential-shaped strings, raw package/log references, dispatch send claims,
  readiness/assurance claims, and source-repo mutation claims
  - passed.

## Remaining Risks And Non-Claims

- No `repository_dispatch` was sent.
- No GitHub token, secret, workflow, release, release asset, or package artifact
  was created or modified.
- No `Tahjali11/Mythic-Edge` repository files were inspected or mutated.
- This does not implement the Mythic Edge receiving-side workflow.
- This does not run ratchets, open baseline PRs, mutate baselines, publish
  releases, or promote fixtures.
- This does not claim parser truth, fixture promotion, corpus readiness,
  release readiness, deploy readiness, production readiness, analytics truth,
  AI truth, coaching truth, privacy assurance, security assurance, or full
  corpus parity.

## Recommended Next Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge-Corpus issue #17.

Repository:
Tahjali11/Mythic-Edge-Corpus

Repository URL:
https://github.com/Tahjali11/Mythic-Edge-Corpus

Operating repo/worktree:
Mythic-Edge-Corpus issue #17 implementation branch/worktree.

Tracker:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13

Issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/17

Previous issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/16

Previous PR:
https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/24

Previous merge commit:
df882af26e090ca0b037877ebb16052f047b0e94

Source contract:
docs/contracts/corpus_repository_dispatch_into_mythic_edge.md

Implementation handoff:
docs/implementation_handoffs/corpus_repository_dispatch_into_mythic_edge_comparison.md

Review goal:
Review the Corpus-side repository_dispatch payload builder and no-send
validation support against the reviewed contract. Lead with findings ordered by
severity. Confirm whether the implementation stays dry-run, public-safe,
notification-only, non-authoritative, and fail-closed.

Focus files:
- tools/corpus_repository_dispatch.py
- tests/test_corpus_repository_dispatch.py
- docs/implementation_handoffs/corpus_repository_dispatch_into_mythic_edge_comparison.md

Protected boundaries:
- Do not mutate Tahjali11/Mythic-Edge.
- Do not send repository_dispatch.
- Do not create or modify GitHub secrets/tokens.
- Do not publish corpus packages.
- Do not create release/package artifacts.
- Do not run ratchets.
- Do not open baseline PRs.
- Do not import raw corpus/private files.
- Do not read private logs, local app data, secrets, credentials, webhook URLs,
  or runtime artifacts.
- Do not claim parser truth, fixture promotion, corpus readiness, release
  readiness, deploy readiness, production readiness, analytics truth, AI truth,
  coaching truth, privacy assurance, security assurance, or full corpus parity.

Suggested validation:
- python3 -m unittest discover -s tests -p 'test_corpus_repository_dispatch.py'
- python3 -m unittest discover -s tests
- python3 -m ruff check tools tests
- git diff --check

End with:
- findings first, or state no findings
- validation reviewed or rerun
- remaining risks
- recommended next role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge-Corpus"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge-Corpus"
  tracker: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13"
  issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/17"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/16"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/24"
  previous_merge_commit: "df882af26e090ca0b037877ebb16052f047b0e94"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contracts/corpus_repository_dispatch_into_mythic_edge.md"
  target_artifact: "docs/implementation_handoffs/corpus_repository_dispatch_into_mythic_edge_comparison.md"
  verdict: "repository_dispatch_payload_builder_fail_closed_fix_ready_for_review"
  fixed_finding_ids:
    - "CORPUS-DISPATCH-E-001"
    - "CORPUS-DISPATCH-E-002"
    - "CORPUS-DISPATCH-E-003"
  risk_tier: "High"
  repository_dispatch_sent: false
  release_publishing_executed: false
  package_artifact_created: false
  release_asset_created: false
  github_secret_or_token_changed: false
  ratchet_execution_authorized: false
  baseline_pr_creation_authorized: false
  mythic_edge_mutation_authorized: false
  parser_truth_claimed: false
  fixture_promotion_claimed: false
  corpus_readiness_claimed: false
```
