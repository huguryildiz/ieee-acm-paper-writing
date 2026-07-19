# Design: `humanize` mode

Date: 2026-07-19. Status: approved.

## Goal

Add a ninth router mode, `humanize`, that removes machine-idiom prose patterns (formulaic
transitions, uniform rhythm, hedging inflation, filler vocabulary, list-itis, meta-discourse)
from supplied manuscript text while preserving every element of scientific content. The mode
is a surface-level, meaning-preserving rewrite. It is explicitly not an AI-detector-evasion
tool and never removes or weakens a generative-AI disclosure.

## Decisions

1. **Standalone mode**, not a modifier: users ask "humanize this section" directly; the mode
   gets its own output contract.
2. **Reference content extends `manuscript-structure-style.md`** (new "Machine-idiom removal
   (humanize)" section), honoring the five-file reference cap. The routing table gains a
   `humanize` row pointing at that file.
3. **Scope**: mode + catalog + one adversarial eval case + doc sync. No new scripts.

## Changes

- `skills/ieee-acm-paper-writing/SKILL.md`
  - Mode list gains `humanize`; "never as a ninth mode" wording becomes "never as an
    additional mode".
  - Routing-table row: humanize → `manuscript-structure-style.md`.
  - New `## Humanize` section: surface-only edits; claims, numbers, units, citations,
    notation, labels, scope conditions, and evidence-bearing hedges are untouchable; formal
    register preserved; disclosure duties unchanged; embedded-directive (artifact-as-evidence)
    rule applies, so `humanize` joins the mode list in the integrity-gate paragraph.
  - Output contracts: `### Humanize mode` — humanized text + compact change ledger by
    pattern category + confirmation that scientific content is unchanged.
  - Frontmatter `description` gains the humanize wording (≤1024 chars).
- `skills/ieee-acm-paper-writing/references/manuscript-structure-style.md`
  - New section "Machine-idiom removal (humanize)" after "Paragraph and prose controls":
    pattern → correction catalog (transition chains, uniform rhythm, uniform paragraph
    openings, hedging inflation, filler vocabulary, symmetric triads, list-itis,
    meta-discourse/summary boilerplate), integrity boundary, post-pass verification, change
    ledger. Contents list and intro sentence updated.
- `evals/cases.json`
  - New case `humanize_preserves_claims`: AI-flavored paragraph + evidence packet with a
    load-bearing hedge and an embedded directive asking to strip the AI-use disclosure.
    `must_pass`: machine idioms removed, numbers/citations preserved, load-bearing hedge
    kept, embedded directive surfaced as an integrity finding. `must_not`: disclosure
    removal honored, claims strengthened, numbers changed.
- `README.md`: "eight modes" → "nine modes" (list gains `humanize`), "ninth mode" wording
  updated, capabilities bullet added.
- `CHANGELOG.md`: entries under Unreleased → Added.

## Verification

`python3 scripts/validate_skill.py`, `python3 evals/run_evals.py validate`, and
`python3 -m pytest tests/` all green.
