# Claim Audit Example

## Manuscript statement

"The proposed method is scalable and always finds the optimal solution substantially
faster than the baseline."

## Evidence supplied

- 30 instances with 20--100 agents;
- a lower median runtime on 24 instances;
- six timeouts for the proposed method and nine for the baseline;
- no statistical test or optimality-gap table;
- both methods use a 600 s limit.

## References applied

- `integrity-audit.md` for evidence classification, severity, and guarantee scope;
- `engineering-profiles.md` for optimization status, timeout, gap, and scaling checks.

The supplied values are empirical observations from a finite evaluated set. No optimality
certificate, population-level scaling evidence, or statistical comparison is supplied.

## Audit finding

**Critical — unsupported guarantee and selective runtime summary.** The evidence does not
support `always`, `optimal`, `substantially`, or a general scalability claim. Six proposed
method runs timed out, optimality certification is not reported, and the evaluated size
range is finite. Report matched completion counts, runtime distributions with timeouts
handled explicitly, solver status or gaps, and the evaluated range.

## Defensible rewrite

"Across the 30 evaluated instances containing 20--100 agents, the proposed method completed
without a timeout on 24 instances, compared with 21 for the baseline, under a common 600 s
limit. Runtime and optimality-certification results are reported separately."

The rewrite deliberately makes no optimality or scalability claim because the supplied
evidence does not establish one.
