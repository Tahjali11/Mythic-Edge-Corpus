# Corpus Local Package Preview Command Contract

## Module

`corpus_local_package_preview_command`

Plain English: this contract defines a future local-only preview command for
`Tahjali11/Mythic-Edge-Corpus`. The command should show what a reviewed corpus
package would contain before PR validation, release publishing,
`repository_dispatch`, ratchet comparison, or baseline PR automation exists.

The preview command is a packaging and safety report. It is not parser truth,
not corpus readiness, not release readiness, not production readiness, not a
ratchet result, not fixture promotion, not analytics truth, not AI truth, not
coaching truth, not security assurance, and not privacy assurance.

This Codex B pass writes only this contract. It does not implement the command,
publish packages, create releases, dispatch events, run ratchets, open baseline
PRs, import corpus files, copy raw evidence, read private logs, or mutate
`Tahjali11/Mythic-Edge`.

## Source Artifact

- Repository: `Tahjali11/Mythic-Edge-Corpus`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge-Corpus`
- Issue: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/1
- Related Mythic Edge tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Related Mythic Edge gate issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/560
- Related Mythic Edge gate PR:
  https://github.com/Tahjali11/Mythic-Edge/pull/565
- Related gate merge commit:
  `1ad427447c595550c4d9679941e01b371577dab9`
- Base branch: `main`
- Working branch: `codex/corpus-local-package-preview-contract-1`
- Target artifact:
  `docs/contracts/corpus_local_package_preview_command.md`
- Risk tier: High

Observed during this Codex B pass:

- No local checkout for `Tahjali11/Mythic-Edge-Corpus` existed under the
  workspace at the start of the pass.
- A fresh local checkout of only `Tahjali11/Mythic-Edge-Corpus` was created.
- The operating checkout remote matched
  `https://github.com/Tahjali11/Mythic-Edge-Corpus.git`.
- The corpus repo `main` branch was at initial commit `41211c2`.
- Issue #1 was open.
- Corpus issues #2 through #6 were open.
- No open corpus PRs were present.
- The repo currently contained only `README.md` and `LICENSE`.
- No repo-local `AGENTS.md`, workflow docs, manifest, session ledger, package
  metadata, tools, tests, fixtures, or contracts existed before this pass.
- The related Mythic Edge gate issue #560 was closed and PR #565 was merged,
  but that gate contract says corpus automation readiness remains blocked
  until the corpus issue queue is completed and verified.

Current authorization facts to preserve:

```yaml
implementation_authorized: false
package_preview_contract_authorized: true
package_preview_command_implementation_authorized: false
package_preview_execution_authorized: false
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
security_assurance_claimed: false
privacy_assurance_claimed: false
```

## Source Artifacts Inspected

- Corpus issue #1
- Corpus tracker queue issues #2 through #6
- Related Mythic Edge tracker #388
- Related Mythic Edge gate issue #560
- Related Mythic Edge gate PR #565 metadata
- `docs/contracts/parser_evidence_corpus_automation_readiness_gate.md` from
  Mythic Edge merge commit `1ad427447c595550c4d9679941e01b371577dab9`
- Corpus repo `README.md`
- Corpus repo `LICENSE`

No `Tahjali11/Mythic-Edge` worktree files were mutated. No raw corpus files,
private logs, generated local artifacts, secrets, private reports, release
assets, package artifacts, ratchet outputs, or baseline PR artifacts were read,
created, copied, mirrored, summarized, or committed.

## Observed Current Behavior

The corpus repo is currently a bootstrap repository. It has a README and
license, but it does not yet have:

- a corpus package manifest;
- a session ledger;
- package metadata;
- package preview tooling;
- package safety validation;
- release publishing automation;
- `repository_dispatch` automation;
- ratchet comparison automation;
- baseline PR automation.

The related Mythic Edge gate contract says the cross-repo corpus automation
readiness gate is not cleared. Issue #1 is the first corpus-side capability:
a local preview command that reports what a package would contain without
publishing, dispatching, ratcheting, or proposing baseline changes.

## Problem

The first bad value is treating a future corpus package, manifest, session
ledger, preview summary, or local command output as parser truth, corpus
readiness, release readiness, fixture promotion, ratchet success, baseline
approval, production readiness, analytics truth, AI truth, coaching truth,
security assurance, or privacy assurance.

