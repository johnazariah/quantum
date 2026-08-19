---
date: 2026-08-19
slug: the-catalyst-bottleneck
redirect_from:
  - blog/2026/08/19/bottleneck-08-climate-energy/
landing_summary: >-
  Quantum embedding gives the quantum solver a bounded job inside a larger
  catalyst-screening workflow, rather than asking one device to solve the
  whole material.
notebook: https://github.com/johnazariah/quantum/blob/main/bottleneck/notebooks/08-climate-energy.ipynb
categories:
- The Quantum Bottleneck
- Climate & Energy
tags:
- quantum embedding
- VQE
- catalysis
- active spaces
- climate tech
authors:
- John Azariah
social:
  linkedin: 'I am ending The Quantum Bottleneck with embedding because it gives the quantum solver a bounded job inside a scientific workflow. A catalyst is too large to hand to one device, but its hardest correlated orbitals can sometimes be isolated as an active space.


    The notebook begins after a classical calculation has selected that space and supplied a two-qubit effective Hamiltonian. VQE prepares a trial state, measures its Pauli terms, and compares the resulting energy with an exact benchmark for the same reduced model.


    The surrounding chemistry has not disappeared. Active-space choice, the environment, self-consistency, measurement cost, and hardware errors still determine whether the quantum correction means anything for a real catalyst.


    #QuantumComputing #ClimateTech'
  bluesky: 'I end the series with embedding because it gives the quantum solver a bounded job inside a catalyst workflow. The two-qubit notebook starts from a precomputed active-space Hamiltonian; it does not simulate the catalyst.'
---

# The Catalyst Bottleneck

Better catalysts could change the cost of clean fuels, fertiliser, carbon utilisation, and industrial heat. Their active sites bind intermediates, move charge, and break or form bonds while coupled to a much larger chemical environment.

The capstone starts after a classical workflow has selected and embedded that active site. It runs one two-qubit variational solve for a precomputed effective Hamiltonian.

<!-- more -->

The energy transition depends on both deploying known technologies and finding materials that make difficult reactions cheap, selective, and durable. Relevant processes include water splitting, carbon dioxide reduction, nitrogen fixation, chemical energy storage, and ion transport in batteries. For each one, rate, selectivity, durability, and cost matter.

Catalysts answer those questions through electronic structure. The active site has to bind intermediates neither too weakly nor too strongly, move charge at the right time, and survive the operating environment. That is precisely the regime where classical modelling can become uncertain.

## The active site has surroundings

The chemically important active site sits inside an environment: a surface, a support, a solvent, an electrolyte, a protein scaffold, or a larger material.

Classical methods handle much of that environment well. The difficulty is the strongly correlated fragment where bond breaking, charge transfer, spin state changes, or transition-metal orbitals dominate the answer.

A brute-force quantum calculation of the whole system is impossible. A tiny active-site calculation without the environment is often too crude.

That is the embedding problem: keep the large environment classical enough to be tractable, but solve the hard active space accurately enough that the chemistry is meaningful.

## Give the quantum solver one fragment

Quantum embedding turns the workflow into pieces:

1. use classical computation to choose an active space;
2. compress the environment into an effective Hamiltonian for that active space;
3. solve the active-space Hamiltonian with a stronger quantum or classical method;
4. feed the result back into the larger calculation if the embedding scheme requires self-consistency.

The quantum device receives the active-space Hamiltonian rather than the whole catalyst.

In a near-term teaching setting, that solve step is naturally illustrated with the **variational quantum eigensolver** (VQE): prepare a parameterised state, measure Pauli terms, combine the measurements into an energy, and let a classical loop search over the parameter. [Circuit Bench 08: VQE for H2](../../circuit-bench/08-vqe-h2/README.md) shows that measurement pattern in its smallest chemistry form.

## Where the notebook enters the pipeline

The active-space Hamiltonian is precomputed as a two-qubit toy model with products of Pauli operators such as $Z_0$, $Z_1$, $Z_0Z_1$, $X_0X_1$, and $Y_0Y_1$, where each subscript names the qubit on which the operator acts. Active-space selection and the classical embedding calculation have already happened.

Then the notebook executes one embedded solve step:

- compare a classical embedding baseline with an exact benchmark for the reduced model;
- prepare a one-parameter entangling ansatz;
- measure the Pauli terms in the required bases;
- combine the measurements into an energy estimate;
- compare the VQE result with the exact embedded benchmark.

The solve step calls the three pieces directly:

```python
coeffs = embedded_active_space_coeffs()
E_exact = exact_diagonalisation_energy(coeffs)
E_vqe = compute_active_energy(theta, coeffs, shots=1024)
```

The surrounding classical stages remain outside the notebook:

- it does not run density functional theory (DFT);
- it does not construct a density matrix embedding theory (DMET) bath;
- it does not choose the active space dynamically;
- it does not run a self-consistent embedding loop;
- it does not compute a real catalyst binding trend.

The quantum subroutine begins only after those classical pieces have supplied the reduced Hamiltonian.

## Reality check: the interface matters

Embedding gives quantum hardware a focused job, which makes the classical-quantum interface decisive. That interface must be accurate, stable, and scientifically interpretable.

The active space must include the orbitals that actually drive the chemistry. The effective Hamiltonian must preserve the relevant environmental effects. The quantum solver must approach chemical accuracy, conventionally about 1 kcal/mol for an energy difference, on the reduced problem. The final workflow must turn those energy differences into useful catalyst trends rather than isolated numbers.

And the hardware still matters. VQE-style solve steps face measurement cost, optimiser noise, trial-state limitations, and device errors. Phase-estimation-style solve steps are cleaner in principle but need fault tolerance.

Some climate and energy technologies depend on hard electronic-structure calculations. Embedding is one way to place a quantum solver on the correlated fragment while established classical methods retain the larger environment. The scientific result is only as reliable as the interface between them.

## The final notebook

The [companion notebook](https://github.com/johnazariah/quantum/blob/main/bottleneck/notebooks/08-climate-energy.ipynb) lets you run the precomputed embedded active-space VQE solve step. For the circuit-level VQE measurement pattern, see [Circuit Bench 08 — VQE for H2](../../circuit-bench/08-vqe-h2/README.md).

---

*This is Unit 8 of The Quantum Bottleneck series. Return to the [series overview](../../bottleneck/index.md) for the full companion path.*
