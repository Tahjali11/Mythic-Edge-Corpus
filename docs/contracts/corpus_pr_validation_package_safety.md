# Corpus PR Validation Package Safety Contract

## Module

`corpus_pr_validation_package_safety`

Plain English: this contract defines a future PR validation package-safety
boundary for `Tahjali11/Mythic-Edge-Corpus`. The validation layer should check
proposed corpus changes before they are reviewed or merged. It should fail
closed when package previews, manifest/session metadata checks, path safety, or
forbidden-content scans fail.

The PR validation layer is a package hygiene and review-safety gate. It is not
parser truth, not fixture promotion, not corpus readiness, not release
readiness, not production readiness, not ratchet success, not baseline approval,
not analytics truth, not AI truth, not coaching truth, not security assurance,
and not privacy assurance.

This Codex B pass writes only this contract. It does not implement PR
validation, run package previews, create validation artifacts, publish packages,
create releases, dispatch events, run ratchets, open baseline PRs, import corpus
files, copy raw evidence, read private logs, or mutate `Tahjali11/Mythic-Edge`.

## Source Artifact

- Repository: `Tahjali11/Mythic-Edge-Corpus`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge-Corpus`
- Issue: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/2
- Related Mythic Edge tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Previous issue:
  https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/1
- Previous PR: https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/7
- Previous merge commit:
  `b28ad5e25e05f20846938340350205ad65e504ef`
- Base branch: `main`
- Working branch:
  `codex/corpus-pr-validation-package-safety-2`
- Target artifact:
  `docs/contracts/corpus_pr_validation_package_safety.md`
- Risk tier: High

Observed during this Codex B pass:

- The operating checkout remote matched
  `https://github.com/Tahjali11/Mythic-Edge-Corpus.git`.
- The checkout started clean on `main`.
- `origin/main` was verified at
  `b28ad5e25e05f20846938340350205ad65e504ef`.
- Work was moved to
  `codex/corpus-pr-validation-package-safety-2`, tracking `origin/main`.
- Issue #2 was open.
- Issue #1 was closed after PR #7 merged the local package preview command
  contract.
- The repository currently contains `README.md`, `LICENSE`, and the issue #1
  contract.
- The local package preview command is still contract-only; it is not
  implemented or executed by this pass.
- No `Tahjali11/Mythic-Edge` worktree files were inspected or mutated by this
  pass.

Current authorization facts to preserve:

```yaml
implementation_authorized: false
pr_validation_contract_authorized: true
pr_validation_implementation_authorized: false
pr_validation_execution_authorized: false
package_preview_execution_authorized: false
validation_artifact_creation_authorized: false
release_publishing_authorized: false
repository_dispatch_authorized: false
ratchet_execution_authorized: false
baseline_pr_creation_authorized: false
raw_corpus_import_authorized: false
private_log_read_authorized: false
mythic_edge_mutation_authorized: false
parser_truth_claimed: false
fixture_promotion_claimed: false
corpus_readiness_claimed: false
release_readiness_claimed: false
production_readiness_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
```

## Source Artifacts Inspected

- Corpus issue #2
- Corpus issue #1
- Corpus issue #1 deployer closeout comment
- `README.md`
- `LICENSE`
- `docs/contracts/corpus_local_package_preview_command.md`

No raw corpus files, private logs, generated local artifacts, private reports,
package artifacts, release assets, dispatch payloads, ratchet outputs, baseline
PR artifacts, or `Tahjali11/Mythic-Edge` source files were read, created,
copied, mirrored, summarized, or committed.

## Observed Current Behavior

The corpus repo is still a bootstrap repository. It has:

- a README;
- a license;
- a contract for a future local package preview command.

It does not yet have:

- a corpus package manifest;
- a session ledger;
- package metadata;
- package preview tooling;
- PR validation tooling;
- package safety validation;
- release publishing automation;
- `repository_dispatch` automation;
- ratchet comparison automation;
- baseline PR automation.

The issue #1 contract defines a future local/report-only preview command. Issue
#2 is the next safety layer: PR validation that can run that preview command and
additional package-safety checks when implementation is separately authorized.

