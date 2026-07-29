---
date: 2026-08-03
notebook: https://github.com/johnazariah/quantum/blob/main/bottleneck/notebooks/03-drug-discovery.ipynb
categories:
- The Quantum Bottleneck
- Drug Discovery
tags:
- VQE
- molecular simulation
- quantum chemistry
- electronic structure
authors:
- John Azariah
social:
  linkedin: 'Drug-development estimates can reach several billion dollars, but quantum chemistry owns only part of that bill. I wanted this example to isolate that part rather than let a two-qubit circuit masquerade as a drug-discovery platform.


    I use H2 at one bond length because it is the smallest molecule that keeps the complete VQE loop visible. We prepare a trial state, measure the Z, X, and Y terms, reconstruct an energy, and compare it with exact diagonalisation of the same reduced Hamiltonian.


    A drug-relevant calculation brings back the pieces this notebook leaves out: molecular integrals, active-space selection, an expressive trial state, a large measurement budget, and the classical chemistry workflow around the quantum solver.


    This post is dedicated to Prof Robert Ditchfield: https://faculty-directory.dartmouth.edu/robert-ditchfield


    You taught us Quantum Chemistry (Chem 81) in the fall of 1991, and ignited a spark that still burns today! Thank you for being one of my most memorable teachers at Dartmouth!


    #QuantumComputing #DrugDiscovery'
  bluesky: 'I use H2 at one bond length because two qubits expose VQE''s measurement loop. It is not a drug simulation; molecular integrals, active-space choice, measurement cost, and the classical chemistry around the solver still matter.'
---

# The $2B Molecule

