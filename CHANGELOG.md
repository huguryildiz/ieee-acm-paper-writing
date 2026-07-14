# Changelog

## Unreleased

### Added

- The MIT license text to the installable skill directory so CLI and manual copies retain the
  distribution terms.
- Regression tests that bind evaluation verdicts to the current case definition and agent-output
  artifact, plus HTML-anchor and reference-style link checks.
- "IEEE editorial style essentials" subsection in `references/venue-guidance.md`, summarizing the
  IEEE Editorial Style Manual for Authors (spelling, acronym definition, reference numbering,
  figure/table citation, Acknowledgment placement, number and date formats, inclusive language),
  with the current manual and venue instructions taking precedence.
- "IEEE reference style essentials" subsection in `references/venue-guidance.md`, distilling the
  IEEE Reference Style Guide for Authors (in-text citation form, reference-list mechanics,
  canonical formats for the common source types, FORCE11 dataset/software citation, abbreviation
  and URL-breaking rules), with the current guide and venue instructions taking precedence; the
  rules digest is archived in `docs/guides/ieee-reference-style-guide.md`.
- "Mathematical notation and equation editing" section in
  `references/manuscript-structure-style.md`, distilling IEEE Publication Operations' *Editing
  Mathematics* guide: equation-as-sentence punctuation, in-line math constraints, display-equation
  break/alignment rules, consecutive numbering, Roman-function and boldface conventions, and
  near-equality symbol semantics (≈, ≃, ∼, ≅), with venue templates taking precedence.
- "ACM reference format essentials" subsection in `references/venue-guidance.md`, distilling ACM's
  master submission template (numeric vs. author-year citation modes, reference-list mechanics,
  schematic formats for the common source types, DOI resolver form, acknowledgment/history-date
  placement, CCS/keyword/ORCID and accessibility requirements), with the current template and venue
  instructions taking precedence; the rules digest is archived in
  `docs/guides/acm-reference-format-guide.md`.
- Repo-side provenance digests of the source guides under `docs/guides/`
  (`ieee-editorial-style-manual.md`, `ieee-editing-mathematics.md`, `acm-reference-format-guide.md`),
  link-checked by the validator; not part of the installable skill.
- Behavioral eval cases covering both reference behaviors: `ieee_reference_format_audit` and
  `acm_reference_format_audit` test whether the agent catches mechanical defects (en-dash citation
  ranges, more-than-six-author truncation, "ibid.", DOI form, author-year/numeric mode mixing,
  missing fields, acknowledgment placement); `ieee_reference_format_generate` tests whether the
  agent produces a correct IEEE reference from raw fields (initials, author truncation, bare DOI)
  without inventing an absent field.
- `examples/reference-format-example.md`, a worked example spanning both directions: it audits a
  broken IEEE reference excerpt, produces a correct reference from raw fields, shows the IEEE and
  ACM forms side by side, and flags a genuinely missing field as an author query instead of filling
  it; linked from the SKILL.md router.

### Changed

- Prepared the citation metadata for v0.1.1 and clarified that calibration modifies a drafting,
  audit, outline, or venue-adaptation mode rather than defining a ninth output mode.
- Rephrased public integrity statements as behavioral requirements instead of unconditional model
  guarantees.
- Regenerated the agent interface prompt to keep scientific-evidence audit separate from optional
  exposition calibration.

### Fixed

- Evaluation reports now reject missing, replaced, or prompt-stale agent outputs; manual verdicts
  are preserved only while both case and output hashes match.
- The repository validator now aligns both evaluation schemas, rejects duplicate frontmatter keys,
  validates the generated agent interface, and checks HTML, reference-style, and anchored links.
- Routing expectations now follow the router's mandatory references, and the ACM venue case carries
  the manuscript excerpt it asks the agent to adapt.
- The installable calibration reference no longer discloses corpus-specific counts.

### Removed

- The committed behavioral audit record (`evals/results/2026-07-14-behavioral-audit.md`)
  and the `evals/results/` directory. The remaining committed behavioral evidence is the
  historical comparison snapshot in
  [`evals/comparisons/optimization-claim-scope.md`](evals/comparisons/optimization-claim-scope.md).

## v0.1.0 — 2026-07-14

Initial public release. Subsequent audit-driven corrections are recorded under Unreleased.

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
- Behavioral audit record: `evals/results/2026-07-14-behavioral-audit.md`
  (removed after release; see Unreleased above).
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
