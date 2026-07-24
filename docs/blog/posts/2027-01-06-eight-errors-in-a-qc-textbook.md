---
date: 2027-01-06
categories:
  - Lessons from the Trenches
tags:
  - quantum computing
  - education
  - correctness
  - review
authors:
  - John Azariah
social:
  linkedin: |
    A correctness audit of a quantum computing textbook turned up eight high-severity errors, and none of them were typos. They were conceptual mistakes that a competent reader would trust on first pass: a financial pricing example that computed the wrong quantity, a normalisation that used the wrong count, an operator identity with the indices reversed.

    The post walks through each error class, explains why it is easy to make (the concepts are genuinely close neighbours), and offers a checklist for anyone writing or reviewing quantum computing educational material. The common thread is that quantum computing sits at an intersection of disciplines, and each discipline has conventions that quietly collide with the others.

    Full post (link in first comment).
  bluesky: |
    Eight high-severity errors in a quantum computing textbook, none of them typos. A post about the conceptual traps that sit at the intersection of physics, CS, and chemistry conventions, and a checklist for catching them before publication.
---

# Eight Invisible Bugs: A Reviewer's Field Guide to Quantum Computing Errors

*For the authors who invited the audit — and for every reviewer who has ever read a manuscript, found something that felt wrong, and then doubted themselves because the notation was unfamiliar. Trust that instinct.*

<!-- more -->

## Why reviewing quantum material is unusually hard

I recently had the privilege of conducting a full correctness audit on a quantum computing textbook manuscript. The book was well-written, conceptually coherent at the big-picture level, and clearly the product of serious care. It was also wrong in eight places that mattered.

None of the errors were typos. None produced compiler warnings or crashed a simulation. Each one looked *exactly right* to a reader who had not yet internalised the precise distinction the error violated — and that is what makes quantum computing education so treacherous.

The problem is structural. Quantum computing sits at the intersection of at least four disciplines — linear algebra, quantum mechanics, computer science, and (for chemistry applications) molecular physics — and each discipline brings conventions that quietly collide with the others. A physicist's "raising operator" means something precise; a computer scientist's "qubit" means something precise; a chemist's "active orbital" means something precise. But the moment you write a textbook that addresses all three audiences, these terms start rubbing against each other in ways that produce *silent* conceptual errors.

This post is a field guide. I will walk through the eight high-severity findings from that audit, grouped by *why* they were easy to make, and close with a checklist that any author or reviewer can apply. The goal is not to embarrass anyone — the errors were all fixed before publication — but to name the traps clearly enough that the next person sees them coming.

---

## "I definitely computed *something*…"

### The wrong financial quantity

The manuscript's finance chapter set up a quantum amplitude estimation (QAE) circuit to price a European call option — that is, to estimate the expected payoff $\max(S_T - K, 0)$, where $S_T$ is the stock price at maturity and $K$ is the strike price. QAE is a quantum algorithm that estimates the probability of measuring a marked state, then converts that probability into a financial expectation.

But the worked example actually computed something different. It marked all states where the payoff *exceeded a threshold* and estimated the probability of that event:

$$\Pr[\text{payoff} > \text{threshold}].$$

That is a digital option (a binary bet on whether the price crosses a level), not a vanilla call. The standard amplitude-estimation construction for pricing a call encodes a *bounded payoff function* $f(x)$ into an ancilla amplitude:

$$\sum_x \sqrt{p_x}\lvert x\rangle\left(\sqrt{1-f(x)}\lvert 0\rangle + \sqrt{f(x)}\lvert 1\rangle\right),$$

and then estimates $\mathbb{E}[f(X)]$ — the expected value of the payoff, not the probability of exceeding a threshold.

**Why it is easy to make.** Both constructions use QAE. Both involve marking states and estimating amplitudes. The difference is *what* you encode into the ancilla rotation — a binary flag (threshold exceeded: yes/no) or a continuous payoff value (how much was it exceeded by). If you are thinking "amplitude estimation prices options" without pausing on the encoding step, you naturally land on the simpler binary version.

