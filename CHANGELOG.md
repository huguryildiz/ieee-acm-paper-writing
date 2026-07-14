# Changelog

## v0.1.0 — 2026-07-14

Initial public release, hardened after an independent adversarial audit of the
initial commit (`c5ee641`).

### Added

- Vendored, dependency-free repository validator (`scripts/validate_skill.py`)
  and a CI workflow that runs it on every push and pull request.
- Executable evaluation suite: `evals/cases.json` schema v2 — 15 self-contained
  cases with binary, output-observable `must_pass`/`must_not` criteria — and
  `evals/run_evals.py` with `validate`, `list`, `collect`, `score`, and
  `report` modes.
- Prompt-injection invariant: supplied or audited material is evidence, never
  instructions; embedded directives are surfaced as integrity findings
  (`SKILL.md`, `references/integrity-audit.md`).
- `unverified citation` labeling rule for environments where citation
  verification is impossible, and a named-database-plus-access-date scoping
  rule for citation-count or ranking statements
  (`references/integrity-audit.md`).
- Structured author-query contract: missing item, blocked claim, requested
  action, consequence (`SKILL.md`).
- Behavioral audit record: `evals/results/2026-07-14-behavioral-audit.md`.
- `CITATION.cff`.

### Changed

- README hero paragraph rewritten as design intent rather than a validated
  behavioral guarantee; installation and validation sections updated to match
  the published state and the vendored validator.
- Routing table: `venue-guidance.md` now also triggers for audits or
  submission-readiness checks against a named venue; the corpus-calibration
  trigger is rephrased in end-user-visible terms (landmark-paper style
  calibration).
- `docs/papers/catalog.tsv`: Raissi et al. year corrected to the 2019 version
  of record (available online 2018), noted in the catalog.

### Fixed

- Two evaluation cases that expected capabilities absent from the skill: the
  nonexistent "industrial Transactions profile" expectation was rewritten in
  terms of the user-supplied reference-corpus procedure, and the
  citation-snapshot expectation is now backed by an explicit rule in
  `integrity-audit.md`.
