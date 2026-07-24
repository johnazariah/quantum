---
date: 2027-02-03
categories:
  - Quantum Foundations
tags:
  - quantum computing
  - Hamiltonian simulation
  - Schrödinger equation
  - unitarity
authors:
  - John Azariah
social:
  linkedin: |
    The Schrödinger equation appears in two forms that serve completely different purposes. One is an eigenvalue problem that gives you hydrogen orbitals. The other is an initial-value problem whose solution is a unitary propagator, the object that advances a quantum state forward in time. Quantum computing lives entirely in the second form, and the bridge between them is shorter than most textbooks suggest. This post builds it from first principles with a single two-level system as the running example: spectral decomposition, the propagator, unitarity as conservation of probability, and the exact reason why naive Euler integration breaks the physics.

    First in a new series: Quantum Foundations and Advanced Methods.

    #QuantumComputing #HamiltonianSimulation
  bluesky: "The Schrödinger equation has two forms. Quantum computing lives in the one your undergrad course barely touched. New post builds the bridge from wavefunctions to propagators, first principles, one running example."
---

# From Wavefunctions to Propagators: The Bridge to Quantum Circuits

*For my PhD supervisor, who pointed out that the gap between "I learned Schrödinger in undergrad" and "I understand Hamiltonian simulation" is surprisingly narrow — and that the right running example makes it disappear entirely.*

<!-- more -->

!!! note "Part 1 of *Quantum Foundations and Advanced Methods*"
    This series builds the structural ideas beneath quantum algorithm design: Hamiltonian simulation, adiabatic state preparation, parameter transfer, and the block-encoding/signal-processing framework that unifies them. Each post is self-contained.

## Two equations, one name, and a twenty-year confusion

Here is a thing I wish someone had told me clearly in undergrad: the "Schrödinger equation" refers to *two* entirely different mathematical objects, and quantum computing uses the one my coursework barely touched.

The **time-independent** equation is the one you spend months on in a physics degree. It is an *eigenvalue problem*:

$$\hat{H}\,\psi(\vec{r}) = E\,\psi(\vec{r}).$$

You feed in a differential operator — the Hamiltonian for hydrogen, say — and out come wavefunctions $\psi_{n\ell m}(\vec{r})$ and energy levels $E_n$. It tells you which standing-wave patterns exist and at what energies. It says nothing about what happens *next*.

The **time-dependent** equation is a different beast:

$$i\hbar\,\frac{\partial}{\partial t}\,\Psi = \hat{H}\,\Psi.$$

This is not an eigenvalue problem. It is an *initial-value problem*: given a state right now, how does it evolve? Same operator, same eigenvalues, but the question has shifted from "what states *exist*?" to "what *happens*?"

Quantum computing is almost exclusively concerned with the second question. We prepare a state, evolve it under some Hamiltonian, and measure. The entire computational model reduces to one challenge: how do you implement $e^{-iHt}$ for a given $H$? That operator — the *propagator* — is where this post is headed.

## From functions to vectors — or, why no calculus survives

In hydrogen, the state $\psi(\vec{r})$ is a function in an infinite-dimensional Hilbert space, $\hat{H}$ is a differential operator, and every inner product involves an integral over all of $\mathbb{R}^3$. For quantum computing on $N$ two-level systems, *none of this machinery persists*.

The Hilbert space becomes $\mathbb{C}^{2^N}$ — a finite-dimensional vector space. The state is a column vector, the Hamiltonian (a Hermitian matrix — that is, one equal to its own conjugate transpose, $H = H^\dagger$) is a $2^N \times 2^N$ matrix, and inner products are finite sums:

| Hydrogen (continuous) | $N$ two-level systems (finite) |
|---|---|
| State: a function $\psi(\vec{r})$ | State: a vector $\lvert\psi\rangle \in \mathbb{C}^{2^N}$ |
| Hamiltonian: a differential operator | Hamiltonian: a Hermitian matrix $H$ |
| Inner product: $\int \phi^*\psi\,d^3r$ | Inner product: $\langle\phi\lvert\psi\rangle = \sum_i \phi_i^* \psi_i$ |
| Eigenvalues and eigenfunctions | Eigenvalues and eigenvectors |