The second bad value is allowing a package preview to read, copy, summarize, or
include raw corpus evidence, private logs, generated local artifacts, secrets,
private reports, source-repo files, release artifacts, ratchet outputs, or
baseline PR artifacts.

Without a preview command, later release workflows could package the wrong
files, omit reviewed metadata, include unsafe artifacts, or drift from the
repo-owned manifest/session ledger. With a preview command that overclaims,
the corpus repo could accidentally look release-ready before PR validation,
publishing, dispatch, ratchet, and baseline proposal gates exist.

## Scope Decision

This contract approves a contract-only local package preview boundary.

Codex C implementation is not automatically authorized by this contract. A
later Codex C pass may proceed only if a user or lifecycle handoff explicitly
authorizes a local preview command, bootstrap metadata fixtures, and tests.

If later authorized, the narrow Codex C implementation surface is:

- `tools/corpus_package_preview.py`
- `tests/test_corpus_package_preview.py`
- public-safe bootstrap metadata fixtures under a reviewed corpus metadata
  path, if the implementation contract authorizes them
- optional README text documenting the local-only command

This contract defines:

- future command purpose;
- future command surface;
- allowed input classes;
- forbidden input classes;
- expected manifest/session-ledger relationship;
- deterministic local output shape;
- fail-closed status vocabulary;
- package safety checks;
- local/report-only boundaries;
- downstream issue separation;
- validation expectations for later Codex C and Codex E.

This contract does not authorize:

- code implementation in Codex B;
- package preview execution;
- package artifact creation;
- release publishing;
- `repository_dispatch`;
- ratchet comparison;
- baseline PR creation;
- raw corpus import;
- raw/private evidence reads;
- package upload;
- GitHub release creation;
- GitHub issue or PR creation;
- mutation of `Tahjali11/Mythic-Edge`;
- parser behavior changes;
- corpus readiness, release readiness, production readiness, analytics truth,
  AI truth, coaching truth, security assurance, or privacy assurance claims.

## Owning Layer And Truth Boundary

Owner: `Tahjali11/Mythic-Edge-Corpus`, Corpus / Provenance packaging boundary.

Truth boundary:

- Mythic Edge parser/state remains the owner for parser interpretation,
  parser events, match/game identity, deduplication, and final reconciliation.
- Mythic Edge evidence-pipeline contracts own harvest, review, confidence, and
  corpus metadata diff semantics.
- Mythic-Edge-Corpus owns package preview, package validation, release,
  dispatch, ratchet, and baseline proposal automation after each capability is
  separately contracted and implemented.
- The local package preview command may report whether committed public-safe
  corpus metadata and package candidates are internally consistent.
- The preview command must not approve parser truth, fixture promotion, corpus
  metadata movement, release readiness, ratchet success, or baseline changes.

Required future data flow:

```text
reviewed public-safe corpus metadata
  -> local package preview
  -> later PR validation
  -> later reviewed release publishing
  -> later bounded repository_dispatch
  -> later ratchet comparison
  -> later baseline PR proposal
```

Forbidden shortcut:

```text
local package preview
  -/-> corpus readiness
  -/-> parser truth
  -/-> fixture promotion
  -/-> release publishing
  -/-> repository_dispatch
  -/-> ratchet success
  -/-> baseline PR approval
  -/-> production readiness
```

## Future Command Surface

Recommended future command:

```bash
python3 tools/corpus_package_preview.py \
  --package-root corpus \
  --manifest corpus/manifest.v1.json \
  --session-ledger corpus/session_ledger.v1.json \
  --format text
```

Optional future JSON output may be supported:

```bash
python3 tools/corpus_package_preview.py \
  --package-root corpus \
  --manifest corpus/manifest.v1.json \
  --session-ledger corpus/session_ledger.v1.json \
  --format json
```

V1 behavior:

- output goes to stdout only;
- no files are written by default;
- command exits nonzero on blocked, unsafe, invalid, missing, stale, or
  inconsistent package state;
- command is deterministic for the same checkout and inputs;
- command uses repo-relative paths only;
- command never follows paths outside the repository;
- command never reads hidden/private/local-only paths;
- command never creates package archives, release assets, dispatch payloads,
  ratchet reports, or baseline PR artifacts.