**The check.** When your worked example claims to compute quantity $X$, write down *exactly* what the circuit measures. Does that measurement, after post-processing, actually equal $X$? Or does it equal something nearby but different?

---

### The wrong normalisation in Shor's algorithm

Shor's algorithm for integer factorisation uses the quantum Fourier transform (QFT) — a unitary transformation that maps computational basis states to frequency-domain states — to extract the period $r$ of modular exponentiation. After measuring the output register, the input register collapses to a periodic superposition of states congruent to some $x_0$ modulo $r$.

The manuscript wrote this state as:

$$\frac{1}{\sqrt{r}} \sum_{j=0}^{r-1} \lvert x_0 + jr\rangle.$$

The normalisation $1/\sqrt{r}$ implies there are exactly $r$ terms. But the number of terms is not $r$ — it is $M \approx Q/r$, where $Q = 2^n$ is the size of the input register. The correct state is:

$$\frac{1}{\sqrt{M}} \sum_{j=0}^{M-1} \lvert x_0 + jr\rangle,$$

where $M = \lfloor (Q - 1 - x_0)/r \rfloor + 1$ depends on both the register size and the specific value $x_0$.

**Why it is easy to make.** Both $r$ and $M$ describe "how many evenly-spaced terms there are." If you are writing quickly and thinking about the period, $r$ feels like the natural count. The error is invisible unless you check dimensions: a register of size $Q$ holding $r$ terms (where typically $Q \gg r$) would have a ridiculous occupation density.

**The check.** For any quantum state you write down, count the terms and confirm the normalisation squares to 1. If the number of terms depends on the register size, say so.

---

## "It works like Deutsch-Jozsa, right?" (Narrator: it does not)

### The catalyst that is not a catalyst

In Deutsch-Jozsa's algorithm, a single ancilla qubit prepared in the state $\lvert - \rangle = (\lvert 0\rangle - \lvert 1\rangle)/\sqrt{2}$ acts as a "phase-kickback catalyst": the oracle flips it conditionally, the relative phase propagates back into the input register, and the ancilla returns to $\lvert -\rangle$ unchanged. It genuinely *catalyses* the phase without being consumed.

The manuscript extended this catalyst language to Shor's full period-finding circuit, describing the modular-exponentiation register as returning to its starting state and leaving all information purely in the phase of the input register. That is wrong. In Shor's circuit, the modular-exponentiation register is generally *entangled* with the input register until it is measured or traced out. It does not return to its starting state; it is not a catalyst.

**Why it is easy to make.** Both circuits use phase kickback. Both extract information into the input register. The Deutsch-Jozsa version is simple and memorable, and it *feels* like it should generalise — after all, the mechanism is "the same." But a single-qubit oracle that acts as $\lvert x \rangle \lvert b \rangle \to \lvert x \rangle \lvert b \oplus f(x)\rangle$ on $\lvert - \rangle$ is structurally different from a multi-qubit modular exponentiation that maps $\lvert x\rangle\lvert 0\rangle \to \lvert x\rangle\lvert a^x \bmod N\rangle$.

**The check.** When you claim a mechanism from circuit $A$ also operates in circuit $B$, write down the *specific unitary* in both cases and check whether the structural property you are claiming (catalyst behaviour, factorisation, commutativity) actually holds for the larger, more complex case.

---

## Mind the order — it's a doozy!

### The raising operator that "leaves $\lvert 1\rangle$ unchanged"

The manuscript's chapter on VQE (the variational quantum eigensolver — an algorithm that finds the lowest eigenvalue of a Hamiltonian by optimising a parameterised quantum circuit) described the raising operator as:

> "$\frac{1}{2}(X - iY)$ flips $\lvert 0\rangle$ to $\lvert 1\rangle$ while leaving $\lvert 1\rangle$ unchanged."

