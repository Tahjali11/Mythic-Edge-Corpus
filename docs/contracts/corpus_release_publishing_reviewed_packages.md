# Corpus Release Publishing For Reviewed Packages Contract

## Module

`corpus_release_publishing_reviewed_packages`

Plain English: this contract defines a future release-publishing boundary for
`Tahjali11/Mythic-Edge-Corpus`. The future release workflow should publish only
reviewed, public-safe corpus packages after local package preview and PR
validation gates exist and pass.

Release publishing is package distribution and provenance recording. It is not
parser truth, not fixture promotion, not corpus readiness, not production
readiness, not ratchet success, not baseline approval, not analytics truth, not
AI truth, not coaching truth, not security assurance, and not privacy
assurance.

This Codex B pass writes only this contract. It does not implement release
publishing, create package artifacts, create GitHub releases, run package
preview, run PR validation, dispatch events, run ratchets, open baseline PRs,
import corpus files, copy raw evidence, read private logs, or mutate
`Tahjali11/Mythic-Edge`.

## Source Artifact

- Repository: `Tahjali11/Mythic-Edge-Corpus`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge-Corpus`
- Issue: https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/3
- Previous issue:
  https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/2
- Previous PR:
  https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/8
- Previous merge commit:
  `e51e713ef6bae8246fefd7424a9197fe60cbfaa8`
- Related Mythic Edge tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Base branch: `main`
- Working branch:
  `codex/corpus-release-publishing-reviewed-packages-3`
- Target artifact:
  `docs/contracts/corpus_release_publishing_reviewed_packages.md`
- Risk tier: High

Observed during this Codex B pass:

- The operating checkout remote matched
  `https://github.com/Tahjali11/Mythic-Edge-Corpus.git`.
- The checkout started clean on `main`.
- `origin/main` was verified at
  `e51e713ef6bae8246fefd7424a9197fe60cbfaa8`.
- Work was moved to
  `codex/corpus-release-publishing-reviewed-packages-3`, tracking
  `origin/main`.
- Issue #3 was open.
- Issue #2 was closed after PR #8 merged the PR validation package-safety
  contract.
- The related Mythic Edge tracker #388 was open.
- The repository currently contains `README.md`, `LICENSE`, and the issue #1
  and #2 contracts.
- The local package preview command and PR validation package-safety layer are
  still contract-only; neither was implemented or executed by this pass.
- No `Tahjali11/Mythic-Edge` worktree files were inspected or mutated by this
  pass.

Current authorization facts to preserve:

```yaml
implementation_authorized: false
release_publishing_contract_authorized: true
release_publishing_implementation_authorized: false
release_publishing_execution_authorized: false
package_artifact_creation_authorized: false
release_asset_creation_authorized: false
github_release_creation_authorized: false
package_preview_execution_authorized: false
pr_validation_execution_authorized: false
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

- Corpus issue #3
- Corpus issue #2
- Corpus issue #2 deployer closeout comment
- Corpus PR #8 metadata
- Related Mythic Edge tracker #388 summary
- `README.md`
- `LICENSE`
- `docs/contracts/corpus_local_package_preview_command.md`
- `docs/contracts/corpus_pr_validation_package_safety.md`

No raw corpus files, private logs, generated local artifacts, private reports,
package artifacts, release assets, dispatch payloads, ratchet outputs, baseline
PR artifacts, or `Tahjali11/Mythic-Edge` source files were read, created,
copied, mirrored, summarized, or committed.

## Observed Current Behavior

The corpus repo is still a bootstrap repository. It has:

- a README;
- a license;
- a contract for a future local package preview command;
- a contract for future PR validation package-safety checks.

It does not yet have:

- a corpus package manifest;
- a session ledger;
- package metadata;
- package preview tooling;
- PR validation tooling;
- release package tooling;
- release publishing automation;
- release assets;
- `repository_dispatch` automation;
- ratchet comparison automation;
- baseline PR automation.

Issue #3 is the next planned safety layer after preview and PR validation. It
must define the release boundary without skipping the fact that the predecessor
layers are currently contracts, not implemented gates.

## Problem

Reviewed corpus packages need a reproducible release boundary before Mythic
Edge can safely consume corpus updates through later dispatch, ratchet, or
baseline proposal workflows.

The first bad value is treating a release package, release candidate, checksum,
GitHub release, release note, tag, package manifest, PR validation summary, or
human review note as parser truth, fixture promotion, corpus readiness, release
readiness, ratchet success, baseline approval, production readiness, analytics
truth, AI truth, coaching truth, security assurance, or privacy assurance.

The second bad value is allowing release publishing to include unreviewed files,
raw/private/generated/runtime artifacts, external corpus contents, secrets,
exact private paths, private reports, dispatch payloads, ratchet outputs,
baseline PR artifacts, or copied `Tahjali11/Mythic-Edge` source files.

The third bad value is letting release publishing trigger downstream actions.
Publishing a reviewed corpus package must not dispatch into Mythic Edge, run
parser ratchets, open baseline PRs, update Mythic Edge metadata, or imply those
later gates are ready.

## Scope Decision

This contract approves a contract-only release-publishing boundary.

Codex C implementation is not automatically authorized by this contract. A
later Codex C pass may proceed only if a user or lifecycle handoff explicitly
authorizes release-publishing tooling, package-artifact creation, focused tests,
and any GitHub release or workflow surface.

If later authorized, the narrow Codex C implementation surface may include:

- a release package builder under `tools/`;
- focused tests under `tests/`;
- package metadata schema fixtures, if separately authorized;
- release-note template text;
- a local dry-run command for release package construction;
- a GitHub release workflow only if a later implementation handoff explicitly
  authorizes that surface.

This contract defines:

- future release-publishing purpose;
- required predecessor gates;
- release package identity and naming vocabulary;
- release package metadata and checksum expectations;
- allowed inputs;
- forbidden inputs;
- reviewed package publication rules;
- release status vocabulary;
- default-branch and tag rules;
- human review requirements;
- no-dispatch, no-ratchet, no-baseline boundaries;
- validation expectations for later Codex C and Codex E.

This contract does not authorize:

- code implementation in Codex B;
- package artifact creation;
- release asset creation;
- GitHub release creation;
- release publishing execution;
- package preview execution;
- PR validation execution;
- `repository_dispatch`;
- ratchet comparison;
- baseline PR creation;
- raw corpus import;
- raw/private evidence reads;
- package upload;
- GitHub Actions workflow creation;
- GitHub issue or PR creation;
- mutation of `Tahjali11/Mythic-Edge`;
- parser behavior changes;
- corpus readiness, release readiness, production readiness, analytics truth,
  AI truth, coaching truth, security assurance, or privacy assurance claims.

## Owning Layer And Truth Boundary

Owner: `Tahjali11/Mythic-Edge-Corpus`, release packaging and publication
boundary.

Truth boundary:

- Mythic Edge parser/state remains the owner for parser interpretation,
  parser events, match/game identity, deduplication, and final reconciliation.
- Mythic Edge evidence-pipeline contracts own harvest, review, confidence, and
  corpus metadata diff semantics.
- The issue #1 local package preview boundary owns local/report-only package
  preview semantics.
- The issue #2 PR validation boundary owns PR package-safety semantics.
- This issue #3 boundary owns reviewed corpus package release semantics.
- Later corpus issues separately own `repository_dispatch`, ratchet comparison,
  and baseline PR proposal automation.

Release publishing may say:

- a reviewed public-safe corpus package was built from the approved repository
  state;
- the package references explicit manifest/session metadata;
- package checksums match the published release assets;
- required predecessor validation evidence was present;
- a human reviewer approved publication.

Release publishing must not say:

- parser interpretation is correct;
- fixtures should be promoted;
- Mythic Edge should consume the release;
- a dispatch should be sent;
- a ratchet passed;
- a baseline PR should be opened;
- a package is production-ready;
- the release is security assurance or privacy assurance.

Required future data flow:

```text
reviewed public-safe corpus PR
  -> local package preview command
  -> PR validation package-safety checks
  -> human review and merge to default branch
  -> reviewed package release publishing
  -> later repository_dispatch issue
  -> later ratchet comparison issue
  -> later baseline PR issue
```

Forbidden shortcut:

```text
release publishing
  -/-> parser truth
  -/-> fixture promotion
  -/-> corpus readiness
  -/-> repository_dispatch
  -/-> ratchet success
  -/-> baseline approval
  -/-> production readiness
