# Corpus Phase 5 Decomposition Decision Packet Contract

## Module

`corpus_phase_5_decomposition_decision_packet`

Plain English: this contract defines the required decision packet before any
future Corpus Phase 5 decomposition work. A decomposition packet is a reviewed
planning artifact that explains whether a Corpus surface should stay where it
is, be split inside this repository, be deferred, or require a later explicitly
approved boundary decision.

This contract is contract-only. It does not implement code, move files, publish
packages, create package or release artifacts, send `repository_dispatch`, run
ratchets, open baseline PRs, mutate Mythic Edge, import raw corpus/private
files, read private logs, or claim parser truth, corpus readiness, release
readiness, deploy readiness, production readiness, security assurance, privacy
assurance, analytics truth, AI truth, or coaching truth.

## Source Context

- Repository: `Tahjali11/Mythic-Edge-Corpus`
- Issue: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/29
- Related completed Corpus tracker:
  https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13
- Related project roadmap:
  https://github.com/Tahjali11/Mythic-Edge/issues/568
- Target artifact:
  `docs/contracts/corpus_phase_5_decomposition_decision_packet.md`
- Risk tier: High

Observed during this Codex B pass:

- Issue #29 was open and requested this contract-only artifact.
- Corpus tracker #13 was closed after the public-safe automation/dry-run lane.
- The local checkout was clean but on a stale branch with a gone upstream.
- Work was moved to an isolated issue worktree on `origin/main`:
  `codex/corpus-phase-5-decomposition-decision-packet-29`.
- `origin/main` was verified at `74b63eebcc2d`.
- No repo-local `AGENTS.md` exists in the Corpus repository.
- `README.md` currently contains only the repository title.
- Existing contracts, implementation handoffs, tests, tools, public-safe
  bootstrap metadata, and the public-safe dry-run report were inspected as
  context only.

Codex E reconciliation:

- `CORPUS-PHASE5-E-001` found that the original contract wording could be read
  as letting a reviewed decision packet authorize implementation or Codex C
  work.
- `CORPUS-PHASE5-E-002` found that the decision-packet false-authority envelope
  did not require every protected false/not-claimed flag needed for this lane.
- This revision clarifies that a decision packet is recommendation and routing
  evidence only, and that all protected flags must remain explicitly false.

Current authorization facts to preserve:

```yaml
implementation_authorized: false
file_move_authorized: false
cross_repo_extraction_authorized: false
pr_creation_authorized: false
package_publishing_authorized: false
package_artifact_creation_authorized: false
release_asset_creation_authorized: false
repository_dispatch_authorized: false
ratchet_execution_authorized: false
baseline_pr_creation_authorized: false
baseline_mutation_authorized: false
mythic_edge_mutation_authorized: false
raw_corpus_import_authorized: false
private_log_read_authorized: false
private_path_read_authorized: false
parser_behavior_change_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
parser_truth_claimed: false
fixture_promotion_claimed: false
baseline_approval_claimed: false
corpus_readiness_claimed: false
release_readiness_claimed: false
deploy_readiness_claimed: false
production_readiness_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
analytics_truth_claimed: false
ai_truth_claimed: false
coaching_truth_claimed: false
```

## Source Artifacts Inspected

- Corpus issue #29
- Corpus tracker #13
- Mythic Edge project roadmap #568
- `README.md`
- `docs/contracts/corpus_local_package_preview_command.md`
- `docs/contracts/corpus_pr_validation_package_safety.md`
- `docs/contracts/corpus_release_publishing_reviewed_packages.md`
- `docs/contracts/corpus_repository_dispatch_into_mythic_edge.md`
- `docs/contracts/corpus_ratchet_comparison_for_mythic_edge_corpus_releases.md`
- `docs/contracts/corpus_baseline_pr_proposal_after_ratchet_comparison.md`
- `docs/contract_test_reports/corpus_public_safe_end_to_end_dry_run.md`
- `docs/implementation_handoffs/`
- `corpus/manifest.v1.json`
- `corpus/session_ledger.v1.json`
- public-safe Corpus tools and focused tests as inventory references only

No Mythic Edge worktree was inspected or mutated by this pass. No private logs,
raw corpus files, private paths, secrets, generated local artifacts, package
artifacts, release assets, dispatch payloads, ratchet outputs, or baseline PR
artifacts were created.

## Observed Current Behavior

The Corpus repository now contains a public-safe automation support lane:

