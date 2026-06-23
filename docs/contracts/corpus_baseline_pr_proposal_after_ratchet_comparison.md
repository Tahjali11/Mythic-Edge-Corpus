# Corpus Baseline PR Proposal After Ratchet Comparison Contract

## Module

`corpus_baseline_pr_proposal_after_ratchet_comparison`

Plain English: this contract defines a future baseline PR proposal boundary for
reviewed `Tahjali11/Mythic-Edge-Corpus` releases after ratchet comparison. A
future helper may prepare public-safe draft PR proposal metadata from an
approved ratchet comparison report so reviewers can decide whether a baseline
update should be opened in `Tahjali11/Mythic-Edge`.

The baseline PR proposal helper is review evidence only. It is not parser
truth, not fixture promotion, not baseline approval, not corpus readiness, not
release readiness, not deploy readiness, not production readiness, not ratchet
success, not full corpus parity, not analytics truth, not AI truth, not
coaching truth, not security assurance, and not privacy assurance.

This Codex B pass writes only this contract. It does not implement proposal
tooling, create or open baseline PRs, mutate baselines, mutate
`Tahjali11/Mythic-Edge`, run ratchets, publish releases, create package
artifacts, create release assets, send `repository_dispatch`, import raw
corpus data, copy raw evidence, read private logs, or change parser behavior.

## Source Artifact

- Repository: `Tahjali11/Mythic-Edge-Corpus`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge-Corpus`
- Issue: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/6
- Previous issue:
  https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/5
- Previous PR:
  https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/11
- Previous merge commit:
  `05ee36916092b253b6f1462c16edd6897fc1faa8`
- Base branch: `main`
- Working branch:
  `codex/corpus-baseline-pr-proposal-6`
- Target artifact:
  `docs/contracts/corpus_baseline_pr_proposal_after_ratchet_comparison.md`
- Risk tier: High

Observed during this Codex B pass:

- The operating checkout remote matched
  `https://github.com/Tahjali11/Mythic-Edge-Corpus.git`.
- The checkout started clean on `main`.
- `origin/main` was verified at
  `05ee36916092b253b6f1462c16edd6897fc1faa8`.
- Work was moved to `codex/corpus-baseline-pr-proposal-6`.
- Issue #6 was open.
- Issue #5 was closed after PR #11 merged the ratchet-comparison contract.
- PR #11 was merged into `main` at the expected merge commit.
- The target contract did not exist before this pass.
- The repository currently contains `README.md`, `LICENSE`, and the issue #1
  through #5 contracts.
- The local package preview command, PR validation package-safety layer,
  release-publishing layer, repository-dispatch layer, and ratchet-comparison
  layer are still contract-only at the time of this pass.
- No `Tahjali11/Mythic-Edge` worktree files were inspected or mutated by this
  pass.

Current authorization facts to preserve:

```yaml
implementation_authorized: false
baseline_pr_proposal_contract_authorized: true
baseline_pr_proposal_implementation_authorized: false
baseline_pr_creation_authorized: false
baseline_mutation_authorized: false
ratchet_execution_authorized: false
ratchet_report_artifact_creation_authorized: false
release_publishing_authorized: false
repository_dispatch_authorized: false
package_artifact_creation_authorized: false
release_asset_creation_authorized: false
mythic_edge_mutation_authorized: false
source_repo_branch_creation_authorized: false
source_repo_commit_authorized: false
source_repo_status_check_authorized: false
source_repo_comment_authorized: false
source_repo_review_authorized: false
source_repo_label_authorized: false
raw_corpus_import_authorized: false
private_log_read_authorized: false
parser_behavior_change_authorized: false
parser_truth_claimed: false
fixture_promotion_claimed: false
baseline_approval_claimed: false
corpus_readiness_claimed: false
release_readiness_claimed: false
deploy_readiness_claimed: false
production_readiness_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
```

## Source Artifacts Inspected

