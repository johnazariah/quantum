---
date: 2026-08-17
notebook: https://github.com/johnazariah/quantum/blob/main/bottleneck/notebooks/07-materials-science.ipynb
categories:
- The Quantum Bottleneck
- Materials Science
tags:
- Hubbard model
- quantum simulation
- phase estimation
- materials science
- strongly correlated systems
authors:
- John Azariah
social:
  linkedin: 'The materials notebook solves a two-site Hubbard model by exact classical diagonalisation. Its quantum circuit begins only after one known energy has been shifted, rounded onto a three-bit phase grid, and compiled into a phase-estimation readout.


    The Hubbard benchmark introduces the competition between electron hopping and on-site repulsion, while the circuit demonstrates how quantum phase estimation turns an eigenphase into measured bits. Controlled evolution under the Hubbard Hamiltonian is not implemented.


    Scaling towards useful materials requires a faithful Hamiltonian encoding, state preparation, controlled time evolution, phase precision, error correction, and comparison with tensor-network, Monte Carlo, and embedding methods in the regimes where they work.


    #QuantumComputing #MaterialsScience'
  bluesky: 'This notebook diagonalises a two-site Hubbard model classically, then reads one known energy with compiled three-bit QPE. It demonstrates phase extraction, not quantum simulation of the Hubbard Hamiltonian.'
---

# The Materials Maze

Catalysts, superconductors, battery materials, magnetic compounds, and transition-metal oxides derive useful behaviour from electrons acting collectively. Strong correlation can make a compact Hamiltonian into a difficult many-body calculation.

Unit 7 separates two jobs. It solves a two-site Hubbard model by exact classical diagonalisation, then feeds one known energy into a compiled three-bit quantum phase-estimation circuit.

<!-- more -->

Density functional theory succeeds across a broad range of materials. Strongly correlated regimes remain difficult: electrons localise, spins couple, orbitals compete, and small energy differences decide the phase of the material.

## Two terms, one hard many-body problem

The Hubbard model is the standard teaching example because it is simple to write and hard to solve in general:

$$
H = -t \sum_{\sigma} (c_{1\sigma}^{\dagger}c_{2\sigma} + \text{h.c.}) + U \sum_i n_{i\uparrow}n_{i\downarrow}.
$$

Here $c_{i\sigma}^{\dagger}$ and $c_{i\sigma}$ create and remove an electron with spin $\sigma$ on site $i$; $n_{i\sigma}$ counts that occupation; and `h.c.` adds the Hermitian-conjugate hopping term.

The hopping term $t$ rewards delocalisation. The interaction term $U$ penalises double occupation. When $U/t$ is small, electrons can spread out. When $U/t$ is large, localisation dominates.

On two sites, we can diagonalise the model exactly. On large lattices, the Hilbert space grows rapidly and classical methods have to fight sign problems, truncation errors, finite-size effects, or uncontrolled approximations depending on the regime.

That is why the Hubbard model keeps appearing in discussions of quantum simulation. It is small enough to state, but rich enough to expose the computational difficulty of correlated matter.

## Put the energy into phase

For a fault-tolerant quantum computer, a natural route is Hamiltonian simulation plus quantum phase estimation (QPE).

If $|\psi\rangle$ is an eigenstate of a Hamiltonian $H$, then time evolution gives

$$
e^{-iHt}|\psi\rangle = e^{-iEt}|\psi\rangle.
$$

The energy $E$ appears as a phase. QPE estimates that phase using controlled powers of the time-evolution operator and an inverse quantum Fourier transform (QFT).

Implementing controlled $e^{-iHt}$ accurately for the material Hamiltonian is the hard part. The notebook isolates the phase-readout stage after computing a small exact benchmark.

For the side paths, [Circuit Bench 10: Quantum Phase Estimation](../../circuit-bench/10-quantum-phase-estimation/README.md) shows the phase-readout circuit directly, while [Circuit Bench 09: Quantum Fourier Transform](../../circuit-bench/09-quantum-fourier-transform/README.md) explains the inverse-QFT machinery used inside it.

## Solve classically, read phase quantum mechanically

The notebook keeps its two jobs separate.

First, it solves the half-filled two-site Hubbard model exactly. This gives a benchmark spectrum and shows how the ground-state energy changes as $U/t$ increases. On two sites this is a crossover in a toy benchmark, not a true bulk Mott transition.

Second, it picks one benchmark energy, shifts and rescales it into a phase window, rounds that phase onto a three-bit grid, and feeds the result into a compiled QPE toy circuit.

At a schematic level, the handoff looks like:

```python
E_exact = hubbard_2site_energies(t_hop=1.0, U=4.0)[0]
encoded_phase = energy_to_three_bit_phase(E_exact)
counts = run_compiled_qpe(encoded_phase)
```

The circuit then recovers the encoded phase as a dominant bit string. This demonstrates binary phase extraction after compilation; controlled evolution under the Hubbard Hamiltonian is absent.

The division of work is explicit:

- exact diagonalisation supplies the two-site benchmark energy;
- the energy-to-phase map is chosen classically;
- the QPE circuit is compiled for that known phase;
- controlled approximation of Hubbard time evolution is not implemented.

The notebook therefore locates QPE in the materials workflow while keeping the classical benchmark and compiled phase oracle explicit.

## Reality check: beyond two sites

Credible long-term materials algorithms require accurate Hamiltonian encodings, state preparation with meaningful overlap, controlled time evolution, phase precision, error correction, and careful resource estimates.

Near-term variational approaches can teach us about ansatz design and measurement. Fault-tolerant phase-estimation methods offer a clearer route to precise energies, but they demand hardware far beyond today's small devices.

There is also a modelling question before the quantum circuit starts. Real materials involve basis choices, downfolding to smaller effective models, embedding the surrounding environment, finite-temperature effects, defects, phonons, and experimental interpretation. Tensor-network methods, quantum Monte Carlo where the sign problem is controlled, dynamical mean-field methods, and other classical approximations remain the relevant baselines. A quantum computer would be one subroutine inside that scientific workflow.

The notebook connects an exact Hubbard benchmark to a compiled QPE readout. Turning that readout into a materials algorithm requires the missing state preparation and controlled Hamiltonian evolution, at a scale and precision that can compete with those classical methods.

## Inspect the handoff

The [companion notebook](https://github.com/johnazariah/quantum/blob/main/bottleneck/notebooks/07-materials-science.ipynb) lets you diagonalise the two-site Hubbard benchmark and run the compiled three-bit QPE toy. For the gate-level phase-readout pattern, see [Circuit Bench 10 — Quantum Phase Estimation](../../circuit-bench/10-quantum-phase-estimation/README.md).

---

*This is Unit 7 of The Quantum Bottleneck series. Next up: [The Catalyst Bottleneck](bottleneck-08-climate-energy.md) — where a quantum solve step must fit inside a classical embedding workflow.*