Because the preview command is still contract-only at the time of this pass,
future PR validation must treat the missing command as a blocked dependency
until a later implementation issue lands it.

## Problem

Corpus PRs need deterministic safety checks before any release workflow can be
trusted. Without a PR validation boundary, a contributor branch could propose
package changes that:

- omit required manifest or session-ledger metadata;
- include files not declared by repo-owned metadata;
- include package files outside the package root;
- include raw/private/generated/runtime artifacts;
- include release artifacts, dispatch payloads, ratchet outputs, or baseline
  PR artifacts;
- include unsafe path forms;
- drift from the local package preview contract;
- appear merge-ready or release-ready before downstream gates exist.

The first bad value is any PR validation status, package preview result,
manifest/session metadata check, file inventory, safety scan, status check,
workflow summary, reviewer note, or future check-run output being treated as
parser truth, fixture promotion, corpus readiness, release readiness, ratchet
success, baseline approval, production readiness, analytics truth, AI truth,
coaching truth, security assurance, or privacy assurance.

The second bad value is any PR validation layer that rewrites contributor
branches, auto-sanitizes unsafe files, pushes fixes, creates baseline PRs,
publishes packages, dispatches events, runs parser ratchets, or mutates
`Tahjali11/Mythic-Edge`.

## Scope Decision

This contract approves a contract-only PR validation package-safety boundary.

Codex C implementation is not automatically authorized by this contract. A
later Codex C pass may proceed only if a user or lifecycle handoff explicitly
authorizes PR validation tooling, package-safety tests, and any workflow files.

If later authorized, the narrow Codex C implementation surface may include:

- a package-safety validator under `tools/`;
- focused tests under `tests/`;
- tiny public-safe bootstrap metadata fixtures, if separately authorized;
- a local validation entrypoint for PR checks;
- a GitHub Actions workflow only if the implementation handoff explicitly
  authorizes CI wiring for PR validation.

This contract defines:

- future PR validation purpose;
- future PR validation command surface;
- relationship to the local package preview command;
- allowed inputs;
- forbidden inputs;
- package inventory checks;
- manifest/session-ledger checks;
- forbidden file and content checks;
- fail-closed status vocabulary;
- contributor/reviewer output requirements;
- no-write and no-auto-sanitization boundaries;
- downstream issue separation;
- validation expectations for later Codex C and Codex E.

This contract does not authorize:

- code implementation in Codex B;
- PR validation execution;
- package preview execution;
- durable validation artifact creation;
- GitHub Actions workflow creation;
- status check creation;
- package artifact creation;
- release publishing;
- `repository_dispatch`;
- ratchet comparison;
- baseline PR creation;
- raw corpus import;
- raw/private evidence reads;
- package upload;
- GitHub release creation;
- automatic contributor-branch rewrite;
- automatic safe-file rewrite;
- GitHub issue or PR creation;
- mutation of `Tahjali11/Mythic-Edge`;
- parser behavior changes;
- corpus readiness, release readiness, production readiness, analytics truth,
  AI truth, coaching truth, security assurance, or privacy assurance claims.

## Owning Layer And Truth Boundary

Owner: `Tahjali11/Mythic-Edge-Corpus`, PR validation and package-safety
boundary.

Truth boundary:

- Mythic Edge parser/state remains the owner for parser interpretation,
  parser events, match/game identity, deduplication, and final reconciliation.
- Mythic Edge evidence-pipeline contracts own harvest, review, confidence, and
  corpus metadata diff semantics.
- The issue #1 local package preview boundary owns local/report-only package
  preview semantics.
- This issue #2 boundary owns PR validation package-safety semantics.
- Later corpus issues separately own release publishing, dispatch, ratchet, and
  baseline PR proposal automation.

PR validation may say:

- the proposed package preview passed or failed package-safety checks;
- manifest/session metadata is present, missing, malformed, or inconsistent;
- proposed files are declared, undeclared, unsupported, unsafe, or blocked;
- a contributor/reviewer must take manual action.

PR validation must not say:

- parser interpretation is correct;
- fixtures should be promoted;
- corpus metadata should move into Mythic Edge;
- a release should be published;
- a dispatch should be sent;
- a ratchet passed;
- a baseline PR should be opened;
- a package is production-ready.

Required future data flow:

```text
reviewed public-safe corpus PR
  -> local package preview command
  -> PR validation package-safety checks
  -> human review
  -> later release publishing issue
  -> later repository_dispatch issue
  -> later ratchet comparison issue
  -> later baseline PR issue
```

Forbidden shortcut:

```text
PR validation
  -/-> parser truth
  -/-> fixture promotion
  -/-> corpus readiness
  -/-> release publishing
  -/-> repository_dispatch
  -/-> ratchet success
  -/-> baseline approval
  -/-> production readiness
```

## Future PR Validation Surface

Recommended future local validation command:

```bash
python3 tools/corpus_pr_validate_package_safety.py \
  --base-ref origin/main \
  --head-ref HEAD \
  --package-root corpus \
  --manifest corpus/manifest.v1.json \
  --session-ledger corpus/session_ledger.v1.json
```

Recommended future PR workflow shape, if separately authorized:

- checkout PR head safely;
- fetch the base branch without force pushing or mutating the contributor
  branch;
- run the local package preview command;
- run package inventory checks;
- run manifest/session-ledger consistency checks;
- run path and file-class checks;
- run forbidden marker checks;
- print a deterministic summary;
- exit nonzero on blocked, invalid, unsafe, inconsistent, unsupported, or
  review-required package state.

V1 behavior:

- output should be stdout/check-summary only;
- no files should be written by default;
- validation must be deterministic for the same checkout and inputs;
- validation must use repo-relative paths only;
- validation must not follow paths outside the repository;
- validation must not auto-sanitize, delete, rewrite, or push contributor
  changes;
- validation must not create package archives, release assets, dispatch
  payloads, ratchet reports, or baseline PR artifacts.

If a later implementation wants durable report artifacts, check-run annotations,
autofix suggestions, or workflow file creation, it requires explicit issue and
contract authority.

## Allowed Input Classes

PR validation may inspect only committed, public-safe, repo-owned inputs in the
PR checkout:

- corpus package manifest metadata;
- session ledger metadata;
- package root inventory;
- package README or package notes;
- license and attribution metadata;
- reviewed public-safe sanitized fixtures, if they exist in this repo and are
  declared by manifest/session metadata;
- schema files or validation metadata committed to this repo;
- package configuration committed to this repo;
- output from the local package preview command, once that command exists.

The validator may read included public-safe text/JSON files only after path and
extension allowlist checks pass. If content scanning finds forbidden markers,
validation must report symbolic failure categories without echoing unsafe
content.

## Forbidden Input Classes

PR validation must not inspect, import, copy, mirror, summarize, hash, or
commit:

- raw corpus evidence;
- raw Arena log files;
- compressed raw logs;
- private local logs;
- app-data;
- live MTGA data;
- generated local artifacts;
- private reports;
- private strategy notes;
- private decklists;
- secret or connection material;
- local environment files;
- SQLite databases;
- workbook exports;
- runtime status files;
- failed posts;
- release assets;
- package archives;
- dispatch payloads;
- ratchet reports;
- baseline PR artifacts;
- source files from `Tahjali11/Mythic-Edge`;
- external corpus contents.

If a forbidden input is discovered, validation must fail closed and must not
include raw values, raw paths outside the repo, raw payloads, hashes, or
snippets in output.

## Package Preview Dependency

The issue #1 local package preview command is a required dependency for full PR
validation. Future PR validation must handle preview states explicitly:

- `preview_missing`: preview command is absent.
- `preview_failed`: preview command exited nonzero.
- `preview_invalid_output`: preview output is malformed.
- `preview_blocked`: preview reported a blocked package state.
- `preview_passed`: preview reported a local/report-only package preview that
  can be consumed by PR validation.

Rules:

- `preview_missing`, `preview_failed`, `preview_invalid_output`, and
  `preview_blocked` must fail PR validation.