- Corpus issue #6
- Corpus issue #6 Codex A reconciliation comment
- Corpus issue #5
- Corpus PR #11 metadata
- `README.md`
- `LICENSE`
- `docs/contracts/corpus_local_package_preview_command.md`
- `docs/contracts/corpus_pr_validation_package_safety.md`
- `docs/contracts/corpus_release_publishing_reviewed_packages.md`
- `docs/contracts/corpus_repository_dispatch_into_mythic_edge.md`
- `docs/contracts/corpus_ratchet_comparison_for_mythic_edge_corpus_releases.md`

No raw corpus files, private logs, generated local artifacts, private reports,
package artifacts, release assets, dispatch payloads, ratchet outputs,
baseline PR artifacts, secrets, tokens, credentials, or
`Tahjali11/Mythic-Edge` source files were read, created, copied, mirrored,
summarized, or committed.

## Observed Current Behavior

The corpus repo currently has:

- a README;
- a license;
- a contract for a future local package preview command;
- a contract for future PR validation package-safety checks;
- a contract for future release publishing of reviewed packages;
- a contract for future bounded repository dispatch into Mythic Edge;
- a contract for future ratchet-comparison reports.

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
- baseline PR proposal tooling;
- baseline PR artifacts;
- source-repo branch or PR automation.

Issue #6 is the planned proposal layer after ratchet comparison. It must define
how a future helper may prepare a public-safe baseline PR proposal without
normalizing parser output, mutating baselines, creating PRs, or approving
anything automatically.

## Problem

Automatically proposing baseline updates can save review time after a trusted
ratchet comparison report exists, but it is the highest-risk corpus automation
step because it can make current parser output look approved too easily.

The first bad value is any ratchet report, package version, release tag,
checksum, comparison category, changed-output summary, generated branch name,
draft PR title, draft PR body, validation note, or proposal status being
treated as parser truth, fixture promotion, baseline approval, corpus
readiness, release readiness, deploy readiness, production readiness, full
corpus parity, analytics truth, AI truth, coaching truth, security assurance,
or privacy assurance.

The second bad value is any Corpus-side helper that mutates
`Tahjali11/Mythic-Edge`, opens or updates source-repo PRs, creates branches,
commits baseline files, posts comments, creates labels, creates status checks,
runs ratchets, publishes releases, sends dispatch events, imports raw/private
corpus files, reads private logs, or creates credentials before a separate
exact authorization exists.

The third bad value is proposal text that hides uncertainty. Failed,
unsafe, stale, unsupported, non-public-safe, non-comparable, degraded, or
review-required ratchet output must block the proposal rather than produce
clean PR text.

## Scope Decision

This contract approves a contract-only baseline PR proposal boundary.

Codex C implementation is not automatically authorized by this contract. A
later Codex C pass may proceed only if a user or lifecycle handoff explicitly
authorizes proposal tooling, tests, public-safe fixtures, and any no-write
validation surface.

If later authorized, the narrow Codex C implementation surface in this
repository may include:

- a public-safe proposal schema validator under `tools/`;
- a local no-write proposal preview command under `tools/`;
- focused tests under `tests/`;
- tiny public-safe proposal examples;
- documentation for expected Mythic Edge receiving-side review inputs.

Actual baseline mutation, source-repo branch creation, source-repo commits,
source-repo PR creation, source-repo comments, source-repo reviews, source-repo
labels, source-repo status checks, parser execution, parser output generation,
golden replay execution, feature-equity ratchet execution, and source-repo
workflow implementation belong to `Tahjali11/Mythic-Edge` and require a
separate receiving-side contract plus explicit user authorization.

This contract defines:

- baseline PR proposal purpose and non-claims;
- owning layer and truth boundary;
- required predecessor gates;
- eligible and blocked ratchet report statuses;
- public-safe draft PR title, body, branch, and metadata vocabulary without
  creating any PR;
- evidence summary fields and checksum/provenance requirements;
- fail-closed conditions;
- least-privilege future credential and source-repo action requirements;
- validation evidence needed for a later implementation;
- separation from actual baseline PR creation, source-repo mutation, and
  baseline mutation;
