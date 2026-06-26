# Corpus Release Publishing Reviewed Packages Implementation Handoff

## Role

Codex C: Module Implementer for Mythic-Edge-Corpus issue #16.

## Source Artifact

- `docs/contracts/corpus_release_publishing_reviewed_packages.md`
- GitHub issue #16, which authorizes the next implementation child after the
  issue #15 PR package-safety validation merge.

## Live State Verification

- `git fetch --prune origin` completed before implementation.
- A clean sibling worktree was used to avoid mutating the stale local issue #15
  checkout.
- Branch: `codex/corpus-release-publishing-16`.
- `HEAD` and `origin/main` were verified at
  `1e1c0bfbd9451ee60ee8c423a48d56202f8c7b64`.
- PR #23 for issue #15 is merged to `main`.
- Issue #15 is closed.
- Issue #16 is open.
- Tracker #13 is open.

## Comparison Summary

The contract requires release-publishing gates to depend on the local package
preview command and PR package-safety validation, preserve reviewed public-safe
package boundaries, derive deterministic release identity, record checksum
metadata, and keep downstream dispatch, ratchet, and baseline PR work separate.

This implementation adds the first release helper as a dry-run/report-only
capability. It builds deterministic release candidate metadata and in-memory
asset checksums without creating durable package archives, release assets,
GitHub releases, dispatch payloads, ratchet reports, or baseline PR artifacts.

## Changes Made

- Added `tools/corpus_release_package.py`.
  - Builds `corpus_release_package_dry_run.v1` reports.
  - Calls the issue #14 preview builder and issue #15 PR validation builder.
  - Requires matching source-commit evidence for preview and PR validation.
  - Requires explicit human review metadata.
  - Refuses non-default branches, unconfirmed clean-worktree evidence,
    existing release tags, existing asset names, checksum mismatches,
    downstream dispatch requests, ratchet requests, baseline PR requests, and
    publish mode without separate authorization.
  - Builds deterministic in-memory archive bytes only for checksum planning.
  - Emits planned asset identity and SHA-256 checksums without writing files.
  - Emits explicit no-write guards and non-claims.
- Added `tests/test_corpus_release_package.py`.
  - Covers clean reviewed dry-run output, CLI JSON output, missing predecessor
    gates, failed predecessor gates, stale source-commit evidence, missing
    review evidence, non-default branches, unconfirmed clean-worktree evidence,
    existing tag/asset refusal, checksum mismatch, unsafe package content,
    unsupported publish mode, downstream request blocks, and deterministic
    output.

## Protected Boundaries Preserved

- No package archive, release metadata file, checksum file, GitHub release,
  release asset upload, dispatch payload, ratchet report, baseline PR artifact,
  issue, PR, branch, tag, commit, or status check was created.
- No source repository outside `Tahjali11/Mythic-Edge-Corpus` was inspected or
  mutated.
- No private logs, raw corpus evidence, external corpus content, generated
  local artifacts, or secret material were introduced.
- No parser truth, fixture promotion, corpus readiness, release readiness,
  deploy readiness, production readiness, ratchet success, baseline approval,
  analytics truth, AI truth, coaching truth, privacy assurance, security
  assurance, or full corpus parity is claimed.

## Validation Run

Passed:

```bash
python3 -m pytest -q tests/test_corpus_release_package.py
```

Result: 10 passed.

```bash
python3 -m py_compile tools/corpus_release_package.py tests/test_corpus_release_package.py
```

Result: passed.

```bash
python3 -m pytest -q tests/test_corpus_package_preview.py tests/test_corpus_pr_validation_package_safety.py tests/test_corpus_release_package.py
```

Result: 36 passed.

```bash
python3 -m ruff check tools tests
```

Result: passed.