- local package preview tooling;
- PR package-safety validation tooling;
- release package dry-run metadata tooling;
- no-send repository-dispatch payload validation;
- ratchet comparison report construction from supplied public-safe inputs;
- no-write baseline PR proposal preview;
- a public-safe end-to-end dry-run report;
- public-safe bootstrap corpus metadata and focused tests.

The public-safe dry-run report records that these stages compose without
requesting external actions. That report remains diagnostic evidence only. It
does not authorize real package publishing, release asset creation,
`repository_dispatch`, ratchet execution, baseline mutation, baseline PR
creation, Mythic Edge mutation, corpus readiness, parser truth, release
readiness, or assurance claims.

## Problem

The first bad value is treating a decomposition packet as implementation
authority. A packet may recommend a boundary; it must not move files, create a
new public interface, publish artifacts, trigger cross-repo actions, or approve
readiness by itself.

The second bad value is treating historical Corpus automation evidence as
current clearance for a refactor. Existing contracts, handoffs, tests, and
dry-run reports may explain current surfaces, but they do not prove that a
future decomposition is safe unless the packet ties that evidence to the exact
candidate, current commit, target paths, downstream consumers, and proposed
behavior-preserving validation.

The third bad value is extracting Corpus behavior across repositories before
the boundary is stable, independently testable, separately governed, and safer
than a same-repo decomposition.

## Scope Decision

This contract approves only the shape and rules for a future Corpus Phase 5
decomposition decision packet.

The packet may:

- classify Corpus public-safe automation surfaces;
- describe current behavior and ownership;
- compare same-repo decomposition, keep-local, defer, and review-required
  choices;
- identify tests and validation required before any later behavior-preserving
  implementation;
- reference ARS or refactor evidence as advisory historical context;
- request a later child issue that may separately ask for implementation,
  review, or fresh evidence authority.

The packet must not:

- implement code;
- move files;
- authorize Codex C work;
- authorize implementation;
- authorize file moves;
- create or modify public interfaces;
- publish packages;
- create release/package artifacts;
- send `repository_dispatch`;
- run ratchets;
- open baseline PRs;
- mutate baselines or Mythic Edge;
- import raw corpus/private files;
- read private logs or private paths;
- claim parser truth, fixture promotion, baseline approval, corpus readiness,
  release readiness, deploy readiness, production readiness, analytics truth,
  AI truth, coaching truth, security assurance, or privacy assurance.

## Implementation Authority Boundary

A Corpus Phase 5 decomposition decision packet has no implementation authority.
This is true even when:

- `final_decision` is `same_repo_decomposition`;
- Codex E accepts the packet;
- a human accepts the packet as a planning artifact;
- the packet names behavior-preservation tests;
- the packet names a proposed destination;
- the packet includes a future Codex C prompt.

Required interpretation:

```yaml
decision_packet_authorizes_implementation: false
decision_packet_authorizes_file_moves: false
decision_packet_authorizes_public_interface_changes: false
decision_packet_authorizes_codex_c: false
```

A later Codex C implementation may begin only if a separate current issue,
handoff, or explicit user instruction authorizes implementation and sets the
relevant implementation flags to true for that later scope. The decision packet
may be a prerequisite input to that later authorization, but it cannot create
that authorization itself.

Any packet text that says or implies "this packet authorizes implementation",
"this packet authorizes Codex C", "review acceptance authorizes code changes",
or "same-repo decomposition is approved for implementation" is invalid and must
be routed to `blocked` or `review_required`.

## Owning Layer And Truth Boundary

Owner: `Tahjali11/Mythic-Edge-Corpus`, public-safe Corpus automation and
evidence-support planning boundary.

Truth and authority boundary:

- Mythic Edge parser/state layers own parser behavior, parser truth, match/game
  interpretation, fixture-promotion semantics, corpus status changes, and
  source-repo mutation authority.
- The Corpus repository owns only its public-safe package preview, package
  validation, release dry-run, dispatch no-send, ratchet report, baseline
  proposal preview, public-safe metadata, tests, contracts, and handoffs.
- A Corpus decomposition packet may classify and route Corpus repository
  surfaces. It may not approve Mythic Edge source changes or parser/corpus
  truth.
- A Corpus decomposition packet may recommend same-repo decomposition first.
  It may not approve cross-repo extraction unless a later issue explicitly
  proves the boundary and authorizes that decision.