- `preview_passed` is necessary but not sufficient for PR validation success.
- Preview output must not be treated as parser truth, corpus readiness, release
  readiness, or fixture-promotion approval.

## Manifest And Session Ledger Checks

Future PR validation should verify:

- manifest file exists;
- session ledger file exists;
- manifest schema version is explicit;
- session ledger schema version is explicit;
- package ID and package version are explicit;
- every included package file is declared by the manifest;
- every session-backed corpus file has a ledger entry;
- every included ledger entry maps to at least one manifest entry;
- declared files exist on disk;
- undeclared files under package root are blocked unless explicitly allowed by
  a later contract;
- duplicate entries are blocked;
- stale, unsupported, conflicting, or malformed entries fail closed.

These checks are metadata consistency checks only. They do not decide whether
parser interpretation is correct.

## Package Inventory And Path Safety Checks

Future PR validation should verify:

- sort paths lexicographically by normalized repo-relative path;
- normalize path separators to `/`;
- reject absolute paths;
- reject path traversal;
- reject symlinks that leave the repository;
- reject ignored/generated/runtime/cache paths;
- reject hidden local metadata unless explicitly allowed by a later contract;
- reject binary or archive suffixes unless explicitly allowed by a later
  package-format contract;
- reject undeclared files under the package root;
- reject declared files missing from disk;
- reject package files outside the package root;
- reject package roots outside the repository;
- reject changed files that imply release, dispatch, ratchet, or baseline PR
  artifacts.

V1 should avoid content digests in public output unless a later contract
requires them. If a later implementation computes digests internally for
safety, it must never digest forbidden/raw/private files and must not treat a
digest as content approval.

## Forbidden Marker And File-Class Checks

Future PR validation should fail closed on:

- raw/private log markers;
- compressed raw log suffixes;
- generated runtime/cache paths;
- local-only machine artifact paths;
- credential-shaped content;
- workbook export suffixes;
- local database suffixes;
- package archive suffixes;
- release asset markers;
- dispatch payload markers;
- ratchet report markers;
- baseline PR artifact markers;
- source-repo paths or copied source snippets;
- external corpus references that imply copied raw content.

Validation output must use symbolic reason codes. It must not echo raw unsafe
content, private paths, local machine paths, copied payloads, or secret-shaped
values.

## Output Shape

Text output should include:

- repository;
- base ref;
- head ref;
- package root;
- manifest path;
- session ledger path;
- package preview status;
- total changed package files;
- total included files;
- total manifest entries;
- total session ledger entries;
- top-level validation status;
- safety-check summary;
- deterministic inventory summary;
- blocked or review-required reason codes;
- explicit non-claims.

JSON output, if supported later, should include:

```yaml
object: corpus_pr_validation_package_safety
schema_version: corpus_pr_validation_package_safety.v1
repository: Tahjali11/Mythic-Edge-Corpus
repository_url: https://github.com/Tahjali11/Mythic-Edge-Corpus
base_ref: string
head_ref: string
package_root: string
manifest_ref: object
session_ledger_ref: object
package_preview_ref: object
status: string
changed_package_files: list
inventory_summary: object
manifest_session_summary: object
safety_checks: list
blocked_reason_codes: list
review_notes: list
non_claims: list
```

Output must not include raw corpus payloads, raw private content, local absolute
paths, secret-shaped content, private logs, generated local artifacts, package
archives, release upload metadata, dispatch payloads, ratchet results, or
baseline PR payloads.

## Status Vocabulary

PR validation status values:

- `contract_only`: contract exists, but implementation is not authorized.
- `validation_ready`: validator exists and can run locally.
- `validation_report_only`: validation can report locally or in PR checks, but
  no artifact writes are authorized.
- `passed_report_only`: package-safety validation passed as hygiene evidence
  only.
- `blocked_missing_preview_command`: required preview command is absent.
- `blocked_preview_failed`: preview command failed.
- `blocked_preview_invalid_output`: preview output is malformed.
- `blocked_missing_manifest`: required manifest is absent.
- `blocked_missing_session_ledger`: required session ledger is absent.
- `blocked_invalid_metadata`: manifest or ledger is malformed.
- `blocked_manifest_ledger_mismatch`: manifest and ledger relationships do not
  reconcile.
