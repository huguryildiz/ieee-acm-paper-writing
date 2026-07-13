# Engineering method and domain profiles

Use the applicable sections for the manuscript's methods and domains. Load multiple sections for
hybrid work. These reporting contracts complement, but do not establish, scientific validity.

## Contents

- Mathematical optimization
- Machine learning and ML-assisted engineering
- Simulation and digital twins
- Computer systems and cyber-physical-system engineering
- Communications, networking, signal processing, and sensing
- Energy systems, robotics, and autonomy

## Mathematical optimization

### Formulation contract

Present sets, indices, graphs and stages; parameters and units; decision variables and domains;
objective or ordered objectives; constraints grouped by role; transformations and relaxations;
and the feasible-region and guarantee scope. Define every symbol and explain what each constraint
enforces and why it is required.

Check dimensions, domains, quantifiers, signs, bounds, index ranges, and edge cases. Identify every
product, ratio, norm, maximum, or nonlinear function before claiming linearity. State the
assumptions and exactness of reformulations, discretizations, and linearizations.

### Method classification and guarantees

Name the actual computational role:

- exact formulation solved to a certificate;
- relaxation or bound;
- decomposition under stated convergence conditions;
- restricted candidate, path, column, or master formulation;
- approximation algorithm with a proved ratio;
- heuristic without a certificate;
- learning-assisted initialization, fixing, pruning, branching, pricing, or cut selection.

Do not call a restricted search space exact without scoping exactness to that space. Attach every
theorem-level statement to the problem class, regularity assumptions, algorithm variant, error
measure, iteration notion, and finite or asymptotic regime.

Distinguish convergence of iterates, residuals, objectives, feasibility, and certificates. Keep
theoretical rate, oracle calls, per-iteration work, runtime, memory, and solution quality separate.

### Special cases and experiments

For multiobjective work, state scalarization or enumeration method, normalization, preferences,
dominance tolerance, and frontier coverage. For stochastic or robust work, define information,
scenario construction, probability or uncertainty model, risk measure, and out-of-sample test.

Report solver/version, settings, threads, hardware, limits, instance families, seeds, primal value,
best bound, gap, feasibility, runtime, and status separately. Include timeouts and infeasible cases.
A faster incumbent is not faster proof of optimality.

Use a theorem-first exposition when guarantees are central: problem class, informal main result,
formal definitions, theorem and proof, algorithm, then experiments addressing practical questions
not settled by the proof.

## Machine learning and ML-assisted engineering

### Learning contract

State input object and observation unit, feature availability at inference, supervision source,
architecture and size, loss and regularization, optimizer, stopping rule, data splits, inference
procedure, and integration into the engineering system.

Prevent leakage across time, site, device, subject, topology, simulation realization, and
optimization instance. Fit preprocessing and selection on training data only.

### Computational role

Distinguish whether learning replaces the primary method, predicts an intermediate quantity,
produces a heuristic, initializes another algorithm, fixes variables or actions, prunes candidates,
selects solver decisions, or acts as a simulator/controller surrogate. State how this changes
correctness. Warm starts may preserve a feasible region; pruning may not.

Identify where prior knowledge enters: observations, features, architecture, loss, constraints,
simulator, initialization, or post-processing. State whether enforcement is exact, approximate,
or only empirically tested.

### Physics-informed and equation-discovery work

For physics-informed models, report equations, boundary and initial terms, loss weights,
collocation sampling, nondimensionalization, architecture, optimizer phases, stopping, seeds,
reference solver, and domain-wide error. A soft residual penalty encourages but does not guarantee
physical satisfaction.

For equation discovery, report derivative estimation, candidate library, scaling, sparsity
selection, coefficient uncertainty, identifiability, held-out trajectories, noise, and missing-term
tests. A sparse equation is not automatically causal, unique, or physically correct.

### Evaluation and style

Use task metrics with uncertainty and simple, strong, domain baselines. Report selection budgets
and claim-linked ablations. Name the tested shift rather than claiming generic robustness.

For scientific ML papers, progress from governing problem to representation, knowledge mechanism,
training or fitting objective, repeated case-study contract, and failure boundary. Keep data
efficiency, physical consistency, numerical accuracy, optimization success, extrapolation, and
cost as distinct claims.

## Simulation and digital twins

### Validity layers

Separate conceptual-model validity, code verification, numerical verification, and empirical
validation/calibration. Passing one layer does not establish another; repeatability is not physical
validation.

Report equations or transition rules, initial/boundary conditions, parameters and units,
resolution, method, tolerance, random processes, scenarios, software, stopping, and material
hardware. Identify measured, calibrated, fitted, assumed, and selected coefficients. Separate
calibration from validation data.

Report convergence, conservation or analytic pins, benchmark comparisons, sensitivity,
uncertainty propagation, replication and diagnostics, numerical failures, and cost where relevant.

### Digital-twin boundary

Before using “digital twin,” declare the physical referent, digital representation, automated
physical-to-digital flow, automated digital-to-physical flow, synchronization cadence, state
estimator, model version, and operational purpose. Use narrower terms for an offline model or
one-way shadow when coupling is absent.

Separate connectivity from calibration, calibration from validation, prediction from decision
support, and decision support from control. Bidirectional data alone does not establish model
validity or safe decisions. Measure operational claims against a comparator using accuracy, delay,
decision quality, downtime, resources, latency, or violations.

### Comparison and style

