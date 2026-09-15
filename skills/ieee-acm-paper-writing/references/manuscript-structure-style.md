# Manuscript structure and writing style

Use this reference for section drafting, rewriting, outlining, compression, humanization, or
structural style calibration. Official venue requirements override these functional contracts.

## Contents

- Select a contribution archetype
- Section contracts
- Paragraph and prose controls
- Machine-idiom removal (humanize)
- Rhetorical-move frames (closed set)
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

After the clustered survey, narrow to the closest one or two studies and enumerate their
differences explicitly — by scope, model realism, and method — each difference checkable. Close
with a restrained gap statement scoped to what was actually surveyed, not to the field at large.

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

Give each constraint or constraint group a functional name (for example, flow conservation, energy
balance, bandwidth, or disjointness) and reuse that name when the constraint reappears in analysis.
For each, let the prose answer four questions: what it enforces, why it is needed (what breaks
without it), how its terms map to the physical system, and whether it additionally removes symmetry,
phantom flows, subtours, or infeasible configurations. Introduce every displayed equation with a
lead-in clause, and when its meaning is not self-evident, follow it with an interpretation that
names the role of each term rather than restating the algebra.

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

For each figure, table, or experiment, follow a five-step sequence: identify what is shown and its
axes; state the dominant trend in one sentence; quantify it with exact values, units, and
comparator-scoped percentage changes; give the mechanism, grounded in the model and labeled as a
hypothesis when it is one; and state the design implication. Do not narrate every plotted point;
cover the dominant trend, the exceptions, and the implication.

Use Discussion for mechanisms, alternatives, misspecification, validity, deployment trade-offs,
negative results, and generalization boundaries. Tie future work to demonstrated limitations.

### Conclusion and limitations

Reconstruct the claim chain: problem, contribution, evidence, and boundary. Distinguish proof,
observation, interpretation, and conjecture. Introduce no new result, benchmark, guarantee,
application, or citation-dependent novelty claim. Add explicit limitations when material, even if
legacy exemplars did not foreground them.

## Paragraph and prose controls

- Give each paragraph one function and one controlling claim.
- In exposition of a model, method, or formulation, write for a reader who does not already know
  the passage: state what the component does, how its parts produce that behavior, and why it
  matters for the problem. Build this pedagogical clarity by explaining connections already present
  in the evidence, never by adding claims, mechanisms, or interpretations the source does not
  support. Results interpretation still follows the results-before-interpretation and
  Discussion-placement rules of the section contracts.
- Make an abstract statement concrete using only material already in the evidence: ground a
  constraint or mechanism in the specific instance it refers to (a named node, set, quantity, or
  condition) when this aids understanding. Never invent an instance, value, or example to
  illustrate a point.
- When two objectives or effects conflict, state both directions before motivating a joint
  treatment: name what increasing the design variable improves and what it worsens, then explain
  why optimizing the objectives independently fails.
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
| Metaphor and vogue nouns: “tapestry,” “realm,” “journey,” “landscape” (figurative), “myriad,” “plethora” | Replace with the literal technical noun plus a count or set, e.g. “many” or the actual number. |
| Stock importance and momentum phrases: “paving the way,” “shed light on,” “a testament to,” “plays a crucial/vital/key role,” “underscores/highlights the importance of,” “In today's world,” “In recent years, there has been growing interest in” | Delete, or replace with the specific consequence, mechanism, or a dated and sourced trend that makes the point checkable. |

After the pass, reread the result against the source: every claim, number, citation, symbol,
and condition must survive with unchanged meaning. Report the pass as a change ledger grouped
by pattern category; do not annotate individual edits inline in the manuscript text.

### Plain-lexicon substitutions

Prefer the short common word; keep a longer word only in its defined technical sense. Apply during
drafting, rewriting, and humanizing, never at the cost of a term's technical meaning.

| Avoid | Prefer |
| --- | --- |
| utilize | use (keep “utilization” as a technical term, e.g. bandwidth utilization) |
| demonstrate | show |
| facilitate | enable, allow |
| in order to | to |
| prior to | before |
| subsequently | then |
| numerous | many |
| possess | have |
| commence | begin |
| endeavor | attempt |
| ascertain | determine |
| elucidate | explain |
| aforementioned | this/that + noun |
| leverage (verb) | use, exploit |
| methodology | method (unless the methodology itself is the subject) |

### Before and after

Generic illustrations of the controls above. They are patterns to apply, not text to copy.

- Promotional claim to verifiable statement.
  - Before: *Our novel framework achieves remarkable gains across a plethora of realistic scenarios,
    demonstrating its great potential.*
  - After: *The proposed method reduces peak per-unit cost by 18.4% on average over 20 randomized
    instances (Table III).*
- Redundant motivation to a single statement plus a new layer.
  - Before: *Energy efficiency is crucial because batteries cannot be replaced. […] Since replacing
    batteries is infeasible, energy-efficient operation is of utmost importance.*
  - After: *Because batteries cannot be replaced in the field, the system lifetime is set by the
    energy budget of the most heavily loaded unit. This coupling turns a local operating decision
    into a system-level design problem.*
- AI-flavored prose to humanized plain academic English.
  - Before: *Moreover, our comprehensive evaluation demonstrates remarkable improvements,
    highlighting the potential of the approach and paving the way for robust, scalable, and reliable
    deployments.*
  - After: *Joint optimization extends the objective by 21.7% on average over the sequential
    baseline across 20 instances (Table IV). The gain comes from the solver's freedom to trade one
    cost against another, which the sequential design fixes in its first stage.*