- explicit non-claims.

This contract does not authorize:

- code implementation in Codex B;
- baseline PR proposal execution;
- baseline PR creation;
- source-repo branch creation;
- source-repo commit creation;
- source-repo PR creation;
- source-repo comment, status check, review, label, or milestone creation;
- baseline mutation;
- ratchet execution;
- ratchet report artifact creation;
- parser output generation;
- parser behavior changes;
- package artifact creation;
- release asset creation;
- release publishing execution;
- repository-dispatch execution;
- GitHub Actions workflow creation;
- token or secret creation;
- mutation of `Tahjali11/Mythic-Edge`;
- raw corpus import;
- raw/private evidence reads;
- corpus readiness, release readiness, deploy readiness, production readiness,
  analytics truth, AI truth, coaching truth, security assurance, or privacy
  assurance claims.

## Owning Layer And Truth Boundary

Owner: `Tahjali11/Mythic-Edge-Corpus`, public-safe baseline PR proposal
contract and proposal vocabulary boundary.

Truth boundary:

- Mythic Edge parser/state remains the owner for parser interpretation,
  parser events, match/game identity, deduplication, final reconciliation, and
  generated parser outputs.
- Mythic Edge evidence-pipeline contracts own harvest, review, confidence,
  corpus metadata diff, parser-owned ratchet command behavior,
  fixture-promotion semantics, baseline files, source-repo branches, and
  source-repo PRs.
- The issue #1 local package preview boundary owns local/report-only package
  preview semantics.
- The issue #2 PR validation boundary owns PR package-safety semantics.
- The issue #3 release-publishing boundary owns reviewed corpus package release
  semantics.
- The issue #4 repository-dispatch boundary owns release notification
  semantics.
- The issue #5 ratchet-comparison boundary owns public-safe diagnostic report
  vocabulary and comparison categories.
- This issue #6 boundary owns public-safe baseline PR proposal vocabulary only.

Baseline PR proposal may say:

- a reviewed ratchet comparison report is eligible for human review;
- a draft source-repo PR could be prepared by a separately authorized Mythic
  Edge workflow;
- the proposal references a reviewed package version, release tag, release
  URL, checksums, ratchet report ID, Mythic Edge commit, and public-safe
  changed-output summary;
- a reviewer should inspect the proposal before any source-repo action.

Baseline PR proposal must not say:

- parser interpretation is correct;
- fixtures should be promoted;
- baselines should be updated;
- a PR has been opened;
- a PR should be merged;
- a ratchet result proves full corpus parity;
- a release is production-ready;
- the proposal is security assurance or privacy assurance.

Required future data flow:

```text
reviewed public-safe corpus release
  -> release metadata and checksum verification
  -> bounded notification or manual selection
  -> receiving-side Mythic Edge parser-output comparison surface
  -> public-safe ratchet comparison report
  -> public-safe baseline PR proposal preview
  -> separately authorized Mythic Edge PR creation workflow, if approved
```

Forbidden shortcut:

```text
baseline PR proposal
  -/-> parser truth
  -/-> fixture promotion
  -/-> baseline mutation
  -/-> source-repo branch creation
  -/-> source-repo PR creation
  -/-> source-repo mutation
  -/-> merge readiness
  -/-> release readiness
  -/-> deploy readiness
  -/-> production readiness
```

## Required Predecessor Gates

A future baseline PR proposal implementation must fail closed unless all
required predecessor gates are satisfied:

- the local package preview command exists and passed for the exact package
  candidate;
- the PR validation package-safety layer exists and passed for the exact
  package candidate;
- a reviewed public-safe package release was published by the approved release
  workflow;
- the repository-dispatch boundary exists and either a bounded dispatch
  notification was sent or a public-safe manual release-selection ref exists;
