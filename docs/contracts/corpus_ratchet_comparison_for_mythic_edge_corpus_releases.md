# Corpus Ratchet Comparison For Mythic Edge Corpus Releases Contract

## Module

`corpus_ratchet_comparison_for_mythic_edge_corpus_releases`

Plain English: this contract defines a future ratchet-comparison boundary for
reviewed `Tahjali11/Mythic-Edge-Corpus` releases. A future ratchet comparison
may compare Mythic Edge parser output against an approved corpus release package
and produce a bounded diagnostic report for human/Codex review.

The ratchet report is diagnostic evidence only. It is not parser truth, not
fixture promotion, not baseline approval, not corpus readiness, not release
readiness, not deploy readiness, not production readiness, not analytics truth,
not AI truth, not coaching truth, not full corpus parity, not security
assurance, and not privacy assurance.

This Codex B pass writes only this contract. It does not implement ratchet
comparison, run ratchets, publish releases, create package artifacts, create
release assets, send `repository_dispatch`, open baseline PRs, mutate
`Tahjali11/Mythic-Edge`, import raw corpus data, copy raw evidence, read
private logs, or change parser behavior.

## Source Artifact

- Repository: `Tahjali11/Mythic-Edge-Corpus`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge-Corpus`
- Issue: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/5
- Previous issue:
  https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/4
- Previous PR:
  https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/10
- Previous merge commit:
  `32a70399d1924aed3e35d37e2dfad64ac0a48670`
- Base branch: `main`
- Working branch:
  `codex/corpus-ratchet-comparison-5`
- Target artifact:
  `docs/contracts/corpus_ratchet_comparison_for_mythic_edge_corpus_releases.md`
- Risk tier: High

Observed during this Codex B pass:

- The operating checkout remote matched
  `https://github.com/Tahjali11/Mythic-Edge-Corpus.git`.
- The checkout started clean on `main`.
- `origin/main` was verified at
  `32a70399d1924aed3e35d37e2dfad64ac0a48670`.
- Work was moved to `codex/corpus-ratchet-comparison-5`.
- Issue #5 was open.
- Issue #4 was closed after PR #10 merged the repository-dispatch contract.
- PR #10 was merged into `main` at the expected merge commit.
- Issue #6 was open and explicitly remains a later baseline PR workflow.
- The target contract did not exist before this pass.
- The repository currently contains `README.md`, `LICENSE`, and the issue #1
  through #4 contracts.
- The local package preview command, PR validation package-safety layer,
  release-publishing layer, and repository-dispatch layer are still
  contract-only at the time of this pass.
- No `Tahjali11/Mythic-Edge` worktree files were inspected or mutated by this
  pass.

Current authorization facts to preserve:

```yaml
implementation_authorized: false
ratchet_comparison_contract_authorized: true
ratchet_comparison_implementation_authorized: false
ratchet_execution_authorized: false
ratchet_report_artifact_creation_authorized: false
baseline_pr_creation_authorized: false
baseline_mutation_authorized: false
release_publishing_authorized: false
repository_dispatch_authorized: false
package_artifact_creation_authorized: false
release_asset_creation_authorized: false
mythic_edge_mutation_authorized: false
raw_corpus_import_authorized: false
private_log_read_authorized: false
parser_behavior_change_authorized: false
parser_truth_claimed: false
fixture_promotion_claimed: false
corpus_readiness_claimed: false
release_readiness_claimed: false
deploy_readiness_claimed: false
production_readiness_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
```

## Source Artifacts Inspected

- Corpus issue #5
- Corpus issue #5 Codex A reconciliation comment
- Corpus issue #4
- Corpus issue #4 deployer closeout comment
- Corpus PR #10 metadata
- Corpus issue #6
- `README.md`
- `LICENSE`
- `docs/contracts/corpus_local_package_preview_command.md`
- `docs/contracts/corpus_pr_validation_package_safety.md`
- `docs/contracts/corpus_release_publishing_reviewed_packages.md`
- `docs/contracts/corpus_repository_dispatch_into_mythic_edge.md`

