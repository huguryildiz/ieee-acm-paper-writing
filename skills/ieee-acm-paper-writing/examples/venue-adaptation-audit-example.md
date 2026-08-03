# Venue-Adaptation Audit Example (Live Test Fixture)

This self-contained fixture exercises `venue-adapt --html-map` on a plausible production-stage
ACM proceedings package. The package is synthetic. It deliberately withholds the conference and
track so that general publisher requirements can be separated from venue-specific review,
anonymity, and length rules.

General ACM production rules used by the fixture were checked on 3 August 2026 against the
[official `acmart` class guide](https://portalparts.acm.org/hippo/latex_templates/acmart.pdf) and
[ACM's LaTeX best-practices guide](https://authors.acm.org/binaries/content/assets/publications/taps/latex-best_practices-06-may-2020.pdf).
Those sources do not establish the unidentified conference's submission rules.

## Synthetic package record

- Package label: “three-page ACM proceedings paper, final source.”
- No conference name, track, author instructions, rights-form metadata, or page-limit source is
  supplied.
- `architecture.pdf` is an informational system diagram, not a decorative image.
- `example.bib` contains a synthetic placeholder entry rather than citable source metadata.
- No scientific data, analysis record, citation ledger, or conference-specific compliance
  checklist is supplied.

## Flawed source excerpts

Copy the package record and the fenced blocks below into a fresh session when running the live
test.

```latex
\documentclass[sigconf]{acmart}
\usepackage[margin=0.62in]{geometry} % fit the paper into three pages
\settopmatter{printacmref=false} % save space

\begin{document}
\title{Latency-Aware Coordination for Edge Systems}
\begin{abstract}
We present a coordination mechanism for latency-sensitive edge workloads.
\end{abstract}

% The CCS Concepts block was deleted because the terms are not part of the
% scientific argument.
\keywords{}

\begin{figure}
  \includegraphics[width=\linewidth]{architecture.pdf}
  \caption{System architecture.}
\end{figure}

\bibliographystyle{ACM-Reference-Format}
\bibliography{example}
\end{document}
```

```bibtex
@article{placeholder,
  author = {Researcher, J. Q.},
  title = {Example Article},
  year = {2025}
}
```

```text
Submission note: Once the source passes ACM production validation, the reported results are
scientifically validated and the paper is submission-ready.
```

## Expected audit boundary

A correct run must first request the exact conference and track. It may then apply only the
publisher-level production rules verified above: retain the `acmart`-controlled layout, restore
required reference metadata, supply CCS concepts and keywords for this three-page production
fixture, add a meaningful figure description, and replace placeholder bibliography metadata from
an authoritative record. It must keep production validation separate from scientific validity and
must not invent conference-specific anonymity, mode, page-limit, rights, or disclosure rules.

The corresponding canonical map data are in
[`venue-adaptation-audit-map.json`](venue-adaptation-audit-map.json); the checked-in HTML is
generated from that JSON. The retained map records one application of the current skill to this
synthetic fixture. It is an example of the output contract, not a submission-readiness decision or
a benchmark.
