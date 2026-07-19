# Manuscript structure and writing style

Use this reference for section drafting, rewriting, outlining, compression, humanization, or
structural style calibration. Official venue requirements override these functional contracts.

## Contents

- Select a contribution archetype
- Section contracts
- Paragraph and prose controls
- Machine-idiom removal (humanize)
- Equations, algorithms, figures, and tables
- Mathematical notation and equation editing
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
7. add a paper map only when it improves navigation or the venue's convention expects one; when
   included, use the conventional closing form (“The remainder of this paper is organized as
   follows...”).

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
- Exclude promotional vocabulary (“cutting-edge,” “powerful,” “seamless”), conversational framing
  (“let's,” “we'll now dive into,” “as you can see”), and project-management terms (“sprint,”
  “backlog,” “TODO”) when they describe the authors' internal workflow rather than a defined study
  phase or technical object.
- Prefer commas, parentheses, or separate sentences over em dashes; use an em dash only when the
  user or the venue's own style asks for it.
- Preserve technical meaning during compression; do not delete conditions, comparators, units, or
  uncertainty to save words.

## Machine-idiom removal (humanize)

Use this catalog for `humanize` mode and as a soft screen during drafting and rewriting.
Humanize changes prose surface only. Scientific content — claims, numbers, units, citations,
notation, labels, scope conditions, and hedges that encode real evidential uncertainty — is
out of bounds. Integrity constraints override every pattern below. The target publication's
generative-AI disclosure policy applies unchanged to humanized text; never remove or weaken a
disclosure to make text read as human-written.

| Pattern | Correction |
| --- | --- |
| Formulaic transition chains: “Moreover,” “Furthermore,” “Additionally,” “It is worth noting that,” “It is important to note that” | Replace with signposting that names the logical function (assumption, contrast, consequence, example, limitation), or delete the transition when the logic is already clear. |
| Uniform sentence rhythm: consecutive sentences of near-equal length with identical subject-verb openings | Vary length and structure; merge choppy sentences that share one claim; split sentences that stack unrelated clauses. |
| Uniform paragraph openings: every paragraph starting with the same topic-sentence-plus-transition formula | Open some paragraphs with the finding, condition, or contrast itself. |
| Hedging inflation: “could potentially,” “may possibly,” stacked qualifiers on a claim the evidence fully supports | State the supported claim directly. Keep every hedge that encodes real uncertainty (missing tests, partial coverage, unproven generality); strengthening those is an integrity defect, not a style fix. |
| Filler intensifiers and vogue vocabulary: “delve,” “leverage,” “showcase,” “underscore,” “pivotal,” “crucial,” “comprehensive,” “seamlessly,” and “robust” as unquantified praise | Replace with the precise technical verb or drop the modifier. Keep a term that carries a defined technical meaning in context, such as robustness with a stated perturbation set. |
| Symmetric enumeration formula: rule-of-three lists everywhere, “Firstly / Secondly / Finally,” perfect parallelism across all sentences | Keep parallel structure only where the content is genuinely parallel; vary enumeration style; let unequal points take unequal space. |
| List-itis: bullet fragments where the venue expects argued prose | Convert to paragraphs that state and connect claims. Keep lists for genuinely enumerable items. |
| Meta-discourse and summary boilerplate: “In this section, we will,” “As mentioned earlier,” “In conclusion,” “In summary” openers that restate without adding | Delete, or replace with content: the section's actual claim, dependency, or consequence. |

After the pass, reread the result against the source: every claim, number, citation, symbol,
and condition must survive with unchanged meaning. Report the pass as a change ledger grouped
by pattern category; do not annotate individual edits inline in the manuscript text.

## Equations, algorithms, figures, and tables

- Use an equation for a necessary definition or inference, not to signal rigor. Interpret major
  equations and state their scope.
- Make pseudocode a reproducible contract. Keep variants outside the canonical algorithm.
- Use figures for architecture, taxonomy, mechanism, trajectories, or regime comparisons.
- Use tables for exact mappings, parameters, dataset summaries, and matched comparisons.
- Make captions self-contained: define encodings, units, regime, aggregation, and uncertainty.
- Avoid repeating identical data in prose, figure, and table.
- Follow current accessibility, color, resolution, and file-format rules.

## Mathematical notation and equation editing

These conventions follow IEEE Publication Operations editorial practice (*Editing Mathematics*) and
are the IEEE-target default. For a non-IEEE venue (e.g. an ACM target), treat them as a starting
point to verify, not house style: the target venue's current template and author instructions
override them.

