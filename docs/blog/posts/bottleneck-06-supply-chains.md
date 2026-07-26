---
date: 2026-08-12
notebook: https://github.com/johnazariah/quantum/blob/main/bottleneck/notebooks/06-supply-chains.ipynb
categories:
- The Quantum Bottleneck
- Supply Chains
tags:
- QAOA
- QUBO
- scheduling
- logistics
- combinatorial optimisation
authors:
- John Azariah
social:
  linkedin: 'Two nurses and two shifts need only two bits in this notebook because Nurse B''s assignment is implied by Nurse A''s. Even here, one hard coverage rule and one soft preference must be combined without letting the penalty weight overwhelm the objective.


    The notebook enumerates all four assignments, maps the exact QUBO cost to an Ising Hamiltonian, tunes one QAOA layer classically, and runs the two-qubit circuit. The circuit biases samples towards feasible schedules; it does not guarantee the optimum.


    A real roster adds variables, legal and skill constraints, penalty design, and a serious comparison with mixed-integer and constraint-programming solvers.


    #QuantumComputing #Optimisation'
  bluesky: 'A two-bit nurse schedule exposes QUBO penalty design: one hard coverage rule and one soft preference. The notebook maps that cost to a two-qubit QAOA circuit that biases samples towards feasible schedules.'
---

# The Scheduling Nightmare

A supply chain is a web of discrete choices: assign people to shifts, route trucks through depots, place inventory, and match jobs to machines. Difficulty accumulates when coverage, capacity, timing, preferences, and cost must hold together.

The companion notebook reduces that modelling problem to two nurses, two shifts, and two bits. One rule is hard, one preference is soft, and all four assignments can be checked by hand.

<!-- more -->

Binary decisions appear across staffing, routing, inventory placement, machine scheduling, and supplier allocation. Changing one assignment can make another infeasible, so a small change need not produce a small change in cost.

The number of assignments grows exponentially with the number of binary decisions.

## When constraints become costs

Take a tiny staffing problem. Suppose $x_{ij}$ is a binary variable that says whether nurse $i$ works shift $j$. Even before preferences, overtime, skill mixes, legal rest periods, and fairness rules enter the model, the number of possible assignments grows exponentially with the number of binary choices.

The standard optimisation move is to turn those choices into an objective function. Reward useful assignments, penalise broken constraints, and search for the bitstring with the lowest cost.

One common form is a **quadratic unconstrained binary optimisation** (QUBO) problem,

$$
C(x) = x^T Q x,
$$

where $x$ is a vector of bits and $Q$ encodes both the objective and the penalties. The word "unconstrained" says that the original constraints have been folded into the cost function as penalties.

Penalty encoding creates a new engineering problem: small penalties can make infeasible schedules attractive, while large penalties can drown out the real objective.

## From QUBO to phases

Gate-based quantum optimisation usually starts by mapping the QUBO to an Ising Hamiltonian. Binary variables become spin variables, and the cost function becomes an energy landscape.

The Quantum Approximate Optimisation Algorithm (QAOA) then alternates two operations:

1. a **phase separator** that gives each bitstring a phase depending on its cost;
2. a **mixer** that moves amplitude between neighbouring bitstrings.

After a few rounds, the circuit is measured. QAOA offers no guarantee of a good schedule; its aim is to bias the measurement distribution towards low-cost bitstrings.

For the gate-level version of that idea, [Circuit Bench 07: QAOA for MaxCut](../../circuit-bench/07-qaoa-maxcut/README.md) is the side path. The staffing notebook uses the same phase-separator-and-mixer rhythm, but with a scheduling QUBO rather than a graph cut.

## Two shifts, two bits

The notebook uses two bits, $x_0$ and $x_1$, to say whether Nurse A takes the day and night shifts. Feasibility requires $x_0 + x_1 = 1$; Nurse B then takes the remaining shift. This micro-example therefore needs two variables rather than one variable for every nurse-shift pair.

That leaves every step visible:

- define the binary variables;
- build the QUBO penalties;
- convert the QUBO to an Ising form;
- check the exact classical costs for all assignments;
- run a one-layer QAOA circuit on Quokka;
- compare the measured bitstrings with the low-cost assignments.

Schematically, the handoff has the following structure. The notebook builds the matrix and exact Ising coefficients directly rather than defining these three wrapper functions:

```python
Q = build_scheduling_qubo()
ising = qubo_to_ising(Q)
counts = run_qaoa(ising, gamma, beta)
```

The translation is the useful part: a scheduling problem becomes a cost function; the cost function becomes an Ising Hamiltonian; the Hamiltonian becomes a circuit whose measurements sample candidate schedules.

Realistic rostering, penalty tuning at scale, and comparison with industrial mixed-integer solvers are outside this two-bit pipeline.

## Reality check: back to the roster

There are several places where this can fail before quantum hardware becomes the limiting factor.

First, the QUBO model has to be good. If the business objective is vague, if the constraints are missing, or if the penalty weights are badly chosen, the quantum circuit will faithfully optimise the wrong thing.

Second, the qubit count grows with the number of binary decisions. Real planning problems can require thousands or millions of variables before decomposition.

Third, QAOA is an optimisation heuristic. The choice of depth, angles, mixer, constraints, and post-processing all matter. A shallow circuit may be too weak; a deep circuit may be too noisy.

The relevant alternatives include quantum annealers, mixed-integer and branch-and-bound solvers, constraint programming, local search, tensor-network methods, and classical decomposition. The notebook focuses on gate-based QAOA because it exposes the circuit mechanism directly.

QUBO and Ising formulations provide a precise bridge from discrete planning to quantum optimisation circuits. This notebook crosses it with two bits and one QAOA layer. A useful scheduling result must scale the model, hardware, and hybrid optimiser together while competing with those established methods.

## Build the schedule

The [companion notebook](https://github.com/johnazariah/quantum/blob/main/bottleneck/notebooks/06-supply-chains.ipynb) lets you build the scheduling QUBO, derive the Ising form, and run a one-layer QAOA instance. For the circuit pattern in isolation, see [Circuit Bench 07 — QAOA for MaxCut](../../circuit-bench/07-qaoa-maxcut/README.md).

---

*This is Unit 6 of The Quantum Bottleneck series. Next up: [The Materials Maze](bottleneck-07-materials-science.md) — where the assignments give way to interacting electrons in a lattice.*