## Rhetorical-move frames (closed set)

Sentences that perform a rhetorical move — importance, gap, purpose, method choice, result,
interpretation, limitation, transition — use either a frame from the inventory below or a plain
declarative sentence. The inventory is a closed set, not a quota: no frame is mandatory, and the
blocked patterns at the end of this section are never used. It is a derivative distillation of a
public academic phrasebook, rewritten as engineering templates, and is not citable.

Three conditions govern every use. A frame supplies sentence shape only: fill X, Y, and every
bracketed slot from the evidence alone, and drop the frame when a slot has no filler there. An
importance or gap frame becomes available only when the evidence packet states that importance or
that gap; otherwise open with the technical object itself. Scope a gap to the set actually
surveyed, meaning what those studies do not report, never what the field has never done.

Frames by move:

- **Establishing importance or motivation** (evidence must state it):
  - “X is required for Y under [stated condition].”
  - “X sets the [named bound, cost, or limit] on Y.”
  - “In [stated setting], X determines Y.”
- **Stating a gap or unresolved issue** (evidence must state it):
  - “Previous work on X has not addressed Y.”
  - “The studies surveyed here report X but not Y.”
  - “[Prior method] was evaluated on X; its behavior on Y is not reported.”
  - “Whether X holds under [condition] is unresolved in the surveyed work.”
  - “The closest study differs from this work in [named axis].”
- **Stating purpose, scope, and contribution**:
  - “This paper addresses [task statement].”
  - “The objective of this study is to [verb] X under [stated conditions].”
  - “This paper formulates X, implements Y, and evaluates it on Z.”
  - “The contributions are [artifact], [result], and [evaluated finding].”
  - “X lies outside the scope of this paper.”
- **Defining and classifying**:
  - “The term X denotes Y.”
  - “Throughout this paper, X refers to Y.”
  - “X is defined as Y, with [units and validity domain].”
  - “X is classified into [n] types by [stated criterion].”
- **Describing method choice and procedure**:
  - “X was measured with Y.”
  - “X was selected because [stated reason].”
  - “For [stated purpose], X was used.”
  - “The instance set consists of [n] cases with [stated properties].”
  - “X was computed with [named tool and version].”
- **Reporting a result**:
  - “Table [n] reports X for Y.”
  - “X was [value, unit] under [stated condition].”
  - “X changed by [value] relative to [named comparator].”
  - “[n] of [N] runs [outcome].”
  - “No difference between X and Y was detected at [stated test and level].”
- **Interpreting and hedging** (hedge strength matches the evidence, never the ambition):
  - “These results suggest that X.”
  - “It is therefore possible that X.”
  - “X is consistent with Y; the present design does not identify the cause.”
  - “A possible explanation is X, which this study does not test.”
- **Agreeing or disagreeing with prior results**:
  - “These results agree with [cited work] for X.”
  - “These results differ from [cited work], which reported Y.”
  - “[Cited work] measured X under [different condition], so the two are not directly comparable.”
- **Stating a limitation, boundary, or the work it requires**:
  - “A limitation of this study is X.”
  - “This study did not evaluate X.”
  - “These results are limited to [stated regime] and were not tested outside it.”
  - “Generalization of X to Y is not established here.”
  - “The audited work does not report X, so Y cannot be checked.”
  - “Establishing whether X holds under Y requires [named experiment].”
- **Contrasting, comparing, and transitioning**:
  - “X differs from Y in [named axis].”
  - “Compared with X, Y [verb] by [quantified difference].”
  - “In contrast to X, Y does not [property].”
  - “This interpretation differs from that of [cited work], which [claim].”

### Blocked frames

Do not use the patterns below in any mode. Each asserts something the evidence rarely carries.
Where the packet does supply the underlying fact, use the plain form named with it; where it does
not, the sentence has no basis at all.

- Promotional importance: “plays a vital, pivotal, crucial, or key role”; “is fast becoming a key
  instrument”; “is essential for a wide range of.” Plain form: what X fixes, and under which
  condition.
- Unbounded literature claims: “a growing body of literature”; “considerable critical attention”;
  “a much debated question”; “has been extensively studied.” Plain form: the count and the
  boundary of the set actually read.
- Surprise framing: “surprisingly, X has not been examined”; “the most striking result to emerge”;
  “a remarkable result.” Plain form: the value and its comparator.
- Priority and originality: “the first study to”; “fills a gap in the literature”; “sheds new
  light on.” Plain form: the artifact and what it was evaluated against.
- Era framing: “in recent years, there has been an increasing amount of literature on”; “over the
  past decades the field has seen a stunning transformation.” Plain form: a dated, sourced
  observation, or nothing.
- Evaluative praise of a cited work: “in his excellent study”; “this ground-breaking analysis.”
  Plain form: what that work did, and what it did not report.
- Counterfactual critique: “the study would have been more convincing if the authors had.” Plain
  form: the missing item and what reporting it would make checkable.

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

When a request asks for an identifiable author's personal prose or makes generated text appear to
be that author's work, decline that style constraint. Give an explicit causal reason, using
"because" or an equivalent construction: an individual textual fingerprint belongs to that author,
is not a transferable corpus pattern, and reproducing it would misrepresent authorship. Merely
announcing a neutral alternative does not explain the refusal. Still complete the substantive
writing task in a neutral scholarly voice, using only high-level structural and reasoning patterns
that do not imitate the author. Declining the style constraint does not relax the closed-world
gate: recheck the neutral alternative after the refusal, including small grammatical complements
that would add an actor, receiver, scope, capability, or causal relation.
