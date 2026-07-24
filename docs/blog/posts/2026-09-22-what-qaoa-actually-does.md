---
date: 2026-09-22
categories:
  - QAOA from Scratch
tags:
  - QAOA
  - quantum computing
  - combinatorial optimisation
  - interference
authors:
  - John Azariah
social:
  linkedin: 'QAOA is not "try all answers at once." It is structured interference: phase rotations encode problem quality, a mixer lets amplitude flow between neighbours, and the two alternate until good solutions reinforce and bad ones cancel. This post explains the mechanism from zero, using 100 light switches and 133 rules as the running example, and makes the honest claim: QAOA does not make NP-hardness evaporate, but it does sculpt probability toward good answers in a way that improves monotonically with circuit depth.


    #QuantumComputing #Optimisation'
  bluesky: 'QAOA explained from zero. Phase rotations set up interference, a mixer exploits it, and repetition sharpens the filter. One running example, no prerequisites, honest claims.'
---

# What QAOA Actually Does

*This series is dedicated to Stephen Jordan — who posed the question that became a PhD project, and whose patient insistence on "but what does it actually compute?" forced the clarity that made the answer publishable.*

<!-- more -->

## A hundred switches and a hundred-odd rules

Here is a puzzle you can describe to anyone.

You have 100 light switches on the wall, each either up or down. Taped beside them are 133 rules, each involving exactly three switches:

> Switches 7, 23, and 41 must have an odd number in the UP position.

You want to flip switches until as many rules as possible are satisfied.

How hard is that? A random configuration satisfies about half the rules — because each three-way XOR (exclusive-or: the parity check "is the count odd?") is equally likely to land on 0 or 1 for a random assignment. That fifty percent is your baseline. Can you do better?

A good classical heuristic called *simulated annealing* — accept random flips that improve the score, occasionally accept bad flips to escape dead ends — pushes to about 94%. That is a strong classical baseline, and it is not going anywhere. A recent quantum algorithm called DQI (Decoded Quantum Interferometry, with belief-propagation decoding), which combines quantum interference with classical error-correction, reaches about 87%.

And then there is QAOA.

**QAOA** — the Quantum Approximate Optimisation Algorithm[^farhi2014] — alternates two operations in a quantum circuit, and at sufficient depth it crosses that 87% line and keeps climbing. The interesting contest is quantum-vs-quantum: QAOA against DQI, in a regime where DQI is provably limited (Post 7 delivers that punchline). The rest of this series builds the full machinery. This post explains *what QAOA actually does*, in a way you can hold in your head before a single equation arrives.

## "Tries all answers at once" — and why that misses the point

The sentence you will hear, usually delivered with unearned confidence, is:

> A quantum computer tries all answers at once.

There is a grain of truth buried here. A quantum computer *can* hold all $2^{100}$ switch configurations simultaneously in a state called a **superposition**. Each configuration carries a complex number called its **amplitude**. The probability of seeing any particular configuration when you measure is the squared magnitude of its amplitude.

But if you prepared that superposition and immediately measured — if "trying all answers at once" were the whole story — you would just get a random bit string. You would have used quantum hardware to generate a coin flip. Superposition alone solves nothing.

The useful word is *interference*.

A quantum algorithm is useful when it arranges the computation so that amplitudes of unwanted possibilities cancel and amplitudes of wanted possibilities reinforce. The possibilities being *present* in superposition is the prerequisite. Their amplitudes being made to interfere — constructively for good answers, destructively for bad ones — is the mechanism.

QAOA is one specific way to arrange that interference for optimisation problems. It does not guarantee the optimum. It does not make NP-hardness evaporate. It produces a probability distribution over candidate answers, and the claim — the honest, quantifiable claim — is that good answers appear more often than they would under blind random sampling.

## The two knobs on the mixing console

QAOA works by alternating two operations, each controlled by an angle. Think of them as two knobs on a mixing console.

### Knob one: the phase separator (angle $\gamma$)

The first operation examines every configuration's quality — how many of the 133 rules it satisfies — and rotates that configuration's amplitude by an angle proportional to its score. In symbols:

$$e^{-i\gamma C}\lvert z\rangle = e^{-i\gamma \cdot C(z)}\lvert z\rangle$$

Here $\lvert z\rangle$ is a computational-basis state (one specific setting of all 100 switches), $C(z)$ is the number of rules that setting satisfies, and $\gamma$ is the angle parameter that controls how aggressively we rotate. The operator $C$ is the cost function, now promoted to a quantum observable — but for now, the only thing that matters is that it *scores* each configuration.

If you measured immediately after this step, nothing would have changed. Rotating a complex number does not change its magnitude, and measurement probabilities depend only on magnitude. No probabilities have shifted. So why bother?

Because *phases determine interference*. Two amplitudes with aligned phases will reinforce each other in the next step. Two amplitudes with misaligned phases will cancel. The phase separator is laying down the interference pattern — setting the stage for what happens next.

### Knob two: the mixer (angle $\beta$)

The second operation allows amplitude to flow between configurations that differ by a single switch flip. Each switch is independently rotated around the $X$-axis (the "bit-flip" axis) by angle $\beta$:

$$e^{-i\beta X_j} = \begin{pmatrix} \cos\beta & -i\sin\beta \\ -i\sin\beta & \cos\beta \end{pmatrix}$$

where $X_j$ is the Pauli-$X$ operator on switch $j$ — the operator that flips a single bit. Applied independently to all 100 switches, this creates a local diffusion of amplitude: probability weight seeps from each configuration into its one-flip neighbours.

And *now* the interference takes effect.