No raw corpus files, private logs, generated local artifacts, private reports,
package artifacts, release assets, dispatch payloads, ratchet outputs, baseline
PR artifacts, secrets, tokens, credentials, or `Tahjali11/Mythic-Edge` source
files were read, created, copied, mirrored, summarized, or committed.

## Observed Current Behavior

The corpus repo currently has:

- a README;
- a license;
- a contract for a future local package preview command;
- a contract for future PR validation package-safety checks;
- a contract for future release publishing of reviewed packages;
- a contract for future bounded repository dispatch into Mythic Edge.

It does not yet have:

- a corpus package manifest;
- a session ledger;
- package metadata;
- package preview tooling;
- PR validation tooling;
- release package tooling;
- release publishing automation;
- release assets;
- repository-dispatch automation;
- ratchet comparison tooling;
- ratchet report artifacts;
- baseline PR automation.

Issue #5 is the next planned diagnostic layer after dispatch. It must define
how a future comparison report may describe differences between a reviewed
corpus release and Mythic Edge parser output without performing the comparison
now and without mutating the receiving repository.

## Problem

Reviewed corpus package releases need a bounded way to support parser
regression review. A release package and dispatch event are useful only if a
receiving workflow can compare parser outputs against the package and explain
what changed.

The first bad value is any corpus release, package asset, checksum, dispatch
payload, parser output, comparison category, ratchet report, validation note,
or review summary being treated as parser truth, fixture promotion, corpus
readiness, release readiness, deploy readiness, production readiness, baseline
approval, full corpus parity, analytics truth, AI truth, coaching truth,
security assurance, or privacy assurance.

The second bad value is any ratchet comparison layer that mutates baselines,
opens PRs, edits `Tahjali11/Mythic-Edge`, changes parser behavior, promotes
fixtures, publishes releases, sends dispatch events, imports raw/private
corpus files, reads private logs, or turns diagnostic deltas into automatic
approval.

The third bad value is a report that hides uncertainty. Missing packages,
checksum mismatches, unsupported schema versions, missing parser comparison
surfaces, unsafe content, degraded evidence, and non-comparable outputs must
produce blocked, review-required, or unsupported report states instead of clean
pass/fail claims.

## Scope Decision

This contract approves a contract-only ratchet-comparison boundary.

Codex C implementation is not automatically authorized by this contract. A
later Codex C pass may proceed only if a user or lifecycle handoff explicitly
authorizes ratchet-comparison tooling, tests, safe public fixtures, and any
workflow file surface.

If later authorized, the narrow Codex C implementation surface in this
repository may include:

- a public-safe report schema validator under `tools/`;
- focused tests under `tests/`;
- tiny public-safe ratchet report examples;
- documentation for expected Mythic Edge receiving-side inputs.

Actual parser execution, parser output generation, golden replay execution,
feature-equity ratchet execution, baseline mutation, baseline PR creation, and
source-repo workflow implementation belong to `Tahjali11/Mythic-Edge` and
require a separate receiving-side contract.

This contract defines:

- ratchet comparison purpose and non-claims;
- owning layer and truth boundary;
- approved corpus release/package inputs and integrity checks;
- receiving-side assumptions for Mythic Edge without mutating or implementing
  in that repo;
- deterministic comparison result categories;
- public-safe ratchet report schema and vocabulary;
- provenance, package version, release tag, checksum, source commit, parser
  commit, and freshness requirements;
- fail-closed conditions;
- validation evidence needed for a later implementation;
- separation from issue #6 baseline PR automation;
- explicit non-claims.

This contract does not authorize:

- code implementation in Codex B;
- ratchet execution;
- ratchet report artifact creation;
- parser output generation;
- parser behavior changes;
- package artifact creation;
- release asset creation;
- release publishing execution;
- repository-dispatch execution;
- GitHub Actions workflow creation;
- status check creation;
- baseline mutation;
- baseline PR creation;
- GitHub issue or PR creation;
- mutation of `Tahjali11/Mythic-Edge`;
- raw corpus import;
- raw/private evidence reads;
- corpus readiness, release readiness, deploy readiness, production readiness,
  analytics truth, AI truth, coaching truth, security assurance, or privacy
  assurance claims.

