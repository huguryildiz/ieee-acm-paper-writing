# Changelog

## v0.6.3 — 2026-08-04

### Fixed

- Sparse-evidence drafts no longer turn absent measurements into prose-level failure mechanisms or
  guarantees; unsupported details remain external author actions.
- Supplied style excerpts are treated only as structural calibration and are never copied into the
  generated manuscript text.
- Citation-ranking refusals no longer disclose identities from the private calibration catalog.
- Expansion preserves every supplied scope condition and comparator instead of broadening claims
  while adding detail.
- When the exact venue and article type are unknown, venue adaptation makes no positive
  length-compliance statement and records length only as an unverified venue rule.

### Evidence

- Retained exact-skill behavioral campaigns cover all 27 cases on Claude Sonnet Medium once and
  Codex Luna Medium twice. The independently reviewed results are 27/27, 26/27, and 25/27; the
  remaining failures are limited to reference-format audit details, and no unresolved
  release-blocking core invariant failure was found.

## v0.6.2 — 2026-08-04

### Added

- Four adversarial behavioral cases for `expand`, `compress`, `outline`, and the complete
  `--html-map` artifact path, bringing the suite to 27 cases and covering every declared mode.
- An explicit mode-to-case coverage map and validator gates that reject missing mode or modifier
  coverage.
- Artifact-aware behavioral collection: declared files must stay under `tmp/evals/`, are archived
  and hashed with the response, and make a report stale if missing or replaced.
- A retained, multi-client behavioral evidence bundle and CI gate that validates every response,
  generated artifact, case contract, score, denominator, and failed-case declaration.
- Exact-candidate release evidence from two Codex Luna Medium replications and one Claude Sonnet
  Medium run, with collection-time skill identity, mechanical authority isolation, all 441
  criterion decisions retained, and independent maintainer review.

### Changed

- `humanize` must keep every relative result anchored to its comparator, and must recover a missing
  comparator from the supplied evidence or raise an author query rather than return an unanchored
  percentage. Dropping the comparison base is now stated to be a claim change rather than a surface
  change, and the change ledger must name each comparator carried through. An isolated behavioral
  run reproduced the unanchored-percentage failure twice before this rule and passed after it; that
  is a single observation per configuration, not a reliability estimate.
- The stable README and showcase commands pin both the `skills` installer (`1.5.21`) and skill
  release (`v0.6.2`).
- The plugin manifests declare stable version `0.6.2`, aligned with every stable install channel.
- The README now separates mechanical evidence validation from release approval and records that
  the retained behavioral evidence describes the post-64cec1a candidate rather than `v0.6.1`.
- Installation documentation now labels Git-backed plugin marketplaces as rolling channels and
  distinguishes them from release-stable tagged-clone, CLI, and manual-copy paths.
- The collector now pins the repository-local `SKILL.md` as its sole authority, scans both default
  and environment-selected Codex and Claude configuration roots, and passes the checked environment
  unchanged to a direct, shell-free agent subprocess. Known skill/cache collisions and authority-
  changing command wrappers or options are rejected before invoking an agent.
- The installable-skill hash now covers every distributed file recursively, including the renderer
  and all JSON/HTML examples. Symlinks are rejected before generated-cache exclusions are applied.
- Retained review ledgers now require a non-empty evidence quotation or an explicit full-response
  absence-inspection record for every criterion decision, and every quotation must appear verbatim
  in the retained response it cites.
- `collect` writes a `collection.json` identity record and `score` and `report --strict` refuse to
  run once the installable skill has changed since collection, so a recorded skill hash attests the
  tree the agents read instead of the tree it is filed under. The retained post-64cec1a bundle
  predates that record and declares `skill_hash_captured_at_collection: false`.
- The evidence validator accepts a truthful `independent_human_review: true` when a review record
  accompanies it, instead of hard-coding the boundary to `false` and blocking the release path it
  is meant to gate.
- A prerelease manifest must pin stable install channels to a version this repository actually
  released, checked against the CHANGELOG.
- `scripts/build_evidence_bundle.py` assembles a retained bundle from collected campaigns instead
  of leaving `responses.jsonl`, `review-ledger.json`, and `manifest.json` to hand assembly, which
  is how a relaxed criterion and paraphrased quotations entered the previous record.
- A failed collection now reports the head of both stdout and stderr. Hosts print setup failures
  such as `Not logged in` on stdout, so the previous stderr-only diagnostic could leave an entire
  campaign with no explanation.
