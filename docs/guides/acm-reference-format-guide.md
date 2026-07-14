# ACM Reference Format and Submission Template — rules digest

Repo-side documentation; not installed with the skill. This digest records the author-facing
formatting rules from ACM's master submission template — the "ACM Reference Format," its worked
reference examples, and the manuscript-structure conventions — that inform the skill, so their
provenance survives independently of the source document.

- Source: Association for Computing Machinery, *Submission Template for ACM Papers* (Word master
  article template; single-column submission version). Accessed 14 July 2026 via a published copy
  supplied by the maintainer. Authoritative distribution:
  [ACM author resources](https://www.acm.org/publications/authors/reference-formatting).
- Encoded in the skill: "ACM reference format essentials" in
  [`venue-guidance.md`](../../skills/ieee-acm-paper-writing/references/venue-guidance.md).
- Precedence: the current official template and venue-specific author instructions override
  everything below. ACM SIGs and journals customize this template; never assume one page limit,
  section order, citation mode, or rights model across all ACM venues.
- Schematic by construction: the reference formats below use placeholder authors, titles, and
  identifiers rather than the source document's worked citations, matching the anonymized
  convention used for the IEEE digests in this directory.

## Citation modes

- ACM venues use one of two in-text modes: **numeric** brackets ("as shown in [5]") or
  **author-year** ("as shown in [Harel 1978]"). A manuscript uses one mode throughout.
- The production workflow generates final citation labels from the reference list after
  acceptance. Before that, keep numeric numbers or a "primary-author last name + year" placeholder
  consistent with the chosen mode.
- The "ACM Reference Format" block at the top of a processed article (author list, year, full
  title and subtitle, venue, publisher, city, page count) is generated automatically after
  acceptance; authors do not hand-build it in the submission version.

## Reference-list mechanics

- Order every entry author(s) → year → title: "A. B. Author, C. D. Author, and E. F. Author. Year.
  Title of work." Use full given names as printed when available; join the final author with "and."
- The year follows the author list immediately and stands as its own sentence; the title ends with
  a period.
- Close a reference carrying a DOI with the full resolver form (a doi.org URL) and no trailing
  period. Older ACM output prefixes it with "DOI:"; the current form is the bare resolver URL.
- The reference section carries a "REFERENCES" heading; entries use the template's `Bib_entry`
  style. Acknowledgments (with `GrantSponsor` / `GrantNumber` styles) sit **before** the
  references.
- For journals and PACMs, history dates follow the references: "Received Month Year; revised Month
  Year; accepted Month Year." The revised date is optional.

## Schematic reference formats by source type

- **Journal / magazine article** — A. B. Author and C. D. Author. Year. Title of article. Abbrev.
  Journal Name vol, no (Month Year), page–page. *DOI resolver URL.* Use "Article N" plus a page
  count ("Article 5 (April 2007), 50 pages") when the venue numbers by article; "13–es" marks an
  electronic-supplement page.
- **Proceedings paper** — A. B. Author and C. D. Author. Year. Title of paper. In Proceedings of
  the Full Conference Name (Acronym 'YY). Publisher, City, State, Country, page–page. *DOI resolver
  URL.* Spell the publisher as the venue prints it ("Association for Computing Machinery, New York,
  NY, USA"; "ACM, New York"; "USENIX Association, Berkeley, CA"); use "Article N, M pages" for
  article-paginated proceedings.
- **Book** — A. B. Author. Year. Title of Book (Nth ed.). Publisher, City, State.
- **Edited book / series volume** — A. B. Editor (Ed.). Year. Title of Book (Nth ed.). Series Name,
  Vol. N. Publisher, City. *DOI resolver URL.*
- **Technical report** — A. B. Author and C. D. Author. Year. Title of Report. Technical Report No.
  XXX. Institution, City, State.
- **Ph.D. dissertation** — A. B. Author. Year. Title. Ph.D. Dissertation. University, City, State.
  Append "UMI Order Number: XXX" when supplied.
- **Master's thesis** — A. B. Author. Year. Title. Master's thesis. University, City, Country.
- **Website / online reference** — A. B. Author. Year. Title. Retrieved Month day, year from URL.
  For a corporate or undated source: author, then "Retrieved from URL."
- **Software** — A. B. Author or Team. Year. Name of Software. Publisher or Foundation, City,
  Country. URL.
- **Dataset** — A. B. Author and C. D. Author. Year. Title of Dataset. Retrieved Month day, year
  from URL, or close with a DOI when one exists.
- **Patent** — A. B. Author. Year. Title. (Month Year). Patent No. XXX, Filed date, Issued date.
- **Video** — A. B. Author. Year. Title. Video. In Venue (dates). Publisher, City, page. *DOI
  resolver URL* — or "Video. (date). Retrieved Month day, year from URL" for online video.
- **Preprint** — A. B. Author. Year. Title. arXiv:XXXX.XXXXX. Retrieved from the arXiv abstract
  URL.

## Manuscript-structure conventions from the same template

These are recorded for provenance; the skill applies them through `venue-guidance.md` and
`manuscript-structure-style.md`, not from this file.

- **Single-column submission.** The review version is one column with no headers, footers, or
  author-supplied page numbers; production adds output design after acceptance. Do not alter the
  template's paragraph styles or margins.
- **Indexing metadata.** Insert CCS concepts from the ACM Computing Classification System (with the
  matching XML pasted into the document properties) and author-supplied keywords. Every author of
  an accepted article must supply an ORCID iD.
- **Accessibility is mandatory, not optional.** Build tables with native table markup and marked
  header rows — never as images. Give every non-decorative figure a plain-text figure description
  (alt text) that adds information beyond the caption. Keep figures usable in grayscale by
  referring to shapes and patterns rather than color alone.
- **Floats.** Insert tables and figures after their first in-text reference. Table captions sit
  above the table (`TableCaption`); figure captions below (`FigureCaption`).
- **Math.** Numbered display equations use the `DisplayFormula` style with a right-hand equation
  number; unnumbered ones use `DisplayFormulaUnnum`. Text immediately after a display equation
  takes the `ParaContinue` style. Theorems, lemmas, and proofs use the `Statements` style.
- **Anonymization.** For double-blind review, omit author and affiliation details, clear the
  author metadata field, and remove acknowledgments, identifying citations, and related-work
  discussion that would reveal authorship. Any required generative-AI disclosure must not leak
  author identity, and an AI tool is never listed as an author.
- **Rights and access.** ACM has moved to a fully open-access model; confirm whether an accepted
  article is covered by an institutional agreement (e.g. ACM Open) or carries an article-processing
  charge. Treat this as an author obligation to resolve, not a formatting detail.