## Owning Layer And Truth Boundary

Owner: `Tahjali11/Mythic-Edge-Corpus`, release-package ratchet comparison
contract and report vocabulary boundary.

Truth boundary:

- Mythic Edge parser/state remains the owner for parser interpretation,
  parser events, match/game identity, deduplication, final reconciliation, and
  generated parser outputs.
- Mythic Edge evidence-pipeline contracts own harvest, review, confidence,
  corpus metadata diff, parser-owned ratchet command behavior, and
  fixture-promotion semantics.
- The issue #1 local package preview boundary owns local/report-only package
  preview semantics.
- The issue #2 PR validation boundary owns PR package-safety semantics.
- The issue #3 release-publishing boundary owns reviewed corpus package release
  semantics.
- The issue #4 repository-dispatch boundary owns release notification semantics.
- This issue #5 boundary owns public-safe ratchet comparison report vocabulary
  and diagnostic categories.
- Issue #6 separately owns auto-open baseline PR planning after ratchet
  comparison is stable and reviewed.

Ratchet comparison may say:

- a reviewed release package was validated as an input;
- parser output for a specific Mythic Edge commit was compared to package
  expectations under a separately authorized receiving-side surface;
- comparison output contained new passes, new failures, missing families,
  changed outputs, degraded evidence, unsupported cases, or review-required
  rows;
- a report should be reviewed by a human/Codex role.

Ratchet comparison must not say:

- parser interpretation is correct;
- fixtures should be promoted;
- baselines should be updated;
- a PR should be opened;
- a ratchet result proves full corpus parity;
- the release is production-ready;
- the report is security assurance or privacy assurance.

Required future data flow:

```text
reviewed public-safe corpus release
  -> release metadata and checksum verification
  -> bounded notification or manual selection
  -> receiving-side Mythic Edge parser-output comparison surface
  -> public-safe ratchet comparison report
  -> later issue #6 baseline PR helper, if separately authorized
```

Forbidden shortcut:

```text
ratchet comparison report
  -/-> parser truth
  -/-> fixture promotion
  -/-> baseline mutation
  -/-> baseline PR creation
  -/-> source-repo mutation
  -/-> release readiness
  -/-> deploy readiness
  -/-> production readiness
```

## Approved Corpus Release Inputs

A future ratchet comparison may use only reviewed, public-safe release inputs
already authorized by the issue #3 and #4 contracts:

- `package_id`;
- `package_version`;
- `release_tag`;
- GitHub release URL;
- public-safe release asset names and URLs;
- public-safe release metadata JSON;
- public-safe checksum asset;
- SHA-256 checksums for public-safe release assets;
- release source commit;
- release channel;
- manifest ref and session-ledger ref;
- package preview validation ref;
- PR validation ref;
- human review ref;
- optional repository-dispatch payload metadata, if it is public-safe and
  bounded by the issue #4 contract.

The comparison layer must not use:

- raw package bytes from unverified assets;
- raw corpus evidence outside reviewed release assets;
- private local corpus files;
- generated local artifacts;
- external corpus contents;
- private reports;
- raw logs;
- source files copied from `Tahjali11/Mythic-Edge`;
- ratchet reports from previous runs as hidden truth;
- baseline PR artifacts.

## Required Input Integrity Checks

A future implementation must fail closed unless:

- the package release exists;
- the release tag matches the package version;
- the release metadata schema version is supported;
- the package asset, metadata asset, and checksum asset names match the release
  metadata;
- every listed asset URL belongs to `Tahjali11/Mythic-Edge-Corpus`;
- every listed checksum uses an approved algorithm such as SHA-256;
- every downloaded public-safe release asset matches its checksum;
- release source commit is present and well-formed;
- package preview and PR validation refs are present;
- human review ref is present;
- no asset, metadata field, or report field contains forbidden markers;
- receiving-side Mythic Edge comparison surface is explicitly authorized before
  parser output is generated or compared.