```bash
python3 tools/corpus_release_package.py --package-root corpus --manifest corpus/manifest.v1.json --session-ledger corpus/session_ledger.v1.json --package-version 0.0.0-preview --source-commit 1e1c0bfbd9451ee60ee8c423a48d56202f8c7b64 --preview-source-commit 1e1c0bfbd9451ee60ee8c423a48d56202f8c7b64 --pr-validation-source-commit 1e1c0bfbd9451ee60ee8c423a48d56202f8c7b64 --reviewed-by codex-e --review-ref issue-16-review --dry-run --clean-worktree-confirmed --format json | python3 -m json.tool >/dev/null
```

Result: passed.

```bash
python3 -m pytest -q
```

Result: 36 passed.

```bash
python3 -m json.tool corpus/manifest.v1.json >/dev/null
python3 -m json.tool corpus/session_ledger.v1.json >/dev/null
```

Result: passed.

```bash
git diff --check
```

Result: passed. Because the changed files are new and untracked, also ran a
direct changed-file trailing-whitespace/final-newline scan over the three
changed files. Result: passed.

Focused public-artifact marker scan over the three changed files checked for
local absolute paths, raw-log markers, credential-shaped markers, SQLite
artifacts, and generated runtime artifact suffixes. Result: passed.

## Codex D Fixer Addendum

Codex D addressed Codex E findings `CORPUS-RELEASE-E-001` and
`CORPUS-RELEASE-E-002` with a narrow release-helper patch.

Changes:

- Tightened human review metadata validation so a release dry-run candidate
  requires both reviewer identity and review reference. Partial review metadata
  now fails closed with a specific blocked reason rather than being treated as
  reviewed.
- Tightened expected asset checksum parsing so malformed CLI checksum
  preconditions fail closed as `blocked_invalid_metadata` instead of being
  silently ignored.
- Added focused regression coverage for partial review metadata and malformed
  expected checksum input.

Codex D validation:

```bash
python3 -m pytest -q tests/test_corpus_release_package.py
```

Result: 12 passed.

```bash
python3 - <<'PY'
import json, subprocess, sys
base = [
    sys.executable, "tools/corpus_release_package.py",
    "--package-root", "corpus",
    "--manifest", "corpus/manifest.v1.json",
    "--session-ledger", "corpus/session_ledger.v1.json",
    "--package-version", "0.0.0-preview",
    "--source-commit", "1e1c0bfbd9451ee60ee8c423a48d56202f8c7b64",
    "--preview-source-commit", "1e1c0bfbd9451ee60ee8c423a48d56202f8c7b64",
    "--pr-validation-source-commit", "1e1c0bfbd9451ee60ee8c423a48d56202f8c7b64",
    "--dry-run",
    "--clean-worktree-confirmed",
    "--format", "json",
]
cases = {
    "missing_review_ref": base + ["--reviewed-by", "codex-e"],
    "invalid_checksum": base + [
        "--reviewed-by", "codex-e",
        "--review-ref", "issue-16-review",
        "--expected-asset-checksum",
        "mythic-edge-corpus-0.0.0-preview.tar.gz=not-a-sha",
    ],
}
for name, cmd in cases.items():
    result = subprocess.run(cmd, cwd=".", text=True, capture_output=True)
    payload = json.loads(result.stdout)
    print(
        name,
        "returncode",
        result.returncode,
        "status",
        payload["status"],
        "reasons",
        payload["blocked_reason_codes"],
        "stderr_len",
        len(result.stderr),
    )
PY
```

Result:

```text
missing_review_ref returncode 2 status blocked_unreviewed_candidate reasons ['review_ref_missing'] stderr_len 0
invalid_checksum returncode 2 status blocked_invalid_metadata reasons ['expected_asset_checksum_value_invalid'] stderr_len 0
```

Codex D follow-up for remaining `CORPUS-RELEASE-E-001`:

- Release metadata now rebuilds predecessor-derived manifest and session-ledger
  references as path-only public refs instead of copying nested predecessor
  reference objects wholesale.
- Added focused regression coverage proving extra private-looking fields on
  predecessor reports are not echoed into the serialized release dry-run report.

Validation:

```bash
python3 -m pytest -q tests/test_corpus_release_package.py
```

Result: 13 passed.