- release source commit is reachable from the approved default branch;
- release tag matches package version;
- release metadata JSON exists and passes schema validation;
- release asset checksums exist and refer only to public-safe release assets;
- no raw/private/generated/runtime source is included in release metadata;
- a human reviewer approved the exact release and ratchet candidate;
- the receiving-side Mythic Edge ratchet comparison surface exists and is
  separately authorized;
- a public-safe ratchet comparison report exists and passes schema validation;
- the ratchet report references the exact package version, release tag,
  release URL, release source commit, Mythic Edge commit, and comparison
  contract refs;
- the ratchet report contains no forbidden markers, raw outputs, source
  patches, source snippets, private paths, or secrets;
- the ratchet report status is eligible under this contract;
- a human/Codex review gate explicitly authorizes proposal generation in
  no-write mode;
- no source-repo branch, commit, PR, comment, review, label, status check,
  baseline mutation, ratchet run, release, dispatch, deploy, or production
  action is requested by the proposal step.

If any predecessor is absent, stale, blocked, failed, ambiguous,
review-required, unsupported, or invalid, proposal generation must write
nothing outside explicitly authorized local/no-write preview output.

## Eligible And Blocked Ratchet Report Statuses

Eligible input statuses for a future no-write proposal preview:

- `comparison_report_ready_for_review`
- `comparison_completed_with_deltas`
- `comparison_completed_with_no_deltas`

Eligibility rules:

- `comparison_report_ready_for_review` may produce a proposal preview only if
  all required metadata is present and the report includes explicit
  review-required language.
- `comparison_completed_with_deltas` may produce a proposal preview only if
  every delta is public-safe, categorized, and linked to reduced evidence refs.
- `comparison_completed_with_no_deltas` may produce a no-op proposal summary,
  but it must not open a PR or imply readiness.

Blocked input statuses:

- `contract_only`
- `blocked_missing_release`
- `blocked_missing_release_metadata`
- `blocked_missing_checksum`
- `blocked_checksum_mismatch`
- `blocked_unsupported_package`
- `blocked_missing_receiver_contract`
- `blocked_missing_parser_surface`
- `blocked_forbidden_content`
- `blocked_private_input`
- `blocked_baseline_mutation_requested`
- `blocked_baseline_pr_requested`
- `blocked_source_mutation_requested`
- `blocked_release_or_dispatch_requested`
- `review_required` without explicit human/Codex proposal authorization
- `unsupported`
- `invalid`
- any unknown future status.

Blocked statuses must produce symbolic refusal metadata only. They must not
produce draft PR text that looks actionable.

## Proposal Status Vocabulary

Baseline PR proposal status values:

- `contract_only`: contract exists, but implementation is not authorized.
- `proposal_preview_ready_for_review`: no-write proposal metadata can be
  reviewed by a human/Codex role.
- `proposal_preview_no_deltas`: ratchet report had no public-safe deltas; no
  source-repo PR should be proposed.
- `proposal_preview_degraded`: proposal metadata exists, but degradation or
  uncertainty requires review before any source action.
- `proposal_blocked_missing_ratchet_report`: ratchet report is absent.
- `proposal_blocked_ineligible_ratchet_status`: ratchet report status is not
  eligible.
- `proposal_blocked_missing_integrity_metadata`: package release, checksum, or
  provenance metadata is absent.
- `proposal_blocked_checksum_or_release_mismatch`: release integrity metadata
  does not match the report.
- `proposal_blocked_stale_report`: report freshness or referenced commits do
  not match the requested proposal.
- `proposal_blocked_forbidden_content`: report or proposed text includes
  forbidden content.
- `proposal_blocked_raw_or_private_input`: raw corpus, private, generated,
  external, or source-repo input would be required.
- `proposal_blocked_source_action_requested`: source-repo branch, commit, PR,
  comment, review, label, or status check creation was requested.
- `proposal_blocked_baseline_mutation_requested`: baseline file mutation was
  requested.
- `proposal_blocked_ratchet_execution_requested`: ratchet execution was
  requested.
