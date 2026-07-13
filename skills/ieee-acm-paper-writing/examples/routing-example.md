# Routing Example

## Request

"Audit the Results and Conclusion of an IEEE Transactions paper that uses a graph neural
network to warm-start a mixed-integer optimizer for robotic task allocation."

## References to load

Load, in this order:

1. `integrity-audit.md`;
2. `manuscript-structure-style.md`;
3. `engineering-profiles.md`;
4. `venue-guidance.md`.

Read each selected reference completely. Within `engineering-profiles.md`, apply the optimization,
machine-learning, and robotics/autonomy contracts. Verify the exact Transactions author
instructions independently.

## Key audit boundaries

- A warm start may improve time-to-feasible or runtime without changing exact-solver
  guarantees; the manuscript must show which claim the evidence supports.
- Test leakage, solver seeds, time limits, hardware, and matched instances are required for
  a defensible comparison.
- `Optimal` must be scoped to solver status and formulation; a good learned incumbent is
  not itself an optimality certificate.

## Anonymous corpus-calibration route

For the request:

"Our users cannot access the source PDFs. Restructure the Introduction using the technical writing
patterns extracted from the local corpus."

Load, in this order:

1. `manuscript-structure-style.md`;
2. `engineering-profiles.md`;
3. `corpus-calibration.md`;
4. `integrity-audit.md` if any scientific claim is added or changed.

Select the contribution archetype and technical area, then build the application ledger from
`corpus-calibration.md`. Use the anonymous structural and technical patterns without naming,
quoting, or requiring access to any source paper. The calibration may shape prose but cannot serve
as a citation or supply missing manuscript evidence.