```

## Required Predecessor Gates

A future release-publishing implementation must fail closed unless all required
predecessor gates are satisfied:

- the local package preview command exists and passes for the exact release
  candidate;
- the PR validation package-safety layer exists and passes for the exact
  release candidate;
- the release candidate is based on the approved default branch;
- the release candidate includes explicit manifest and session-ledger metadata;
- every packaged file is declared by the manifest;
- every session-backed file is reconciled with the session ledger;
- no forbidden file class or forbidden marker is present;
- a human reviewer approved the exact release candidate;
- the target release tag does not already exist;
- the target release asset names do not already exist;
- no downstream dispatch, ratchet, or baseline PR action is requested by the
  release step.

If any predecessor is absent, stale, blocked, failed, ambiguous,
review-required, unsupported, or invalid, release publishing must write nothing
and publish nothing.

## Future Release Package Identity

The future release package should derive identity from committed package
metadata:

```yaml
package_id: "mythic-edge-corpus"
package_schema_version: "corpus_package.v1"
package_version: "<manifest-owned version>"
release_tag: "corpus-package-v<package_version>"
release_name: "Mythic Edge Corpus <package_version>"
release_channel: "reviewed"
source_commit: "<default-branch commit>"
```

Rules:

- `package_version` must be explicit in the package manifest.
- `release_tag` must be deterministic and derived from `package_version`.
- Release tags must be immutable by default.
- Replacing a published package requires a later replacement policy contract.
- Version metadata must not be inferred from local filesystem timestamps.
- Version metadata must not be inferred from private logs, raw corpus payloads,
  or generated local artifacts.

If the repository later needs prerelease channels, backfills, or replacement
releases, those need separate issue authority.

## Future Release Artifact Shape

The future release may include only reviewed public-safe assets:

- one package archive containing allowed corpus package files;
- one release metadata JSON file;
- one checksum file for the published public-safe release assets;
- optional release notes generated from public-safe metadata.

Recommended future asset naming:

```text
mythic-edge-corpus-<package_version>.tar.gz
mythic-edge-corpus-<package_version>.metadata.json
mythic-edge-corpus-<package_version>.checksums.txt
```

Package archives are forbidden in the repository working tree unless a later
implementation issue explicitly authorizes creating them as release outputs.
They must not be committed back into the repo by default.

## Release Metadata Shape

Future release metadata JSON should include:

```yaml
object: corpus_release_package_metadata
schema_version: corpus_release_package_metadata.v1
repository: Tahjali11/Mythic-Edge-Corpus
repository_url: https://github.com/Tahjali11/Mythic-Edge-Corpus
package_id: string
package_version: string
release_tag: string
release_channel: reviewed
source_commit: string
source_branch: main
manifest_ref: object
session_ledger_ref: object
package_preview_ref: object
pr_validation_ref: object
review_ref: object
included_files_summary: object
asset_checksums: list
safety_checks: list
blocked_reason_codes: list
non_claims: list
```

Release metadata must not include raw corpus payloads, private content, local
absolute paths, secret-shaped content, private logs, generated local artifacts,
dispatch payloads, ratchet results, baseline PR payloads, copied source files,
or external corpus contents.

## Checksum Boundary

Future checksums may cover only public-safe release assets produced from
reviewed committed package contents.

Checksum rules:

- Use a deterministic algorithm such as SHA-256.
- Include checksums for release assets, not for rejected files.
- Never hash raw/private/generated/runtime files.
- Never publish hash lists for private logs, private reports, external corpus
  contents, app-data, source-repo files, or files outside the approved package
  root.
- Treat checksums as package integrity metadata only.
- Do not treat checksums as parser truth, content approval, security assurance,
  privacy assurance, or release readiness.

## Allowed Input Classes

Release publishing may inspect only committed, public-safe, repo-owned inputs
after predecessor gates are implemented and pass:

- corpus package manifest metadata;
- session ledger metadata;
- package root inventory;
- package README or package notes;
- license and attribution metadata;
- reviewed public-safe sanitized fixtures, if they exist in this repo and are
  declared by manifest/session metadata;
- schema files or validation metadata committed to this repo;
- package configuration committed to this repo;
- package preview output for the exact release candidate;
- PR validation output for the exact release candidate;
- human review metadata for the exact release candidate;
- default-branch commit metadata.

The release workflow may read included public-safe files only after path and
extension allowlist checks pass. If content scanning finds forbidden markers,
publishing must fail with symbolic failure categories without echoing unsafe
content.

## Forbidden Input Classes

Release publishing must not inspect, import, copy, mirror, summarize, hash, or
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
- dispatch payloads;
- ratchet reports;
- baseline PR artifacts;
- source files from `Tahjali11/Mythic-Edge`;
- external corpus contents.

If a forbidden input is discovered, release publishing must fail closed and must
not include raw values, raw paths outside the repo, raw payloads, hashes, or
snippets in output.

## Default Branch And Release Workflow Rules

Future release publishing must:

- run only from the approved default branch unless a later contract authorizes a
  dedicated release branch;
- verify the local checkout matches the intended remote repository;
- verify the release source commit is reachable from the approved default
  branch;
- verify the working tree is clean before building release assets;
- verify predecessor validation evidence references the same source commit;
- fail if the target tag already exists;
- fail if release assets would overwrite existing assets;
- produce deterministic asset names;
- produce deterministic release metadata ordering;
- avoid force-push, tag rewrite, or release overwrite behavior by default.

Release publishing must not mutate contributor branches or create automatic
baseline branches.

## Future Command Surface

Recommended future local dry-run command:

```bash
python3 tools/corpus_release_package.py \
  --package-root corpus \
  --manifest corpus/manifest.v1.json \
  --session-ledger corpus/session_ledger.v1.json \
  --package-version <package_version> \
  --dry-run