Dirac notation is just bookkeeping for this dictionary. $\lvert\psi\rangle$ is a column vector; $\langle\psi\rvert$ is its conjugate transpose (a row vector); $\langle\phi\lvert\psi\rangle$ is the complex inner product; and $H\lvert\psi\rangle$ is a matrix acting on a vector. No calculus remains. "Solving the Schrödinger equation" is diagonalising a matrix.

An observable is a Hermitian matrix $O$ whose expected value in state $\lvert\psi\rangle$ is $\langle O\rangle = \langle\psi\lvert O\lvert\psi\rangle$. The energy expectation is $\langle H\rangle$. Everything quantum computing needs lives in this finite-dimensional picture.

## The ODE that runs the universe (in miniature)

Set $\hbar = 1$ (measuring time in units of inverse energy — a conventional choice that removes a constant from every formula). The time-dependent Schrödinger equation becomes:

$$\frac{d}{dt}\,\lvert\psi\rangle = -iH\,\lvert\psi\rangle.$$

A first-order linear ODE for a vector, with the constant matrix $-iH$ on the right-hand side.

That factor of $i$ is not cosmetic — it is the *structural* feature that makes time evolution a rotation rather than a stretch. Without it you would get exponential growth or decay. With it you get phase accumulation. This single distinction is why quantum computing works at all: information is *rotated*, never dissipated. (The *Linear Algebra for Fun and Profit* series explored this divide in its final post, "What a Difference `i` Makes." Here we arrive at the same point from the physics side.)

## Solving it: phases on eigenstates

### The propagator

For any square matrix $M$, define the matrix exponential $e^{M} := \sum_{k=0}^{\infty} M^k/k!$ (the series converges for every finite-dimensional $M$). Then

$$\lvert\psi(t)\rangle = e^{-iHt}\,\lvert\psi_0\rangle$$

solves the ODE. You can verify this by differentiating term by term:

$$\frac{d}{dt}e^{-iHt} = -iH\,e^{-iHt},$$

with initial condition $e^{0} = I$ giving $\lvert\psi(0)\rangle = \lvert\psi_0\rangle$.

The operator $U(t) = e^{-iHt}$ is the **propagator** — it advances any initial state $\lvert\psi_0\rangle$ forward by time $t$. This is the object at the heart of quantum simulation: every quantum algorithm that "simulates a Hamiltonian" is implementing some approximation to $U(t)$.

### Making the exponential concrete via spectral decomposition

Because $H$ is Hermitian, the spectral theorem guarantees an orthonormal eigenbasis $\{\lvert E_n\rangle\}$ with real eigenvalues $E_n$:

$$H = \sum_n E_n\,\lvert E_n\rangle\langle E_n\rvert.$$

(We label eigenstates by their energies, $\lvert E_0\rangle, \lvert E_1\rangle, \ldots$ in increasing order, to avoid any collision with the initial state $\lvert\psi_0\rangle$ or the computational basis $\lvert 0\rangle, \lvert 1\rangle$.)

Any function of $H$ acts eigenvalue-by-eigenvalue:

$$f(H) = \sum_n f(E_n)\,\lvert E_n\rangle\langle E_n\rvert.$$

Taking $f(x) = e^{-ixt}$:

$$e^{-iHt} = \sum_n e^{-iE_n t}\,\lvert E_n\rangle\langle E_n\rvert.$$

### What moves, and what stays frozen

Expand the initial state: $\lvert\psi_0\rangle = \sum_n c_n\lvert E_n\rangle$ where $c_n = \langle E_n\lvert\psi_0\rangle$. Then