Checksums are integrity metadata only. They do not prove parser correctness,
fixture validity, privacy completeness, security assurance, or production
readiness.

## Receiving-Side Assumptions

`Tahjali11/Mythic-Edge` is a separate repository and must own its consuming
behavior through a separate or paired contract before any actual ratchet
execution occurs.

The Mythic Edge receiving-side contract should define:

- accepted corpus package ID and schema versions;
- accepted release channels;
- release asset download and checksum verification behavior;
- safe temporary artifact locations;
- parser-output generation command surface;
- public-safe comparison output shape;
- protected-surface checks;
- no private log reads by default;
- no baseline mutation;
- no baseline PR creation;
- no fixture promotion;
- no parser behavior change;
- no automatic issue closure;
- no deploy or production action;
- failure/refusal reporting;
- non-claims.

Until the receiving-side contract exists and is implemented, the only valid
ratchet comparison status in this corpus repo is `contract_only`,
`blocked_missing_receiver_contract`, or `review_required`.

## Comparison Result Categories

Future comparison reports may use these top-level categories:

- `not_evaluated`: comparison was not attempted.
- `matched_expected_output`: parser output matched a corpus expectation under
  the authorized comparison surface.
- `new_pass`: a case that previously failed now matches expected output.
- `new_failure`: a case that previously matched now fails or cannot be
  reconciled.
- `changed_output`: parser output changed and requires review.
- `missing_family`: expected corpus family or package section was unavailable
  in parser comparison output.
- `missing_case`: expected corpus case was unavailable in parser comparison
  output.
- `extra_output`: parser comparison produced public-safe output not declared by
  the release package.
- `degraded_evidence`: source evidence or package metadata exists but is
  partial, stale, disabled, assumption-limited, or degraded.
- `unsupported_package`: package schema, release channel, or metadata version
  is unsupported.
- `unsupported_parser_surface`: receiving-side parser comparison surface is
  missing or unsupported.
- `checksum_or_integrity_failure`: release asset integrity could not be
  verified.
- `forbidden_content_blocked`: forbidden input or output content was detected.
- `not_comparable`: package and parser output cannot be compared safely.
- `review_required`: a human/Codex reviewer must inspect ambiguity.
- `invalid`: report schema or required metadata is malformed.

Category rules:

- Categories are diagnostic labels only.
- Categories must not imply fixture promotion, baseline approval, readiness, or
  parser truth.
- `new_pass` is good evidence for review, not approval to update baselines.
- `new_failure` is a regression candidate, not proof of a parser bug until the
  owning repo reviews it.
- `changed_output` must preserve expected and actual output refs as
  public-safe summaries, not raw payloads.
- `missing_family`, `missing_case`, and `extra_output` must not be silently
  collapsed into pass/fail totals.

## Public-Safe Ratchet Report Shape

A future ratchet report, if separately authorized, must be a small
public-safe envelope:

```yaml
object: corpus_ratchet_comparison_report
schema_version: corpus_ratchet_comparison_report.v1
report_id: public_safe_id
source_repository: Tahjali11/Mythic-Edge-Corpus
source_repository_url: https://github.com/Tahjali11/Mythic-Edge-Corpus
target_repository: Tahjali11/Mythic-Edge
target_repository_url: https://github.com/Tahjali11/Mythic-Edge
package_id: mythic-edge-corpus
package_version: string
release_tag: corpus-package-v<package_version>
release_url: string
release_source_commit: full_git_sha
release_channel: reviewed
release_metadata_ref: public_safe_ref
checksum_ref: public_safe_ref
asset_checksums_verified: true | false
mythic_edge_commit: full_git_sha | unknown
mythic_edge_comparison_contract_ref: public_safe_ref | missing
comparison_surface: unknown
comparison_status: contract_only
started_at_utc: omitted_or_public_safe
completed_at_utc: omitted_or_public_safe
summary:
  total_cases: integer
  matched_expected_output: integer
  new_passes: integer
  new_failures: integer
  changed_outputs: integer
  missing_families: integer
  missing_cases: integer
  degraded_evidence: integer
  unsupported: integer
  review_required: integer
results: []
blocked_reason_codes: []
validation_refs: []
non_claims: []
```