## Candidate Surface Vocabulary

A decision packet must classify each candidate as exactly one primary
`candidate_surface_class`:

- `package_preview_surface`: local package preview command, schema, tests, or
  report-only package inventory behavior.
- `package_validation_surface`: PR package-safety validation, path checks,
  forbidden marker checks, manifest/session-ledger checks, and tests.
- `release_dry_run_surface`: reviewed release package dry-run metadata,
  planned asset identity/checksum metadata, and no-write release validation.
- `repository_dispatch_boundary_surface`: no-send dispatch payload builder,
  receiver-contract metadata, payload validation, and no-token/no-send guards.
- `ratchet_report_surface`: public-safe ratchet comparison report construction
  from supplied safe inputs without executing ratchets.
- `baseline_pr_proposal_surface`: no-write baseline PR proposal preview and
  review-only title/body/branch metadata.
- `public_safe_dry_run_surface`: composition helper and report showing the
  public-safe Corpus loop can run without external action.
- `ledger_or_manifest_surface`: `corpus/manifest.v1.json`,
  `corpus/session_ledger.v1.json`, session metadata, and schema expectations.
- `test_surface`: focused unit tests, public-safe regression tests, or
  validation command grouping.
- `implementation_handoff_surface`: Codex C/D/E handoff documentation and
  comparison reports.
- `contract_or_prompt_surface`: contracts, workflow handoffs, or issue-routing
  text.
- `cross_repo_boundary_candidate`: any candidate that would require Mythic
  Edge, Automation Artifacts, Security, Fable, Analytics, or another repository
  to own part of the Corpus behavior.
- `unknown_review_required`: a candidate whose surface cannot be safely
  classified from committed public-safe metadata.

If more than one class appears to apply, the packet must choose the highest-risk
class and list the secondary classes in `secondary_surface_classes`.

## Decision Vocabulary

Allowed `final_decision` values:

- `keep_local`: keep the candidate at its current path and document why no
  split is warranted now.
- `same_repo_decomposition`: split or reorganize the candidate within
  `Tahjali11/Mythic-Edge-Corpus` only as a planning recommendation. This value
  does not authorize implementation, Codex C, file moves, public interface
  changes, or test edits.
- `defer`: no current change; the candidate should be revisited after a named
  dependency, evidence packet, or tracker update.
- `request_fresh_evidence`: request a later public-safe ARS/refactor/review
  evidence pass before any decomposition decision.
- `request_mythic_edge_contract_child`: request a separate Mythic Edge contract
  because the candidate touches parser truth, baselines, fixture promotion, or
  Mythic Edge source authority.
- `reject_unsafe`: reject the decomposition route because it would require a
  forbidden input, action, or claim.
- `unsupported`: the packet cannot make a decision from committed public-safe
  inputs.
- `review_required`: human or Codex E review is required before the candidate
  can advance.

Forbidden decision values and claims:

- `implementation_approved`
- `implementation_ready`
- `codex_c_authorized`
- `file_move_approved`
- `public_interface_change_approved`
- `package_publish_approved`
- `release_asset_approved`
- `repository_dispatch_approved`
- `ratchet_approved`
- `baseline_pr_approved`
- `mythic_edge_mutation_approved`
- `parser_truth_confirmed`
- `fixture_promotion_confirmed`
- `baseline_approved`
- `corpus_ready`
- `release_ready`
- `deploy_ready`
- `production_ready`
- `security_assured`
- `privacy_assured`

## Required Decision Packet Envelope

A future decision packet must use a public-safe envelope with these fields:

```yaml
object: "corpus_phase_5_decomposition_decision_packet"
schema_version: "corpus_phase_5_decomposition_decision_packet.v1"
packet_id: "<stable-public-safe-id>"
repository: "Tahjali11/Mythic-Edge-Corpus"
source_issue: "<Corpus issue URL>"
related_project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
target_commit: "<40-character-commit-or-symbolic-review-ref>"
created_by_role: "Codex A|Codex B|Codex E|human"
created_at_utc: "<ISO-8601-UTC>"
packet_status: "draft|review_ready|blocked|deferred|superseded"
implementation_authority:
  decision_packet_authorizes_implementation: false
  decision_packet_authorizes_file_moves: false
  decision_packet_authorizes_public_interface_changes: false
  decision_packet_authorizes_codex_c: false
  separate_authority_required: true
  separate_authority_ref: "none"
candidate_count: <integer>
non_claims:
  - "not_parser_truth"
  - "not_fixture_promotion"
  - "not_baseline_approval"
  - "not_corpus_readiness"
  - "not_release_readiness"
  - "not_deploy_readiness"
  - "not_production_readiness"
  - "not_analytics_truth"
  - "not_ai_truth"
  - "not_coaching_truth"
  - "not_security_assurance"
  - "not_privacy_assurance"
false_authority_flags:
  implementation_authorized: false
  file_move_authorized: false
  cross_repo_extraction_authorized: false
  pr_creation_authorized: false
  package_publishing_authorized: false
  package_artifact_creation_authorized: false
  release_asset_creation_authorized: false
  repository_dispatch_authorized: false
  ratchet_execution_authorized: false
  baseline_pr_creation_authorized: false
  baseline_mutation_authorized: false
  mythic_edge_mutation_authorized: false
  raw_corpus_import_authorized: false
  private_log_read_authorized: false
  private_path_read_authorized: false
  parser_behavior_change_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  parser_truth_claimed: false
  fixture_promotion_claimed: false
  baseline_approval_claimed: false
  corpus_readiness_claimed: false
  release_readiness_claimed: false
  deploy_readiness_claimed: false
  production_readiness_claimed: false
  analytics_truth_claimed: false
  ai_truth_claimed: false
  coaching_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```

The packet must fail closed if any false-authority flag is missing, true, or
contradicted by free text. The packet must also fail closed if any
`implementation_authority` field is missing, true, or contradicts the
separate-authority requirement.

## Required Candidate Fields

Each candidate row must include:

- `candidate`: stable public-safe candidate name.
- `candidate_surface_class`: one value from the candidate surface vocabulary.
- `secondary_surface_classes`: optional list from the same vocabulary.
- `current_path`: current repo-relative path or path group.
- `current_behavior`: plain-English description of behavior today.
- `truth_or_authority_owner`: exact owning layer; for Corpus candidates this
  should normally be Corpus public-safe automation, not Mythic Edge parser
  truth.
- `upstream_dependencies`: contracts, metadata files, tests, tools, dry-run
  reports, or review inputs required before the candidate works.
- `downstream_consumers`: tests, tools, reports, contracts, handoffs, or
  cross-repo consumers affected by a future change.
- `public_safe_inputs`: committed public-safe inputs allowed for decision
  making.
- `forbidden_inputs`: raw/private/generated/runtime inputs that must not be
  read or echoed.
- `proposed_destination`: `same_path`, repo-relative destination, `defer`, or
  `later_contract_required`.
- `why_not_keep_local`: required if proposing any split.
- `why_not_move_to_existing_repo`: required if proposing same-repo
  decomposition or deferral; must explicitly address why Mythic Edge is not the
  owner unless parser truth/source mutation authority is involved.
- `why_not_new_repo`: required for any candidate that looks extractable.
- `new_public_interface_needed`: boolean.
- `new_public_interface_description`: required if the boolean is true; must be
  symbolic and must not expose raw data or private implementation details.
- `corpus_public_safe_boundary`: how the candidate preserves no-publish,
  no-dispatch, no-ratchet, no-baseline, no-private-read, and no-Mythic-Edge
  mutation rules.
- `ars_refactor_evidence_status`: subsection described below.
- `behavior_preservation_tests`: focused tests or validation commands required
  before a later implementation could be reviewed.
- `rollback_plan`: how a later implementation can be reverted without package,
  dispatch, ratchet, baseline, or Mythic Edge side effects.
- `final_decision`: one value from the allowed decision vocabulary.
- `decision_reason`: short public-safe rationale.
- `owner_acceptance_ref`: issue, review, or human approval ref for accepting
  the decision packet as planning evidence only. This field must not be treated
  as Codex C or implementation authority.
- `next_authority_required`: exact later authority needed before any code,
  file-move, public-interface, package, dispatch, ratchet, baseline, or Mythic
  Edge action.
- `non_claims`: candidate-level non-claims.

## ARS And Refactor Evidence Status

ARS and refactor evidence may be referenced only as advisory context. The
decision packet must not treat ARS/refactor evidence as source-repo authority,
readiness proof, or implementation approval.

Required fields:

```yaml
ars_refactor_evidence_status:
  prior_evidence_found: true|false
  reviewed_repository: "<repo-or-none>"
  reviewed_scope: "<path-or-symbolic-scope-or-none>"
  reviewed_commit: "<commit-or-none>"
  evidence_artifact: "<public-safe-artifact-ref-or-none>"
  evidence_tooling: "ARS|Refactor Scout|manual review|none"
  current_target_commit: "<commit-or-symbolic-review-ref>"
  relevant_changes_since_review: "none_known|known_changes|unknown"
  evidence_status: "current|historical|absent|not_needed|fresh_evidence_requested|review_required|unsupported"
  fresh_evidence_needed: true|false
  reason: "<public-safe-reason>"
```

Rules:

- `current` is allowed only when the evidence matches the reviewed repository,
  reviewed scope, reviewed commit, current target commit, relevant tooling
  contract, and current decomposition question.
- `historical` must be used when evidence exists but target commit, scope, or
  decomposition question differs.
- `fresh_evidence_requested` may request a later public-safe review path, but
  it does not authorize ARS execution, source inspection, probes, module
  sweeps, issue creation, or source-repo mutation.
- `unsupported` or `review_required` must be used if evidence would require
  private inputs, raw diffs, source patches, or non-public artifacts.

## Same-Repo-First Policy

The default decision must be `keep_local`, `same_repo_decomposition`, `defer`,
or `review_required`.

Cross-repo extraction is out of scope unless a later contract proves all of the
following:

- the boundary is stable;
- the boundary is independently testable;
- the boundary has a separately governed owner;
- the new public interface is smaller and clearer than the current local one;
- keeping the behavior local is riskier than extraction;
- downstream consumers can be updated without changing parser truth, publishing
  behavior, dispatch behavior, ratchet execution, baseline mutation, or Mythic
  Edge source authority;
- rollback is possible without package, dispatch, ratchet, baseline, or Mythic
  Edge side effects.

If any condition is missing, the only allowed decisions are `keep_local`,
`same_repo_decomposition`, `defer`, `request_mythic_edge_contract_child`,
`reject_unsafe`, or `review_required`.

## Corpus Public-Safe Automation Boundary

Allowed decision inputs:

- committed Corpus contracts;
- committed public-safe implementation handoffs;
- committed public-safe dry-run reports;
- committed public-safe Corpus metadata under `corpus/`;
- public-safe tool and test inventory;
- GitHub issue and PR metadata;
- roadmap text from public issues;
- public-safe ARS/refactor evidence references.

Forbidden decision inputs:

- raw corpus/private files;
- raw private logs;
- private paths;
- secrets, credentials, tokens, API keys, or webhook URLs;
- generated local artifacts;
- private reports;
- raw diffs, source patches, or source snippets from other repositories;
- unreviewed package artifacts;
- release assets;
- dispatch payloads intended to be sent;
- ratchet execution outputs;
- baseline PR branches, commits, or source patches;
- Mythic Edge worktree contents unless a later issue explicitly authorizes
  that inspection.

Forbidden actions:

- code implementation;
- file moves;
- package archive creation;
- release metadata file creation;
- checksum file creation;
- GitHub release creation;
- release asset upload;
- `repository_dispatch` send;
- ratchet execution;
- baseline mutation;
- baseline PR creation;
- Mythic Edge source inspection or mutation;
- raw corpus import;
- private log read;
- issue/PR/comment/status-check creation from packet contents;
- readiness, truth, or assurance claims.

## Fail-Closed Rules

A packet is invalid and must be routed to `blocked`, `unsupported`, or
`review_required` if it:

- omits a required packet or candidate field;
- uses a forbidden decision value;
- sets any false-authority flag to true;
- omits any required false-authority flag;
- omits the `implementation_authority` object;
- sets any `implementation_authority` field to an implementation-approving
  value;
- implies that a decision packet, review acceptance, owner acceptance, or
  `same_repo_decomposition` decision authorizes Codex C, implementation, file
  moves, public interface changes, tests, or code changes;
- treats public-safe dry-run success as corpus readiness;
- treats a no-send dispatch payload as an approved dispatch;
- treats a ratchet report object as ratchet execution;
- treats a baseline proposal preview as an approved baseline PR;
- routes parser truth, fixture promotion, or baseline approval into Corpus;
- references private inputs, raw logs, private paths, secrets, raw diffs, or
  source patches;
- proposes cross-repo extraction without satisfying the same-repo-first policy;
- lacks rollback and behavior-preservation validation.

## Validation Expectations For Later Implementation

