# Scientific integrity and manuscript audit

Use this reference whenever drafting, changing, or auditing a scientific claim, and for
submission-readiness or cross-section review.

## Contents

- Evidence classes and claim ledger
- Citation and quantitative integrity
- Guarantee, statistical, and causal boundaries
- Reproducibility and negative evidence
- Audit procedure and severity
- Cross-section consistency

## Evidence classes and claim ledger

Classify each load-bearing statement before writing it:

- **verified fact**: directly supported by an inspected source artifact;
- **model assumption**: imposed to make analysis possible;
- **method choice**: selected by the authors rather than established by evidence;
- **hypothesis or interpretation**: plausible but not directly observed;
- **planned work**: not yet executed;
- **simulated result**: generated under an explicit model and scenario;
- **empirical result**: observed from a declared experiment or dataset;
- **external claim**: supported by a verified primary or authoritative source.

Maintain a claim ledger with: claim, evidence artifact, location, scope, uncertainty, comparison,
and allowed wording. If evidence is missing, omit the claim or return an external author query.
Never repair missing evidence with fluent prose.

Apply this authority order for technical claims:

1. verified data, experiment artifacts, solver logs, certificates, and test outputs;
2. implemented code and configuration actually used;
3. formal model specifications and recorded project decisions;
4. current primary literature and authoritative standards;
5. narrative notes and manuscript drafts.

Report conflicts. Do not silently select the convenient source.

## Citation and quantitative integrity

- Verify identity, version, year, and persistent identifier against an authoritative record.
- Read the relevant passage. Metadata correctness does not establish claim support.
- Distinguish primary evidence from surveys, tutorials, perspectives, and research agendas.
- Scope the citing sentence no more broadly than the source evidence.
- Do not use citation count, publication venue, or author reputation as proof of correctness.
- Do not invent citations, identifiers, page numbers, datasets, or standards.

For every number, record unit, denominator, population or instance set, aggregation, uncertainty,
and source artifact. Check tables, figures, abstract, body, and conclusion for identical definitions.
Do not report a percentage without its denominator or a relative change without the comparator.

## Guarantee, statistical, and causal boundaries

Attach every guarantee to its assumptions, feasible region, algorithm variant, tolerance,
probability mode, data regime, and certificate. Distinguish:

- theoretical rate from wall-clock behavior;
- approximation bound from observed solution quality;
- model optimality from deployment quality;
- a feasible incumbent from a certified optimum;
- sampled-problem behavior from population or distribution guarantees;
- physical regularization from exact physical satisfaction.

For statistical claims, state the sampling or replication unit, sample size, dependence structure,
test, effect size, interval, multiplicity treatment, missing-data handling, and analysis status.
Keep statistical significance, practical importance, and robustness separate. Do not treat seeds,
time steps, pixels, packets, or repeated measurements from one underlying realization as
independent samples without justification.

Use causal language only when the design identifies a causal effect and the assumptions are
defended. Otherwise use association, prediction, comparison, or mechanism-consistent language.

## Reproducibility and negative evidence

Report versions and identities for data, code, configuration, environment, hardware, seeds,
models, solver or simulator, and preprocessing. State selection, stopping, exclusion, and failure
rules. Distinguish deterministic reruns from statistical reproducibility across runs.

Include failed, infeasible, timed-out, unstable, negative, and disconfirming cases when they belong
to the evaluated set. Do not condition headline results on success without reporting the excluded
fraction and scientific consequence.

Archived, synthetic, mock, expected, or planned artifacts cannot support completed-result
language. A public artifact is not automatically independently reproduced.

## Audit procedure and severity

Audit read-only unless the user requests edits. Inspect the manuscript and controlling evidence,
then build a cross-section claim matrix. Test each claim adversarially:

1. What exact artifact supports it?
2. Does the artifact establish the same object, metric, regime, and comparator?
3. Which assumptions or exclusions narrow it?
4. Is contradictory or failed evidence omitted?
5. Does another section state a stronger version?
6. Would a reasonable reader infer more than the evidence supports?

Classify findings:

- **Critical**: fabricated or contradicted evidence, invalid load-bearing result, false guarantee,
  unrecoverable reproducibility failure, or material ethics/compliance defect;
- **Major**: unsupported central claim, invalid comparison, missing assumption, leakage, incorrect
  statistic, or external-validity overreach;
- **Minor**: localized ambiguity, incomplete reporting, notation inconsistency, or weak but
  repairable qualification;
- **Editorial**: wording or presentation issue with no change to scientific meaning.

For each finding give location, claim, evidence or missing evidence, consequence, and concrete
correction. Do not create empty severity sections.

## Cross-section consistency

Check that:

- abstract and conclusion contain no claim absent from the verified body;
- contributions match delivered artifacts and evaluated findings;
- notation, units, datasets, baselines, metrics, and sample counts are stable;
- method choices described in prose match code and configuration;
- results match displayed tables and figures;
- discussion distinguishes observation, interpretation, mechanism, and generalization;
- limitations cover material internal, construct, and external validity threats;
- venue rules and disclosure statements are verified separately from scientific claims.

Never call a manuscript submission-ready while a load-bearing claim, citation, result, or venue
requirement remains unresolved.