Report rules:

- `report_id` must be public-safe and must not encode private file names, local
  paths, account names, deck names, or exact private timestamps.
- Refs must point to public-safe release metadata, contract refs, or
  repo-relative public fixtures, not raw content.
- Timestamps may be omitted. If present, they must be coarse/public-safe and
  must not reveal private play/capture windows.
- `results` may contain only public-safe IDs, categories, reason codes, and
  reduced expected/actual summary refs.
- `results` must not include raw parser payloads, raw logs, raw corpus content,
  source snippets, private paths, or secrets.
- `summary` counts are review metadata only. They must not be treated as
  readiness, full parity, or merge approval.
- `non_claims` must include parser truth, fixture promotion, baseline approval,
  readiness, analytics, AI, coaching, security, and privacy non-claims.

Recommended future per-result shape:

```yaml
case_id: public_safe_id
family_id: public_safe_id
result_category: not_evaluated
expected_ref: public_safe_ref
actual_ref: public_safe_ref | missing
evidence_status: unknown
comparison_confidence: unknown
freshness: unknown
reason_codes: []
review_required: true
non_claims: []
```

## Status Vocabulary

Ratchet comparison status values:

- `contract_only`: contract exists, but implementation is not authorized.
- `blocked_missing_release`: reviewed package release is absent.
- `blocked_missing_release_metadata`: release metadata is absent.
- `blocked_missing_checksum`: checksum metadata is absent.
- `blocked_checksum_mismatch`: release asset integrity failed.
- `blocked_unsupported_package`: package schema, version, or release channel is
  unsupported.
- `blocked_missing_receiver_contract`: Mythic Edge receiving-side comparison
  contract is absent.
- `blocked_missing_parser_surface`: authorized parser output comparison surface
  is absent.
- `blocked_forbidden_content`: forbidden content appeared in inputs or outputs.
- `blocked_private_input`: private or raw input would be required.
- `blocked_baseline_mutation_requested`: comparison attempted to mutate a
  baseline.
- `blocked_baseline_pr_requested`: comparison attempted to create or prepare a
  baseline PR.
- `blocked_source_mutation_requested`: comparison attempted to mutate
  `Tahjali11/Mythic-Edge`.
- `blocked_release_or_dispatch_requested`: comparison attempted release
  publishing or dispatch.
- `comparison_report_ready_for_review`: public-safe report exists and needs
  review.
- `comparison_completed_with_no_deltas`: report exists with no public-safe
  deltas, but this is not readiness.
- `comparison_completed_with_deltas`: report exists with public-safe deltas that
  require review.
- `review_required`: a reviewer must inspect ambiguity.
- `unsupported`: requested comparison mode is outside this contract.
- `invalid`: required fields are missing, contradictory, or unsafe.

For issue #5 during Codex B, the only current status is `contract_only`.

## Failure And Refusal Vocabulary

Failure/refusal reason codes should include:

- `missing_release_metadata`
- `missing_package_asset`
- `missing_checksum_asset`
- `checksum_mismatch`
- `release_tag_mismatch`
- `package_version_mismatch`
- `unsupported_package_schema`
- `unsupported_release_channel`
- `source_commit_mismatch`
- `missing_predecessor_preview_evidence`
- `missing_predecessor_pr_validation_evidence`
- `missing_human_review`
- `missing_receiver_contract`
- `missing_parser_comparison_surface`
- `payload_or_metadata_contains_forbidden_content`
- `report_contains_local_path`
- `report_contains_secret_marker`
- `report_contains_raw_corpus_content`
- `report_contains_private_log_marker`
- `parser_output_unavailable`
- `parser_output_schema_unsupported`
- `family_missing_from_package`
- `family_missing_from_parser_output`
- `case_missing_from_package`
- `case_missing_from_parser_output`
- `expected_actual_not_comparable`
- `changed_output_review_required`
- `baseline_mutation_requested`
- `baseline_pr_requested`
- `source_mutation_requested`
- `release_or_dispatch_requested`
- `review_required`
- `unsupported`