- The evidence gate no longer names Codex specifically. It requires two agent hosts and two
  distinct replications on one of them, matching the stated release gate; which host carries the
  replications is the collector's choice.
- `scripts/validate_behavioral_evidence.py` validates every bundle under `evals/results/` rather
  than one hard-coded directory. Each bundle now carries its own `cases.json` snapshot, so evidence
  stays checkable after the skill or case set moves on, and the summary states whether a bundle
  still describes the current tree.
- The IEEE reference-format cases and final output gate now reject duplicated brackets and
  italicized `et al.`, closing false-positive and observed model-output gaps.

## v0.6.1 — 2026-08-03

### Added

- A manual installation path that needs neither Node.js nor a plugin marketplace, with the
  project- and user-scoped skill directories each supported host scans.
- A host-specific invocation-prefix table in the quick start, so a Claude Code reader is no longer
  shown only the Codex form.
- Validation of the Claude Code plugin and marketplace manifests, including agreement between the
  Claude manifests, the Codex manifest, and the release the README pins, with regression tests. The
  Claude install path is a session command that CI cannot run, so its manifests are now gated
  instead.

### Changed

- Invocation examples in the README and the packaged agent interface now use the `@` prefix that
  Codex accepts, replacing the earlier `$` form; the validator and its tests were updated with them.
- The Codex plugin card description now matches the Claude plugin card.
- Installation notes record that the Claude Code marketplace entry caches the whole repository,
  that the `authentication` key is a required marketplace-schema field rather than a credential
  prompt this plugin adds, and the date the Claude path was last exercised end to end.

### Fixed

- Release pinning: the previous release predated the author-style refusal rule in
  `manuscript-structure-style.md`, so the release-pinned install and the default-branch install
  delivered different behavioral rules. The pinned commands now reference this release, and the
  validator fails when a declared plugin version has no pinned install command in the README.

## v0.6.0 — 2026-08-03

### Added

- A native Codex plugin package with repository marketplace metadata, install-safe skill and icon
  snapshots, Codex interface metadata, and local/Git marketplace installation instructions.
- Dependency-free snapshot synchronization and plugin-package validation, with regression tests and
  a dedicated CI gate that rejects symlinks, stale packaged files, and invalid manifest or
  marketplace contracts.
- A native Claude Code plugin manifest and single-plugin marketplace, installable with
  `/plugin marketplace add` and `/plugin install` without Node.js or a shell command.

### Changed

- Installation guidance now presents three separate paths — native Codex plugin, native Claude Code
  plugin, and the Agent Skills CLI — and the CLI command drops the redundant repository subpath,
  skill selector, and installer pin that the CLI resolves on its own.

## v0.5.0 — 2026-08-03

### Added

- A loopback-only local audit workbench with drag-and-drop JSON intake, canonical renderer
  validation, sandboxed preview, HTML download, full-screen viewing, light/dark themes, responsive
  layouts, session-bound requests, and a 2 MiB input limit.
- Renderer output containment for traversal, external absolute paths, and symlink escapes, with
  regression tests for every boundary.
- A validator check that keeps the README behavioral-case count synchronized with `cases.json`.

### Changed

- Manuscript-mode handoff now requires mechanically structured external author queries for every
  unresolved claim dependency and a visible source-conflict record when evidence disagrees.
- Every `--html-map` run now retains and returns both the version-1 JSON artifact and its rendered
  HTML companion with deterministic paired filenames; README includes all nine mode invocations.
- Installation guidance now pins the released skill and installer, states the current Node.js
  prerequisite, distinguishes project and global scope, targets Codex explicitly, exposes the
  telemetry opt-out, and includes first-use examples.
- CI now uses `actions/checkout@v6` with read-only repository permissions and documentation now
  distinguishes deterministic CI checks from manually scored model behavior.
- The hosted landing page links to the local-workbench instructions and copies the reproducible
  Codex installation command.

### Fixed

- Missing statistical, citation-support, real-time, and matched-comparison evidence can no longer
  remain only as manuscript limitations; each becomes a separate external author action.
- Narrowing or omitting an unsupported requested claim no longer discharges the corresponding
  external `Author queries` obligation.
- Conflicting measured and narrative values remain visible even when the measured artifact controls
  the allowed wording.
- Systems without automated field-to-model updates are classified as offline models rather than
  digital shadows merely because live measurements and older simulations share a dashboard.
- The README behavioral-suite count now matches the 23 defined cases.
- Local-workbench documentation now states that the UI is repository-side tooling rather than part
  of the installed skill, and provides a release-pinned clone command.