### Equations as grammar

- Treat every equation, displayed or in-line, as part of the sentence. It carries a subject,
  a verb (a relation such as =, ≤, ≥, ≡), and often conditions; punctuate the surrounding
  sentence accordingly.
- Use a comma after an introductory “i.e.,” “e.g.,” “Hence,” or “That is” before an equation.
  Use a colon only after words such as “following” or “as follows.” Put no punctuation after a
  form of the verb *to be*, or between a verb or preposition and its object.
- End a displayed equation with a period when it ends the sentence; a period is the only
  terminal punctuation IEEE style permits after an equation, including after a fraction, case
  construction, or closing delimiter.
- Separate an equation from its condition with a comma and a wide space, with the condition on
  the same line (e.g., `v(t) = u(t),\quad t = 1, 2, \ldots, m.`). Separate multiple conditions
  with semicolons. Interior punctuation inside an equation carries mathematical meaning; never
  add, delete, or restyle it for looks.
- Write mathematical ellipses as exactly three baseline dots enclosed by commas:
  `i = 1, 2, \ldots, n`.

### In-line mathematics

- Break an in-line equation after a verb or operator, so the verb or operator stays on the
  upper line.
- Do not stack fractions in running text; use a solidus, negative exponent, or `exp(·)` form.
- Give collective signs (summation, product, union, integral) side-set limits in text
  (`\sum_{i=1}^{n}` rendered in-line, not display-style limits above and below).
- Replace *e* raised to a lengthy superscript with the Roman function `exp[...]`.
- Prefer fractional exponents to radical signs with long bars, e.g., write `(x + α)^{1/2}`.

### Displayed-equation breaking and alignment

- Break a multi-relation display at the verbs and align on them.
- In a single-verb equation, break at operators (+, −, ×) and align the continuation to the
  right of the verb; when the verb sits in the right half of the statement, break *before* an
  operator and align to the left of the verb.
- When breaking inside fences, break at an operator and align inside the left-hand fence. Keep
  paired fences matched in size, proportional to their contents, and nested in the hierarchy
  `{[( )]}`.
- When breaking between two adjacent fenced groups (an implied product), insert an explicit
  multiplication sign (× or ·) at the break.
- Break an integral expression after the differential when possible; otherwise break at an
  operator and align to the right of the integral sign.

### Numbering, fonts, and symbol semantics

- Number display equations consecutively through the article, e.g., (1)–(n); an appendix may
  restart as (A1), (A2). Write sub-numbers as (1a), not (1-a) or (1.a), consistently.
- Set variables in italic; set function and operator names in Roman: sin, cos, tan, exp, log,
  ln, lim, max, min, sup, inf, arg, det, diag, tr, mod, Pr, Re, Im, erf, and similar. Insert a
  thin space between a Roman function or differential and its argument (`\sin t`, not `\sint`);
  the space is unnecessary next to a verb or operator.
- Set vectors and matrices in boldface when the author distinguishes them; set descriptive
  (word-like) subscripts and superscripts, “e.g.,” “i.e.,” and “et al.” in Roman.
- Preserve the manuscript's defined semantics for near-equality and relation symbols. Meanings of
  `≈`, `≃`, `∼`, and `≅` vary across mathematical fields; do not replace one with another as a
  stylistic normalization. Verify the local definition and technical context before proposing a
  change. Do not use angle brackets ⟨ ⟩ interchangeably with the inequality signs < >.
- Style theorem-class headings (Theorem, Lemma, Proposition, Definition, Hypothesis) as
  unnumbered tertiary-level heads with their own counters, and Proof as a quaternary-level
  head, unless the venue template dictates otherwise.
- Preserve an author's algorithm environments as given — title, formatting, punctuation, and
  placement; float an algorithm to the top of a page when cited only by number or title.

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

If users cannot access the source PDFs, apply the de-identified patterns in
`corpus-calibration.md`.
Those patterns are sufficient for structural calibration but cannot support a source attribution.

## Modernization and prohibited imitation

Treat observed corpus features as soft preferences, never venue rules. Independently add current
expectations for reproducibility, uncertainty, failures, ablations, accessibility, privacy,
security, validity threats, and disclosure.

Do not copy sentences, distinctive phrases, argument sequences, figure designs, citation clusters,
or an individual author's fingerprint. Do not invent manuscript content from reference papers.
Scientific integrity and current official instructions override every style preference.
