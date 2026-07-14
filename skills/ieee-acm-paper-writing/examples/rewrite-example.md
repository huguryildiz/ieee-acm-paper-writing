# Rewrite Example

## Source note

"Our algorithm is much better. It saves 18% energy. Tested on 50 scenarios."

## References applied

- `integrity-audit.md` for quantitative and comparison integrity;
- `manuscript-structure-style.md` for Results prose;
- the communications/energy sections of `engineering-profiles.md` for metric and simulation scope.

## Required evidence before rewriting

- definition of energy and aggregation statistic;
- exact baseline;
- whether 18% is a mean, median, minimum, or one selected case;
- scenario construction and matched evaluation set;
- variability or uncertainty;
- exclusions, failures, and missing runs.

## Manuscript-ready rewrite when the effect is verified

For this illustrative example, assume the author resolves the queries above by confirming that
the 18% value is the median per-node communication-energy reduction against Baseline B across all
50 matched scenarios under the Section IV-A traffic load and channel model.

"Across 50 matched simulation scenarios, the proposed controller reduced median per-node
communication energy by 18% relative to Baseline B under the common traffic load and
channel model defined in Section IV-A."

## External author query

"Provide the per-scenario distributions or a justified uncertainty summary for both methods.
Without them, the manuscript can report the verified median difference but cannot characterize
variability, statistical uncertainty, or robustness across scenarios."

Keep the author query outside manuscript prose. Do not insert synthetic intervals or publishable
placeholders.