Ensure methods see matched scenarios, inputs, random streams, budgets, and stopping rules. Separate
simulator variance from method variance. Scope unvalidated findings as conditional on the model.

For reviews, state scope or research questions, define contested terms, explain classification
method, then synthesize applications, enabling components, challenges, and open research. Do not
turn category prevalence or examples into validation evidence.

## Computer systems and cyber-physical-system engineering

### System contract

Classify the contribution as architecture, mechanism, protocol, implementation, measurement,
dataset/testbed, optimization, or empirical finding. Describe components, interfaces, state,
data/control flow, trust and failure boundaries, deployment assumptions, and resources. Distinguish
implemented, simulated, mocked, and offline components.

Define events, state, clocks, communication, failure model, attacker model, and physical process
before reasoning about order, consistency, deadlines, resilience, or control. Distinguish logical
order, wall-clock time, synchronized estimates, and observed message order.

For real-time work, report sampling, actuation, delay, jitter, scheduling, clock error, deadlines,
miss consequences, and timing distributions. Mean latency does not prove deadline compliance.

### Evaluation and claim boundaries

Tie each experiment to a claim. Cover latency and tails, throughput/goodput, CPU/memory/bandwidth/
energy/storage, availability and recovery, scaling, workload sensitivity, matched baselines, and
operational failures where applicable.

Keep safety, security, reliability, resilience, schedulability, and average performance separate.
Random-fault evidence does not establish adversarial security. One larger point does not establish
scalability. A faster system with worse quality is a trade-off.

Report code/config identity, workload, deployment, hardware, measurement method, warm-up,
repetitions, aggregation, and nondeterminism. Address representativeness, maturity, hardware
specificity, emulator fidelity, measurement perturbation, and untested conditions.

For foundational or position writing, define the abstraction and expose its failure with a small
counterexample or diagram before proposing requirements. Keep research agendas distinct from
implemented contributions.

## Communications, networking, signal processing, and sensing

### Model and layers

Keep propagation, transceiver/link behavior, networking, application utility, and reliability
distinct. Define signal, channel, noise/interference, synchronization, sampling, bandwidth, power,
coding/modulation, topology, traffic, channel knowledge, and units as applicable.

Distinguish channel gain from received power and SNR; bit/packet/link failure from node/system
failure; detection probability from coverage/connectivity; capacity bounds from achieved
throughput; simulated channels from measured channels; and offline knowledge from online
information.

### Analytical and empirical evidence

For analytical work, state placement, traffic, reception, resource, asymptotic, probability,
stationarity, independence, and identifiability assumptions. Label upper bound, lower bound, and
achievable construction separately. A scaling law is not finite-system measured throughput.

For signal recovery, place signal class, sensing conditions, noise, decoder, norm, and probability
next to the guarantee. For spectral estimators, specify segmentation, overlap, window,
normalization, transform length, and averaging; distinguish bin spacing, resolution, leakage,
variance, and computation.

For experiments, report equipment, calibration, waveform, sampling, environment, geometry,
repetitions, and preprocessing. Define denominators and regimes for error, outage, efficiency,
latency, localization, detection, coverage, and connectivity.

### Comparisons and style

Match bandwidth, power, latency, reliability, hardware, channel knowledge, and complexity. Do not
infer robustness from one model or environment or translate link improvement to system utility
without an evaluated bridge.

For surveys, move from application scope to design factors, architecture/taxonomy, cross-layer
relationships, category synthesis, and open problems. For theory, state model and main result early,
then order formal arguments by dependency. For signal methods, use representation or estimator,
computation, trade-offs, and bounded applications.

## Energy systems, robotics, and autonomy

### Physical and operational model

State physical dynamics, network/topology, time scale, constraints, uncertainty, sensing,
actuation, and control authority. Distinguish planning, scheduling, estimation, control, and
real-time execution. Separate safety, stability, feasibility, regulation, and performance.

For energy systems, report power-flow approximation, demand/renewable/price/outage provenance,
storage dynamics and terminal conditions, reserve and contingency definitions, resolution,
scenarios, and operational feasibility.

For distributed scheduling, state actors, feasible actions, individual and system objectives,
tariff or incentive mechanism, information exchange, equilibrium concept, and the assumptions
linking equilibrium to aggregate performance.

For a microgrid, identify electrical boundary, connection mode, resource interfaces, local and
supervisory control, protection, islanding, black start, and resynchronization. Separate laboratory,
pilot, and operational evidence.

### Robotics and autonomy

Report platform, sensors, actuators, controller frequency, compute, environment/task distribution,
estimation and calibration, safety constraints, intervention policy, and simulation/lab/field
evidence separately.

For localization and mapping, distinguish posterior representation, motion model, observation
model, data association, map assumptions, loop closure, approximation, and consistency. Define
tracking, global localization, catastrophic displacement, ambiguity, and recovery regimes before
using “robust.”

Report success, collisions/violations, time, energy, tracking error, recovery, failures, and human
interventions. Do not treat correlated episodes as independent or claim sim-to-real transfer
without real-system evidence.

### Style and external validity

For architecture prose, lead with the system transition and interacting physical, communication,
information, and control layers. For formal scheduling, progress from actors to mechanism,
equilibrium/algorithm, and matched simulation. For robotics, define regime and probabilistic model
before implementation and organize evaluation around nominal, ambiguous, failure, and recovery
conditions.

Bound claims to tested grids, robots, environments, operating regimes, disturbances, and hardware.
State stability, recursive feasibility, safety, or constraint satisfaction only with applicable
proof or certificate.
