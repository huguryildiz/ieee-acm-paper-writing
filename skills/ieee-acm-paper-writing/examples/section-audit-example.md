# Section-Audit Example (Live Test Fixture)

A self-contained flawed Results + Conclusion excerpt for exercising the `audit`,
`section-audit`, and `rewrite` modes end to end, with an answer key of planted flaws.

The manuscript below is entirely synthetic. Its system, numbers, citations, and venue are
invented for this fixture; nothing in it refers to a real paper, author, or result.

## Flawed source excerpt

Copy only the fenced block below into a fresh session when running a live test. Do not paste
the answer key or expected-behavior sections into the session under test.

```text
V. RESULTS

We evaluate the proposed learning-assisted dispatch framework, in which a gradient-boosted
model warm-starts a mixed-integer linear program for microgrid unit commitment. All
experiments use our 34-bus test feeder. The warm-started solver finds the optimal dispatch
in every instance, confirming that the learned initializer preserves solution quality.

Our method significantly outperforms the conventional MILP baseline, reducing solve time by
23%. In the most demanding winter-peak scenario, operating cost falls by 41%, which
demonstrates the economic value of the approach in realistic conditions. A comparable
speedup was independently confirmed in [17], further validating our design choices.

The learned initializer was trained on 10,000 historical operating points and evaluated on
held-out scenarios drawn from the same year of feeder data. Across the evaluation set, the
warm start never degraded solver performance.

VI. CONCLUSION

This paper proved that learning-assisted warm starting makes mixed-integer dispatch
tractable for real-time operation in all operating conditions. The proposed framework
reduces solve time by 23% and operating cost by 41% while preserving optimality. Moreover,
the framework generalizes to transmission-level unit commitment and to networks with high
renewable penetration, making it directly deployable by system operators. Future versions
of the framework will incorporate battery degradation, which we expect to further improve
economic performance.
```

## Planted flaws (answer key)

Each flaw is labeled with the concern layer and the reference file whose contract catches it.
Layers: **S** = scientific support, **M** = method/domain reporting, **V** = venue compliance.

1. **Unscoped `optimal`** — "finds the optimal dispatch in every instance" carries no solver
   status, MIP gap, tolerance, or time limit; a warm start does not by itself certify
   optimality. [S] — `integrity-audit.md`, optimization contract in
   `engineering-profiles.md`.
2. **Bare 23% solve-time claim** — no baseline configuration, no aggregation statistic
   (mean? median? one instance?), no instance count, no variability. [S] —
   `integrity-audit.md`.
3. **`significantly outperforms` without a test** — "significantly" asserts statistical
   significance with no test, p-value, or uncertainty summary anywhere in the excerpt. [S] —
   `integrity-audit.md`.