A later Codex C implementation may be considered only after all of these are
true:

- a decision packet is reviewed and accepted as planning evidence;
- a separate current issue, handoff, or explicit user instruction authorizes
  implementation for a specific candidate;
- the later authority explicitly sets the relevant implementation flags to true
  for that specific scope;
- protected actions outside that later scope remain false.

The later implementation should include validation appropriate to the
candidate, such as:

- focused unit tests for moved or split functions;
- before/after report-only command output comparison;
- unchanged public-safe dry-run status and no-external-action guards;
- JSON validation for `corpus/manifest.v1.json`,
  `corpus/session_ledger.v1.json`, and public-safe session metadata when
  relevant;
- no new package/release/dispatch/ratchet/baseline artifacts;
- no Mythic Edge mutation or source inspection;
- no private/raw/generated/local artifact reads;
- no false authority flags or readiness/truth/assurance claims;
- `git diff --check`;
- focused public-artifact scan for private paths, raw logs, secrets, dispatch
  send claims, package publish claims, ratchet execution claims, baseline PR
  creation claims, Mythic Edge mutation claims, and readiness/truth/assurance
  claims.

Validation evidence must be public-safe and committed only if a later issue
authorizes that artifact. Runtime or private evidence must remain out of scope.

## Example Candidate Row

```yaml
candidate: "corpus_public_safe_dry_run_orchestrator"
candidate_surface_class: "public_safe_dry_run_surface"
secondary_surface_classes:
  - "test_surface"
current_path: "tools/corpus_public_safe_dry_run.py"
current_behavior: "Composes the public-safe Corpus dry-run stages without external actions."
truth_or_authority_owner: "Corpus public-safe automation; not Mythic Edge parser truth."
upstream_dependencies:
  - "package preview"
  - "PR package-safety validation"
  - "release dry-run metadata"
  - "dispatch no-send validation"
  - "ratchet report construction from supplied safe inputs"
  - "baseline proposal preview"
downstream_consumers:
  - "tests/test_corpus_public_safe_dry_run.py"
  - "docs/contract_test_reports/corpus_public_safe_end_to_end_dry_run.md"
public_safe_inputs:
  - "committed Corpus metadata"
  - "committed public-safe tool outputs"
forbidden_inputs:
  - "raw private logs"
  - "private paths"
  - "package artifacts"
  - "dispatch sends"
  - "ratchet execution outputs"
proposed_destination: "same_path"
why_not_keep_local: "Not applicable because the recommended decision is keep_local."
why_not_move_to_existing_repo: "The behavior is Corpus-specific public-safe orchestration and does not belong to Mythic Edge parser truth."
why_not_new_repo: "The boundary is not independently useful outside Corpus."
new_public_interface_needed: false
new_public_interface_description: "none"
corpus_public_safe_boundary: "No package publish, dispatch send, ratchet execution, baseline mutation, or Mythic Edge mutation."
ars_refactor_evidence_status:
  prior_evidence_found: false
  reviewed_repository: "none"
  reviewed_scope: "none"
  reviewed_commit: "none"
  evidence_artifact: "none"
  evidence_tooling: "none"
  current_target_commit: "<target-commit>"
  relevant_changes_since_review: "unknown"
  evidence_status: "absent"
  fresh_evidence_needed: false
  reason: "Same-repo keep-local decision can be reviewed from committed public-safe Corpus artifacts."
behavior_preservation_tests:
  - "python3 -m unittest tests/test_corpus_public_safe_dry_run.py"
  - "python3 -m json.tool corpus/manifest.v1.json >/dev/null"
rollback_plan: "Revert the later same-repo change; no external artifacts should exist."
final_decision: "keep_local"
decision_reason: "No extraction boundary is proven."
owner_acceptance_ref: "Codex E review or human approval of the packet as planning evidence only."
next_authority_required: "Separate implementation issue or explicit handoff with implementation_authorized true before Codex C."
non_claims:
  - "not_corpus_readiness"
  - "not_parser_truth"
  - "not_release_readiness"
```

## Validation Requirements For Codex E

Codex E should review whether this contract:

- includes all required Phase 5 packet fields from roadmap #568;
- preserves same-repo-first decomposition;
- separates Corpus public-safe automation authority from Mythic Edge parser
  truth and source-repo mutation authority;
- prevents ARS/refactor evidence from becoming execution, inspection, or
  readiness authority;