The first half is correct: the raising operator $\sigma^+ = (X - iY)/2$ satisfies $\sigma^+\lvert 0\rangle = \lvert 1\rangle$. But it does not "leave $\lvert 1\rangle$ unchanged." It *annihilates* it:

$$\sigma^+\lvert 1\rangle = 0.$$

The zero vector, not $\lvert 1\rangle$. "Unchanged" suggests a projection or identity; "annihilated" means the state is destroyed — it maps to something outside the physical Hilbert space (the zero vector has no normalisation).

**Why it is easy to make.** The word "leaves unchanged" is a natural shorthand for "does not flip it back to $\lvert 0\rangle$." In that sense the intuition is almost right — the raising operator does not *lower*. But "does not lower" and "leaves unchanged" are different claims, and the distinction matters the moment you do algebra with the result.

### The Y-measurement basis that was assembled backwards

In the same chapter, the manuscript described measuring in the $Y$ basis (one of the three Pauli bases) by applying $S^\dagger H$ before a computational-basis measurement, then claimed:

$$S^\dagger H \cdot Y \cdot H S = Z.$$

That identity is incorrect — the gate order is reversed. The correct relation, if you apply $H S^\dagger$ as the measurement unitary $U$, is:

$$U^\dagger Z U = Y \quad\Longleftrightarrow\quad H S^\dagger \cdot Y \cdot S H = Z.$$

**Why it is easy to make.** Basis-change identities involve compositions of gates where the adjoint reverses the order. If you are writing from memory rather than re-deriving, it is natural to place $S^\dagger$ on the same side as $H$ in the order you would *apply* them to the state, rather than the order the conjugation identity requires. The error is invisible unless you multiply it out.

**The check.** For any claimed operator identity $A B C = D$, multiply it out explicitly — even if it takes an extra line. Alternatively, check on the computational basis: if $S^\dagger H Z H S = Y$ is claimed, apply both sides to $\lvert 0\rangle$ and see whether you get the same vector.

---

## The phase transition that could not possibly be there

### The phase transition that is not a phase transition

The manuscript's materials-science chapter presented a 2-site Hubbard model (a minimal quantum model of interacting electrons on a lattice) and described the energy curve as showing a "Mott insulator transition" — a quantum phase transition where a conducting material becomes an insulator as electron-electron repulsion dominates.

But a 2-site system cannot exhibit a genuine phase transition. Phase transitions are properties of the thermodynamic limit (infinitely many sites); they require a discontinuity or divergence in some order parameter that *cannot* occur in a finite system. What a 2-site dimer shows is a smooth *crossover* from delocalised to localised behaviour as the interaction strength $U/t$ increases. Calling it a "transition" is physically inaccurate, and claiming it is "visible in the ground-state energy curve" overstates what the example demonstrates.

**Why it is easy to make.** The 2-site behaviour *looks like* a transition: there is a qualitative change in character as $U/t$ grows. The word "transition" feels descriptive. And the actual phase transition at infinite size is the whole reason the model is interesting, so it is natural to point ahead to it. But the pedagogical claim — "you can *see* the transition here" — is wrong, because what you can see is a finite-size precursor, not the thing itself.

**The check.** When your toy example claims to demonstrate phenomenon $P$, ask: does $P$ have a definition that requires features this example provably cannot have? (Infinite size, broken symmetry, a divergent correlation length.) If so, name what the example *actually* shows — the precursor, the trend, the analogy — and be explicit about what it cannot show.

---

## When the numbers fight each other

### Orders of magnitude that do not agree

The manuscript gave resource estimates for simulating the Hubbard model (a lattice model of interacting electrons) using quantum phase estimation (QPE — an algorithm that extracts eigenvalues of a unitary operator by measuring interference patterns in an ancilla register). One chapter quoted Babbush-style numbers: an $8 \times 8$ lattice needing roughly 400 logical qubits and $10^{11}$ T-gates. A later deep-dive chapter then claimed a $10 \times 10$ lattice needed only $10^7$ gates on about 200 qubits.

