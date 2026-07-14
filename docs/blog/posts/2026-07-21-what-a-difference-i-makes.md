---
date: 2026-07-21
categories:
  - Linear Algebra for Fun and Profit
tags:
  - eigenvalues
  - quantum computing
  - machine learning
authors:
  - John Azariah
---

# Machine Learning and Quantum Computing: What a Difference `i` Makes

*Power iteration ranks web pages. Imaginary time cools a quantum system. Phase estimation reads an energy off a circuit. They are all one move: apply a function of the operator $H$ and let the spectrum sort itself out. The only thing separating the machine-learning half of that sentence from the quantum half is a single factor of $i$.*

<!-- more -->

!!! note "Part 2 of *Linear Algebra for Fun and Profit*"
    Part 1, **How to Raise `e` to a Matrix**, builds the machinery this post spends: the matrix exponential, the spectral theorem, and why $e^{-iHt}$ is a rotation. Read that first if $\lvert n\rangle\langle n\rvert$ or "functions of $H$" are unfamiliar.

## The one idea

Every eigensolver in this post is a way of applying a **function of $H$** to filter its spectrum. Three functions recur:

- a growing power or exponential, $H^k$ or $e^{+Ht}$, which **stretches** the spectrum and amplifies an extremal eigenvector;
- the propagator $e^{-iHt}$, which **rotates** and exposes eigenvalues as phases to be read;
- the Rayleigh quotient, which turns "find the lowest eigenvalue" into "minimise a function."

The stretch is the engine of power iteration, Lanczos, and imaginary-time preparation; it is also, with the $i$ removed, the engine of PageRank and principal component analysis. The rotation is the engine of quantum phase estimation. That is the whole map, and the punchline is that the difference between the two is exactly the $i$ in the exponent.

## What this post covers

This is the companion walkthrough to a longer piece; the full text (eigenproblem, the variational principle, the classical eigensolvers, phase estimation, imaginary-time and adiabatic preparation, and the variational quantum eigensolver) is being adapted here and lands before publication. The figures below are the spine of it.

![The Rayleigh quotient bounds the ground energy from above; its minimum is the ground state.](lafp02-rayleigh.png)

![Power iteration: apply a growing power of the operator and the extremal eigenvector wins.](lafp02-power-iteration.png)

![Eigenvector centrality by power iteration: the same algorithm that ranks a friendship network, and the web.](lafp02-centrality.png)

![Imaginary-time evolution: the ground-seeking, i-free sibling of power iteration.](lafp02-imaginary-time.png)

![Quantum phase estimation reads an eigenphase off the propagator.](lafp02-qpe.png)

![The variational quantum eigensolver loop.](lafp02-vqe-loop.png)

![The two failure modes of a variational search: local minima and barren plateaus.](lafp02-vqe-landscape.png)

*Draft in progress; full prose lands before the 21 July publication date.*