- `proposal_blocked_release_or_dispatch_requested`: release publishing or
  dispatch execution was requested.
- `proposal_blocked_missing_human_review`: human/Codex proposal review gate is
  absent.
- `review_required`: a reviewer must inspect ambiguity before any next action.
- `unsupported`: requested proposal mode is outside this contract.
- `invalid`: required fields are missing, contradictory, or unsafe.

For issue #6 during Codex B, the only current status is `contract_only`.

## Public-Safe Proposal Shape

A future proposal preview, if separately authorized, must be a small
public-safe envelope:

```yaml
object: corpus_baseline_pr_proposal
schema_version: corpus_baseline_pr_proposal.v1
proposal_id: public_safe_id
proposal_status: contract_only
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
ratchet_report_id: public_safe_id
ratchet_report_ref: public_safe_ref
ratchet_report_status: comparison_completed_with_deltas
mythic_edge_commit: full_git_sha
mythic_edge_base_branch: main
mythic_edge_candidate_branch_name: proposed_safe_branch_name
draft_pr_title: string
draft_pr_body_sections: []
changed_output_summary: {}
validation_summary: {}
review_gate_refs: []
blocked_reason_codes: []
non_claims: []
```

Proposal rules:

- `proposal_id` must be public-safe and must not encode private file names,
  local paths, account names, deck names, or exact private timestamps.
- Refs must point to public-safe release metadata, ratchet report refs,
  contract refs, or repo-relative public fixtures, not raw content.
- `mythic_edge_candidate_branch_name` must be proposed text only. It must not
  create a branch.
- `draft_pr_title` and `draft_pr_body_sections` must be proposed text only.
  They must not open or update a PR.
- `changed_output_summary` may contain counts and symbolic categories only. It
  must not contain raw parser payloads, raw corpus content, source snippets, or
  patches.
- `validation_summary` may list public-safe validation command names and
  statuses only. It must not include private output excerpts.
- `non_claims` must include parser truth, fixture promotion, baseline
  approval, readiness, analytics, AI, coaching, security, and privacy
  non-claims.

## Proposed Branch And PR Metadata Vocabulary

Future proposal previews may include these source-repo metadata fields as text
only:

- proposed source repository: `Tahjali11/Mythic-Edge`;
- proposed base branch;
- proposed head branch name;
- proposed draft PR title;
- proposed PR body;
- `Refs` issue links;
- package version;
- release tag;
- release URL;
- checksum verification summary;
- ratchet report ID and ref;
- Mythic Edge source commit;
- changed-output summary;
- validation summary;
- protected-surface summary;
- review checklist;
- non-claims;
- next-role routing.

Branch-name rules:

- Proposed branch names must be deterministic and repo-safe, for example
  `codex/corpus-baseline-proposal-<package_version>-<short_report_id>`.
- Proposed branch names must not include local usernames, local paths, private
  timestamps, deck names, secret values, raw hashes of private content, or
  free-form ratchet output.
- Proposed branch names must not target protected or production branches.

PR-title rules:

- The title must identify the update as a draft/review proposal.
- The title must include the package version or report ID only if those values
  are public-safe.
- The title must not say "approved", "ready", "parser fixed", "baseline
  confirmed", "production ready", or similar stronger claims.

PR-body rules:

- Use `Refs`, not `Closes`, for issue/tracker links unless a later Codex F/G
  source-repo handoff explicitly authorizes closing behavior.
- Include a "Not Claimed" or "Non-Claims" section.
- Include a "Review Required Before Merge" section.
- Include a "Protected Surfaces" section.
- Include a "Validation Evidence" section.
- Include a "Changed Output Summary" section with public-safe categories only.
- Include a "Package Provenance" section with release tag, URL, checksums, and
  source commits.
- Do not include raw diffs, patches, source snippets, raw parser outputs, raw
  corpus payloads, private paths, private logs, secrets, tokens, credentials,
  exact private timestamps, or model-provider output.

## Evidence Summary Fields