- `blocked_unsafe_path`: unsafe path form was discovered.
- `blocked_forbidden_content`: forbidden content markers were discovered.
- `blocked_raw_or_private_input`: raw corpus, private, generated, external, or
  source-repo input was discovered.
- `blocked_package_artifact`: package archive, release asset, dispatch payload,
  ratchet report, or baseline PR artifact was discovered in scope.
- `blocked_auto_sanitization_required`: the PR would require a rewrite or
  sanitization step that V1 must not perform.
- `review_required`: a human reviewer must inspect an ambiguous package state.
- `unsupported`: requested validation mode is outside this contract.
- `invalid`: required fields are missing, contradictory, or unsafe.

For issue #2 during Codex B, the only current status is `contract_only`.

## Safety Check Vocabulary

Safety checks should include:

- `preview_command_required`
- `repo_relative_paths_only`
- `no_path_traversal`
- `package_root_only`
- `manifest_declared_files_only`
- `session_ledger_reconciled`
- `changed_files_reviewed`
- `no_raw_corpus_evidence`
- `no_private_logs`
- `no_generated_local_artifacts`
- `no_secret_or_connection_material`
- `no_release_artifacts`
- `no_dispatch_payloads`
- `no_ratchet_reports`
- `no_baseline_pr_artifacts`
- `no_source_repo_files`
- `no_external_corpus_contents`
- `no_auto_sanitization`
- `no_contributor_branch_writeback`
- `report_only_non_claims_present`

Safety checks are hygiene evidence only. They are not security assurance or
privacy assurance.

## No-Write And No-Auto-Sanitization Rules

V1 PR validation must be no-write by default:

- do not modify contributor files;
- do not delete unsafe files;
- do not generate replacement safe files;
- do not push commits;
- do not update PR branches;
- do not upload package archives;
- do not write durable validation artifacts unless separately authorized;
- do not open issues or PRs;
- do not add labels, comments, reviews, or status checks unless a later
  implementation contract explicitly authorizes that GitHub surface.

When unsafe content is found, the validator should fail with symbolic,
reviewable reason codes and leave the human contributor/reviewer to make the
next scoped change.

## Downstream Issue Separation

Issue #2 must remain separate from:

- #3 release publishing for reviewed corpus packages;
- #4 `repository_dispatch` into Mythic Edge;
- #5 ratchet comparison for corpus releases;
- #6 auto-open baseline PR workflow after ratchet comparison.

PR validation may produce hygiene evidence that later issues consume, but it
must not implement those downstream capabilities or imply that they are ready.

## Validation Requirements For Later Codex C

If later authorized, Codex C should add focused tests for:

- missing preview command;
- preview command failure;
- malformed preview output;
- missing manifest;
- missing session ledger;
- malformed manifest;
- malformed session ledger;
- manifest entry missing from disk;
- file on disk missing from manifest;
- manifest/session ledger mismatch;
- path traversal;
- absolute path;
- generated/runtime/cache path;
- forbidden raw/private marker;
- package archive/release asset in scope;
- dispatch payload in scope;
- ratchet report in scope;
- baseline PR artifact in scope;
- contributor-branch writeback is not attempted;
- deterministic ordering;
- text output non-claims;
- JSON output shape, if implemented.

Recommended future validation commands:

```bash
python3 -m pytest -q tests/test_corpus_pr_validation_package_safety.py
python3 tools/corpus_pr_validate_package_safety.py --base-ref origin/main --head-ref HEAD --package-root corpus --manifest corpus/manifest.v1.json --session-ledger corpus/session_ledger.v1.json
git diff --check
```

Those commands are future implementation validation only. They are not
authorized by this Codex B pass.

## Validation Requirements For Codex E

Codex E should review:

- whether this contract preserves issue #1's local/report-only preview boundary;
- whether PR validation fails closed when the preview command is missing,
  failed, blocked, or malformed;
