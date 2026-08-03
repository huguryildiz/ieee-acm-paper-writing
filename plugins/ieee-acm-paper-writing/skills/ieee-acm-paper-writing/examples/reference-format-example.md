# Reference Formatting Example

Illustrative only. It shows both reference behaviors against publisher-level reference guidance:
**detecting**
and correcting broken formatting, and **producing** a correct reference from raw fields — in each
case flagging a genuinely missing field instead of inventing it. The bibliographic entries are
schematic placeholders, not real works to copy.

## Source: an IEEE reference excerpt with mechanical errors

In-text: "Several works address this problem [2]-[5], and the estimator of [7] extends it (see
also ibid.)."

Reference list:

- [2] A. Author, B. Author, C. Author, D. Author, E. Author, F. Author, G. Author, and H. Author,
  "A study of spectral estimation," IEEE Trans. Signal Process., vol. 5, no. 2, pp. 10–20, 2019.
- [7] J. K. Author, "A learned pruning method," IEEE Trans. Autom. Control, vol. 8, no. 1,
  pp. 3–9, 2021, doi: https://doi.org/10.1109/TAC.2021.123456.

## References applied

- `integrity-audit.md` for the flag-do-not-invent rule on missing bibliographic fields;
- the "IEEE reference style essentials" section of `venue-guidance.md` for the citation and
  reference-list mechanics.

## Audit findings

These are formatting defects (Editorial), not scientific defects; none of the technical claims
change.

- **Citation range.** `[2]-[5]` uses an en-dash range. IEEE writes every cited number out:
  `[2], [3], [4], [5]`.
- **Author count.** Reference [2] lists eight authors in full. IEEE lists up to six names, then the
  first author followed by "et al."
- **"ibid."** must be replaced with the explicit earlier reference number and the list renumbered
  if needed.
- **DOI field.** IEEE gives the DOI as a bare identifier (`doi: 10.1109/TAC.2021.123456`), not as a
  full `https://doi.org/` resolver URL.

## Corrected IEEE form

In-text: "Several works address this problem [2], [3], [4], [5], and the estimator of [7] extends
it (see also [4])."

Reference list:

- [2] A. Author et al., "A study of spectral estimation," IEEE Trans. Signal Process., vol. 5,
  no. 2, pp. 10–20, 2019.
- [7] J. K. Author, "A learned pruning method," IEEE Trans. Autom. Control, vol. 8, no. 1,
  pp. 3–9, 2021, doi: 10.1109/TAC.2021.123456.

## The same entries under ACM numeric style

The venue rules differ; do not carry IEEE mechanics into an ACM list. ACM orders each entry
author → year → title and keeps the full DOI resolver URL:

- [1] A. Author, B. Author, C. Author, D. Author, E. Author, and F. Author. 2019. A study of
  spectral estimation. IEEE Trans. Signal Process. 5, 2 (2019), 10–20.
- [2] J. K. Author. 2021. A learned pruning method. IEEE Trans. Autom. Control 8, 1 (2021), 3–9.
  https://doi.org/10.1109/TAC.2021.123456

## Producing a reference from raw fields (generative)

The reverse task: build a reference from supplied fields, adding nothing that is not given.

Raw fields for a journal article — authors: A. B. Carter, D. E. Fong, G. H. Iyer, J. K. Lee,
M. N. Osei, R. P. Quinn, S. T. Ustun; title: "Sparse recovery for wideband sensing"; journal:
IEEE Trans. Signal Process.; vol. 71; no. 4; pp. 1201–1215; year 2023; DOI 10.1109/TSP.2023.987654.
No publication month is supplied.

IEEE form — seven authors collapse to the first plus "et al."; given names become initials before
the surname; the DOI is a bare identifier:

- [1] A. B. Carter et al., "Sparse recovery for wideband sensing," IEEE Trans. Signal Process.,
  vol. 71, no. 4, pp. 1201–1215, 2023, doi: 10.1109/TSP.2023.987654.

ACM numeric form — order is author → year → title; ACM lists every author rather than truncating;
the DOI keeps its full resolver URL; the "(Month Year)" field shows the year alone because no month
was given:

- [1] A. B. Carter, D. E. Fong, G. H. Iyer, J. K. Lee, M. N. Osei, R. P. Quinn, and S. T. Ustun.
  2023. Sparse recovery for wideband sensing. IEEE Trans. Signal Process. 71, 4 (2023),
  1201–1215. https://doi.org/10.1109/TSP.2023.987654

The author-count rule differs by venue: IEEE caps the printed list at six names, ACM lists all.
Do not carry one venue's truncation into the other.

## External author query

"Reference [2] under ACM style omits the month of publication that the ACM Reference Format
requests in the '(Month Year)' field. Provide the issue month, or confirm it is unavailable.
Do not let the citation imply a month that the source does not establish."

Keep the author query outside the manuscript. Correct the mechanics you can verify from the given
data; never fill an unknown bibliographic field from memory.
