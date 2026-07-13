# Manuscript structure and writing style

Use this reference for section drafting, rewriting, outlining, compression, or structural style
calibration. Official venue requirements override these functional contracts.

## Contents

- Select a contribution archetype
- Section contracts
- Paragraph and prose controls
- Equations, algorithms, figures, and tables
- Reference-corpus calibration
- Modernization and prohibited imitation

## Select a contribution archetype

Select structure by contribution type before domain or citation impact:

| Archetype | Stable structural pattern |
| --- | --- |
| Foundational theorem or method | Define the object and model, state the principal result early, develop formal machinery in dependency order, then give consequences or bounded applications. |
| Algorithm plus evaluation | Name the task and failure regime, specify model and algorithm, expose implementation choices, organize experiments by claim or case, and close with supported capability plus limits. |
| Survey, tutorial, or categorical review | Declare scope and taxonomy, move from definitions to categories and relationships, synthesize gaps by axis, and separate established knowledge from open questions. |
| Vision, architecture, or position article | Begin with a system transition or abstraction failure, expose interacting layers, identify technical consequences, and end with a bounded agenda rather than a performance claim. |
| Methods reference | Build from precursors to a canonical method, conditions and stopping rules, extensions, reusable patterns, and application mappings. Use strong navigation. |

Do not blend archetypes indiscriminately. A research article may use a short survey move without
inheriting a review's breadth or a reference work's heading depth.

## Section contracts

### Title

Name the technical object, task, and distinguishing method or setting when informative. Avoid
unsupported priority, universality, superiority, and promotional terms. Use abbreviations or
symbols only when they materially improve retrieval and the target venue permits them.

### Abstract

Write a self-contained problem, gap, method, evaluation, verified principal result, and implication.
Use one paragraph unless a structured abstract is required. Include no citation, numbered equation,
undefined abbreviation, or result absent from the body.

Adapt the move sequence to the archetype:

- theorem or method: setting, formal problem, mechanism, scoped result, application boundary;
- algorithm: task and failure regime, mechanism, evaluation design, principal result, limitation;
- review: scope, organizing question, classification axes, synthesis, open gap;
- position: inadequate abstraction, consequence, and required replacement property.

Do not impose a universal word count. Verify the current venue rule.

### Introduction

Use paragraphs as argument units:

1. establish the technical object and importance;
2. specify the obstacle, contradiction, or failure regime;
3. define the model boundary or taxonomy needed to reason about it;
4. identify the closest unresolved gap by technical axis;
5. state contributions as artifacts, results, or evaluated findings;
6. preview evidence and scope;
7. add a paper map only when it improves navigation.

Make each contribution falsifiable and parallel. Distinguish formulation, implementation, dataset,
analysis, theorem, empirical result, and synthesis. Do not count one contribution at multiple
abstraction levels.

### Related work and background

Organize related work by assumption, method family, decision variable, data regime, guarantee, or
evaluation setting. End each cluster with the unresolved issue relevant to the present work. Do not
use a paper-by-paper chronology or claim novelty from rhetorical confidence.

Include only background required to understand the contribution. Separate established definitions
from the manuscript's own assumptions and design choices.

### System, physical, and problem model

Define entities, sets, signals, states, inputs, outputs, disturbances, units, and validity domain.
Separate physical behavior, measurement, communication, control, reliability, and decisions when
analytically distinct. Identify measured, calibrated, fitted, assumed, and selected quantities.

### Formulation and algorithm

Order definitions, assumptions, propositions, algorithms, and evidence by dependency rather than
discovery chronology. Define every symbol before use. Explain what each equation or constraint
does and why it is needed.

Put a result close to its assumptions and name the controlled quantity, probability statement,
asymptotic variable, and comparison object. Put an algorithm after its model and state inputs,
outputs, initialization, update order, parameters, stopping rule, and returned object.

### Experimental methodology

Specify data or instance provenance, inclusion and preprocessing, baselines, ablations, parameters,
hardware and software, time limits, seeds, replication unit, statistics, failure handling, and
artifact availability. Separate exploratory from confirmatory work and performed experiments from
plans.

### Results and discussion

Present observations before interpretation. Organize by research question, claim, failure regime,
or representative case. Keep quality, feasibility, reliability, runtime, resource cost, and
certificate quality distinct. Define metrics and denominators; report uncertainty and failures.

Use Discussion for mechanisms, alternatives, misspecification, validity, deployment trade-offs,
negative results, and generalization boundaries. Tie future work to demonstrated limitations.

### Conclusion and limitations

Reconstruct the claim chain: problem, contribution, evidence, and boundary. Distinguish proof,
observation, interpretation, and conjecture. Introduce no new result, benchmark, guarantee,
application, or citation-dependent novelty claim. Add explicit limitations when material, even if
legacy exemplars did not foreground them.

## Paragraph and prose controls

- Give each paragraph one function and one controlling claim.
- Prefer definition before abbreviation and one term per concept.
- Use signposting that names logical function: assumption, contrast, consequence, example, or
  limitation. Avoid transitions that announce only section order.
- Prefer direct technical verbs such as “defines,” “derives,” “measures,” “observes,” “indicates,”
  and “hypothesizes.”
- Calibrate certainty to evidence. Avoid promotional forecasts and unbounded novelty language.
- Preserve technical meaning during compression; do not delete conditions, comparators, units, or
  uncertainty to save words.

## Equations, algorithms, figures, and tables

- Use an equation for a necessary definition or inference, not to signal rigor. Interpret major
  equations and state their scope.
- Make pseudocode a reproducible contract. Keep variants outside the canonical algorithm.
- Use figures for architecture, taxonomy, mechanism, trajectories, or regime comparisons.
- Use tables for exact mappings, parameters, dataset summaries, and matched comparisons.
- Make captions self-contained: define encodings, units, regime, aggregation, and uncertainty.
- Avoid repeating identical data in prose, figure, and table.
- Follow current accessibility, color, resolution, and file-format rules.

## Reference-corpus calibration

When local reference papers exist, select 3-6 that match target venue era, article type, method,
domain, contribution type, and length. Extract aggregate patterns rather than prose:

- section order and allocation;
- Abstract and Introduction paragraph functions;
- contribution-list form;
- placement of related work and limitations;
- roles of equations, algorithms, figures, and tables;
- caption completeness and terminology conventions;
- qualification of claims and treatment of negative results.

If users cannot access the source PDFs, apply the anonymous patterns in `corpus-calibration.md`.
Those patterns are sufficient for structural calibration but cannot support a source attribution.

## Modernization and prohibited imitation

Treat observed corpus features as soft preferences, never venue rules. Independently add current
expectations for reproducibility, uncertainty, failures, ablations, accessibility, privacy,
security, validity threats, and disclosure.

Do not copy sentences, distinctive phrases, argument sequences, figure designs, citation clusters,
or an individual author's fingerprint. Do not invent manuscript content from reference papers.
Scientific integrity and current official instructions override every style preference.