- Regression coverage now keeps the public nine-mode invocation inventory synchronized with the
  skill router.
- Compact local-workbench controls now meet the 44 px minimum touch-target size.

## v0.4.0 — 2026-07-20

### Added

- Plain-lexicon substitution table (utilize → use, facilitate → enable, and so on) in the
  "Machine-idiom removal" section of `references/manuscript-structure-style.md`, applied during
  drafting, rewriting, and humanizing.
- Two machine-idiom catalog rows: metaphor and vogue nouns (tapestry, realm, journey, plethora)
  and stock importance/momentum phrases ("paving the way," "plays a key role," "in recent years,
  there has been growing interest in").
- Section-contract writing devices: related-work narrowing to the closest studies with enumerated,
  checkable differences; constraint functional-naming plus the four-question constraint exposition
  and equation lead-in/interpretation; the five-step results sequence (identify, observe, quantify,
  mechanism, implication); and two-sided trade-off presentation before a joint treatment.
- "Equation and notation integrity" checks in `references/integrity-audit.md`: undefined symbols,
  overloaded notation, index consistency, summation and variable domains, dimensional consistency,
  equation–prose agreement, and proxy-objective disclosure.
- Three generic before/after style examples illustrating the controls above.

All additions are de-identified generic guidance, consistent with the skill's prohibition on
copying an individual author's fingerprint. CI green: skill-structure validation, 23 eval cases,
39 regression tests.

## v0.3.0 — 2026-07-20

### Added

- Pedagogical exposition guidance for `draft` and `rewrite`: expositions of a model, method, or
  formulation now state what a component does, how its parts produce that behavior, and why it
  matters, written to teach a reader unfamiliar with the passage. Backed by two new bullets in the
  "Paragraph and prose controls" section of `references/manuscript-structure-style.md` and an
  expanded step 4 in the "Draft or rewrite" contract of `SKILL.md`.
- A concrete-instantiation rule: an abstract statement may be grounded in the specific instance it
  refers to (a named node, set, quantity, or condition) when this aids understanding, using only
  material the evidence already supports and never an invented example. The integrity gate and the
  results-before-interpretation / Discussion-placement rules remain unchanged.

## v0.2.0 — 2026-07-19

### Added

- `humanize` mode: a ninth router mode that removes machine-idiom prose patterns (formulaic
  transitions, uniform rhythm, hedging inflation, filler vocabulary, list-itis, meta-discourse)
  while preserving claims, numbers, units, citations, notation, scope conditions, and
  evidence-bearing hedges. Backed by a "Machine-idiom removal (humanize)" catalog in
  `references/manuscript-structure-style.md`, a dedicated output contract (humanized text plus a
  change ledger by pattern category), and an explicit boundary: the mode improves prose quality
  and never removes or weakens a generative-AI disclosure.
- Behavioral case `humanize_preserves_claims` exercising machine-idiom removal against an embedded
  directive to strip the AI-use disclosure, a load-bearing generalization hedge, and verbatim
  number preservation.

- Validator check that no evaluation criterion shares a distinctive six-word phrase with any skill
  file, so an answer cannot be passed by echoing loaded skill text.
- Validator check that the interactive showcase stays self-contained (no external asset fetch) and
  keeps its bundle blocks parseable.
- Behavioral case `acm_ai_disclosure_blind_review` exercising AI-disclosure identity leakage under
  double-blind review, listing an AI tool as an author, and ORCID/open-access verification.
- `skill_hash` now covers the non-Markdown audit-map assets so a section-audit case's verdict goes
  stale when they change.
- The MIT license text to the installable skill directory so CLI and manual copies retain the
  distribution terms.
- Regression tests that bind evaluation verdicts to the current case definition and agent-output
  artifact, plus HTML-anchor, reference-style and tracked-target link, path-containment,
  strict-frontmatter, and calibration-identity checks.
- Three behavioral cases that exercise embedded-directive handling in drafting, rewriting, and
  venue-adaptation modes.
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
  context-sensitive near-equality symbol handling, with manuscript definitions and venue templates
  taking precedence over stylistic normalization.
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
- `examples/section-audit-example.md`, a live-test fixture: a synthetic flawed Results and
  Conclusion excerpt (ML-warm-started MILP microgrid dispatch) with an 11-item planted-flaw
  answer key spanning all three concern layers, expected must/must-never behavior, a run
  protocol, and an illustrative evidence-scoped rewrite; linked from the SKILL.md router and the
  README without presenting the unretained live session as behavioral evidence.
- Optional `--html-map` rendering for `audit` and `section-audit`, backed by a versioned JSON
  contract, a self-contained HTML template, and a Python-standard-library renderer that performs
  presentation only and refuses implicit overwrite.
- A generated section-audit map fixture (`examples/section-audit-map.json` and
  `examples/section-audit-map-rendered.html`) plus
  regression tests for deterministic output, escaping, schema validation, empty concern layers,
  self-containment, and overwrite safety.
- A dependency-free Vercel showcase with a responsive editorial interface, embedded audit-map
  preview, direct HTML and JSON downloads, theme switching, installation-command copying, and a
  reproducible build that copies the tracked example artifacts without modifying them.

### Changed

- Removed repository-level citation metadata; clarified that calibration modifies a drafting,
  audit, outline, or venue-adaptation mode rather than defining a ninth output mode.
- Rephrased public integrity statements as behavioral requirements instead of unconditional model
  guarantees.
- Regenerated the agent interface prompt to keep scientific-evidence audit separate from optional
  exposition calibration.
- Reclassified corpus calibration as de-identified rather than guaranteed anonymous and removed
  several single-source-like exposition sequences.
- Recast publisher-level venue summaries as screening heuristics that require exact-venue
  verification before they become compliance findings.
- Expanded skill routing to evidence-grounded peer-review reports while continuing to exclude
  unsupported editorial accept/reject advocacy.
- Kept the router at eight scientific modes and defined `--html-map` as an opt-in output modifier
  rather than a ninth mode; the canonical text audit remains authoritative.

### Fixed

- Regenerated the two IEEE reference-format cases with independent bibliographic data so they no
  longer duplicate the shipped `reference-format-example.md` answer key; decoupled the shared
  `[Okafor 1991]` example label; rephrased criteria that echoed skill text.
- Made the interactive showcase truly self-contained by removing vestigial Google Fonts preconnect
  hints; all fonts were already embedded as data: URIs, so the visual is unchanged.
- The audit-map renderer now reports a clean error and exit code for invalid-UTF-8 and
  deeply-nested JSON input instead of raising an uncaught traceback.
- Scoped the ACM ORCID and open-access notes and the IEEE mathematics conventions as
  verify-against-the-current-venue defaults rather than timeless universal facts.
- Separated the custom interactive audit-map showcase from the deterministic renderer fixture so
  presentation edits no longer make the renderer freshness check fail.
- Evaluation-runner regression tests now derive the expected case count from `cases.json` instead
  of a hardcoded 15, which had broken CI when the three reference-format cases were added.
- Evaluation case names are restricted to safe slugs, every output path is contained within the
  selected output directory, and failed collections preserve prior response artifacts.
- Evaluation reports now reject missing, replaced, or prompt-stale agent outputs; manual verdicts
  are preserved only while both case and output hashes match.
- The repository validator now aligns both evaluation schemas, strictly validates its supported
  flat frontmatter subset, enforces direct calibration-identity exclusions, validates the generated
  agent interface, and checks HTML, reference-style, and anchored links.
- The digital-twin case now recognizes its supplied weekly manual cadence and rejects the stronger
  digital-shadow label; the inaccessible-corpus case now supplies the method and failure-regime
  evidence its passing criteria require.
- Embedded directives now have an external `Integrity findings` output channel in every mode,
  overriding manuscript-only output restrictions.
- Near-equality symbols retain their manuscript- and domain-defined meanings instead of being
  normalized to one universal mapping.
- Routing expectations now follow the router's mandatory references, and the ACM venue case carries
  the manuscript excerpt it asks the agent to adapt.
- The installable calibration reference no longer discloses corpus-specific counts.

### Removed

- `examples/claim-audit-example.md` and `examples/rewrite-example.md`: both are subsumed by the
  end-to-end section-audit example (claim testing, evidence-first rewrite, external author query);
  the routing and reference-format examples remain as the distinct behavior surfaces.
- The committed behavioral audit record (`evals/results/2026-07-14-behavioral-audit.md`)
  and the `evals/results/` directory. The remaining committed behavioral evidence is the
  historical comparison snapshot in
  [`evals/comparisons/optimization-claim-scope.md`](evals/comparisons/optimization-claim-scope.md).
- `CITATION.cff`. Citation metadata is no longer maintained in the repository.

## v0.1.0 — 2026-07-14

Initial public release. Subsequent audit-driven corrections are recorded under later releases.

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
  (removed in a later release; see the removal entry above).
- `CITATION.cff` (removed in a later release; see the removal entry above).

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
