# Mythic Edge Corpus Agent Entry Point

Operate as a senior software engineer maintaining Mythic Edge's public-safe
corpus artifact repository. Prefer narrow, well-verified, repo-local changes
over broad workflow expansion.

This repository stores sanitized Corpus metadata, public-safe bootstrap
sessions, review contracts, implementation handoffs, package preview helpers,
package-safety validation helpers, release dry-run helpers, no-send dispatch
payload validation, ratchet comparison reports, and baseline PR proposal
previews.

This repository does not own parser truth, parser behavior, fixture promotion,
source-repo mutation, baseline approval, release readiness, deploy readiness,
production readiness, security assurance, privacy assurance, analytics truth,
AI truth, or coaching truth.

## Repo Role

`Tahjali11/Mythic-Edge-Corpus` owns public-safe Corpus support artifacts and
tools, including:

- corpus manifest and session-ledger metadata;
- sanitized public-safe session examples;
- local package preview reports;
- PR package-safety checks;
- release package dry-run metadata;
- no-send `repository_dispatch` payload validation;
- ratchet comparison report objects from supplied public-safe inputs;
- baseline PR proposal previews;
- Corpus contracts, handoffs, reports, and tests.

Treat these as support and provenance surfaces. They can help later workflows
review corpus changes, but they do not become parser truth or source-repo
authority by being committed here.

## What This Repo Does Not Own

Do not use this repository to authorize or perform:

- Mythic Edge parser behavior changes;
- parser-owned fact changes;
- fixture promotion;
- corpus status mutation in the source parser repo;
- source-repo branches, commits, PRs, comments, reviews, labels, or status
  checks;
- package publishing or GitHub release publishing;
- `repository_dispatch` sends;
- ratchet execution;
- baseline mutation or baseline PR creation;
- release, deploy, production, security, privacy, analytics, AI, or coaching
  claims.

If a request needs any of those actions, route it through a separate current
issue, contract, and explicit owner approval in the owning repository.

## Parser Truth Boundary

Parser truth remains owned by `Tahjali11/Mythic-Edge` parser/state code and
normalized parser outputs. Corpus evidence may support review, provenance, and
regression planning. It is not a second parser and not a workbook or dashboard
truth source.

Committing or packaging Corpus metadata does not prove:

- a parser behavior is correct;
- a fixture should be promoted;
- a ratchet passed against current source behavior;
- a baseline should change;
- corpus parity is complete.

## Sanitized Artifact Rules

Committed Corpus artifacts must be public-safe and deterministic where
practical.

Preferred artifact properties:

- explicit schema version;
- stable package, session, proposal, report, or payload ID;
- source kind and source label;
- reviewed public issue, PR, commit, contract, manifest, or ledger reference
  where applicable;
- explicit no-write, no-send, or report-only status;
- explicit non-claims;
- no raw private content;
- no local machine paths.

Use structured JSON validation for manifest, ledger, session, release, dispatch,
ratchet, and baseline proposal artifacts whenever those files are touched.

## Private And Raw Data Boundary

Do not read, import, echo, or commit:

- raw `Player.log` files;
- raw `UTC_Log` files;
- private logs or private corpus files;
- private decklists or private match records;
- workbook exports;
- app-data paths or local absolute paths;
- generated local artifacts;
- runtime artifacts;
- screenshots;
- credentials, tokens, API keys, webhook URLs, or secrets;
- private evidence.

If a future task needs private evidence, stop and require a separate owner
approval naming the exact source class, symbolic source label, artifact class,
redaction policy, and destination repository.

## Fixture Promotion Boundary

Fixture promotion requires a separate owner-approved workflow in the owning
source repository. Corpus package previews, release dry runs, dispatch
validation, ratchet reports, and baseline proposal previews are not fixture
promotion.

Do not create, promote, mutate, or delete fixtures from this repository unless a
current issue and contract explicitly authorize that exact fixture operation.

## Provenance And Source Labels

Corpus metadata should preserve public-safe provenance without leaking raw data.
When applicable, include:

- schema version;
- package version or session ID;
- manifest and ledger refs;
- source repository and reviewed public commit ref;
- contract or handoff ref;
- public-safe source kind;
- object status;
- validation summary;
- non-claims.

Use value-source labels conservatively:

- `public_safe_synthetic`: intentionally synthetic public-safe data.
- `public_safe_bootstrap`: committed bootstrap metadata.
- `reviewed_public_ref`: public issue, PR, commit, contract, or handoff ref.
- `report_only`: diagnostic output only.
- `no_write_preview`: proposed output with no external write.
- `no_send_validation`: payload validation with no dispatch.

