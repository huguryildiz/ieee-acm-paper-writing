# Local paper corpus

Use this directory for the reference papers used to calibrate the skill. Downloaded papers and
derived local artifacts are intentionally excluded from Git; only this guide, `catalog.tsv`, and
the empty directory skeleton are tracked.

## Workflow

1. Put new, unsorted downloads in `library/inbox/`.
2. Move each paper to the matching domain directory after checking its title and DOI.
3. Use the `local_file` value in `catalog.tsv` when practical.
4. Record any replacement DOI, version-of-record issue, or access limitation in the catalog.
5. Do not commit PDFs, extracted full text, publisher packages, or supplementary archives.

The corpus is a calibration and retrieval aid. Inclusion does not make a paper an authority for
venue formatting, prove that its claims are correct, or authorize sentence-level imitation.

Derived, non-citable synthesis is stored in the skill's anonymous
`references/corpus-calibration.md`. It transfers technical exposition, structural, and rhetorical
patterns without bibliographic identities or copied prose. Use `catalog.tsv` and the source PDF to
verify any claim that will be attributed to a paper.

## Structure

```text
docs/papers/
├── README.md
├── catalog.tsv
└── library/
    ├── inbox/
    ├── communications-networking/
    ├── signal-processing-sensing/
    ├── energy-systems/
    ├── robotics-autonomy/
    ├── mathematical-optimization/
    ├── simulation-digital-twins/
    ├── ml-assisted-engineering/
    └── computer-cyber-physical-systems/
```
