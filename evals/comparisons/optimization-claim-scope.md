# Historical A/B Comparison: Optimization Claim Scope

This comparison records one controlled, non-deterministic model run per condition. It is a
worked example, not evidence that the skill is generally superior. The scientific data below
are a synthetic evaluation fixture and must not be cited as an empirical study result.

> **Status:** Historical snapshot. The recorded runs predate the current five-reference
> architecture. Their prompts, outputs, and assessment are preserved as executed and must not be
> represented as a validation of the current skill. A fresh controlled run is required for a
> current comparison.

## Controls

- Date: 2026-07-14
- CLI: Codex 0.142.5
- Model: `gpt-5.5`
- Reasoning effort: `none`
- Execution: ephemeral, read-only, no web access
- Shared task and evidence: identical across conditions
- Baseline condition: instructed not to use or inspect any skill, repository, file, or web
  source; executed outside the repository
- Skill condition: instructed to use `skills/ieee-acm-paper-writing/SKILL.md` and its required
  references, but forbidden from reading `README.md`, `evals/`, or the skill's `examples/`
- Skill snapshot: pre-consolidation reference layout; exact historical file set was not sealed in
  this comparison artifact
- Replications: one per condition

The two runs therefore isolate skill access reasonably well, but one run per condition cannot
estimate output variance or establish a statistically reliable treatment effect. The missing
sealed skill snapshot also prevents exact reproduction of the historical treatment condition.

## Current-skill routing expectation

For this task, the current skill should read:

1. `integrity-audit.md` for claim classification, guarantee scope, failure reporting, and author
   queries;
2. `manuscript-structure-style.md` for conclusion and prose contracts;
3. `engineering-profiles.md` for the mathematical-optimization status, gap, timeout, and scaling
   rules.

It should not load `corpus-calibration.md` because the task does not request corpus-derived style
or technical calibration. It should not load `venue-guidance.md` because no exact IEEE or ACM
publication is supplied and no venue adaptation is requested.

## Shared task

> Rewrite the following conclusion paragraph for an engineering manuscript. Preserve only
> claims supported by the evidence packet. Put any indispensable missing information after the
> rewrite under an "Author queries" heading.

### Original conclusion

> The proposed decomposition method is highly scalable and always finds the global optimum
> substantially faster than the monolithic baseline. It is therefore suitable for large
> real-time deployments.

### Evidence packet

- Synthetic evaluation fixture; it is not field or production evidence.
- 40 matched MILP instances containing 20--200 tasks.
- Both methods used the same formulation, hardware, solver version, and 600 s wall-clock limit.
- Proposed method: 27 `OPTIMAL`, 8 `TIME_LIMIT` with feasible incumbent, 5 `TIME_LIMIT` with no
  incumbent.
- Monolithic baseline: 23 `OPTIMAL`, 12 `TIME_LIMIT` with feasible incumbent, 5 `TIME_LIMIT`
  with no incumbent.
- For time-limited feasible proposed runs, the final optimality gap had median 3.2% and maximum
  11.4%.
- Median runtime computed only over runs proven optimal was 71 s for the proposed method and
  94 s for the baseline.
- No censored-runtime analysis, statistical significance test, real-time deadline, deployment
  experiment, or instances above 200 tasks were supplied.

## Baseline output without the skill

> The synthetic evaluation indicates that the proposed decomposition method can improve
> solution performance relative to the monolithic baseline on the tested MILP instances. Under
> identical formulation, hardware, solver version, and a 600 s wall-clock limit, the proposed
> method proved optimality on 27 of 40 instances, compared with 23 of 40 for the monolithic
> baseline. Among runs that reached proven optimality, the median runtime was 71 s for the
> proposed method and 94 s for the baseline. For proposed runs that terminated with a feasible
> incumbent but without proof of optimality, the final optimality gap had a median of 3.2% and a
> maximum of 11.4%. These results suggest a potential computational advantage on synthetic
> instances with 20--200 tasks, but they do not establish global superiority, statistical
> significance, scalability beyond the tested range, or suitability for real-time deployment.
>
> **Author queries**
>
> Define the real-time deadline or operational latency requirement if real-time suitability is
> to be claimed.
>
> Provide censored-runtime analysis and statistical testing if claims of faster performance are
> retained.
>
> Add larger or production-representative instances if scalability or deployment readiness is
> to be asserted.

## Output with the skill

> The proposed decomposition method was evaluated on 40 matched synthetic MILP instances with
> 20--200 tasks under the same formulation, hardware, solver version, and 600 s wall-clock limit
> as the monolithic baseline. It certified optimality on 27 instances, compared with 23 for the
> baseline, and both methods failed to find an incumbent on 5 instances. Among runs that were
> proven optimal, the median runtime was 71 s for the proposed method and 94 s for the baseline.
> For the 8 proposed runs that reached the time limit with a feasible incumbent, the final
> optimality gap had a median of 3.2% and a maximum of 11.4%. These results suggest a potential
> computational advantage on the evaluated synthetic instances, but they do not establish
> unconditional global optimality, scalability beyond 200 tasks, or suitability for real-time
> deployment.
>
> **Author queries**
>
> AQ-1 | Real-time suitability | No real-time deadline, tail-latency analysis, or deployment
> experiment is supplied | Provide deadline-driven evaluation or remove the claim | Current
> evidence supports only bounded synthetic MILP runtime behavior.
>
> AQ-2 | Scalability | No instances above 200 tasks or scaling analysis beyond the fixture is
> supplied | Add larger-scale experiments or censored-runtime analysis | Avoid broad scalability
> claims.
>
> AQ-3 | Faster than baseline | Runtime medians are computed only over runs proven optimal, with
> no censored-runtime analysis or statistical test | Analyze all matched runs with an appropriate
> timeout-aware method | Avoid claiming substantial or statistically supported speedup.

## Assessment

| Criterion | Baseline | With skill | Observation |
| --- | --- | --- | --- |
| Removes `always` and the unconditional global-optimality claim | Pass | Pass | Both outputs scope optimality to solver certificates. |
| Removes unsupported scalability and deployment claims | Pass | Pass | Both limit the conclusion to synthetic instances with at most 200 tasks. |
| Avoids claiming a statistically supported speedup | Pass | Pass | Both identify the missing timeout-aware analysis and statistical test. |
| Reports failure cases in the manuscript text | Partial | Pass | The skill output explicitly reports the five no-incumbent runs for both methods. |
| Uses the skill's missing-evidence contract | No | Pass | The skill output uses structured `AQ` records with action and consequence fields. |
| Reports all supplied baseline statuses | Partial | Partial | Neither output explicitly states the baseline's 12 feasible timeouts; a stronger result paragraph would report the complete status distribution or point to a table. |

The baseline already satisfies the central scientific-integrity requirement in this run. The
observed incremental effect of the skill is narrower: more explicit failure reporting and a
structured, actionable missing-evidence ledger. Repeated runs over all cases in
`evals/cases.json` are required before making a general performance claim about the skill.

This assessment applies only to the recorded historical snapshot. Re-evaluate the current
five-reference version with sealed skill contents, multiple replications, identical model and
runtime settings, preserved raw outputs, and a predefined scoring rubric before comparing versions
or claiming improvement.