Failure output must use symbolic reason codes and public-safe metadata. It must
not echo raw payload values, raw output values, source snippets, or unsafe
content.

## Fail-Closed Rules

Future validation must fail closed when:

- package release metadata is absent;
- package release metadata is malformed;
- package release schema is unsupported;
- release tag and package version do not match;
- release assets are missing;
- checksums are missing or do not match;
- release source commit is absent or malformed;
- predecessor preview, PR validation, release, or dispatch evidence is missing
  when required;
- receiving-side Mythic Edge contract is absent;
- parser comparison surface is absent or unsupported;
- parser output cannot be generated by an authorized receiving-side workflow;
- package and parser output are not comparable;
- required family/case IDs are missing;
- forbidden raw/private/generated/runtime content is present;
- local absolute paths, private markers, raw provider payloads, raw logs,
  secrets, credentials, tokens, or webhook URLs appear;
- the comparison attempts baseline mutation;
- the comparison attempts baseline PR creation;
- the comparison attempts source-repo mutation;
- the comparison attempts release publishing or dispatch;
- the report claims parser truth, fixture promotion, readiness, full parity,
  security assurance, or privacy assurance.

Fail-closed outcomes must use public-safe statuses and reason codes. They must
not echo forbidden content.

## Downstream Issue Separation

Issue #5 must remain separate from:

- issue #6 auto-open baseline PR workflow after ratchet comparison;
- any Mythic Edge receiving-side workflow implementation;
- any parser behavior change;
- any corpus metadata update in `Tahjali11/Mythic-Edge`;
- any fixture-promotion workflow;
- any release replacement, prerelease, or backfill policy;
- any readiness, deploy, production, analytics, AI, or coaching workflow.

Ratchet comparison may produce diagnostic report evidence that later workflows
consume, but it must not implement or imply the readiness of those later
workflows.

## Validation Requirements For Later Codex C

If later authorized, Codex C should add focused tests for:

- missing release metadata;
- malformed release metadata;
- missing package asset;
- missing checksum asset;
- checksum mismatch;
- release tag/package version mismatch;
- unsupported package schema;
- unsupported release channel;
- missing predecessor preview evidence;
- missing predecessor PR validation evidence;
- missing human review ref;
- missing receiving-side contract;
- missing parser comparison surface;
- package and parser output not comparable;
- new pass category;
- new failure category;
- changed output category;
- missing family category;
- missing case category;
- extra output category;
- degraded evidence category;
- unsupported parser surface category;
- forbidden raw/private/generated/runtime marker in inputs;
- local absolute path in report;
- secret-shaped marker in report;
- attempted baseline mutation refusal;
- attempted baseline PR refusal;
- attempted source-repo mutation refusal;
- attempted release/dispatch refusal;
- symbolic failure output;
- no baseline mutation, no baseline PR, no release publishing, no dispatch, and
  no Mythic Edge mutation.

Recommended future validation commands:

```bash
python3 -m pytest -q tests/test_corpus_ratchet_comparison_report.py
python3 tools/corpus_ratchet_comparison_report.py --validate-only --report <public_safe_report.json>
git diff --check
```

Those commands are future implementation validation only. They are not
authorized by this Codex B pass.

## Validation Requirements For Codex E

Codex E should review:

- whether this contract preserves issue #1 preview, issue #2 PR validation,
  issue #3 release-publishing, and issue #4 dispatch dependencies;
- whether ratchet comparison is diagnostic/report-only;
- whether approved inputs are release metadata and public-safe package assets
  only;
- whether checksum and release provenance are integrity metadata only;
- whether the receiving-side Mythic Edge surface is clearly separate;
- whether comparison result categories avoid parser truth, fixture promotion,
  baseline approval, readiness, and full-parity claims;
