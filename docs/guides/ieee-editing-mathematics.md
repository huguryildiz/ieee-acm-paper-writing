# IEEE mathematics-editing provenance note

This repository-side note identifies the external guidance consulted when the skill's
mathematics-editing rules were designed. It is not installed with the skill and is not a
substitute for the source.

- Source: IEEE Publication Operations, *Editing Mathematics*, version 10.27.2023,
  copyright IEEE 2023.
- Official copy: <https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/Editing-Mathematics.pdf>
- Last checked: 4 August 2026.
- Skill location informed by this source:
  [`manuscript-structure-style.md`](../../skills/ieee-acm-paper-writing/references/manuscript-structure-style.md),
  under “Mathematical notation and equation editing.”
- Precedence: current venue instructions and the current official IEEE guide control whenever
  they differ from this repository's synthesis.

## Rights and use boundary

The IEEE document remains a third-party copyrighted work. This note deliberately does not
reproduce its paragraphs, tables, symbol inventories, glossary, examples, or section structure.
It records only a maintainer-authored summary of the editing concerns that were translated into
the skill. Anyone who needs exact wording, examples, or production specifications must consult
the official copy.

## Maintainer-authored synthesis

The skill encodes the following high-level review questions:

- Does surrounding prose treat each displayed expression as part of the sentence that contains
  it, including the necessary grammatical connection and punctuation?
- Are line breaks chosen so that relations and operators remain readable and repeated alignment
  points are visually consistent?
- Have inline expressions been kept compact enough for prose, with tall constructions rewritten
  when they would disrupt line spacing?
- Are equation labels, appendix labels, and cross-references internally consistent and compatible
  with the selected venue template?
- Are variables visually distinguished from named functions, operators, units, abbreviations,
  and other upright text?
- Are vectors, matrices, differentials, indices, delimiters, and spacing used consistently with
  the manuscript's declared notation?
- Have the author’s mathematical meaning and intentionally chosen symbols been preserved during
  stylistic editing?
- When an expression is ambiguous or an image-based source cannot be interpreted reliably, is an
  author query raised instead of reconstructing missing mathematics?

These questions are editorial checks, not mathematical-validity guarantees. Passing them does not
show that a derivation is correct, that notation is complete, or that a venue will accept the
manuscript.

## Update procedure

When the external guide changes:

1. Compare the current official edition with the skill's existing rules.
2. Record only the resulting rule-level change; do not copy source prose or examples.
3. Keep venue-specific requirements in `venue-guidance.md`, not in scientific-integrity rules.
4. Re-run the repository validators after any linked skill file changes.
