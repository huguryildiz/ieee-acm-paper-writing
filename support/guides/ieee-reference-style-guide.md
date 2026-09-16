# IEEE reference-style provenance note

This repository-side note identifies the external guidance consulted when the skill's IEEE
reference-review rules were designed. It is not installed with the skill and is not a substitute
for the source.

- Source: IEEE Publication Operations, *IEEE Reference Guide*.
- Official access point:
  [IEEE Editorial Style Manual](https://journals.ieeeauthorcenter.ieee.org/your-role-in-article-production/ieee-editorial-style-manual/),
  which links the current reference guide and related author resources.
- Last checked: 4 August 2026.
- Skill location informed by this source:
  [`venue-guidance.md`](../../skills/ieee-acm-paper-writing/references/venue-guidance.md),
  under “IEEE reference style essentials.”
- Precedence: the current official guide and the named venue's author instructions control
  whenever they differ from this repository's synthesis.

## Rights and use boundary

The IEEE guide remains a third-party copyrighted work. This note deliberately does not reproduce
its paragraphs, worked references, source-type catalog, publisher list, periodical list, or
abbreviation tables. It records only a maintainer-authored summary of the checks translated into
the skill. Anyone who needs an exact reference form or an official abbreviation must consult the
current IEEE source.

## Maintainer-authored synthesis

The skill encodes the following high-level review questions:

- Does every in-text citation use the manuscript's chosen IEEE numbering convention consistently,
  including punctuation and references to specific pages, sections, equations, or figures?
- Does each bibliography entry describe exactly one source, and can the cited source be identified
  from the supplied metadata without inventing absent fields?
- Are author names, title, container, publication details, date, persistent identifier, and access
  information included only when the manuscript or a verified record supplies them?
- Does the entry type match the source actually cited, rather than forcing a journal-like form onto
  software, data, standards, patents, theses, reports, web material, or unpublished work?
- Are DOI and URL fields normalized without silently changing the identifier or asserting that a
  link resolves when it has not been checked?
- Are journal and conference title abbreviations taken from an authoritative venue record or the
  current IEEE resources rather than guessed from memory?
- Are incomplete, contradictory, or inaccessible records surfaced as author queries instead of
  being completed with plausible-looking metadata?
- Are venue-specific requirements kept separate from scientific-support judgments, so a
  well-formatted reference is not treated as evidence that the cited source supports a claim?

## Deliberate exclusions

This repository does not mirror IEEE's reference examples or controlled abbreviation lists. It
also does not freeze a universal reference template: requirements can differ by source type,
publication, and revision of the official guidance. The skill therefore audits supplied records
conservatively and directs exact-format questions to the current official source.
