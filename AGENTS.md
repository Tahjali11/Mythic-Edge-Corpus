# Mythic Edge Corpus Agent Entry Point

Operate as a senior engineer maintaining Mythic Edge's public-safe Corpus
artifact repository. Prefer narrow, deterministic, repo-local changes.

This repo stores sanitized Corpus metadata, public-safe bootstrap sessions,
review contracts, implementation handoffs, package preview helpers,
package-safety checks, release dry-run helpers, no-send dispatch validation,
ratchet comparison reports, baseline PR proposal previews, and related tests.

It does not own parser truth, parser behavior, fixture promotion, source-repo
mutation, baseline approval, release/deploy/production readiness, security or
privacy assurance, analytics truth, AI truth, or coaching truth.

## Repo Role

`Tahjali11/Mythic-Edge-Corpus` owns public-safe Corpus support artifacts and
tools. Treat them as provenance and review aids. They do not become parser
truth or source-repo authority by being committed here.

Route ownership clearly:

- `Tahjali11/Mythic-Edge`: parser behavior, parser truth, fixture promotion,
  receiving-side ratchets, source code changes, and source-repo PRs.
- `Tahjali11/Mythic-Edge-Corpus`: public-safe metadata, package previews, PR
  safety checks, release dry runs, no-send dispatch validation, ratchet reports,
  baseline proposal previews, and Corpus governance docs.
- `Tahjali11/Mythic-Edge-Automation-Artifacts`: advisory automation metadata.
- `Tahjali11/Mythic-Edge-Security`: security/private artifact routing.
- `Tahjali11/Mythic-Edge-Analytics`: analytics interpretation and endpoint
  schema scaffolds.

Do not mutate sibling repos unless a repo-scoped handoff and explicit owner
approval authorize that exact action.

## Parser Truth And Promotion Boundary

Parser truth remains owned by `Tahjali11/Mythic-Edge` parser/state code and
normalized parser outputs. Corpus evidence may support review, provenance, and
regression planning, but it is not a second parser and not workbook/dashboard
truth.

Committing or packaging Corpus metadata does not prove parser correctness,
fixture promotion, ratchet success, baseline approval, corpus parity, release
readiness, or production behavior.

Fixture creation, mutation, deletion, or promotion requires a separate
owner-approved workflow in the owning source repo. Corpus package previews,
release dry runs, dispatch validation, ratchet reports, and baseline proposal
previews are not fixture promotion.

## Public-Safe Artifact Rules

Committed Corpus artifacts must be public-safe and deterministic where
practical. Prefer explicit schema version, stable object ID, source kind/label,
reviewed public issue/PR/commit/contract/manifest/ledger ref, no-write/no-send/
report-only status, validation summary, and explicit non-claims.

Do not read, import, echo, or commit raw `Player.log`, raw `UTC_Log`, private
logs, private corpus files, private decklists, private match records, workbook
exports, app-data paths, local absolute paths, generated local artifacts,
runtime artifacts, screenshots, credentials, tokens, API keys, webhook URLs,
secrets, or private evidence.

If future work needs private evidence, stop and require owner approval naming
the exact source class, symbolic source label, artifact class, redaction
policy, and destination repo.

Use source labels conservatively, such as `public_safe_synthetic`,
`public_safe_bootstrap`, `reviewed_public_ref`, `report_only`,
`no_write_preview`, and `no_send_validation`. Do not use labels to imply truth,
promotion, readiness, or production behavior.

## Ratchets, Baselines, Release, And Dispatch

Ratchet comparison is diagnostic/report-only unless a later workflow
explicitly authorizes execution and consumption.

Baseline PR proposal helpers are no-write previews unless a later source-repo
workflow authorizes actual PR creation and baseline mutation.

Release package helpers are dry-run/report helpers unless a separate issue
authorizes package artifact creation or release publishing.

Dispatch helpers are no-send validators unless a separate issue authorizes
`repository_dispatch`.

## Explicit Approval Required

Require explicit owner approval and a current scoped issue or contract before:
raw/private import, private log reads, package/release artifact creation,
GitHub release creation, `repository_dispatch`, ratchet execution, baseline PR
creation, baseline mutation, corpus status mutation, fixture operations, source
repo mutation, public source-repo issue/PR/comment/review/label/branch/commit/
status-check creation, or any readiness/truth/security/privacy claim.

Short approvals apply only to the exact active lane.

## Validation

Use the smallest relevant validation first:

```bash
git diff --check
python3 -m json.tool corpus/manifest.v1.json >/dev/null
python3 -m json.tool corpus/session_ledger.v1.json >/dev/null
python3 -m unittest discover -s tests
python3 -m py_compile tools/*.py
python3 -m ruff check tools tests
```

Run only checks relevant to touched files and active contracts. If validation
is not run, state why.

## Handoff

End non-trivial work with role performed, source issue/contract, artifact
changed, files changed, validation, remaining risks, next role, pasteable
prompt when useful, and `workflow_handoff`. For submitter/deployer work, also
include branch, PR, commit, target branch, checks, and checkout cleanup status.