- whether forbidden input classes are broad enough for private/raw corpus
  safety;
- whether manifest/session-ledger ownership is clear;
- whether output avoids raw unsafe content and local absolute paths;
- whether no-write/no-auto-sanitization behavior is explicit;
- whether downstream issues #3 through #6 remain separate;
- whether the contract avoids parser truth, fixture promotion, corpus
  readiness, release readiness, ratchet success, baseline approval, production
  readiness, security assurance, and privacy assurance claims.

## Protected Surfaces And Non-Claims

This contract does not authorize:

- code implementation;
- PR creation;
- issue closure;
- PR validation execution;
- package preview execution;
- GitHub Actions workflow creation;
- durable validation report writes;
- status check creation;
- corpus package publication;
- release creation;
- `repository_dispatch`;
- ratchet comparison;
- baseline PR creation;
- package artifact writes;
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
- production readiness;
- ratchet success;
- baseline approval;
- analytics truth;
- AI truth;
- coaching truth;
- security assurance;
- privacy assurance.

## Recommended Next Role

Codex E should review this contract before Codex C implementation is
considered. If Codex E finds it clean, route to Codex F/G for docs-only
submission and merge. Codex C should not start unless a later handoff
explicitly authorizes implementation of PR validation tooling, package-safety
tests, and any CI/check-run surface.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Corpus issue #2.

Repository:
Tahjali11/Mythic-Edge-Corpus

Repository URL:
https://github.com/Tahjali11/Mythic-Edge-Corpus

Issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/2

Related Mythic Edge tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Previous issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/1

Contract artifact:
docs/contracts/corpus_pr_validation_package_safety.md

Goal:
Review the PR validation package-safety contract. Lead with findings, if any.
Verify that the contract preserves the issue #1 local preview dependency,
fails closed on unsafe package states, forbids raw/private/generated/runtime
artifacts, forbids auto-sanitization and contributor-branch writeback, keeps
release publishing / repository_dispatch / ratchets / baseline PR automation
out of scope, and does not claim parser truth, fixture promotion, corpus
readiness, release readiness, production readiness, security assurance, or
privacy assurance.

Do not implement code.
Do not open a PR.
Do not close issue #2.
Do not publish packages, create releases, dispatch events, run ratchets, open
baseline PRs, import raw corpus data, read private logs, or mutate
Tahjali11/Mythic-Edge.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge-Corpus"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge-Corpus"
  issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/2"
  related_mythic_edge_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/1"
  completed_thread: "B"
  next_thread: "E"
  verdict: "corpus_pr_validation_package_safety_contract_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  branch: "codex/corpus-pr-validation-package-safety-2"
  target_artifact: "docs/contracts/corpus_pr_validation_package_safety.md"
  latest_verified_commit: "b28ad5e25e05f20846938340350205ad65e504ef"
  implementation_authorized: false
  pr_validation_implementation_authorized: false
  pr_validation_execution_authorized: false
  package_preview_execution_authorized: false
  validation_artifact_creation_authorized: false
  release_publishing_authorized: false
  repository_dispatch_authorized: false
  ratchet_execution_authorized: false
  baseline_pr_creation_authorized: false
  raw_corpus_import_authorized: false
  private_log_read_authorized: false
  mythic_edge_mutation_authorized: false
  parser_truth_claimed: false
  fixture_promotion_claimed: false
  corpus_readiness_claimed: false
  release_readiness_claimed: false
  production_readiness_claimed: false
  next_recommended_role: "Codex E"
  stop_conditions:
    - "Do not implement code from this contract without a later accepted review and explicit implementation handoff."
    - "Do not open a PR in Codex B."
    - "Do not close issue #2."
    - "Do not mutate Tahjali11/Mythic-Edge."
    - "Do not publish corpus packages, create releases, dispatch events, run ratchets, or open baseline PRs."
    - "Do not import, copy, mirror, or commit raw corpus/private files."
    - "Do not read private logs, secret or connection material, generated local artifacts, or private reports."
    - "Do not claim parser truth, fixture promotion, corpus readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, security assurance, or privacy assurance."
```
