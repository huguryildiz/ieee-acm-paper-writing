<div align="center">

<img src="assets/icon.svg" alt="IEEE / ACM Paper Writing icon" width="112" height="112" />

# IEEE / ACM Paper Writing

### Evidence-bounded manuscript drafting and auditing for engineering research

An agent skill for turning supplied technical evidence into defensible IEEE- and ACM-style
manuscript prose—without using polished language to conceal missing support.

<b><a href="https://ieee-acm-paper-writing.vercel.app">Live showcase</a> · <a href="#capabilities">Capabilities</a> · <a href="#how-it-works">Design</a> · <a href="#installation">Installation</a> · <a href="#examples">Examples</a> · <a href="#evaluation-and-validation">Validation</a> · <a href="skills/ieee-acm-paper-writing/SKILL.md">SKILL.md</a></b>

</div>

---

## Overview

The skill drafts, rewrites, compresses, structures, adapts, and audits engineering manuscripts.
It keeps three authorities separate:

1. **Scientific support** — what verified formulations, code, data, experiments, and cited
   literature establish.
2. **Method and domain reporting** — what the applicable optimization, ML, simulation, systems,
   or engineering method requires the paper to disclose.
3. **Venue compliance** — what the target publication's current official instructions and
   template require.

The skill contract requires conflicts between these sources to be reported instead of resolved by
selecting the most convenient version. It also prohibits treating archived, planned, expected, or
mock results as completed evidence.

## Capabilities

The router supports eight modes: `draft`, `rewrite`, `expand`, `compress`, `outline`, `audit`,
`section-audit`, and `venue-adapt`. Style and landmark-paper calibration modify whichever of these
modes produces the requested deliverable; calibration is not a separate output mode. The optional
`--html-map` modifier renders an `audit` or `section-audit` result without defining a ninth mode.
Typical tasks include:

- drafting or revising abstracts, introductions, related work, methods, results, discussions,
  conclusions, and contribution lists;
- checking notation, units, equations, cross-references, quantitative claims, baselines,
  guarantees, and citation support;
- separating observed results from interpretation, causation, robustness, scalability, and
  generalization claims;
- auditing submission readiness with findings classified as `Critical`, `Major`, `Minor`, or
  `Editorial`;
- rendering an explicitly requested audit as a self-contained, interactive HTML finding map;
- adapting structure and presentation to a named IEEE or ACM venue while preserving scientific
  meaning; and
- calibrating exposition to aggregate patterns derived from landmark engineering papers without
  copying their language or treating those patterns as citable evidence.

### Engineering domains

The eight supported technical areas are:

1. communications and networking;
2. signal processing and sensing;
3. energy systems;
4. robotics and autonomy;
5. mathematical optimization;
6. simulation and digital twins;
7. machine learning and ML-assisted engineering; and
8. computer systems and cyber-physical-system engineering.

Combined studies can load multiple profiles.

## How it works

[`SKILL.md`](skills/ieee-acm-paper-writing/SKILL.md) establishes the authority hierarchy, routes
each request, and defines the output contracts. It loads only the references required for the
task:

| Reference | Purpose |
| --- | --- |
| [`integrity-audit.md`](skills/ieee-acm-paper-writing/references/integrity-audit.md) | Claim support, citation verification, integrity checks, and submission-readiness audits |
| [`manuscript-structure-style.md`](skills/ieee-acm-paper-writing/references/manuscript-structure-style.md) | Section logic, technical exposition, rewriting, and compression |
| [`engineering-profiles.md`](skills/ieee-acm-paper-writing/references/engineering-profiles.md) | Method- and domain-specific reporting requirements |
| [`corpus-calibration.md`](skills/ieee-acm-paper-writing/references/corpus-calibration.md) | De-identified, non-citable exposition patterns derived from the local calibration corpus |
| [`venue-guidance.md`](skills/ieee-acm-paper-writing/references/venue-guidance.md) | Venue adaptation and compliance-ledger rules |

