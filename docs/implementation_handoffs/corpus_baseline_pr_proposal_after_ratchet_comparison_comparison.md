# Codex C/D Handoff: Corpus Baseline PR Proposal Preview

## Role

Codex C implemented the bounded preview surface for Mythic-Edge-Corpus issue
#19. Codex D then fixed the concrete Codex E blocker findings
`CORPUS-BASEPR-E-001` and `CORPUS-BASEPR-E-002`.

## Source Artifacts

- Repository: `Tahjali11/Mythic-Edge-Corpus`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge-Corpus`
- Tracker: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13
- Issue: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/19
- Previous issue: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/18
- Previous PR: https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/26
- Latest verified commit:
  `c7bde10209711e29e0bcdb3a842510d3d9663bed`
- Source contract:
  `docs/contracts/corpus_baseline_pr_proposal_after_ratchet_comparison.md`

## Artifact Produced

- `tools/corpus_baseline_pr_proposal.py`
- `tests/test_corpus_baseline_pr_proposal.py`
- `docs/implementation_handoffs/corpus_baseline_pr_proposal_after_ratchet_comparison_comparison.md`

## Comparison Summary

The implementation adds a bounded, no-write baseline PR proposal preview
surface. It builds and validates public-safe proposal objects from supplied
ratchet comparison reports and explicit predecessor gate evidence. It does not
mutate baselines, create branches, create commits, open PRs, post comments,
create status checks, run ratchets, publish releases, send
`repository_dispatch`, create package artifacts, or mutate
`Tahjali11/Mythic-Edge`.

Confirmed contract matches:

- Defines a proposal object:
  `corpus_baseline_pr_proposal.v1`.
- Reuses the existing ratchet comparison report validator when available.
- Accepts only explicit in-memory ratchet report input and explicit
  predecessor gate refs.
- Requires package preview, PR validation, release review, dispatch/manual
  selection, ratchet report, and human proposal review evidence before a ready
  proposal preview can be produced.
- Allows proposal previews only for eligible ratchet report statuses:
  `comparison_report_ready_for_review`,
  `comparison_completed_with_deltas`, and
  `comparison_completed_with_no_deltas`.
- Emits review-only draft metadata for delta proposals without performing any
  source-repo action.
- Emits a no-action `proposal_preview_no_deltas` object for no-delta reports.
- Marks degraded or review-required deltas as
  `proposal_preview_degraded` rather than cleanly ready.
- Fails closed for missing reports, ineligible ratchet statuses, missing
  integrity refs, checksum or release mismatches, stale comparison commits,
  missing predecessor evidence, missing human review, forbidden content, and
  out-of-scope action requests.
- Keeps blocked and no-delta proposal objects free of branch names, PR titles,
  and PR body sections.
- Emits only symbolic reason codes for unsafe/private inputs and does not echo
  raw values.
- Preserves explicit no-write guards and non-claims for parser truth, fixture
  promotion, baseline approval, corpus readiness, release readiness, deploy
  readiness, production readiness, analytics truth, AI truth, coaching truth,
  security assurance, privacy assurance, full corpus parity, source-repo
  action, baseline mutation, and ratchet execution.
- Adds a validate-only CLI for already-built public-safe proposal JSON:
  `python3 tools/corpus_baseline_pr_proposal.py --validate-only --proposal <public_safe_proposal.json>`.

Mismatches fixed:

- No baseline PR proposal builder, validator, CLI, or focused tests existed
  before this pass.
- The contract was originally contract-only, but issue #19 explicitly
  authorized bounded no-write proposal preview implementation while keeping
  baseline PR creation, baseline mutation, ratchet execution, release
  publishing, dispatch, and Mythic Edge mutation unauthorized.

## Validation Run

Passed:

- `python3 -m pytest -q tests/test_corpus_baseline_pr_proposal.py`
  - 12 tests passed.
- `python3 -m pytest -q tests/test_corpus_baseline_pr_proposal.py tests/test_corpus_ratchet_comparison_report.py`
  - 30 tests passed.
- `python3 -m pytest -q tests`
  - 91 tests passed.
- `python3 tools/corpus_baseline_pr_proposal.py --validate-only --proposal tests/.tmp_baseline_pr_proposal_manual.json --format json`
  - exited 0 for a temporary public-safe proposal preview.
- `python3 -m py_compile tools/corpus_baseline_pr_proposal.py tests/test_corpus_baseline_pr_proposal.py`
- `git diff --check`
- changed-file whitespace/final-newline scan
- focused changed-file public-safety scan for local absolute paths, raw log
  markers, token-shaped markers, webhook URL markers, and API key markers

## Codex D Fixer Addendum

Codex D addressed Codex E findings `CORPUS-BASEPR-E-001` and
`CORPUS-BASEPR-E-002` with a narrow fail-closed public-safety validation pass.

Fix summary:

- Proposal validation now rejects direct action-request text for source branch,
  commit, PR, comment, status check, review, label, baseline mutation, ratchet
  execution, release publishing, and `repository_dispatch` requests.
- Incoming report/proposal key scanning now catches unexpected snake_case and
  camelCase action key shapes such as source-PR creation, baseline mutation, and
  repository-dispatch markers before preview output is produced.
- Truth, fixture-promotion, baseline-approval, readiness, parity, security, and
  privacy claims now return the contract's specific public-safe symbolic reason
  codes where available.
- Exact symbolic upstream ratchet refusal codes remain allowed as blocked report
  evidence, so already-blocked ratchet reports still route through the
  ineligible-status path instead of being reclassified as unsafe content.
- CLI validate-only failure output remains symbolic and does not echo unsafe
  proposal text.

Additional Codex D validation:

- `python3 -m pytest -q tests/test_corpus_baseline_pr_proposal.py`
  - 16 tests passed.
- `python3 -m pytest -q tests/test_corpus_baseline_pr_proposal.py tests/test_corpus_ratchet_comparison_report.py`
  - 34 tests passed.
- `python3 -m pytest -q tests`
  - 95 tests passed.
- `python3 -m ruff check tools tests`
  - All checks passed.
- `python3 -m py_compile tools/corpus_baseline_pr_proposal.py tests/test_corpus_baseline_pr_proposal.py`
  - Passed.
- `git diff --check`
  - Passed with no output.
- Changed-file whitespace/final-newline scan over the issue #19 artifacts
  - Passed.
- Focused public-marker scan over the issue #19 artifacts
  - Passed.

## Remaining Risks And Non-Claims

- No real ratchet was run.
- No baseline was mutated.
- No baseline PR was created or opened.
- No source-repo branch, commit, comment, status check, review, label, or
  milestone was created.
- No package artifact or release asset was created.
- No release was published.
- No `repository_dispatch` was sent.
- No `Tahjali11/Mythic-Edge` file, branch, issue, PR, or status was mutated.
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

Act as Codex E: Module Reviewer for Mythic-Edge-Corpus issue #19.

Repository:
Tahjali11/Mythic-Edge-Corpus

Repository URL:
https://github.com/Tahjali11/Mythic-Edge-Corpus

Tracker:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13

Issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/19

Previous issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/18

Previous PR:
https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/26

Latest verified commit:
c7bde10209711e29e0bcdb3a842510d3d9663bed

Source contract:
docs/contracts/corpus_baseline_pr_proposal_after_ratchet_comparison.md

Implementation handoff:
docs/implementation_handoffs/corpus_baseline_pr_proposal_after_ratchet_comparison_comparison.md

Goal:
Review the bounded no-write baseline PR proposal preview implementation and
Codex D fixer pass against the contract and issue #19 authorization. Lead with
findings ordered by severity. Verify that the implementation only builds and
validates public-safe proposal preview objects from explicit
ratchet/predecessor inputs and does not create source-repo actions, mutate
baselines, run ratchets, publish releases, send repository_dispatch, create
package artifacts, or mutate Tahjali11/Mythic-Edge.

Review focus:
- tools/corpus_baseline_pr_proposal.py
- tests/test_corpus_baseline_pr_proposal.py
- docs/implementation_handoffs/corpus_baseline_pr_proposal_after_ratchet_comparison_comparison.md

Protected boundaries:
- Do not mutate Tahjali11/Mythic-Edge.
- Do not create baseline PRs, branches, commits, comments, reviews, labels,
  or status checks.
- Do not mutate baselines.
- Do not run real ratchets.
- Do not publish releases or create package artifacts.
- Do not send repository_dispatch.
- Do not read private logs, raw corpus/private files, local app data,
  secrets, credentials, tokens, webhook URLs, or generated local artifacts.
- Do not claim parser truth, fixture promotion, baseline approval, corpus
  readiness, release readiness, deploy readiness, production readiness,
  analytics truth, AI truth, coaching truth, security assurance, privacy
  assurance, or full corpus parity.

Suggested validation:
- python3 -m pytest -q tests/test_corpus_baseline_pr_proposal.py tests/test_corpus_ratchet_comparison_report.py
- python3 -m pytest -q tests
- python3 -m py_compile tools/corpus_baseline_pr_proposal.py tests/test_corpus_baseline_pr_proposal.py
- git diff --check
- focused changed-file public-safety scan

End with:
- findings first
- validation run
- remaining risks
- recommended next role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge-Corpus"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge-Corpus"
  issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/19"
  tracker: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/18"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/26"
  completed_thread: "D"
  next_thread: "E"
  verdict: "baseline_pr_proposal_preview_blockers_fixed_ready_for_review"
  risk_tier: "High"
  latest_verified_commit: "c7bde10209711e29e0bcdb3a842510d3d9663bed"
  source_contract: "docs/contracts/corpus_baseline_pr_proposal_after_ratchet_comparison.md"
  target_artifact: "docs/implementation_handoffs/corpus_baseline_pr_proposal_after_ratchet_comparison_comparison.md"
  baseline_pr_proposal_preview_authorized: true
  baseline_pr_creation_authorized: false
  baseline_mutation_authorized: false
  ratchet_execution_authorized: false
  release_publishing_authorized: false
  repository_dispatch_authorized: false
  mythic_edge_mutation_authorized: false
```
