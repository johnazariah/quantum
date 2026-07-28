---
title: 'Circuit Bench: Application-Oriented Quantum Computing Notes with Executable Circuits'
tags:
  - quantum computing
  - quantum algorithms
  - OpenQASM
  - pedagogy
  - quantum circuits
  - Grover's algorithm
  - quantum Fourier transform
  - variational quantum eigensolver
  - QAOA
  - quantum education
authors:
  - name: John S Azariah
    orcid: 0009-0007-9870-1970
    corresponding: true
    affiliation: 1
affiliations:
  - name: Centre for Quantum Software and Information, School of Computer Science, Faculty of Engineering & Information Technology, University of Technology Sydney, NSW 2007, Australia
    index: 1
    ror: 03f0f6041
date: 8 April 2026
bibliography: paper.bib
---

# Summary

Circuit Bench is an open-source collection of thirteen self-contained
quantum circuit notes, each built around a concrete computational
problem and a working OpenQASM\ 2.0 circuit that runs on Quokka — a
30-qubit quantum computing system designed for education and
exploration\ [@quokka2025].  The resource takes an **application-down**
approach: every circuit note starts with a problem worth solving, builds
the circuit that solves it step by step, and introduces theory only at
the point where it becomes necessary.

The thirteen notes are organized into three progressive tiers:

1. **Foundations** — the fundamental building blocks of quantum
   computation.
    - *Reading a Quantum Circuit*: gates, unitary rotations, Bloch-sphere
      intuition, and measurement bases.
    - *Bell State*: entanglement and measurement correlation.
    - *Teleportation*: transmitting an unknown quantum state via
      entanglement and classical communication.
    - *Deutsch–Jozsa*: the first exponential separation between
      deterministic classical and quantum query complexity.

2. **Algorithms and applications** — querying, searching, optimization,
   and simulation.
    - *Bernstein–Vazirani*: exact recovery of a hidden string in one
      query via Fourier sampling.
    - *Simon's Problem*: the first exponential speedup over randomised
      classical algorithms, and the conceptual ancestor of Shor's
      algorithm.
    - *Grover's Search*: provably optimal unstructured search via
      amplitude amplification\ [@grover1996].
    - *QAOA for MaxCut*: variational combinatorial optimization on a
      triangle graph\ [@farhi2014].
    - *VQE for H~2~*: finding the ground-state energy of the hydrogen
      molecule using a variational eigensolver\ [@peruzzo2014].
    - *Quantum Fourier Transform*: the key subroutine behind phase
      estimation and Shor's algorithm.

3. **Advanced techniques** — phase extraction, noise-aware execution,
   and composite algorithms.
    - *Quantum Phase Estimation*: extracting eigenvalues of a unitary
      operator to arbitrary precision.
    - *Error Mitigation (ZNE)*: zero-noise extrapolation for improving
      results on noisy hardware\ [@temme2017].
    - *Quantum Counting*: combining Grover's operator with phase
      estimation to count solutions without finding them.

Every circuit note includes executable `.qasm` files, expected output for
verification, and a step-by-step explanation with inline mathematics.
The twelve algorithm notes also include auto-generated circuit diagrams,
and longer notes provide collapsible analysis sections with derivations,
proofs, and connections to the broader literature.

The resource is deployed as a static site via MkDocs Material, with
LaTeX mathematics rendered by MathJax.  All content is MIT-licensed.

# Statement of Need

Quantum computing education faces a persistent structural problem: most
resources teach **bottom-up**, starting with linear algebra and the
postulates of quantum mechanics, then building through gates and
circuits toward algorithms.  By the time a student reaches an
interesting application, they have forgotten why they started — or have
already left.

Existing educational resources fall into three categories, each with
limitations:

- **Textbooks** [@nielsen2010; @kaye2007] are comprehensive but
  abstract.  Algorithms are presented as theorems, not as executable
  programs.  Students can follow the proofs but cannot *run* the
  circuits.
- **Framework tutorials** (Qiskit Textbook, Cirq tutorials) are
  executable but platform-locked.  They teach a particular SDK's API,
  not the underlying concepts.  When the API changes, the tutorials
  break.
- **Interactive simulators** (Quirk, IBM Quantum Composer) are
  visual and immediate but shallow.  They let you drag gates but do not
  explain *why* those gates are there or connect the circuit to the
  mathematical structure.

Circuit Bench addresses these gaps by combining three properties
that no existing resource unifies:

1. **Application-oriented structure.** Every circuit note starts with a
   problem — "find a hidden string," "count the solutions," "compute
   the ground-state energy" — and derives the circuit as the solution.
   Theory enters in context, not as prerequisite.

2. **Platform-independent executable code.** Every circuit is a
   standard OpenQASM\ 2.0 file, runnable on any compatible platform.
   No `import` statements, no framework boilerplate, no version
   dependencies.

3. **Layered depth.** The main narrative is accessible to anyone
   comfortable with complex numbers.  Collapsible analysis sections
   provide full linear algebra, density matrix derivations, and proofs
   for students and researchers who want rigour.