4. **Cherry-picked 41% presented as typical** — the best case ("most demanding winter-peak
   scenario") is generalized to "realistic conditions" and then restated in the Conclusion
   as an unconditional result. [S] — `integrity-audit.md`.
5. **Missing reproducibility reporting** — no solver name/version, seeds, hardware, time
   limits, or MIP-gap settings for either method; the comparison is not reconstructible.
   [M] — optimization and ML contracts in `engineering-profiles.md`.
6. **Unverifiable corroborating citation** — "independently confirmed in [17]" uses an
   uncheckable citation as load-bearing evidence for the paper's own claim; the audit must
   flag the claim as unsupported by the manuscript's evidence, not silently accept [17].
   [S] — `integrity-audit.md`.
7. **Potential data leakage left unaddressed** — training and held-out evaluation data come
   from "the same year of feeder data" with no statement of temporal or scenario-level
   separation; the ML contract requires the split protocol to be explicit. [M] —
   `engineering-profiles.md`.
8. **Absolute negative claim without evidence scope** — "never degraded solver performance"
   is an unbounded universal over an evaluation set whose size and composition are never
   stated. [S] — `integrity-audit.md`.
9. **`proved … in all operating conditions`** — the Conclusion converts a single-feeder
   simulation study into a universal proof; scope (one 34-bus feeder, simulated) is
   dropped entirely. [S] — `integrity-audit.md`.
10. **New claims appearing only in the Conclusion** — generalization to transmission-level
    unit commitment, high-renewable networks, and "directly deployable by system operators"
    is supported by no result in Section V. [S] — `integrity-audit.md`,
    `manuscript-structure-style.md` (Conclusion may not exceed Results).
11. **Future work phrased as expected result** — "which we expect to further improve
    economic performance" attaches an anticipated outcome to unimplemented work inside the
    Conclusion. [S/V] — `integrity-audit.md`, `manuscript-structure-style.md`.

## Expected behavior

A correct run of `audit` or `section-audit` on the excerpt must:

- flag substantially all of the planted flaws above, each tied to the sentence that
  triggers it;
- keep evidence requests (baseline definition, aggregation statistic, split protocol,
  solver settings) as external author queries, outside any rewritten prose;
- scope every claim it does rewrite to the 34-bus simulated feeder and the stated
  evaluation set.

A correct run must never:

- invent the missing numbers, statistics, intervals, or solver settings to make the prose
  publishable;
- insert placeholder values ("XX%", synthetic confidence intervals) into manuscript prose;
- accept [17] as verification, or fabricate content for it;
- preserve "proved", "optimal", "all operating conditions", or "never degraded" without
  scoping.

## Manuscript-ready rewrite when the evidence is supplied

This section shows what a passing rewrite looks like. Like the answer key, it must not be
pasted into the session under test. The rewrite below is the verbatim output of a live run
of this skill (audit then rewrite, 2026-07-14) given only the fenced excerpt and the author
confirmations listed next; that run caught 11/11 planted flaws with no false positives.

For this illustrative example, assume the author resolves the audit queries by confirming:
the solver is Gurobi 10.0 with a 60 s time limit and 0.01% MIP-gap tolerance, and every
warm-started instance terminated with status optimal at that tolerance; the 23% value is the
median solve-time reduction against the cold-started identical formulation across all 500
held-out instances; the 41% cost reduction occurred in a single winter-peak scenario where
the cold-started solver hit the 60 s time limit and returned a suboptimal incumbent, so the
comparison is against that incumbent, not against a certified optimum; the held-out set is
temporally separated (trained on January–September, evaluated on October–December of the
same feeder year); and the claim attributed to [17] is dropped as corroboration. Under
those confirmations, a defensible rewrite is:

```text
V. RESULTS

We evaluate a learning-assisted warm start for mixed-integer unit commitment (UC) on our
34-bus microgrid test feeder. A gradient-boosted model, trained on operating points drawn
from January-September of the feeder's historical year, produces an initial solution that
warm-starts a mixed-integer linear program (MILP) solved with Gurobi 10.0 under a 60 s time
limit and a 0.01% relative MIP-gap tolerance. Cold-started and warm-started runs use the
identical MILP formulation and solver settings; only the initialization differs. We evaluate
on 500 held-out UC instances drawn from the same feeder's October-December operating points,
temporally disjoint from the training period.

Every warm-started instance terminated with solver status optimal at the 0.01% gap
tolerance. Across the 500 evaluated instances, the warm start did not increase solve time
in any instance relative to the identically configured cold start, with a median solve-time
reduction of 23%.

In the highest-load instance in the evaluation set, a winter-peak scenario, the cold-started
solver reached the 60 s time limit and returned a suboptimal incumbent, while the
warm-started solver certified optimality within the same limit. Relative to that
time-limited cold-start incumbent, the warm-started solution's operating cost was 41% lower.
Because the comparator in this instance is a suboptimal, time-limited incumbent rather than
a certified optimum, this figure reflects both the warm start's effect and the cold start's
early termination in this single case; it is not a general operating-cost reduction across
the evaluation set.

VI. CONCLUSION

On the 34-bus feeder and the 500-instance evaluation set described above, learning-assisted
warm-starting of the mixed-integer UC solver preserved certified solution quality: every
warm-started run terminated at the 0.01% gap tolerance under the same 60 s time limit and
solver settings as the cold start. The warm start reduced solve time in every evaluated
instance, with a median reduction of 23% relative to the cold-started baseline. In the one
winter-peak instance where the cold start was time-limited, the warm start additionally
certified optimality and reduced operating cost by 41% relative to the cold start's
suboptimal incumbent; this illustrates a scenario-specific benefit rather than a
general operating-cost claim.

These results are scoped to the 34-bus feeder, the trained gradient-boosted initializer, and
the stated Gurobi configuration and time limit. We have not evaluated transmission-level unit
commitment, feeders with substantially higher renewable penetration, or deployment in an
operational control environment, and we make no claim of generalization to those settings.
Incorporating battery degradation into the formulation is left to future work.
```

## External author query

"Supply the per-instance solve-time distribution (or summary statistics such as the IQR)
across the 500 evaluation instances, and confirm whether any instance showed a solve-time
reduction near zero that should be flagged separately. The manuscript currently reports
only the median reduction, which is fully supported by the evidence but omits dispersion
information a reviewer is likely to request for a claim this central to the paper."

Keep the author query outside manuscript prose. Do not insert synthetic intervals or
publishable placeholders.

## How to run the live test

1. Start a fresh session with the skill installed; provide only the fenced excerpt and a
   prompt such as: "Audit this Results and Conclusion section of an IEEE Transactions
   manuscript, then rewrite it."
2. Compare the output against the answer key: count flaws caught, missed, and any
   false positives.
3. Report the result with its denominator (e.g., "9/11 planted flaws caught; missed #7,
   #11") and list the missed flaws by name. A single run is an existence check, not a
   statistical result.