If a later implementation wants a `--write-report` mode, it requires a
separate issue and contract.

## Allowed Input Classes

The preview command may inspect only committed, public-safe, repo-owned inputs:

- corpus package manifest metadata;
- session ledger metadata;
- package root inventory;
- package README or package notes;
- license and attribution metadata;
- reviewed public-safe sanitized fixtures, if they exist in this repo and are
  declared by manifest/session metadata;
- schema files or validation metadata committed to this repo;
- package configuration committed to this repo.

The command may read included public-safe text/JSON files only after path and
extension allowlist checks pass. If content scanning finds forbidden markers,
the command must report symbolic failure categories without echoing the unsafe
content.

## Forbidden Input Classes

The preview command must not inspect, import, copy, mirror, summarize, hash, or
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
- secrets, credentials, tokens, API keys, webhook URLs, or environment files;
- SQLite databases;
- workbook exports;
- runtime status files;
- failed posts;
- release assets;
- package archives;
- ratchet reports;
- baseline PR artifacts;
- source files from `Tahjali11/Mythic-Edge`;
- external corpus contents.

If a forbidden input is discovered, the preview command must fail closed and
must not include raw values, raw paths outside the repo, raw payloads, hashes,
or snippets in output.

## Manifest And Session Ledger Relationship

Future metadata should preserve these relationships:

- The package manifest owns package identity, schema version, package version,
  package root, package entries, declared package roles, public-safe status,
  attribution/source refs, and safety policy version.
- The session ledger owns session-level provenance metadata for included
  public-safe corpus entries.
- Every included package file must be declared by the manifest.
- Every session-backed corpus file must have a ledger entry.
- Every ledger entry included in the package must map to at least one manifest
  entry.
- Manifest and ledger schema versions must be explicit.
- Missing, duplicate, undeclared, stale, unsupported, or conflicting entries
  must fail closed.

The preview command may validate that metadata relationships are internally
consistent. It must not decide whether parser interpretation is correct.

## Package Inventory Rules

Future inventory output must be deterministic:

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
- reject package files outside the package root.

V1 should avoid content digests in public output unless a later contract
requires them. If a later implementation computes digests internally for
safety, it must never digest forbidden/raw/private files and must not treat a
digest as content approval.

## Output Shape

Text output should include:

- package ID;
- package schema version;
- manifest path;
- session ledger path;
- package root;
- total included files;
- total declared manifest entries;
- total session ledger entries;
- status;
- safety-check summary;
- deterministic inventory table;
- blocked or review-required reason codes;
- explicit non-claims.

JSON output, if supported, should include:

```yaml
object: corpus_local_package_preview
schema_version: corpus_local_package_preview.v1
repository: Tahjali11/Mythic-Edge-Corpus
repository_url: https://github.com/Tahjali11/Mythic-Edge-Corpus
package_id: string
package_version: string
manifest_ref: object
session_ledger_ref: object
package_root: string
status: string
inventory: list
safety_checks: list
blocked_reason_codes: list
non_claims: list
```

Output must not include raw corpus payloads, raw private content, local
absolute paths, secrets, private logs, generated local artifacts, package
archives, release upload metadata, dispatch payloads, ratchet results, or
baseline PR payloads.

## Status Vocabulary

Preview status values:

- `contract_only`: contract exists, but implementation is not authorized.
- `preview_ready`: public-safe committed metadata is internally consistent and
  can be previewed locally.
- `preview_report_only`: preview can be printed locally, but no artifact write
  is authorized.
- `blocked_missing_manifest`: required manifest is absent.
- `blocked_missing_session_ledger`: required session ledger is absent.
- `blocked_invalid_metadata`: manifest or ledger is malformed.
- `blocked_manifest_ledger_mismatch`: manifest and ledger relationships do not
  reconcile.
- `blocked_unsafe_path`: an absolute, traversal, external, ignored, generated,
  runtime, cache, hidden, or disallowed path was discovered.
- `blocked_forbidden_content`: forbidden content markers were discovered.
- `blocked_raw_or_private_input`: raw corpus, private, generated, external, or
  source-repo input was discovered.
- `blocked_package_artifact`: package archive, release asset, dispatch payload,
  ratchet report, or baseline PR artifact was discovered in scope.