$$\lvert\psi(t)\rangle = \sum_n c_n\,e^{-iE_n t}\,\lvert E_n\rangle.$$

Each coefficient picks up a phase: $c_n \mapsto c_n e^{-iE_n t}$.

The *populations* are frozen: $\lvert c_n e^{-iE_n t}\rvert^2 = \lvert c_n\rvert^2$ for all $t$. The probability of measuring each energy never changes. Only the *relative phases* between eigenstates evolve — and those phases beat at the energy gaps $E_m - E_n$.

This is the complete picture of what quantum time evolution does: it rotates relative phases between energy eigenstates. Nothing else changes. A single eigenstate is stationary (up to a global phase no measurement can detect). A superposition of different energies *interferes*, and the interference pattern oscillates at gap frequencies.

## Why this is *exactly* conservation of probability

### The chain: Hermitian → unitary → probability preserved

A **unitary** operator is one satisfying $U^\dagger U = I$ — it preserves all inner products and all norms. Here is why the propagator is unitary:

$$U(t)^\dagger U(t) = e^{+iHt}\,e^{-iHt} = e^{0} = I,$$

using two facts: $(e^A)^\dagger = e^{A^\dagger}$, and the exponents commute (both are proportional to $H$, so $[+iHt,\,-iHt] = 0$).

The physical content: a unitary operator preserves the norm $\lVert\psi\rVert^2 = \sum_i \lvert\psi_i\rvert^2$. By the Born rule, that norm *is* the total probability of all measurement outcomes. So:

> **Hermitian $H$** $\;\Rightarrow\;$ **unitary propagator** $\;\Rightarrow\;$ **probability conservation.**

This is not an approximation. It is a theorem. Every quantum gate, every quantum circuit, every quantum algorithm is a unitary transformation, and this chain of reasoning is why.

### The direct proof — even quicker

Differentiate the norm without mentioning eigenstates at all:

$$\frac{d}{dt}\langle\psi\lvert\psi\rangle = \langle\dot\psi\lvert\psi\rangle + \langle\psi\lvert\dot\psi\rangle = \langle\psi\rvert(+iH)\lvert\psi\rangle + \langle\psi\rvert(-iH)\lvert\psi\rangle = 0.$$

The cancellation requires only $H = H^\dagger$. The norm is constant. Period.

## The running example: a two-level system, solved exactly

Let's make all of this concrete. Take two Pauli matrices, $X = \begin{pmatrix}0&1\\1&0\end{pmatrix}$ and $Z = \begin{pmatrix}1&0\\0&-1\end{pmatrix}$, and set

$$H = X + Z = \begin{pmatrix}1&1\\1&-1\end{pmatrix}.$$

This is a Hermitian matrix describing a single two-level system (a spin in a tilted magnetic field, say — not yet a physical qubit, just the simplest non-trivial quantum system that exists).

**Eigenvalues.** Since $X$ and $Z$ anticommute ($XZ + ZX = 0$), we get $H^2 = X^2 + \{X,Z\} + Z^2 = I + 0 + I = 2I$. The eigenvalues are $\pm\sqrt{2}$.

**Propagator in closed form.** Writing $H = \sqrt{2}\,(\hat{n}\cdot\vec{\sigma})$ with unit vector $\hat{n} = (\hat{x} + \hat{z})/\sqrt{2}$, the spin-rotation identity gives:

$$e^{-iHt} = \cos(\sqrt{2}\,t)\,I - i\,\frac{\sin(\sqrt{2}\,t)}{\sqrt{2}}\,H.$$

**Evolution from $\lvert 0\rangle$.** Starting from the computational state $\lvert 0\rangle = (1,\,0)^T$:

$$a(t) = \cos(\sqrt{2}\,t) - i\frac{\sin(\sqrt{2}\,t)}{\sqrt{2}}, \qquad b(t) = -i\frac{\sin(\sqrt{2}\,t)}{\sqrt{2}},$$