- whether report schema is small enough and public-safe;
- whether failure/refusal vocabulary fails closed;
- whether issue #6 baseline PR automation remains later and unauthorized;
- whether the contract avoids parser truth, fixture promotion, corpus
  readiness, release readiness, deploy readiness, production readiness,
  security assurance, and privacy assurance claims.

## Protected Surfaces And Non-Claims

This contract does not authorize:

- code implementation;
- PR creation;
- issue closure;
- package preview execution;
- PR validation execution;
- package artifact creation;
- release asset creation;
- GitHub release creation;
- release publishing execution;
- GitHub Actions workflow creation;
- status check creation;
- repository-dispatch execution;
- ratchet execution;
- ratchet report artifact creation;
- parser output generation;
- baseline mutation;
- baseline PR creation;
- raw corpus import;
- external corpus import;
- private evidence reads;
- private logs;
- generated local artifacts;
- secret or connection material reads;
- `Tahjali11/Mythic-Edge` mutation;
- parser behavior changes.

This contract does not claim:

- parser truth;
- fixture correctness;
- fixture promotion;
- corpus readiness;
- release readiness;
- deploy readiness;
- production readiness;
- ratchet success;
- baseline approval;
- full corpus parity;
- analytics truth;
- AI truth;
- coaching truth;
- security assurance;
- privacy assurance.

## Recommended Next Role

Codex E should review this contract before Codex C implementation is
considered. If Codex E finds it clean, route to Codex F/G for docs-only
submission and merge. Codex C should not start unless a later handoff
explicitly authorizes ratchet-comparison report tooling, tests, safe public
fixtures, and any workflow files. Actual parser execution and receiving-side
workflow implementation must be separately authorized in `Tahjali11/Mythic-Edge`.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Corpus issue #5.

Repository:
Tahjali11/Mythic-Edge-Corpus

Repository URL:
https://github.com/Tahjali11/Mythic-Edge-Corpus

Issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/5

Previous issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/4

Previous PR:
https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/10

Contract artifact:
docs/contracts/corpus_ratchet_comparison_for_mythic_edge_corpus_releases.md

Goal:
Review the ratchet comparison contract. Lead with findings, if any. Verify that
ratchet comparison is diagnostic/report-only, preserves issue #1 preview,
issue #2 PR validation, issue #3 release-publishing, and issue #4 dispatch
dependencies, consumes only reviewed public-safe release inputs, separates the
Mythic Edge receiving-side contract, and leaves issue #6 baseline PR automation
for later.

Do not implement code.
Do not open a PR.
Do not close issue #5.
Do not run ratchets.
Do not mutate Tahjali11/Mythic-Edge.
Do not publish corpus packages, create release assets, send repository_dispatch,
open baseline PRs, import raw corpus data, read private logs, or claim parser
truth, corpus readiness, release readiness, deploy readiness, production
readiness, security assurance, privacy assurance, fixture promotion, baseline
approval, or full corpus parity.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge-Corpus"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge-Corpus"
  issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/5"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/4"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/10"
  completed_thread: "B"
  next_thread: "E"
  verdict: "ratchet_comparison_contract_written_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  latest_verified_commit: "32a70399d1924aed3e35d37e2dfad64ac0a48670"
  target_artifact: "docs/contracts/corpus_ratchet_comparison_for_mythic_edge_corpus_releases.md"
  implementation_authorized: false
  ratchet_execution_authorized: false
  baseline_pr_creation_authorized: false
  release_publishing_authorized: false
  repository_dispatch_authorized: false
  mythic_edge_mutation_authorized: false
  raw_corpus_import_authorized: false
  private_log_read_authorized: false
  stop_conditions:
    - "Do not implement code from this contract."
    - "Do not run ratchet comparison."
    - "Do not mutate Tahjali11/Mythic-Edge."
    - "Do not publish corpus packages or create release/package artifacts."
    - "Do not send repository_dispatch."
    - "Do not open baseline PRs or mutate baselines."
    - "Do not import raw corpus data or read private logs."
    - "Do not claim parser truth, corpus readiness, release readiness, deploy readiness, production readiness, security assurance, privacy assurance, fixture promotion, baseline approval, or full corpus parity."
```