Future proposal previews may summarize:

- package ID;
- package version;
- release tag;
- release URL;
- release source commit;
- release channel;
- release metadata ref;
- checksum ref;
- checksum verification status;
- package preview validation ref;
- PR validation ref;
- human release review ref;
- repository-dispatch or manual selection ref;
- ratchet comparison contract ref;
- ratchet report ID;
- ratchet report ref;
- ratchet report status;
- Mythic Edge commit;
- Mythic Edge comparison contract ref;
- total public-safe cases;
- matched expected output count;
- new pass count;
- new failure count;
- changed output count;
- missing family count;
- missing case count;
- extra output count;
- degraded evidence count;
- unsupported count;
- review-required count;
- blocked reason codes;
- non-claims.

Evidence summaries must not include:

- raw corpus content;
- raw parser output;
- raw log excerpts;
- raw package bytes;
- raw source diffs;
- source patches;
- source snippets;
- full baseline file content;
- local absolute paths;
- private timestamps;
- private decklists;
- private reports;
- secrets, tokens, credentials, or webhook URLs.

## Least-Privilege Future Source-Repo Action Requirements

This contract does not authorize source-repo actions. If a later issue
authorizes actual baseline PR creation, it must require:

- a separate `Tahjali11/Mythic-Edge` contract or implementation handoff;
- explicit user approval for source-repo mutation;
- least-privilege token or GitHub App permissions;
- branch creation permission scoped to the intended source repository;
- pull-request creation permission scoped to draft PRs only;
- no direct push to `main`;
- no merge permission;
- no deployment permission;
- no secret readback;
- no production environment access;
- no broad issue/label/status/review/comment permissions unless separately
  justified;
- no automatic baseline mutation without a reviewed file list;
- no automatic PR opening from failed, unsafe, stale, unsupported, degraded,
  or review-required reports;
- no auto-merge.

Recommended symbolic future credential name, if a later source-repo action
contract approves one:

```text
MYTHIC_EDGE_BASELINE_PR_APP_TOKEN
```

This name is a placeholder for contract discussion only. It does not create,
rotate, authorize, or require any secret.

## Failure And Refusal Vocabulary

Failure/refusal reason codes should include:

- `missing_ratchet_report`
- `ratchet_report_schema_invalid`
- `ratchet_report_status_ineligible`
- `ratchet_report_stale`
- `missing_release_metadata`
- `missing_checksum_metadata`
- `checksum_mismatch`
- `release_tag_mismatch`
- `package_version_mismatch`
- `release_source_commit_mismatch`
- `mythic_edge_commit_missing`
- `missing_predecessor_preview_evidence`
- `missing_predecessor_pr_validation_evidence`
- `missing_release_review`
- `missing_dispatch_or_manual_selection_ref`
- `missing_human_proposal_review`
- `proposal_contains_forbidden_content`
- `proposal_contains_local_path`
- `proposal_contains_secret_marker`
- `proposal_contains_raw_corpus_content`
- `proposal_contains_private_log_marker`
- `proposal_contains_source_patch`
- `proposal_contains_source_snippet`
- `proposal_requests_source_branch`
- `proposal_requests_source_commit`
- `proposal_requests_source_pr`
- `proposal_requests_source_comment`
- `proposal_requests_source_status_check`
- `proposal_requests_source_review`
- `proposal_requests_source_label`
- `proposal_requests_baseline_mutation`
- `proposal_requests_ratchet_execution`
- `proposal_requests_release_publishing`
- `proposal_requests_repository_dispatch`
- `proposal_claims_parser_truth`
- `proposal_claims_fixture_promotion`
- `proposal_claims_baseline_approval`
- `proposal_claims_readiness`
- `review_required`
- `unsupported`

Failure output must use symbolic reason codes and public-safe metadata. It must
not echo raw payload values, raw output values, source snippets, patches, or
unsafe content.

## Fail-Closed Rules

Future validation must fail closed when:

- required predecessor preview, PR validation, release, dispatch/manual
  selection, ratchet, or human review evidence is missing;
- ratchet report metadata is absent;
- ratchet report schema is malformed;
- ratchet report status is ineligible;
- ratchet report freshness or referenced commits are stale;
- release tag and package version do not match;
- release assets are missing;
- checksums are missing or do not match;
- release source commit is absent or malformed;
- Mythic Edge commit is absent or malformed;
- public-safe report refs are not comparable;
- changed-output summary includes raw output values;
- proposed branch/title/body includes forbidden content;
- local absolute paths, private markers, raw provider payloads, raw logs,
  secrets, credentials, tokens, or webhook URLs appear;
- proposal text requests source-repo branch creation, commit creation, PR
  creation, comment, review, label, status check, merge, deploy, or production
  action;
- proposal text requests baseline mutation;
- proposal text requests ratchet execution;
- proposal text requests release publishing or dispatch;
- proposal text claims parser truth, fixture promotion, baseline approval,
  corpus readiness, release readiness, deploy readiness, production readiness,
  full corpus parity, security assurance, or privacy assurance.

Fail-closed outcomes must use public-safe statuses and reason codes. They must
not echo forbidden content.

## Downstream Issue Separation

Issue #6 must remain separate from:

- actual source-repo baseline PR creation;
- any `Tahjali11/Mythic-Edge` receiving-side implementation;
- any parser behavior change;
- any baseline mutation;
- any corpus metadata update in `Tahjali11/Mythic-Edge`;
- any fixture-promotion workflow;
- any release replacement, prerelease, or backfill policy;
- any readiness, deploy, production, analytics, AI, or coaching workflow.

Baseline PR proposal may produce reviewable public-safe proposal metadata that
later workflows consume, but it must not implement or imply the readiness of
those later workflows.

## Validation Requirements For Later Codex C

If later authorized, Codex C should add focused tests for:

- missing ratchet report;
- malformed ratchet report;
- ineligible ratchet report status;
- stale ratchet report;
- missing release metadata;
- missing checksum metadata;
- checksum mismatch;
- release tag/package version mismatch;
- release source commit mismatch;
- missing Mythic Edge commit;
- missing predecessor preview evidence;
- missing predecessor PR validation evidence;
- missing release review;
- missing dispatch or manual selection ref;
- missing human proposal review;
- no-delta proposal summary;
- delta proposal summary;
- degraded proposal summary;
- changed-output category summary;
- new-pass category summary;
- new-failure category summary;
- missing-family and missing-case category summary;
- unsupported and review-required category summary;
- forbidden raw/private/generated/runtime marker in report;
- local absolute path in proposal;
- secret-shaped marker in proposal;
- source patch or source snippet in proposal;
- attempted source branch creation refusal;
- attempted source commit refusal;
- attempted source PR creation refusal;
- attempted source comment/status/review/label refusal;
- attempted baseline mutation refusal;
- attempted ratchet execution refusal;
- attempted release/dispatch refusal;
- symbolic failure output;
- no baseline mutation, no baseline PR, no source-repo action, no ratchet, no
  release publishing, no dispatch, and no Mythic Edge mutation.

Recommended future validation commands:

```bash
python3 -m pytest -q tests/test_corpus_baseline_pr_proposal.py
python3 tools/corpus_baseline_pr_proposal.py --validate-only --proposal <public_safe_proposal.json>
git diff --check
```

Those commands are future implementation validation only. They are not
authorized by this Codex B pass.

## Validation Requirements For Codex E

Codex E should review:

- whether this contract preserves issue #1 preview, issue #2 PR validation,
  issue #3 release-publishing, issue #4 dispatch, and issue #5 ratchet
  comparison dependencies;
- whether proposal generation remains no-write and review-gated;
- whether eligible and blocked ratchet report statuses are conservative enough;
- whether the proposal shape is small enough and public-safe;
- whether draft branch, title, and PR body metadata are clearly proposed text
  only;