```

Recommended future publish command, if separately authorized:

```bash
python3 tools/corpus_release_package.py \
  --package-root corpus \
  --manifest corpus/manifest.v1.json \
  --session-ledger corpus/session_ledger.v1.json \
  --package-version <package_version> \
  --publish
```

V1 behavior:

- dry-run mode must be available before publish mode;
- publish mode must require explicit human approval;
- default behavior should be no publish;
- release assets should be created only in an approved temporary/output
  location before upload;
- release assets must not be committed back to the repository by default;
- output must use repo-relative paths and symbolic reason codes;
- no downstream dispatch, ratchet, or baseline PR action may run.

If later implementation wants GitHub Actions, `gh release`, API release
publishing, signed attestations, or release replacement behavior, it requires
explicit issue and contract authority.

## Status Vocabulary

Release publishing status values:

- `contract_only`: contract exists, but implementation is not authorized.
- `release_dry_run_ready`: release dry-run tooling exists and can evaluate a
  package candidate locally.
- `release_candidate_report_only`: release candidate metadata can be reported,
  but no assets or GitHub release are authorized.
- `release_ready_for_human_review`: predecessor gates passed and a human must
  approve publication.
- `published_reviewed_package`: a reviewed public-safe package was published
  after all release gates passed.
- `blocked_missing_preview_command`: required preview command is absent.
- `blocked_preview_failed`: package preview failed, blocked, or was malformed.
- `blocked_missing_pr_validation`: PR validation package-safety layer is absent.
- `blocked_pr_validation_failed`: PR validation failed, blocked, or was
  malformed.
- `blocked_missing_manifest`: required manifest is absent.
- `blocked_missing_session_ledger`: required session ledger is absent.
- `blocked_invalid_metadata`: manifest, ledger, package, or release metadata is
  malformed.
- `blocked_manifest_ledger_mismatch`: manifest and ledger relationships do not
  reconcile.
- `blocked_unreviewed_candidate`: human review approval is absent.
- `blocked_non_default_branch`: release source is not the approved default
  branch.
- `blocked_existing_tag`: target release tag already exists.
- `blocked_existing_asset`: target release asset already exists.
- `blocked_unsafe_path`: unsafe path form was discovered.
- `blocked_forbidden_content`: forbidden content markers were discovered.
- `blocked_raw_or_private_input`: raw corpus, private, generated, external, or
  source-repo input was discovered.
- `blocked_dispatch_requested`: release step attempted `repository_dispatch`.
- `blocked_ratchet_requested`: release step attempted ratchet comparison.
- `blocked_baseline_pr_requested`: release step attempted baseline PR creation.
- `review_required`: a human reviewer must inspect an ambiguous release state.
- `unsupported`: requested release mode is outside this contract.
- `invalid`: required fields are missing, contradictory, or unsafe.

For issue #3 during Codex B, the only current status is `contract_only`.

## Safety Check Vocabulary

Safety checks should include:

- `preview_command_required`
- `pr_validation_required`
- `default_branch_only`
- `clean_worktree_required`
- `repo_relative_paths_only`
- `no_path_traversal`
- `package_root_only`
- `manifest_declared_files_only`
- `session_ledger_reconciled`
- `human_review_required`
- `immutable_release_tag`
- `no_existing_asset_overwrite`
- `no_raw_corpus_evidence`
- `no_private_logs`
- `no_generated_local_artifacts`
- `no_secret_or_connection_material`
- `no_dispatch_payloads`
- `no_ratchet_reports`
- `no_baseline_pr_artifacts`
- `no_source_repo_files`
- `no_external_corpus_contents`
- `no_repository_dispatch`
- `no_ratchet_execution`
- `no_baseline_pr_creation`
- `release_non_claims_present`

Safety checks are release hygiene evidence only. They are not security
assurance or privacy assurance.

## Downstream Issue Separation

Issue #3 must remain separate from:

- #4 `repository_dispatch` into Mythic Edge;
- #5 ratchet comparison for corpus releases;
- #6 auto-open baseline PR workflow after ratchet comparison.

Release publishing may produce package and provenance evidence that later
issues consume, but it must not implement those downstream capabilities or
imply that they are ready.

## Validation Requirements For Later Codex C

If later authorized, Codex C should add focused tests for:

- missing preview command;
- preview command failure;
- missing PR validation layer;
- PR validation failure;
- missing manifest;
- missing session ledger;
- malformed package metadata;
- manifest/session ledger mismatch;
- unreviewed release candidate;
- non-default-branch release attempt;
- existing tag refusal;
- existing asset refusal;
- path traversal;
- absolute path;
- generated/runtime/cache path;
- forbidden raw/private marker;
- dispatch payload in scope;
- ratchet report in scope;
- baseline PR artifact in scope;
- copied source-repo file in scope;
- deterministic asset naming;
- deterministic release metadata JSON;
- checksum generation for public-safe release assets only;
- no downstream dispatch, ratchet, or baseline PR call;
- dry-run mode creates no release;
- publish mode requires explicit approval;
- release output non-claims.

Recommended future validation commands:

```bash
python3 -m pytest -q tests/test_corpus_release_package.py
python3 tools/corpus_release_package.py --package-root corpus --manifest corpus/manifest.v1.json --session-ledger corpus/session_ledger.v1.json --package-version <package_version> --dry-run
git diff --check
```

Those commands are future implementation validation only. They are not
authorized by this Codex B pass.

## Validation Requirements For Codex E

Codex E should review:

- whether this contract preserves issue #1's preview dependency;
- whether this contract preserves issue #2's PR validation dependency;
- whether release publishing fails closed when predecessor gates are missing,
  failed, blocked, or malformed;
- whether release identity, tag, asset, metadata, and checksum rules are
  deterministic and public-safe;
- whether forbidden input classes are broad enough for private/raw corpus
  safety;
- whether release output avoids raw unsafe content and local absolute paths;
- whether downstream issues #4 through #6 remain separate;
- whether the contract avoids parser truth, fixture promotion, corpus
  readiness, release readiness, ratchet success, baseline approval, production
  readiness, security assurance, and privacy assurance claims.

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
- `repository_dispatch`;
- ratchet comparison;
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
explicitly authorizes release-publishing tooling, package-artifact creation,
release tests, and any GitHub release or workflow surface.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Corpus issue #3.

Repository:
Tahjali11/Mythic-Edge-Corpus

Repository URL:
https://github.com/Tahjali11/Mythic-Edge-Corpus

Issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/3

Previous issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/2

Previous PR:
https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/8

Related Mythic Edge tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Contract artifact:
docs/contracts/corpus_release_publishing_reviewed_packages.md

Goal:
Review the release-publishing contract for reviewed corpus packages. Lead with
findings, if any. Verify that the contract preserves the issue #1 preview
dependency and issue #2 PR validation dependency, fails closed on unsafe or
unreviewed release states, forbids raw/private/generated/runtime artifacts,
keeps repository_dispatch / ratchets / baseline PR automation out of scope, and
does not claim parser truth, fixture promotion, corpus readiness, release
readiness, production readiness, security assurance, or privacy assurance.

Do not implement code.
Do not open a PR.
Do not close issue #3.
Do not publish packages, create releases, dispatch events, run ratchets, open
baseline PRs, import raw corpus data, read private logs, or mutate
Tahjali11/Mythic-Edge.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge-Corpus"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge-Corpus"
  issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/3"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/2"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/8"
  related_mythic_edge_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  completed_thread: "B"
  next_thread: "E"
  verdict: "corpus_release_publishing_reviewed_packages_contract_written_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  latest_verified_commit: "e51e713ef6bae8246fefd7424a9197fe60cbfaa8"
  target_artifact: "docs/contracts/corpus_release_publishing_reviewed_packages.md"
  mythic_edge_mutation_authorized: false
  release_publishing_authorized: false
  package_artifact_creation_authorized: false
  repository_dispatch_authorized: false
  ratchet_execution_authorized: false
  baseline_pr_creation_authorized: false
  raw_corpus_import_authorized: false
  private_log_read_authorized: false
  stop_conditions:
    - "Do not mutate Tahjali11/Mythic-Edge."
    - "Do not publish corpus packages, create releases, dispatch events, run ratchets, or open baseline PRs."
    - "Do not import, copy, mirror, or commit raw corpus/private files."
    - "Do not read private logs, secrets, generated local artifacts, or private reports."
    - "Do not claim parser truth, corpus readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, security assurance, or privacy assurance."
```
