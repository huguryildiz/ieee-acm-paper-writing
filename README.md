<div align="center">

<img src="assets/icon.svg" alt="IEEE / ACM Paper Writing icon" width="112" height="112" />

# IEEE / ACM Manuscript Paper Writing

### Draft, rewrite, humanize, and audit engineering manuscripts without crossing the evidence boundary

A native Codex plugin and Agent Skills package for Codex, Claude Code, and compatible LLM-based
research agents. It turns supplied technical evidence into defensible manuscript prose while
preserving claims, numbers, citations, notation, scope conditions, and uncertainty.

<b><a href="#quick-start">Quick start</a> · <a href="#working-modes">Modes</a> · <a href="#installation">Installation</a> · <a href="#examples">Examples</a> · <a href="#evaluation-and-validation">Validation</a> · <a href="skills/ieee-acm-paper-writing/SKILL.md">SKILL.md</a> · <a href="https://ieee-acm-paper-writing.vercel.app">Audit-map showcase</a></b>

</div>

---

## What this skill does

This is a manuscript-writing skill with an evidence gate. It can draft a new section, rewrite an
existing one, expand or compress technical exposition, remove machine-like prose patterns, build
an evidence-aware outline, audit a manuscript, or adapt it to a named IEEE or ACM venue.

The writing modes are the primary workflow. Audit is the protection layer around that workflow,
not a replacement for it. Before producing publication-ready prose, the skill identifies the
intended claim, its supporting artifact, its scope, and any unresolved dependency. When the
available evidence does not support requested wording, the skill narrows or omits the claim and
returns a structured author query instead of filling the gap with plausible language.

Typical uses include:

- rewriting a Results section while preserving every number, unit, comparator, and uncertainty;
- drafting an Abstract from verified findings without importing claims absent from the body;
- restructuring an Introduction around the technical obstacle, contribution, evidence, and scope;
- explaining a formulation or algorithm without changing notation or guarantee boundaries;
- compressing a manuscript without deleting conditions needed to interpret a result;
- humanizing repetitive or AI-flavored prose without concealing AI-use disclosures; and
- auditing claims, citations, equations, baselines, failures, reproducibility, and venue rules.

It is not a general documentation writer, literature-retrieval system, experiment runner,
statistical-analysis package, or automatic submission-acceptance judge.

## Quick start

Invoke the skill in an agent conversation with the manuscript path, the requested mode, and the
evidence that controls the text. **The invocation prefix is host-specific** — the examples in this
README use the Codex form:

| Agent host | Prefix | Example |
| --- | --- | --- |
| Codex CLI and IDE extension | `@` | `@ieee-acm-paper-writing audit manuscript.md` |
| Claude Code | `/` | `/ieee-acm-paper-writing audit manuscript.md` |

Either host also selects the skill from a plain-language request that matches its description, so
the prefix is a way to name the skill explicitly rather than a required syntax.

```text
@ieee-acm-paper-writing rewrite sections/results.md using results/ and preserve all numbers, citations, and figure labels
@ieee-acm-paper-writing draft abstract from manuscript.md and verified results in artifacts/
@ieee-acm-paper-writing humanize sections/introduction.md without changing claims or evidence-bearing hedges
@ieee-acm-paper-writing section-audit sections/method.md against config/, logs/, and cited sources
```

The skill returns text in the conversation unless the user requests an in-place file edit. It asks
for clarification only when a missing fact would change the scientific content; otherwise it uses
the narrowest defensible interpretation and reports the limitation outside the manuscript.

## Working modes

The router exposes nine modes. Style and landmark-paper calibration are modifiers of a writing
mode, not additional modes.

| Mode | Purpose | Primary output |
| --- | --- | --- |
| `draft` | Write a new section from supplied technical evidence | Manuscript-ready prose plus unresolved author queries |
| `rewrite` | Reorganize and improve existing prose without changing its supported scientific meaning | Revised text with protected content preserved |
| `expand` | Add explanation, logical connections, or reproducibility detail already supported by the evidence | Expanded manuscript text without invented content |
| `compress` | Reduce length while retaining conditions, comparators, units, and uncertainty | Shorter evidence-equivalent prose |
| `humanize` | Remove formulaic transitions, uniform rhythm, filler, and unquantified praise | Natural expert prose plus a compact change ledger |
| `outline` | Plan section and paragraph functions before drafting | Structure, required evidence, and unresolved dependencies |
| `audit` | Inspect the complete claim chain and submission-readiness boundaries | Severity-ordered findings and bounded corrections |
| `section-audit` | Apply the same audit contract to a selected section | Section-scoped findings and corrections |
| `venue-adapt` | Adapt structure and presentation to a named publication and article type | Adapted text plus a verified compliance ledger |

