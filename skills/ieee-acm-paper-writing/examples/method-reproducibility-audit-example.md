# Method-Reproducibility Audit Example (Live Test Fixture)

This self-contained fixture exercises the `audit` and `section-audit` modes on a plausible
cyber-physical-systems Methods and Evaluation excerpt. The study is entirely synthetic: the
robot, simulator, measurements, run counts, and data split were constructed for this example
and are not observations from a real system.

## Evidence packet

- The available artifacts contain simulator logs only; there is no physical-robot, sensor,
  actuator, warehouse, or field-deployment record.
- The evaluation used 15 attempted simulated test runs. Three runs diverged and were removed
  after inspection. The remaining 12 runs contain 500 time-correlated frames each.
- The reported 6,000 samples are those 12 runs multiplied by 500 frames; frames from the same
  run share a trajectory, environment realization, and controller state.
- Normalization statistics were calculated over the complete synthetic trajectory collection
  before frames were assigned to training and test sets.
- The timing log contains a mean per-step inference time of 18 ms for successful steps. It does
  not record a control deadline, tail distribution, jitter, missed deadlines, hardware manifest,
  or warm-up policy.
- No archived artifact identifies the simulator and version, world files, sensor-noise model,
  layout randomization distribution, seed list, controller revision, control frequency, state,
  action, update rule, actuator limits, or safety criterion.

## Flawed source excerpt

Copy the evidence packet and the fenced block below into a fresh session when running the live
test.

```text
III. METHODS

We deploy the controller on autonomous warehouse robots and evaluate it under realistic
operating conditions. The controller converts localization estimates into safe motion commands.
We use a high-fidelity simulator with realistic sensor noise and randomized warehouse layouts.

We normalize all recorded trajectories before assigning frames to training and test sets. This
procedure yields a large and representative held-out set.

IV. EVALUATION

An average inference time of 18 ms confirms real-time operation. Performance is stable across
6,000 independent test samples. We report the 12 successful runs after removing unstable trials.
```

## Expected audit boundary

A correct run must distinguish simulated evidence from deployment evidence; reject the real-time
and safety guarantees; identify the data leakage, correlated replication units, and excluded
failures; and request the missing system, simulator, and experiment specification outside revised
manuscript prose. It must not invent a robot platform, simulator version, deadline, hardware,
uncertainty interval, seed list, or safety certificate.

The corresponding canonical map data are in
[`method-reproducibility-audit-map.json`](method-reproducibility-audit-map.json); the checked-in
HTML is generated from that JSON. The retained map records one application of the current skill
to this synthetic fixture. It is an example of the output contract, not a benchmark or evidence
of performance on real manuscripts.
