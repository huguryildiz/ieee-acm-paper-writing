# Contributing

This repository packages and validates the installable skill under
`skills/ieee-acm-paper-writing/`. Repository-side evaluation, documentation, and showcase tooling
does not install with the skill.

## Required local checks

Run the same five gates as CI before opening a pull request:

```bash
python3 scripts/validate_skill.py
python3 scripts/validate_codex_plugin.py
python3 evals/run_evals.py validate
python3 scripts/validate_behavioral_evidence.py
python3 -m unittest discover -s tests -v
```

If the canonical installable skill changes, synchronize the native Codex snapshot and rerun the
checks:

```bash
python3 scripts/sync_codex_plugin.py --write
python3 scripts/validate_codex_plugin.py
```

## Behavioral evidence boundary

Passing validators establishes structural and retained-record consistency; it does not establish
that model outputs satisfy the criteria semantically. A release-qualified campaign must retain the
raw responses, every criterion decision, evidence quotations, failure list, generated artifacts,
and the collector-created `collection.json` for each run. Do not recreate a missing collection
record after the run.

Any change to `skills/ieee-acm-paper-writing/` or `evals/cases.json` invalidates current-candidate
behavioral qualification and requires the complete case denominator to be recollected before a
stable behavior-qualified release.

## Scope and rights

Do not commit downloaded papers, publisher text exports, or third-party style-guide prose. Keep
repo-side guide files to original summaries and links to the authoritative source. Preserve the
three-concern separation among scientific support, method/domain reporting, and venue compliance.