and you can verify $\lvert a(t)\rvert^2 + \lvert b(t)\rvert^2 = 1$ for all $t$ by direct computation. Unitarity is not a hope — it's algebra.

**The observable beats at the gap.** The expectation of $Z$ oscillates:

$$\langle Z\rangle(t) = \lvert a\rvert^2 - \lvert b\rvert^2 = \frac{1}{2}\bigl(1 + \cos(2\sqrt{2}\,t)\bigr).$$

The oscillation frequency is $2\sqrt{2} = E_+ - E_-$, *exactly* the energy gap. This is the general pattern: observables connecting different energy eigenstates beat at the frequency of the energy difference between them.

This closed-form solution is the "exact" reference against which any numerical integrator — Euler, Trotter, or otherwise — is measured.

## Why Euler breaks it — and why that matters

Given the elegance of the exact solution, why would anyone integrate numerically? Two reasons, and *only* these:

1. **Size.** At $N$ two-level systems, $H$ is $2^N \times 2^N$. Finding the full eigenbasis becomes impossible. Stepping the ODE forward using matrix-vector products does not require knowing the eigenbasis.

2. **Time dependence.** If $H = H(t)$ changes during the evolution — as in an annealing schedule, which we will meet in the next post — then $[H(t), H(t')] \neq 0$ in general, and no closed-form exponential exists.

The simplest integrator is forward Euler: approximate $e^{-iH\Delta t} \approx I - iH\Delta t$. Call this one-step map $M$. Is $M$ unitary?

$$M^\dagger M = (I + iH\Delta t)(I - iH\Delta t) = I + \Delta t^2\,H^2 \neq I.$$

So the norm after one step is:

$$\lVert M\lvert\psi\rangle\rVert^2 = \lVert\psi\rVert^2 + \Delta t^2\,\langle H^2\rangle.$$

*Every* step inflates the norm. This is not numerical noise — it is a *structural* defect. Euler keeps only the first two terms of $e^{-iH\Delta t} = I - iH\Delta t - \frac{1}{2}\Delta t^2 H^2 + \cdots$, and no finite polynomial in $H$ can be unitary. Unitarity belongs to the infinite series.

This is why the quantum simulation community invests so much in methods that preserve unitarity *by construction*:

- **Product formulae** (Trotter-Suzuki splitting) compose exact unitaries of simpler sub-Hamiltonians.
- **Block encodings and quantum signal processing** (QSP — a framework for implementing polynomial transformations of a Hamiltonian's eigenvalues via a structured sequence of signal-processing rotations) achieve unitarity from the architecture up.
- **Variational methods** parameterise a circuit of native unitary gates and optimise the parameters.

The constraint is non-negotiable: if your integrator breaks unitarity, it breaks conservation of probability, and your simulation computes a state that cannot physically exist.

## The bridge, in one paragraph

A Hermitian matrix $H$ has real eigenvalues $E_n$ and an orthonormal eigenbasis $\lvert E_n\rangle$. Time evolution attaches a phase $e^{-iE_n t}$ to each eigenstate; populations are frozen, only relative phases rotate, beating at energy-gap frequencies. The propagator $e^{-iHt}$ is unitary because $H$ is Hermitian, so total probability is exactly conserved. No finite polynomial can replicate this — which is both the *reason* for numerical integration and the *constraint* it must satisfy. You need numerics only when $H$ is too large to diagonalise or too time-dependent to exponentiate analytically.

Everything in quantum computing — from a single-spin rotation to fault-tolerant Hamiltonian simulation — rests on this structure.

## What's next

The next post in this series asks: what if you do not have the ground state, but you *do* have a Hamiltonian whose ground state is easy to prepare? If you slowly deform that easy Hamiltonian into the hard one — respecting a gap condition — you can *adiabatically* arrive at the ground state you actually want. The zoo of strategies for making that work (and the surprisingly many ways it fails) is the subject of Part 2: *Preparing Ground States by Slow Driving*.

Keep rotating!