The resource is designed for three audiences: undergraduate and
graduate students in quantum computing courses who want a hands-on
companion to their textbook; self-taught learners who want to build
intuition by running circuits; and educators who need ready-made,
self-contained modules they can assign or adapt.

# Learning Objectives

After completing the full set of circuit notes, a student will be able to:

1. Construct and interpret quantum circuits for entanglement
   generation, quantum teleportation, and Bell measurements.
2. Explain and implement Fourier sampling algorithms (Deutsch–Jozsa,
   Bernstein–Vazirani, Simon) and articulate the source of their
   quantum advantage.
3. Implement Grover's search for a small instance, explain the
   geometric interpretation, and calculate the optimal number of
   iterations.
4. Construct variational quantum circuits for combinatorial
   optimization (QAOA) and quantum chemistry (VQE), and describe the
   classical–quantum optimization loop.
5. Build and apply the Quantum Fourier Transform, and use it within
   Quantum Phase Estimation to extract eigenvalues.
6. Apply zero-noise extrapolation to mitigate hardware errors in
   circuit outputs.
7. Combine Grover's operator with phase estimation to count solutions
   to a search problem.
8. Read and write OpenQASM\ 2.0 programs and translate between circuit
   diagrams, QASM code, and mathematical descriptions.

# Instructional Design

Each circuit note draws from a flexible six-part structure designed for
circuit construction and verification:

1. **What this circuit does** — the problem, in plain language, with
   motivation.
2. **Circuit components or prerequisites** — qubits, gates, and prior
   concepts, listed explicitly.
3. **Circuit walkthrough** — the circuit, built incrementally with
   mathematical explanation at every step.
4. **The complete circuit** — the executable OpenQASM program in one
   place.
5. **Run it** — execute the circuit, observe the output, and interpret
   the results.
6. **Analysis and practical notes** — derivations, limitations,
   connections to other algorithms, and suggestions for further
   exploration.

This structure keeps every circuit note self-contained: a student can
enter at any point, and where prior knowledge is required, the
components or prerequisites section lists it explicitly with links to
earlier notes.

Longer **analysis sections** are implemented as collapsible admonitions
(using pymdownx.details), allowing students to expand the mathematical
content on demand without disrupting the narrative flow.  Topics covered
include: gate matrix representations, density matrix formalism, the
no-cloning theorem, Bell inequalities, the Walsh–Hadamard transform as
Fourier analysis over $\mathbb{Z}_2^n$, and the hidden subgroup
problem framework.

# Content and Scope

The thirteen circuit notes span the core of quantum algorithms and
provide a coherent progression from fundamental gates to composite
algorithms:

| Circuit note | Qubits | Key concepts |
|--------|--------|-------------|
| 00\ Reading a Quantum Circuit | 1 | Gates, unitary rotations, Bloch sphere, measurement bases |
| 01\ Bell State | 2 | Entanglement, measurement correlation, tensor products |
| 02\ Teleportation | 3 | Bell measurement, classical communication, no-cloning |
| 03\ Deutsch–Jozsa | 3 | Oracles, phase kickback, interference |
| 04\ Bernstein–Vazirani | 4 | Fourier sampling, hidden linear functions |
| 05\ Simon's Problem | 4 | Exponential speedup, hidden period, Gaussian elimination |
| 06\ Grover's Search | 3 | Amplitude amplification, diffusion operator, optimality |
| 07\ QAOA for MaxCut | 3 | Variational ansatz, cost Hamiltonian, hybrid loop |
| 08\ VQE for H~2~ | 2 | Quantum chemistry, Bravyi–Kitaev, variational principle |
| 09\ QFT | 3 | Controlled rotations, factored form, FFT comparison |
| 10\ QPE | 4 | Eigenvalue extraction, inverse QFT, Shor's connection |
| 11\ ZNE | 1–2 | Noise amplification, Richardson extrapolation |
| 12\ Quantum Counting | 4 | Grover + QPE composition, solution counting |

The progression is designed so that later notes reuse concepts and
circuits from earlier ones: the Bell pair from Circuit Bench\ 01 is
consumed by Circuit Bench\ 02; the phase kickback technique from Circuit
Bench\ 03 recurs in Circuit Bench\ 04–06 and\ 10; the QFT from Circuit
Bench\ 09 is inverted inside Circuit Bench\ 10 and\ 12.

# Implementation

The resource is implemented as a MkDocs Material static site, hosted on
GitHub Pages via GitHub Actions continuous deployment.  The repository
structure separates content (Markdown + QASM + expected output) from
presentation (MkDocs theme and configuration).

Circuit diagrams are generated programmatically using a custom
Matplotlib renderer (`generate_circuits.py`) that produces clean,
textbook-style PNG images with consistent visual language: blue for
Hadamard gates, red for Pauli-X, green for Pauli-Z, purple for phase
gates, orange for parameterised rotations, and standard $\oplus$
notation for CNOT targets.

Mathematics is rendered client-side using MathJax\ 3, with both
inline (`$...$`) and display (`$$...$$`) modes.  The site supports
light and dark themes, code copying, search, and responsive layout.

# Acknowledgements

The author thanks the Quokka team at Eigensystems for building the
hardware platform that inspired this resource.

# References