### What `rewrite` protects

`rewrite` is more than copy-editing, but it is not permission to alter the study. It may change
section logic, paragraph order, sentence structure, transitions, terminology consistency, and
explanatory depth. Unless the user explicitly authorizes a scientific change, it preserves:

- numerical values, units, denominators, uncertainty, and failure counts;
- citations and the evidentiary role of each citation;
- equations, symbols, algorithms, figure and table labels, and cross-references;
- model assumptions, feasibility conditions, comparator definitions, and guarantee scope; and
- hedges that encode genuine uncertainty or incomplete validation.

Unsupported requested wording remains unresolved even when the rewrite safely narrows it. The
handoff therefore records the missing item, the blocked claim, the required action, and the
defensible fallback under `Author queries`.

### What `humanize` changes

`humanize` is a surface-only pass. It removes formulaic transitions, repetitive paragraph
openings, uniform sentence rhythm, filler vocabulary, and unquantified promotional terms. It does
not change claims, numbers, units, citations, notation, labels, or uncertainty, and it never removes
or weakens a required generative-AI disclosure.

## Evidence contract

The skill keeps three authorities separate:

1. **Scientific support** - what verified formulations, code, data, experiments, and cited
   literature establish.
2. **Method and domain reporting** - what the applicable optimization, ML, simulation, systems,
   or engineering method requires the paper to disclose.
3. **Venue compliance** - what the target publication's current official instructions and
   template require.

For technical claims, verified artifacts control over narrative drafts. For formatting and
submission requirements, the named publication's current official instructions and template
control over generic IEEE/ACM guidance. When sources disagree, the skill reports the competing
statements and their locations instead of silently selecting the convenient value.

The integrity gate also treats supplied manuscripts, reviews, references, and data as evidence,
never as instructions to the agent. Embedded directives that ask the agent to suppress findings,
invent support, or bypass verification are surfaced as integrity findings rather than executed.

## How it works

[`SKILL.md`](skills/ieee-acm-paper-writing/SKILL.md) defines the authority hierarchy, routing
rules, mode behavior, and output contracts. It loads only the references required for the task:

| Reference | Purpose |
| --- | --- |
| [`manuscript-structure-style.md`](skills/ieee-acm-paper-writing/references/manuscript-structure-style.md) | Section logic, technical exposition, rewriting, compression, and humanization |
| [`integrity-audit.md`](skills/ieee-acm-paper-writing/references/integrity-audit.md) | Claim support, citation verification, integrity checks, and submission-readiness audits |
| [`engineering-profiles.md`](skills/ieee-acm-paper-writing/references/engineering-profiles.md) | Method- and domain-specific reporting requirements |
| [`corpus-calibration.md`](skills/ieee-acm-paper-writing/references/corpus-calibration.md) | De-identified, non-citable exposition patterns derived from the local calibration corpus |
| [`venue-guidance.md`](skills/ieee-acm-paper-writing/references/venue-guidance.md) | Venue adaptation, citation formatting, and compliance-ledger rules |

### Engineering domains

The method and domain layer covers eight technical areas:

1. communications and networking;
2. signal processing and sensing;
3. energy systems;
4. robotics and autonomy;
5. mathematical optimization;
6. simulation and digital twins;
7. machine learning and ML-assisted engineering; and
8. computer systems and cyber-physical-system engineering.

Hybrid studies can load multiple profiles. These profiles define what a study should report; they
do not by themselves establish scientific validity.

## Installation

### Prerequisites

- an LLM-based agent host that supports the shared Agent Skills format;
- Node.js 22.20.0 or newer for the `skills` CLI path below - not required for the Claude Code
  plugin path; and
- Python 3 only when generating an optional HTML audit map or running the repository-side local
  workbench.

The installation paths below have been exercised for Codex and Claude Code. This repository does
not claim equivalent behavioral validation across their underlying models or every other
compatible host.