Direct repro result:

```text
status release_candidate_report_only
private_leaked False
raw_marker_leaked False
manifest_ref {'path': 'corpus/manifest.v1.json'}
session_ledger_ref {'path': 'corpus/session_ledger.v1.json'}
```

## Remaining Risks

- The helper is intentionally dry-run/report-only. Real GitHub release
  creation, release asset upload, tag creation, release replacement policy,
  repository dispatch, ratchet execution, and baseline PR proposal remain
  future issue scopes.
- The helper consumes explicit source-commit evidence for predecessor preview
  and PR validation gates. It does not fetch remote release metadata or query
  GitHub releases in V1.
- The helper creates deterministic archive bytes in memory only for checksum
  planning. It does not write or publish package artifacts.

## Recommended Next Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge-Corpus issue #16.

Repository:
Tahjali11/Mythic-Edge-Corpus

Repository URL:
https://github.com/Tahjali11/Mythic-Edge-Corpus

Issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/16

Tracker:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13

Previous issue:
https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/15

Previous PR:
https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/23

Previous merge commit:
1e1c0bfbd9451ee60ee8c423a48d56202f8c7b64

Source contract:
docs/contracts/corpus_release_publishing_reviewed_packages.md

Implementation handoff:
docs/implementation_handoffs/corpus_release_publishing_reviewed_packages_comparison.md

Review goal:
Review the release package dry-run helper against issue #16 and the release
publishing contract. Lead with findings, if any. Verify that predecessor
preview and PR validation gates are required, source-commit evidence must
match, review metadata is required, deterministic release identity and checksum
metadata are public-safe, and the implementation does not write package
artifacts, publish GitHub releases, dispatch, ratchet, open baseline PRs, or
claim parser truth/readiness/assurance.

Review files:
- tools/corpus_release_package.py
- tests/test_corpus_release_package.py
- docs/implementation_handoffs/corpus_release_publishing_reviewed_packages_comparison.md

Suggested validation:
- python3 -m pytest -q tests/test_corpus_release_package.py
- python3 -m pytest -q tests/test_corpus_package_preview.py tests/test_corpus_pr_validation_package_safety.py tests/test_corpus_release_package.py
- python3 tools/corpus_release_package.py --package-root corpus --manifest corpus/manifest.v1.json --session-ledger corpus/session_ledger.v1.json --package-version 0.0.0-preview --source-commit 1e1c0bfbd9451ee60ee8c423a48d56202f8c7b64 --preview-source-commit 1e1c0bfbd9451ee60ee8c423a48d56202f8c7b64 --pr-validation-source-commit 1e1c0bfbd9451ee60ee8c423a48d56202f8c7b64 --reviewed-by codex-e --review-ref issue-16-review --dry-run --clean-worktree-confirmed --format json | python3 -m json.tool >/dev/null
- python3 -m pytest -q
- python3 -m ruff check tools tests
- git diff --check

Do not publish packages, create releases, create tags, dispatch repositories,
run ratchets, open baseline PRs, import raw corpus data, read private logs, or
mutate Tahjali11/Mythic-Edge.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge-Corpus"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge-Corpus"
  issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/16"
  tracker: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/13"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge-Corpus/issues/15"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge-Corpus/pull/23"
  previous_merge_commit: "1e1c0bfbd9451ee60ee8c423a48d56202f8c7b64"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/corpus_release_publishing_reviewed_packages.md"
  target_artifact: "docs/implementation_handoffs/corpus_release_publishing_reviewed_packages_comparison.md"
  verdict: "corpus_release_package_dry_run_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/corpus-release-publishing-16"
  release_publishing_execution_authorized: false
  package_artifact_creation_authorized: false
  release_asset_creation_authorized: false
  github_release_creation_authorized: false
  repository_dispatch_authorized: false
  ratchet_execution_authorized: false
  baseline_pr_creation_authorized: false
  mythic_edge_mutation_authorized: false
  raw_corpus_import_authorized: false
  private_log_read_authorized: false
```