- whether `Refs` versus `Closes` guidance avoids accidental issue closure;
- whether least-privilege source-repo action requirements are stated without
  authorizing source-repo action;
- whether failure/refusal vocabulary fails closed;
- whether the contract avoids parser truth, fixture promotion, baseline
  approval, corpus readiness, release readiness, deploy readiness, production
  readiness, full corpus parity, security assurance, and privacy assurance
  claims.

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
- token or secret creation;
- token or secret rotation;
- repository-dispatch execution;
- ratchet execution;
- ratchet report artifact creation;
- parser output generation;
- baseline mutation;
- baseline PR creation;
- source-repo branch creation;
- source-repo commit creation;
- source-repo PR creation;
- source-repo comments;
- source-repo reviews;
- source-repo labels;
- source-repo status checks;
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
explicitly authorizes baseline PR proposal validation tooling, tests, safe
public fixtures, and no-write preview behavior. Actual source-repo branch,
commit, PR, comment, review, label, status-check, baseline mutation, or
receiving-side workflow implementation must be separately authorized in
`Tahjali11/Mythic-Edge`.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Corpus issue #6.

Repository:
Tahjali11/Mythic-Edge-Corpus

Repository URL:
https://github.com/Tahjali11/Mythic-Edge-Corpus

Issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/6

Previous issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/5

Previous PR:
https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/11

Contract artifact:
docs/contracts/corpus_baseline_pr_proposal_after_ratchet_comparison.md

Goal:
Review the baseline PR proposal contract. Lead with findings, if any. Verify
that proposal generation is no-write and review-gated, preserves issue #1
preview, issue #2 PR validation, issue #3 release publishing, issue #4 dispatch,
and issue #5 ratchet comparison dependencies, consumes only eligible public-safe
ratchet reports, treats draft branch/title/PR body metadata as proposed text
only, keeps actual source-repo action separate, and forbids parser truth,
fixture promotion, baseline approval, readiness, full-parity, security, and
privacy claims.

Do not implement code.
Do not open a PR.
Do not close issue #6.
Do not mutate Tahjali11/Mythic-Edge.
Do not create baseline PRs, mutate baselines, create source-repo branches,
commits, PRs, comments, reviews, labels, or status checks.
Do not run ratchets.
Do not publish corpus packages, create release assets, send repository_dispatch,
import raw corpus data, read private logs, or claim parser truth, corpus
readiness, release readiness, deploy readiness, production readiness, security
assurance, privacy assurance, fixture promotion, baseline approval, or full
corpus parity.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge-Corpus"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge-Corpus"
  issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/6"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/5"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/11"
  completed_thread: "B"
  next_thread: "E"
  verdict: "baseline_pr_proposal_contract_written_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  branch: "codex/corpus-baseline-pr-proposal-6"
  latest_verified_commit: "05ee36916092b253b6f1462c16edd6897fc1faa8"
  target_artifact: "docs/contracts/corpus_baseline_pr_proposal_after_ratchet_comparison.md"
  implementation_authorized: false
  baseline_pr_creation_authorized: false
  baseline_mutation_authorized: false
  ratchet_execution_authorized: false
  release_publishing_authorized: false
  repository_dispatch_authorized: false
  mythic_edge_mutation_authorized: false
  raw_corpus_import_authorized: false
  private_log_read_authorized: false
  stop_conditions:
    - "Do not implement code from this contract."
    - "Do not mutate Tahjali11/Mythic-Edge."
    - "Do not create baseline PRs or mutate baselines."
    - "Do not create source-repo branches, commits, PRs, comments, reviews, labels, or status checks."
    - "Do not run ratchet comparison."
    - "Do not publish corpus packages or create release/package artifacts."
    - "Do not send repository_dispatch."
    - "Do not import raw corpus data or read private logs."
    - "Do not claim parser truth, corpus readiness, release readiness, deploy readiness, production readiness, security assurance, privacy assurance, fixture promotion, baseline approval, or full corpus parity."
```