Configurations whose phases are aligned with their neighbours — configurations that received *similar* rotations in the previous step, because they have *similar* scores — reinforce each other through the mixing. Configurations whose phases clash with their neighbours cancel out.

The phase separator arranged things so that good configurations cluster in phase space (similar scores → similar phases). The mixer then concentrates amplitude on those clusters through constructive interference. Bad configurations, whose phases are scattered, lose amplitude through destructive interference.

## Why repetition sharpens the lens

One round of (phase separator → mixer) is a crude filter. The good configurations get a bit more amplitude; the bad ones lose a bit. The separation is real but coarse.

With $p$ rounds, each with its own pair of angles $(\gamma_1, \beta_1, \gamma_2, \beta_2, \ldots, \gamma_p, \beta_p)$, the interference pattern refines:

- At $p = 1$: a blurry lens. Tells bright from dark, details lost.
- At $p = 5$: sharper focus. Distinguishes "very good" from "pretty good."
- At $p = 15$: high resolution. Amplitude concentrates tightly on near-optimal configurations.

The angles are tuneable parameters — $2p$ real numbers in total. Choosing them well is itself an optimisation problem, but a *classical* one: find the $2p$ angles that maximise the expected score of whatever configuration you measure at the end.

The full QAOA state after $p$ rounds is written:

$$\lvert\boldsymbol{\gamma},\boldsymbol{\beta}\rangle = U_M(\beta_p)\,U_C(\gamma_p)\cdots U_M(\beta_1)\,U_C(\gamma_1)\lvert s\rangle$$

where $\lvert s\rangle$ is the uniform superposition (all configurations equally weighted), $U_C(\gamma_\ell) = e^{-i\gamma_\ell C}$ is the phase separator at round $\ell$, and $U_M(\beta_\ell) = \prod_j e^{-i\beta_\ell X_j}$ is the mixer. The expected score is:

$$F_p(\boldsymbol{\gamma},\boldsymbol{\beta}) = \langle\boldsymbol{\gamma},\boldsymbol{\beta}\rvert\, C \,\lvert\boldsymbol{\gamma},\boldsymbol{\beta}\rangle$$

and *that* is the number we maximise over the $2p$ angles. Each value of $p$ gives a provable lower bound on how well QAOA can do. Deeper circuits always do at least as well as shallower ones. In the limit $p \to \infty$, QAOA converges to the true optimum.

## The landscape sculptor

I find the best mental image for QAOA is not a search algorithm — it is a landscape sculptor.

Grover's algorithm (the other famous quantum speedup for search) is a *metal detector*: systematic sweep, beep or no beep, $\sqrt{N}$ steps regardless of terrain. It does not know or care what the problem looks like. Its speedup is generic but blind.

QAOA is different. It *knows about the problem*. Its phase-separator gate is derived directly from the cost function — from the specific rules on the wall. Its mixer respects the neighbourhood structure of the search space (amplitude flows between configurations that are one flip apart, not teleporting randomly).

Imagine pouring water on a relief map of the cost landscape. Tilt the ground so that high-scoring configurations are downhill. Let the water flow. Tilt again, at a different angle. Flow again. After enough rounds, the water pools in the deepest valleys.

That is QAOA. Each round is one tilt-and-flow step. The angles $\gamma$ and $\beta$ control the direction and steepness of each tilt. After $p$ rounds, the amplitude (the water) has concentrated in the good regions of the landscape.

And because the gates encode the problem, QAOA can exploit structure that a generic algorithm cannot. This is why it can outperform Grover on problems with structure — and why its performance improves monotonically with depth.

## Where this series goes from here

This post gave you the mechanism in plain language: the phase separator lays down an interference pattern proportional to solution quality; the mixer converts those phase differences into amplitude differences through local diffusion; repetition sharpens the filter until good solutions dominate.

The remaining posts build the full picture:

- **Post 2** formalises the cost function as a quantum operator and introduces our concrete target: Max-3-XORSAT on 4-regular hypergraphs.
- **Post 3** shows why the computation becomes tractable — on tree-structured graphs, you never need to store the full exponential state.
- **Post 4** presents our original contribution: a Walsh-Hadamard factorisation that makes the hardest step efficient.
- **Post 5** traces the engineering journey from "never completes at depth 5" to "depth 11 in ten minutes."
- **Posts 6–8** cover angle universality, fundamental performance ceilings, and how QAOA and Grover relate as two flavours of quantum interference.

The thread connecting all of them: QAOA is quantum interference applied to combinatorial optimisation. The interference is real, the mechanism is precise, the limitations are honest, and the computation is tractable enough to produce exact numerical answers at depths where the results become interesting.

## What this post deliberately left out

I left out several things on purpose — not because they are unimportant, but because they deserve their own posts:

- **The Hamiltonian encoding.** How exactly do you turn "odd parity among three switches" into a quantum operator? Post 2.
- **Why we can compute this classically at all.** The state has $2^{100}$ amplitudes. We are not simulating all of them. Posts 3 and 4.
- **Whether QAOA actually beats the 87% ceiling.** That is the quantitative punchline of the series. Post 7 delivers the number.

For now, the single takeaway:

!!! info "The QAOA mechanism in one sentence"
    QAOA biases a quantum measurement toward good solutions by alternating problem-quality phase rotations (which encode scores into interference phases) with mixing operations (which concentrate amplitude on phase-aligned configurations through local diffusion).

That is what QAOA actually does. Not "tries all answers at once." Not magic. Structured interference — and the mathematics to compute exactly how much it helps.

Keep reading!

[^farhi2014]: Farhi, Goldstone, Gutmann. "A Quantum Approximate Optimization Algorithm." arXiv:1411.4028 (2014).