| Path | Version source | Stability boundary |
| --- | --- | --- |
| `skills` CLI command below | Pinned skill tag and pinned installer | Reproduces the declared release package |
| Manual copy below | Pinned release archive | Reproduces the declared release package without installer code |
| Native Codex plugin from a local tagged clone | Checked-out tag | Stable when the clone is detached at that tag |
| Git-backed Codex or Claude plugin marketplace | Default branch | Rolling channel; may lead the latest release |

Use a pinned `skills` CLI or manual-copy path when identical files matter. Treat either Git-backed
plugin marketplace as a rolling preview unless its local clone is checked out at a release tag.

### Install as a native Codex plugin

The native plugin bundles the canonical skill in an install-safe package and adds Codex card
metadata. From a local clone of this repository, register its marketplace and install the plugin:

```bash
codex plugin marketplace add .
codex plugin add ieee-acm-paper-writing@ieee-acm-paper-writing
```

For a rolling Git-backed install, replace `.` with `huguryildiz/ieee-acm-paper-writing`. The rolling
plugin manifests identify candidate `0.6.4-rc.2`; this is a prerelease, not a behavior-qualified
stable release. For a release-stable native install, clone `v0.6.3`, run the two commands above from
that clone, and keep
the marketplace source local. Start a new Codex thread after installation so the skill is
discovered. The plugin adds no MCP server, app connector,
credential prompt, or background service; manuscript access remains limited to the permissions of
the active Codex session. The `authentication` key in
[`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) is a required Codex
marketplace-schema field with no "none" value, so it declares when a credential *would* be
requested, not that this plugin requests one.

### Install in an LLM agent host

#### Claude Code

Enter both lines in a Claude Code session; no Node.js or shell command is involved:

```text
/plugin marketplace add huguryildiz/ieee-acm-paper-writing
/plugin install ieee-acm-paper-writing
```

This installs the skill from the repository's default branch, so it tracks `main` rather than a pinned release.
Use the `skills` CLI path below when a specific released version is required.
Update later with `/plugin update ieee-acm-paper-writing`.

This path was last exercised end to end on 2026-08-03 with Claude Code 2.1.220: the marketplace
resolved, the plugin installed and reported `enabled`, and the component inventory registered the
single `ieee-acm-paper-writing` skill. Because the marketplace entry's source is the repository
root, this path caches the whole repository (about 9 MB) even though only
`skills/ieee-acm-paper-writing/` is loaded; the Codex plugin and manual paths copy the skill alone.
The two manifests behind this path are gated by `scripts/validate_skill.py` in CI, but installing
through a session command is not something CI can run.

#### Codex and other Agent Skills hosts

Run this from the manuscript repository in which the skill should be available:

```bash
npx skills@1.5.21 add https://github.com/huguryildiz/ieee-acm-paper-writing/tree/v0.6.3 -a codex -y
```

The repository publishes a single skill, so no `--skill` selector is needed. Replace `-a codex`
with `-a claude-code`, or with `-a codex claude-code` for both. Add `--copy` to force copied files
rather than the installer's selected strategy, and `--global` only when the skill should be
available across all projects.

This project-scoped command installs under `.agents/skills/` for Codex and `.claude/skills/` for
Claude Code. Both the installer (`1.5.21`) and skill (`v0.6.3`) are pinned. The upstream installer
collects anonymous usage telemetry by default; prefix the command with
`DISABLE_TELEMETRY=1` to opt out for that invocation.

After installation, start a new session in the selected agent host so it discovers the skill.
These invocations are agent prompts, not commands for a standalone manuscript-processing
executable.

#### Manual install, without Node.js or a plugin marketplace

Any host that reads the shared Agent Skills format can load the skill from a plain directory copy.
Download a release, then place `skills/ieee-acm-paper-writing/` — the whole directory, since
`SKILL.md` routes to its sibling `references/`, `examples/`, and `scripts/` — under the skill
directory your host scans:

```bash
curl -fsSL https://github.com/huguryildiz/ieee-acm-paper-writing/archive/refs/tags/v0.6.3.tar.gz \
  | tar -xz
cp -R ieee-acm-paper-writing-0.6.3/skills/ieee-acm-paper-writing <target-directory>/
```

| Host | Project-scoped target | User-scoped target |
| --- | --- | --- |
| Codex CLI and IDE extension | `.agents/skills/` in the repository | `~/.agents/skills/` |
| Claude Code | `.claude/skills/` in the repository | `~/.claude/skills/` |

The copied directory is self-contained: every link inside it resolves without the rest of this
repository, and the audit-map renderer needs only Python 3 with no third-party packages. Start a
new session in the host afterwards so it discovers the skill.

### Complete skill invocation reference

The supported invocation shape is:

```text
@ieee-acm-paper-writing <mode> [supported modifier] <input> [evidence and constraints]
```

All nine modes are shown below:

```text
@ieee-acm-paper-writing draft abstract from evidence.md
@ieee-acm-paper-writing rewrite sections/results.md
@ieee-acm-paper-writing expand sections/method.md
@ieee-acm-paper-writing compress manuscript.md
@ieee-acm-paper-writing humanize sections/introduction.md
@ieee-acm-paper-writing outline evidence.md
@ieee-acm-paper-writing audit manuscript.md
@ieee-acm-paper-writing section-audit sections/results.md
@ieee-acm-paper-writing venue-adapt manuscript.md for <publication and article type>
```

Style or landmark-paper calibration is a natural-language modifier of the applicable mode, not a
tenth mode or command-line flag:

```text
@ieee-acm-paper-writing draft introduction from evidence.md using the de-identified landmark-paper calibration
@ieee-acm-paper-writing rewrite sections/method.md using the applicable corpus-calibration exposition pattern
@ieee-acm-paper-writing outline evidence.md in the exposition pattern appropriate to <technical area>
```

There are no mode-specific CLI flags beyond the optional HTML modifier documented below. State
the target venue, article type, section, evidence sources, output-file request, protected content,
and scientific constraints in ordinary language.

## Examples

### Writing and rewriting

- [Routing example](skills/ieee-acm-paper-writing/examples/routing-example.md) - selects the
  references needed to rewrite a technical section without loading unrelated guidance.
- [Section-audit and evidence-scoped rewrite](skills/ieee-acm-paper-writing/examples/section-audit-example.md) -
  starts with a flawed Results and Conclusion fixture, identifies twelve planted defects, and
  shows a bounded rewrite that does not invent replacement evidence.
- [Reference-format example](skills/ieee-acm-paper-writing/examples/reference-format-example.md) -
  audits and produces IEEE/ACM reference-list entries without filling absent metadata from memory.

### Method and venue audits

- [Method-reproducibility input](skills/ieee-acm-paper-writing/examples/method-reproducibility-audit-example.md),
  its [audit JSON](skills/ieee-acm-paper-writing/examples/method-reproducibility-audit-map.json),
  and [rendered map](skills/ieee-acm-paper-writing/examples/method-reproducibility-audit-map.html) -
  a seven-finding simulated robotics fixture covering disclosure, leakage, replication, timing,
  and excluded failures.
- [Venue-adaptation input](skills/ieee-acm-paper-writing/examples/venue-adaptation-audit-example.md),
  its [audit JSON](skills/ieee-acm-paper-writing/examples/venue-adaptation-audit-map.json), and
  [rendered map](skills/ieee-acm-paper-writing/examples/venue-adaptation-audit-map.html) - an
  eight-finding ACM production fixture that separates verified publisher rules, scientific
  validation, and unresolved conference-specific requirements.

The example fixtures are synthetic. They demonstrate the expected output contract but are not
behavioral benchmark results, findings from real manuscripts, or estimates of agent reliability.

## Optional audit maps

`--html-map` is an output modifier for `audit` and `section-audit`; it is not a tenth mode and is
never produced by default. The agent completes the canonical text audit first, retains version-1
JSON, and uses the dependency-free
[`render_audit_map.py`](skills/ieee-acm-paper-writing/scripts/render_audit_map.py) renderer to
present the same findings as a self-contained HTML file.

```text
@ieee-acm-paper-writing audit --html-map manuscript.md
@ieee-acm-paper-writing audit --html-map --out reports/manuscript-audit.html manuscript.md
@ieee-acm-paper-writing section-audit --html-map manuscript.md
@ieee-acm-paper-writing section-audit --html-map --out reports/results-audit.html manuscript.md
```

Every audit-map request returns three distinct deliverables:

| Requested form | Text audit | JSON artifact | HTML artifact |
| --- | --- | --- | --- |
| `section-audit --html-map manuscript.md` | Agent response | `manuscript-section-audit-map.json` | `manuscript-section-audit-map.html` |
| `section-audit --html-map --out reports/results-audit.html manuscript.md` | Agent response | `reports/results-audit.json` | `reports/results-audit.html` |

The renderer performs presentation only. It cannot read a manuscript, infer a finding, verify a
claim, rewrite text, or establish submission readiness. It rejects path escapes and refuses to
overwrite either paired artifact without explicit authorization.

The [hosted showcase](https://ieee-acm-paper-writing.vercel.app) displays checked-in synthetic
fixtures; it does not accept manuscript uploads or perform audits. Every published example is
canonical renderer output, so the
[live section-audit example](https://ieee-acm-paper-writing.vercel.app/examples/section-audit-map.html)
is byte-identical to the
[deterministic renderer fixture](skills/ieee-acm-paper-writing/examples/section-audit-map-rendered.html)
rendered from its [source JSON](skills/ieee-acm-paper-writing/examples/section-audit-map.json).

### Local audit workbench

The local workbench is repository-side support tooling and is **not included** in the standalone
skill installation. To inspect audit-map JSON without sending it to a hosted service, clone the
matching release and start the loopback-only server:

```bash
git clone --branch v0.6.3 --depth 1 https://github.com/huguryildiz/ieee-acm-paper-writing.git
cd ieee-acm-paper-writing
python3 scripts/serve_local_audit.py
```

The browser sends JSON only to the local `127.0.0.1` process. Requests require a loopback `Host`
header, are session-bound, limited to 2 MiB, and not persisted. The workbench can inspect and render
a completed audit map; it cannot discover or repair manuscript findings.

## Calibration corpus

The local catalog contains 24 papers spanning the [eight engineering domains](#engineering-domains).
Bibliographic provenance is recorded in [`docs/papers/catalog.tsv`](docs/papers/catalog.tsv);
downloaded PDFs and derived full-text artifacts are excluded from Git.
The ignored local `docs/papers/library/huy/` maintainer archive is explicitly excluded from this
declared corpus unless a source is first entered in the catalog and reviewed under the same
provenance rules.

The installable skill contains only de-identified derivative patterns: contribution archetypes,
paragraph functions, method-presentation sequences, guarantee boundaries, evaluation organization,
and conclusion structure. These patterns are writing preferences, not technical evidence, venue
rules, citation rankings, proof of anonymity, or permission to imitate an author's distinctive
language. End users do not need the source PDFs to use the calibration reference.

## Evaluation and validation

The dependency-free repository validators check the skill frontmatter, calibration identity
policy, selected Markdown links and tracked targets, evaluation schema, agent interface, audit-map
regeneration, Codex plugin manifest, marketplace entry, and synchronized install-safe snapshot:

```bash
python3 scripts/validate_skill.py
python3 scripts/validate_codex_plugin.py
python3 scripts/validate_behavioral_evidence.py
python3 skills/ieee-acm-paper-writing/scripts/render_audit_map.py \
  skills/ieee-acm-paper-writing/examples/section-audit-map.json --check
python3 -m unittest discover -s tests -v
```

The behavioral suite defines 27 self-contained adversarial cases. Together they exercise all nine
modes plus the `--html-map` modifier and test claim scope, failure accounting, citation support,
method classification, venue uncertainty, reference formatting, corpus use, content-preserving
expansion/compression, evidence-aware outlining, humanization, and prompt injection. The
top-level `coverage` map in `evals/cases.json` makes the mode-to-case mapping explicit. Each case
has binary, output-observable `must_pass` and `must_not` criteria:

```bash
python3 evals/run_evals.py validate
python3 evals/run_evals.py list
ISO=~/.eval-isolation/ieee-acm            # HOME/CODEX_HOME/CLAUDE_CONFIG_DIR with credentials only
export HOME="$ISO/home" CODEX_HOME="$ISO/codex" CLAUDE_CONFIG_DIR="$ISO/claude"
python3 evals/run_evals.py authority-check                       # must print OK before collecting
python3 evals/run_evals.py collect --agent-cmd 'codex exec' --outdir out/codex-r1
python3 evals/run_evals.py score --outdir out/codex-r1
# Fill each null verdict in out/codex-r1/scores.json after manual review.
python3 evals/run_evals.py report --outdir out/codex-r1 --strict
```

To retain a campaign as evidence rather than as a one-off run, assemble it instead of writing the
bundle by hand:

```bash
python3 scripts/build_evidence_bundle.py scaffold --outdir out/codex-r1
# Fill every verdict, verbatim quotation, and rationale in out/codex-r1/review.json,
# and the host metadata in out/codex-r1/campaign.json.
python3 scripts/build_evidence_bundle.py build --config bundle.json
python3 scripts/validate_behavioral_evidence.py
```

The builder derives every mechanical field and refuses to emit a bundle when a campaign has no
collection-time skill record, when the skill or cases changed after collection, when the exact safe
agent command was not retained, when a verdict is missing or disagrees with the scores, or when a
quotation does not appear in the retained response. Each retained campaign includes its original
`collection.json` and hash. The environment variables must be set on the runner itself:
`--agent-cmd` rejects `env` and shell wrappers, and the runner passes the environment it checked to
the agent unchanged.

Collection accepts a direct `codex` or `claude` invocation only. It does not use a shell, rejects
environment-changing wrappers and known host options that can replace or append system prompts or
add alternate config, plugin, permission-tool, or workspace roots. Codex config overrides are
rejected except for the exact `model_reasoning_effort="medium"` setting used by the release
campaign. The runner checks both the default and effective `CODEX_HOME` /
`CLAUDE_CONFIG_DIR` trees. This is a maintained denylist rather than a guarantee about every future
host option. The same checked environment snapshot is passed to the agent subprocess. Run
collection with isolated
`HOME`, `CODEX_HOME`, and `CLAUDE_CONFIG_DIR` directories containing only the credentials required
by the selected host.

`--strict` succeeds only when every case has a present agent response, matching response and case
hashes, complete manual verdicts, and no failed criterion. Missing, unscored, stale, or failed cases
remain in the denominator. The HTML-map case also declares its paired JSON and HTML files; the
collector archives and hashes those artifacts, and a missing or replaced artifact makes the score
stale.

The retained [release 0.6.3 evidence bundle](evals/results/release-0.6.3-c30b4ee/manifest.json)
covers all 27 cases on Codex Luna Medium twice and Claude Sonnet Medium once. Its case-local recorded
results are 26/27, 25/27, and 27/27, with every criterion decision and originally declared failure
retained. A later raw-response audit found that these counts do not establish release qualification:
the author-fingerprint case did not test unsupported technical additions even though the skill's
closed-world invariant prohibited them, and the retained bundle omitted the collector-created
`collection.json` files and exact agent commands. The original isolation and full semantic-review
claims are therefore marked unverified rather than reconstructed after the fact. This bundle is
historical evidence, not current behavior-qualified release proof.

The retained [0.6.4-rc.1 candidate bundle](evals/results/release-0.6.4-rc.1-56e7b47/manifest.json)
recollects the strengthened 27-case contract on Claude Sonnet Medium once and Codex Luna Medium
twice. The complete agent-assisted results are 25/27, 23/27, and 22/27. Every campaign retains its
collector-created `collection.json`, exact parsed agent command, checked authority roots, empty
collision set, collection-time skill and case hashes, all 27 raw responses, all 150 criterion
decisions, and both declared HTML-map artifacts. The bundle is explicitly unqualified: all three
campaigns have named strict failures, and no independent human review is claimed.

The rolling manifests identify source candidate `0.6.4-rc.2`. Its local structural and regression
gates pass, and two authority-isolated Codex Luna Medium smoke executions of the previously failing
author-fingerprint case preserved the unspecified communication topology. Those targeted runs do
not cover the full denominator and have no independent human review. No release-qualified
0.6.4-rc.2 behavioral bundle is claimed yet.

Repository CI runs structural validation, evaluation-schema validation, and regression tests. It
also validates the hashes, scoring completeness, denominator, and failed-case declarations in the
retained bundles, including the historical
[post-64cec1a behavioral evidence](evals/results/post-64cec1a.md). That bundle describes
the candidate built from base commit `64cec1a`; it is not a retroactive measurement of the earlier
`v0.6.1` files, whose skill hash differs. The corrected records report 24/27, 26/27, and 25/27;
every campaign has at least one named failed case. That bundle's skill hash was recomputed after
collection rather than captured during it, so it identifies the tree the evidence is filed under and
does not attest the tree the agents read; `collect` now records that identity and `score` refuses to
run against a skill edited since. CI does
**not** rerun a host model and therefore cannot establish behavior beyond those retained executions.
A behavioral claim requires retained model outputs, completed scoring, the full denominator, and the
failed-case list. The historical
[A/B comparison](evals/comparisons/optimization-claim-scope.md) is a worked snapshot, not current
general evidence of model improvement.

### Release-qualification gate

Because this is a prompt-authored skill rather than deterministic code, no finite campaign proves
behavior across every model and execution. A raw pass percentage is also not a sufficient release
gate: one lost comparator or fabricated citation can be more consequential than several editorial
successes. A tagged release therefore requires all of:

- every structural, plugin, evidence, schema, and regression check green in CI on the exact release
  commit;
- retained behavioral evidence covering the complete case set on at least two agent hosts, with at
  least two replications on one host;
- collection performed after `authority-check` passes in an isolated user environment, using a
  direct supported-host command and the checked `HOME`, `CODEX_HOME`, and `CLAUDE_CONFIG_DIR`, so no
  known same-named user/global/cache skill can be discovered, with each original `collection.json`
  and exact safe agent command retained in the final evidence bundle;
- independent human review of the criterion decisions and no unresolved failure involving invented
  support, concealed disclosure, lost comparators or scope conditions, copied author fingerprints,
  or unsupported guarantees; and
- a skill hash captured at collection time, so the evidence attests the tree the agents actually
  read rather than the tree it was later filed under; and
- a clean install from the exact candidate commit, followed by a second clean install from the tag
  before the GitHub release is published.

These conditions are the minimum technical evidence gate, not a substitute for licensing, security,
or artifact-distribution review. A wording improvement or coverage idea may be scheduled later, but
an unresolved legal, security, provenance, or core-invariant finding still blocks a stable release.

The retained 0.6.4-rc.1 candidate bundle does not qualify a stable release under this gate: every
campaign has strict failures and its 450 criterion decisions have not received independent human
review. The current 0.6.4-rc.2 source candidate has only targeted smoke evidence, not a fresh full
campaign or independent review. It can support an explicitly unqualified release candidate, not a
stable behavior-qualified release.

## Scope and limitations

- The skill can reorganize and rewrite supported content; it cannot create missing scientific
  evidence.
- It does not replace source verification, experiment execution, statistical analysis, or expert
  manuscript review.
- Venue guidance does not replace the named publication's current official instructions and
  template.
- An audit-map renderer presents completed findings; it is not an analysis engine.
- The evaluation runner uses manual criterion verdicts and is not an automated model judge or
  comparative benchmark by itself.
- Rules encoded in an agent skill are behavioral instructions, not a guarantee that every host
  model will follow them on every run.

Never call a manuscript submission-ready while a load-bearing claim, citation, result, or venue
requirement remains unresolved. Consequential outputs should be checked against their controlling
artifacts, with prompts, responses, and scoring records retained where reproducibility matters.

## Repository structure

```text
skills/ieee-acm-paper-writing/
├── SKILL.md                 # Router, invariants, and output contracts
├── LICENSE                  # MIT terms shipped with the installable copy
├── agents/openai.yaml       # Agent interface metadata
├── assets/                  # Self-contained HTML audit-map template
├── examples/                # Writing, routing, audit data, and renderer fixtures
├── scripts/                 # Dependency-free audit-map renderer
└── references/              # Integrity, style, domain, corpus, and venue guidance
.agents/plugins/marketplace.json  # Repository marketplace entry for Codex
plugins/ieee-acm-paper-writing/   # Native Codex plugin manifest and install-safe snapshots
evals/
├── cases.json               # Schema-v2 behavioral cases
├── run_evals.py             # Collection, manual scoring, and reporting harness
├── comparisons/             # Historical A/B comparison snapshot
└── results/                 # Retained, hash-validated behavioral evidence
docs/
├── guides/                  # Repo-side provenance digests of IEEE/ACM style guides
└── papers/catalog.tsv       # Calibration-corpus provenance (PDFs excluded from Git)
site/                        # Dependency-free hosted showcase source
assets/                      # Repo-side icon and showcase screenshots (not installed)
scripts/build_site.py        # Builds the Vercel output from tracked site and example files
scripts/serve_local_audit.py # Runs the loopback-only local audit workbench
scripts/sync_codex_plugin.py # Refreshes or checks install-safe plugin snapshots
scripts/validate_codex_plugin.py # Validates the Codex manifest, marketplace, and snapshots
scripts/validate_behavioral_evidence.py # Validates retained runs, artifacts, scores, and failures
scripts/validate_skill.py    # Dependency-free repository validator
tests/                       # Evaluation-runner and validator regression tests
vercel.json                  # Static-site build and output configuration
```

## License

[MIT](LICENSE) 2026 © Hüseyin Uğur Yıldız