- blocks implementation, file moves, publishing, dispatch, ratchets, baseline
  PRs, Mythic Edge mutation, private reads, and readiness/truth/assurance
  claims;
- requires a separate later implementation authority before Codex C;
- requires a complete false-authority envelope for every protected Corpus,
  Mythic Edge, readiness, truth, and assurance flag in this lane.

Suggested validation for this Codex B artifact:

```bash
git diff --check
python3 - <<'PY'
from pathlib import Path
path = Path("docs/contracts/corpus_phase_5_decomposition_decision_packet.md")
data = path.read_text()
data.encode("ascii")
required = [
    "candidate_surface_class",
    "truth_or_authority_owner",
    "why_not_keep_local",
    "why_not_move_to_existing_repo",
    "behavior_preservation_tests",
    "rollback_plan",
    "final_decision",
    "ars_refactor_evidence_status",
    "implementation_authority",
    "next_authority_required",
    "decision_packet_authorizes_codex_c",
    "private_log_read_authorized",
    "corpus_readiness_claimed",
]
missing = [item for item in required if item not in data]
if missing:
    raise SystemExit(f"missing required terms: {missing}")
PY
```

## Recommended Next Role

Codex E: review this contract against issue #29, tracker #13, and roadmap #568.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge-Corpus issue #29.

Repository:
Tahjali11/Mythic-Edge-Corpus

Issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/29

Related completed tracker:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13

Related project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Contract artifact:
docs/contracts/corpus_phase_5_decomposition_decision_packet.md

Goal:
Review the Corpus Phase 5 decomposition decision packet contract. Lead with
findings ordered by severity. Confirm whether the contract includes required
decision-packet fields, preserves same-repo-first decomposition, separates
Corpus public-safe automation authority from Mythic Edge parser truth/source
mutation authority, treats ARS/refactor evidence as advisory only, and blocks
implementation, file moves, package publishing, release/package artifacts,
repository_dispatch, ratchets, baseline PRs, Mythic Edge mutation, raw
corpus/private file import, private-log reads, and readiness/truth/assurance
claims. Confirm that CORPUS-PHASE5-E-001 and CORPUS-PHASE5-E-002 are fixed:
the packet must not authorize Codex C or implementation, and the required
false-authority envelope must cover all protected false/not-claimed flags.

Protected boundaries:
Do not implement code, move files, publish packages, create release/package
artifacts, send repository_dispatch, run ratchets, open baseline PRs, mutate
Mythic Edge, import raw corpus/private files, read private logs, or claim
parser/corpus/readiness/truth/assurance.

Suggested validation:
- git diff --check
- focused public-artifact scan for private paths, raw logs, secrets, generated
  local artifacts, package publish claims, dispatch send claims, ratchet
  execution claims, baseline PR creation claims, Mythic Edge mutation claims,
  and readiness/truth/assurance claims

Expected output:
- Findings, if any
- Validation run
- Recommended next role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge-Corpus"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge-Corpus"
  issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/29"
  related_completed_tracker: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13"
  related_project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "E"
  verdict: "corpus_phase_5_decomposition_decision_packet_contract_reconciled_ready_for_review"
  risk_tier: "High"
  target_artifact: "docs/contracts/corpus_phase_5_decomposition_decision_packet.md"
  fixed_findings:
    - "CORPUS-PHASE5-E-001"
    - "CORPUS-PHASE5-E-002"
  implementation_authorized: false
  file_move_authorized: false
  cross_repo_extraction_authorized: false
  pr_creation_authorized: false
  package_publishing_authorized: false
  package_artifact_creation_authorized: false
  release_asset_creation_authorized: false
  repository_dispatch_authorized: false
  ratchet_execution_authorized: false
  baseline_pr_creation_authorized: false
  baseline_mutation_authorized: false
  mythic_edge_mutation_authorized: false
  raw_corpus_import_authorized: false
  private_log_read_authorized: false
  private_path_read_authorized: false
  parser_behavior_change_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  parser_truth_claimed: false
  fixture_promotion_claimed: false
  baseline_approval_claimed: false
  corpus_readiness_claimed: false
  release_readiness_claimed: false
  deploy_readiness_claimed: false
  production_readiness_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  analytics_truth_claimed: false
  ai_truth_claimed: false
  coaching_truth_claimed: false
  validation:
    - "git diff --check"
    - "ascii and required-term scan"
    - "focused public-artifact scan"
```