Do not use source labels to imply parser truth, fixture promotion, release
readiness, or production behavior.

## Corpus Status, Ratchets, And Baselines

Ratchet comparison is diagnostic and report-only unless a later workflow
explicitly authorizes ratchet execution and consumption. A ratchet report can
summarize public-safe deltas, blockers, or no-delta results, but it must not
claim full corpus parity by itself.

Baseline PR proposal helpers are no-write previews unless a later source-repo
workflow explicitly authorizes actual PR creation and baseline mutation. A
baseline proposal may describe proposed branch, title, or body metadata only
when the relevant contract allows it; that metadata is not a created PR.

Release package helpers in this repository are dry-run/report helpers unless a
separate issue explicitly authorizes package artifact creation or release
publishing.

Dispatch helpers are no-send validators unless a separate issue explicitly
authorizes sending `repository_dispatch`.

## Cross-Repo Routing

Route work by ownership:

- `Tahjali11/Mythic-Edge`: parser behavior, parser truth, fixture promotion,
  receiving-side ratchets, source code changes, and source-repo PRs.
- `Tahjali11/Mythic-Edge-Corpus`: public-safe Corpus metadata, package previews,
  PR safety checks, release dry runs, no-send dispatch validation, ratchet
  reports, baseline proposal previews, and Corpus governance docs.
- `Tahjali11/Mythic-Edge-Automation-Artifacts`: advisory automation metadata,
  ARS/Refactor Scout artifacts, candidate dossiers, prompts, and automation
  policy contracts.
- `Tahjali11/Mythic-Edge-Security`: security intake, private/security artifact
  gates, security inventory gates, and security/privacy routing.
- `Tahjali11/Mythic-Edge-Analytics`: analytics interpretation, scoring-bundle
  metadata, endpoint schema scaffolds, and analytics non-truth boundaries.

Do not mutate sibling repositories from a Corpus task unless a repo-scoped
handoff and explicit owner approval authorize that exact repository and action.

## Validation Expectations

Use the smallest relevant validation first.

Docs-only changes:

```bash
git diff --check
```

JSON metadata changes:

```bash
python3 -m json.tool corpus/manifest.v1.json >/dev/null
python3 -m json.tool corpus/session_ledger.v1.json >/dev/null
```

Python tool or test changes:

```bash
python3 -m unittest discover -s tests
python3 -m py_compile tools/*.py
python3 -m ruff check tools tests
```

Public-safe package, release, dispatch, ratchet, and baseline lanes may require
focused commands named in their active contract or handoff. If validation is not
run, state the exact reason.

## Explicit Owner Approval Required

Require explicit owner approval and a current scoped issue or contract before:

- raw/private corpus import;
- private log reads;
- raw `Player.log` or `UTC_Log` reads;
- package or release artifact creation;
- GitHub release creation;
- `repository_dispatch` sends;
- ratchet execution;
- baseline PR creation;
- baseline mutation;
- corpus status mutation;
- fixture creation, mutation, deletion, or promotion;
- source repository mutation;
- source-repo issue, PR, comment, review, label, branch, commit, or status-check
  creation;
- any claim of readiness, truth, production behavior, security assurance, or
  privacy assurance.

Short approvals apply only to the exact active lane and do not broaden adjacent
Corpus, parser, release, ratchet, baseline, dispatch, or source-repo authority.

## Forbidden Claims Without Later Contract

Do not claim any of the following without a later contract and explicit owner
authorization:

- parser truth;
- fixture promotion;
- baseline approval;
- corpus readiness;
- release readiness;
- deploy readiness;
- production readiness;
- ratchet success;
- full corpus parity;
- security assurance;
- privacy assurance;
- analytics truth;
- AI truth;
- coaching truth.

Prefer explicit non-claims in reports and handoffs, especially when output is
public-safe, report-only, no-write, no-send, dry-run, or preview-only.

## Workflow Handoff Expectations

End non-trivial Corpus workflow work with:

- role performed;
- source issue or contract used;
- artifact produced or changed;
- files changed;
- validation run;
- remaining risks or unverified layers;
- next recommended role;
- pasteable next-role prompt when useful;
- `workflow_handoff` block.

For submitter or deployer roles, also include branch, PR, commit, target branch,
checks, and checkout cleanup status when applicable.