- `review_required`: a human reviewer must inspect an ambiguous package state.
- `unsupported`: requested command mode is outside this contract.
- `invalid`: required fields are missing, contradictory, or unsafe.

For issue #1 during Codex B, the only current status is `contract_only`.

## Safety Check Vocabulary

Safety checks should include:

- `repo_relative_paths_only`
- `no_path_traversal`
- `package_root_only`
- `manifest_declared_files_only`
- `session_ledger_reconciled`
- `no_raw_corpus_evidence`
- `no_private_logs`
- `no_generated_local_artifacts`
- `no_secrets_or_connection_material`
- `no_release_artifacts`
- `no_dispatch_payloads`
- `no_ratchet_reports`
- `no_baseline_pr_artifacts`
- `no_source_repo_files`
- `no_external_corpus_contents`
- `stdout_only`
- `report_only_non_claims_present`

Safety checks are hygiene evidence only. They are not security assurance or
privacy assurance.

## Downstream Issue Separation

Issue #1 must remain separate from:

- #2 PR validation for corpus package safety;
- #3 release publishing for reviewed corpus packages;
- #4 `repository_dispatch` into Mythic Edge;
- #5 ratchet comparison for corpus releases;
- #6 auto-open baseline PR workflow after ratchet comparison.

The preview command may produce local evidence that later issues consume, but
it must not implement those downstream capabilities or imply that they are
ready.

## Validation Requirements For Later Codex C

If later authorized, Codex C should add focused tests for:

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
- deterministic ordering;
- text output non-claims;
- JSON output shape, if implemented;
- stdout-only default behavior.

Recommended future validation commands:

```bash
python3 -m pytest -q tests/test_corpus_package_preview.py
python3 tools/corpus_package_preview.py --package-root corpus --manifest corpus/manifest.v1.json --session-ledger corpus/session_ledger.v1.json --format text
python3 tools/corpus_package_preview.py --package-root corpus --manifest corpus/manifest.v1.json --session-ledger corpus/session_ledger.v1.json --format json | python3 -m json.tool >/dev/null
git diff --check
```

Those commands are future implementation validation only. They are not
authorized by this Codex B pass.

## Validation Requirements For Codex E

Codex E should review:

- whether this contract preserves issue #1's local/report-only boundary;
- whether the future command surface avoids publishing, dispatch, ratchets, and
  baseline PR behavior;
- whether forbidden input classes are broad enough for private/raw corpus
  safety;
- whether manifest/session-ledger ownership is clear;
- whether preview statuses avoid parser truth and readiness claims;
- whether downstream issues #2 through #6 remain separate.

## Protected Surfaces And Non-Claims

This contract does not authorize:

- code implementation;
- PR creation;
- issue closure;
- corpus package publication;
- release creation;
- `repository_dispatch`;
- ratchet comparison;
- baseline PR creation;
- package artifact writes;
- report artifact writes;
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
- analytics truth;
- AI truth;
- coaching truth;
- security assurance;
- privacy assurance.

## Recommended Next Role

Codex E should review this contract before Codex C implementation is
considered. If Codex E finds it clean, route to Codex F/G for docs-only
submission and merge. Codex C should not start unless a later handoff
explicitly authorizes implementation of the local preview command and public
safe bootstrap metadata/tests.

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge-Corpus"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge-Corpus"
  issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/1"
  related_mythic_edge_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  related_mythic_edge_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/560"
  related_mythic_edge_gate_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/565"
  completed_thread: "B"
  next_thread: "E"
  verdict: "corpus_local_package_preview_contract_written_ready_for_review"
  risk_tier: "High"
  target_artifact: "docs/contracts/corpus_local_package_preview_command.md"
  package_preview_command_implementation_authorized: false
  package_preview_execution_authorized: false
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
  stop_conditions:
    - "Do not mutate Tahjali11/Mythic-Edge."
    - "Do not publish corpus packages, create releases, dispatch events, run ratchets, or open baseline PRs."
    - "Do not import, copy, mirror, or commit raw corpus/private files."
    - "Do not read private logs, secrets, generated local artifacts, or private reports."
    - "Do not claim parser truth, corpus readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, security assurance, or privacy assurance."
```