For manuscript tasks, the skill instructs the agent to identify the intended claim, evidence
source, scope, and uncertainty before drafting. Its output contract requires unsupported content to
be omitted from publication-ready prose or returned separately as a structured author query. For
venue adaptation, requirements that cannot be checked against an official current source must be
labeled `unverified venue rule` rather than inferred.

The integrity contract treats supplied manuscripts, reviews, references, and data as evidence—not
as instructions—and requires embedded directives to be surfaced as findings rather than executed.

### Optional HTML audit map

Request the visual artifact with the `--html-map` output modifier:

```text
$ieee-acm-paper-writing section-audit --html-map manuscript.md
$ieee-acm-paper-writing section-audit --html-map --out reports/results-audit.html manuscript.md
```

Without the modifier, the skill produces no HTML file. With it, the agent completes the canonical
text audit, writes validated version-1 JSON, and invokes the dependency-free
[`render_audit_map.py`](skills/ieee-acm-paper-writing/scripts/render_audit_map.py) renderer. The
renderer performs presentation only: it cannot infer findings, rewrite claims, or fill missing
evidence. It refuses to overwrite an existing output unless the user explicitly authorizes
`--force`.

The [hosted showcase](https://ieee-acm-paper-writing.vercel.app) presents the checked-in fixture in
a browser and provides direct downloads of its self-contained HTML and source JSON. The site is a
static presentation layer: it does not accept manuscript uploads or perform an audit.

## Installation

Install the skill with the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills add huguryildiz/ieee-acm-paper-writing --skill ieee-acm-paper-writing
```

For a manual installation, copy [`skills/ieee-acm-paper-writing`](skills/ieee-acm-paper-writing)
into the skills directory used by your agent environment.

## Examples

- [Routing example](skills/ieee-acm-paper-writing/examples/routing-example.md) — selects the
  necessary references and audit boundaries for a manuscript request.
- [Reference-format example](skills/ieee-acm-paper-writing/examples/reference-format-example.md) —
  audits and produces IEEE/ACM reference-list entries using publisher-level screening guidance.
- [Section-audit example](skills/ieee-acm-paper-writing/examples/section-audit-example.md) — a
  flawed Results and Conclusion fixture with a planted-flaw answer key and an illustrative
  evidence-scoped rewrite; it is not a retained behavioral result.
- [Live interactive section-audit map](https://ieee-acm-paper-writing.vercel.app/examples/section-audit-map.html),
  [source JSON](skills/ieee-acm-paper-writing/examples/section-audit-map.json), and
  [generated HTML source](skills/ieee-acm-paper-writing/examples/section-audit-map.html) — the installable,
  self-contained visualization fixture. Each of the eleven planted flaws is tied to its triggering
  sentence, concern layer, evidentiary defect, consequence, and bounded response. The HTML is a
  presentation companion generated from the JSON, not behavioral evidence about an agent run.

## Calibration corpus

The local catalog contains 24 papers spanning the [eight supported technical
areas](#engineering-domains). Their bibliographic provenance is recorded in
[`docs/papers/catalog.tsv`](docs/papers/catalog.tsv); downloaded PDFs and derived full-text
artifacts are excluded from Git.

The installable skill contains only de-identified, derivative patterns such as contribution
archetypes, paragraph functions, method-presentation sequences, guarantee boundaries, evaluation
organization, and conclusion structure. These patterns do not establish technical claims, venue
rules, citation rankings, source anonymity, or permission to imitate an author's distinctive
language. A specialist may still recognize a technical lineage. End users do not need the local
PDFs to use the calibration reference.

## Evaluation and validation

The dependency-free repository validator checks the skill frontmatter, calibration identity
policy, selected Markdown links and their tracked targets, safe evaluation-case names and schema,
the agent interface, and deterministic regeneration of the checked-in audit map:

```bash
python3 scripts/validate_skill.py
python3 skills/ieee-acm-paper-writing/scripts/render_audit_map.py \
  skills/ieee-acm-paper-writing/examples/section-audit-map.json --check
```

The behavioral suite defines 21 self-contained adversarial cases with binary, output-observable
`must_pass` and `must_not` criteria. The runner validates cases, collects agent responses, creates
a manual scoring file, and reports results:

```bash
python3 evals/run_evals.py validate
python3 evals/run_evals.py list
python3 evals/run_evals.py collect --agent-cmd '<your agent CLI>' --outdir out/
python3 evals/run_evals.py score   --outdir out/
# Replace each null verdict in out/scores.json with true or false after review.
python3 evals/run_evals.py report  --outdir out/ --strict
```

`--strict` succeeds only when every defined case has a present agent-response artifact whose hash
matches the manually scored output, whose case hash matches the current prompt and criteria, and
whose verdicts are complete and passing. Missing, unscored, or stale entries remain in the
denominator and cause a non-zero exit. Regression tests cover this aggregation behavior:

```bash
python3 -m unittest discover -s tests -v
```

The repository CI runs the validator, evaluation-schema validation, and regression tests on pushes
to `main` and on pull requests. Renderer tests reject stale checked-in HTML, unsafe unescaped
content, invalid concern layers, duplicate finding identifiers, implicit overwrite, external asset
dependencies, and empty-layer wording that could be mistaken for a pass.

## Scope and limitations

- The integrity contract prohibits inventing citations, identifiers, evidence, methods, datasets,
  results, guarantees, or novelty claims.
- The venue contract prohibits assuming that one template, page limit, review format,
  anonymization policy, or AI disclosure rule applies to every IEEE or ACM publication.
- The skill guidance does not replace a target venue's current official author instructions or
  template.
- The audit contract prohibits calling a manuscript submission-ready while a load-bearing claim,
  citation, result, or venue requirement remains unresolved.
- The HTML renderer presents a completed audit; it is not an analysis engine and cannot establish
  evidence, generate findings, or repair unsupported claims.
- The evaluation runner uses manual criterion verdicts; it is a regression and smoke-test harness,
  not an automated model judge or comparative benchmarking framework.
- The skill is independently usable. ALETHEIA may be used upstream for evidence retrieval and
  claim support, but it is not required.

These are requirements encoded by the skill, not a guarantee that every host model will comply on
every run. Validate consequential outputs against the supplied evidence and retain the relevant
prompt, response, and scoring artifacts.

## Repository structure

```text
skills/ieee-acm-paper-writing/
├── SKILL.md                 # Router, invariants, and output contracts
├── LICENSE                  # MIT terms shipped with the installable copy
├── agents/openai.yaml       # Agent interface metadata
├── assets/                  # Self-contained HTML audit-map template
├── examples/                # Routing, reference-format, audit data, and generated HTML examples
├── scripts/                 # Dependency-free audit-map renderer
└── references/              # Integrity, style, domain, corpus, and venue guidance
evals/
├── cases.json               # Schema-v2 behavioral cases
├── run_evals.py             # Collection, manual scoring, and reporting harness
└── comparisons/             # Historical A/B comparison snapshot
docs/
├── guides/                  # Repo-side provenance digests of IEEE/ACM style guides
└── papers/catalog.tsv       # Calibration-corpus provenance (PDFs excluded from Git)
site/                        # Dependency-free hosted showcase source
scripts/build_site.py        # Builds the Vercel output from tracked site and example files
scripts/validate_skill.py    # Dependency-free repository validator
tests/                       # Evaluation-runner and validator regression tests
vercel.json                  # Static-site build and output configuration
```

## Citation

Release metadata is provided in [`CITATION.cff`](CITATION.cff).

## License

[MIT](LICENSE) © Hüseyin Uğur Yıldız