*To [Prof Robert Ditchfield](https://faculty-directory.dartmouth.edu/robert-ditchfield), who taught us Quantum Chemistry (Chem 81) in the fall of 1991, and ignited a spark that still burns today! Thank you for being one of my most memorable teachers at Dartmouth!*

Published estimates of developing a new medicine span hundreds of millions to several billion US dollars once failed programmes and financing costs are included.[^drug-cost] That bill is not a quantum-chemistry budget; clinical trials, manufacturing, regulation, and failure account for much of it. Early decisions nevertheless depend on questions about molecular energies, bonding, and reaction pathways.

To expose the quantum workflow, Unit 3 uses the smallest chemistry example that carries the full loop: a reduced two-qubit Hamiltonian for $\mathrm{H}_2$ at one bond length.

<!-- more -->

A candidate drug is more than a shape in a docking diagram. Electronic structure helps determine its bonds, charge distribution, conformational energies, and possible reactions. Binding and efficacy also depend on solvation, entropy, dynamics, metabolism, and the biology around the molecule.

More accurate molecular energies could make early screening less empirical, reducing the number of dead ends that are synthesised or advanced for the wrong reasons.

The difficult cases are the ones in which classical computers struggle to calculate those energies accurately.

## Where the classical calculation grows

Electrons are not little planets orbiting nuclei independently. They are indistinguishable quantum particles whose joint state must obey antisymmetry, Coulomb repulsion, and the Pauli principle. The difficult part is **correlation**: the way the motion of one electron changes the possible motion of the others.

Classical chemistry therefore lives on a ladder of approximations:

- **Hartree-Fock** gives each electron an average field from the others. It is fast, but it misses much of the correlation energy.
- **Density functional theory** replaces the full wavefunction with electron density. It is often very useful, but accuracy depends on the functional and can fail for strongly correlated systems.
- **Coupled-cluster and configuration-interaction methods** recover more correlation, but the cost rises steeply.
- **Full configuration interaction** is exact within a chosen basis, but the state space grows exponentially.

The growth is combinatorial. If $N$ electrons can occupy $M$ spin-orbitals, the number of allowed configurations grows like $\binom{M}{N}$. The active spaces that matter for catalysis, transition metals, and bond breaking can become too large for exact classical treatment.

## Put the energy in a variational loop

A quantum computer does not make chemistry easy. What it changes is the representation problem. Qubits can store and manipulate quantum amplitudes without writing the full state vector into classical memory.

For chemistry, the usual workflow is:

1. choose a molecular geometry and basis;
2. build a fermionic Hamiltonian for the electrons;
3. encode that Hamiltonian as qubit operators;
4. prepare a trial quantum state;
5. measure the expected energy;
6. let a classical optimiser adjust the circuit and try again.

That loop is the **variational quantum eigensolver** (VQE). The principle underneath it is simple: for any trial state $|\psi(\theta)\rangle$,

$$
\langle \psi(\theta) | H | \psi(\theta) \rangle \geq E_0,
$$

where $E_0$ is the true ground-state energy of the Hamiltonian. Lower trial energy means a better approximation to the ground state.

The quantum computer prepares and measures $|\psi(\theta)\rangle$. The classical computer chooses the next $\theta$. The algorithm is hybrid because neither side is doing the whole job.

If the measurement-basis language feels sudden, [Circuit Bench 00](../../circuit-bench/00-reading-a-quantum-circuit/README.md) gives the one-qubit version first. For the chemistry-specific circuit used here, [Circuit Bench 08](../../circuit-bench/08-vqe-h2/README.md) walks through the H2 VQE measurement circuit.

## Hydrogen on the bench

The notebook works with a reduced two-qubit Hamiltonian for $\mathrm{H}_2$ at one bond length. Molecular-integral generation, a potential-energy surface, and a protein binding pocket are outside this calculation.

Within that boundary, it shows the anatomy of the VQE loop:

- a precomputed reduced $\mathrm{H}_2$ Hamiltonian;
- an exact diagonalisation benchmark for that same reduced model;
- a Hartree-Fock reference state;
- a one-parameter trial-state, or ansatz, circuit;
- direct measurements in the $Z$, $X$, and $Y$ bases for the Pauli terms;
- a parameter sweep that compares the VQE estimate with the exact benchmark.

The notebook code makes that loop explicit:

```python
coeffs = h2_hamiltonian_coeffs()
E_exact = exact_diagonalisation_energy(coeffs)

for theta in thetas:
    energy = compute_energy(theta, coeffs, shots=1024)
```

Two qubits are enough to make the full pattern visible: encode a Hamiltonian, prepare a trial state, measure Pauli expectations, combine them into an energy, and use a classical loop to search for a lower value.

## Reality check: from $\mathrm{H}_2$ to active spaces

VQE became attractive because it uses shallower circuits than phase-estimation-based chemistry. That makes it a natural algorithm to test on noisy hardware. But "shallower" is not the same as "easy."

There are three hard problems hiding behind the small $\mathrm{H}_2$ example.

First, the **measurement cost** grows. A realistic molecular Hamiltonian can contain many Pauli terms, and each term needs enough shots to estimate its contribution accurately. Grouping commuting terms, classical shadows, and other measurement strategies help, but they do not remove the issue.

Second, the **ansatz matters**. A circuit that cannot represent the relevant chemistry will not find the right energy, no matter how clever the optimiser is. A very expressive circuit may become too deep or too hard to optimise.

Third, **scale changes the story**. A drug-sized system is not two qubits at one bond length. The credible path is an active-space calculation: use classical methods for the parts they handle well, and reserve the quantum device for the strongly correlated subproblem.

VQE gives the quantum device a specific job inside a larger chemistry workflow: estimate the energy of a prepared state. For a drug-relevant active space, the surrounding work includes choosing orbitals, constructing the Hamiltonian, preparing a state that represents the relevant chemistry, budgeting many measurements, and comparing with strong classical methods.

## Try the molecule

The [companion notebook](https://github.com/johnazariah/quantum/blob/main/bottleneck/notebooks/03-drug-discovery.ipynb) lets you run the single-geometry $\mathrm{H}_2$ VQE anatomy demo. For the gate-level side path, see [Circuit Bench 08 — VQE for H2](../../circuit-bench/08-vqe-h2/README.md).

[^drug-cost]: Schlander et al., ["How Much Does It Cost to Research and Develop a New Drug? A Systematic Review and Assessment"](https://doi.org/10.1007/s40273-021-01065-y), *PharmacoEconomics*, 2021. The review found a wide range driven by methods, included development phases, failures, and capital costs.

---

*This is Unit 3 of The Quantum Bottleneck series. Next up: [The Feature Explosion](bottleneck-04-machine-learning.md) — when the data bottleneck moves from molecules to feature spaces.*