Those claims cannot both be correct in the same resource model. Even as back-of-the-envelope estimates, the deep-dive number is far too small relative to the chapter it is supposed to elaborate. A $10 \times 10$ lattice is larger than an $8 \times 8$ one; the qubit count and gate count should both be *larger*, not four orders of magnitude smaller.

### Active-space accounting that uses two conventions simultaneously

Separately, the manuscript's chemistry chapters described an active space of "16 active orbitals" and then claimed this became "~12–16 qubits" after encoding and tapering. But another chapter used the convention where active orbitals are *spatial* orbitals, and explicitly stated that 10–14 active orbitals become 20–28 qubits after Jordan-Wigner encoding (a mapping from fermionic operators to qubit operators that represents each spin-orbital as one qubit).

If "16" means spatial orbitals, the qubit count before tapering is about 32, not 12–16. If "16" means spin-orbitals (where each spatial orbital contributes two spin-orbitals), the terminology needs to say so. The two chapters were using incompatible conventions for the same word without flagging the difference.

**Why both are easy to make.** Resource estimates live in a thicket of assumptions: which algorithm variant, which error-correction overhead, which encoding, Trotterised or qubitised, logical or physical qubits. Different papers quote different layers of the stack. If you pull numbers from two sources without normalising them to the same layer, they *will* disagree — and unless you put them on the same page (which the manuscript unfortunately did), the disagreement may not be obvious to any single reader.

**The check.** Whenever two sections quote resource estimates for the same problem at different sizes, ensure they are consistent: larger problem → larger (or equal) resources. When mixing spatial-orbital and spin-orbital language, state the convention once, clearly, and use it consistently. A simple table — "spatial orbitals → spin-orbitals → qubits (before tapering) → qubits (after tapering)" — eliminates the ambiguity.

---

## The reviewer's checklist

Every error above fell into one of four traps. Here is the short version you can tape to your monitor:

!!! tip "Before you ship quantum computing educational material"

    1. **Did I compute the thing I claimed?** Write down exactly what the circuit measures. Trace it through post-processing. Does the final quantity match the heading?

    2. **Did I generalise a mechanism beyond its domain?** If circuit $B$ "works like" circuit $A$, write down the unitary for both. Does the structural property survive the generalisation?

    3. **Are my operator identities correct in this specific order?** Multiply them out. Check on a basis state. The adjoint reverses the composition order — did you reverse it?

    4. **Can my toy example actually demonstrate what I claimed?** Does the phenomenon require features (infinite size, broken symmetry, divergent correlations) that a finite example provably cannot have?

    5. **Do my resource estimates agree with each other?** Larger problem → at least as many resources. Same word (orbital, qubit, gate) → same convention everywhere.

    6. **Is every symbol defined before I use it?** Read as a stranger arriving from a search result. The first unresolvable token is a defect.

---

## The uncomfortable conviction

The experience left me with one uncomfortable conviction: *every* quantum computing textbook probably has errors like these, and most of them are never caught. The genre is young. The reviewer pool is small. The disciplinary intersection makes it genuinely hard for any single expert to catch all the traps — a physicist might miss the CS convention issue, a computer scientist might miss the chemistry encoding subtlety, and a mathematician might miss the finite-size-scaling caveat.

The saving grace is that these errors are *findable*. They are not deep controversies or matters of interpretation. Each one has a concrete, checkable correction. The checklist above is not brilliance — it is just discipline. Multiply out your identities. Count your terms. Name your conventions. Check your examples against their own definitions.

If you are writing quantum computing material — a textbook, a tutorial, a lecture — I hope this field guide saves you the discomfort of a post-publication erratum. And if you are reviewing someone else's: trust your instinct when something feels wrong. The notation may be unfamiliar, but the smell of a conceptual slip is the same in every field.

*Keep checking!*
