---
date: 2026-07-29
notebook: https://github.com/johnazariah/quantum/blob/main/bottleneck/notebooks/02-cryptography.ipynb
categories:
- The Quantum Bottleneck
- Cryptography
tags:
- Shor's algorithm
- period-finding
- RSA
- QFT
- quantum phase estimation
authors:
- John Azariah
social:
  linkedin: 'Shor''s algorithm is usually introduced as the quantum algorithm that factors numbers. I think that description skips the useful move: the circuit estimates a period, and ordinary number theory turns that period into factors.


    N=15 and a=7 earn their place because every arithmetic step fits on the page. The notebook compiles one known phase branch, reads 1/4 as 010, recovers period 4 with continued fractions, and obtains 3 and 5 with greatest-common-divisor arithmetic.


    At cryptographic scale, all the omitted machinery returns. A real implementation still needs reversible modular exponentiation, error correction, and millions of physical qubits. Factoring 15 is the transparent example; those missing resources are the reason RSA is not falling to today''s hardware.


    This post is for Simon Middlemiss: https://www.linkedin.com/in/simon-middlemiss-3959b12/


    In memory of that glorious talk we did together in Las Vegas in 2019. Truly one of the very best!


    #QuantumComputing #Cryptography'
  bluesky: 'Shor''s algorithm is usually introduced as a factoring algorithm. I chose N=15 because it makes the more useful move visible: a quantum circuit exposes a period, then classical arithmetic turns that period into factors.'
---

# The Trapdoor

*For [Simon Middlemiss](https://www.linkedin.com/in/simon-middlemiss-3959b12/), in memory of that glorious talk we did together in Las Vegas in 2019! Truly one of the very best!*

The Rivest-Shamir-Adleman (RSA) cryptosystem publishes a number $N = pq$ while keeping its prime factors $p$ and $q$ secret. Multiplying the primes is routine; no efficient classical algorithm is known for recovering them from a suitably large product.

Shor's algorithm changes that security assumption by reducing factoring to period-finding. The notebook uses $N = 15$ and $a = 7$, with one known phase branch compiled into a small circuit. It demonstrates the phase readout and classical post-processing while leaving scalable modular exponentiation outside the circuit.

<!-- more -->

RSA's method and modulus are public. Its security rests on a one-way asymmetry:

```text
easy:  multiply two large primes
hard:  recover those primes from their product
```

If you are given two large primes, multiplying them is routine. Given only their product $N$, recovering the primes appears to be much harder. That asymmetry is the trapdoor: the factors make decryption and signing efficient, while the public modulus leaves an attacker facing the factoring problem.

Since RSA was published in 1978,[^rsa] this public-key idea has shaped the secure web, software updates, certificates, VPNs, messaging systems, and the everyday assumption that two machines can agree on secrets over a public network.

There is no proof that classical factoring is hard. RSA relies on decades of evidence that the best known classical algorithms still do not make large moduli easy to factor.

Shor's algorithm found a different route: change the factoring problem into a period-finding problem.[^shor]

## The shape under RSA

The notebook starts with $N = 15$ because 15 is the smallest RSA-shaped composite that lets the mechanism be visible without drowning us in arithmetic.

Nobody needs a quantum computer to factor 15. This instance is useful because it exposes the reduction without burying it under reversible arithmetic. Pick a number $a$ that is coprime to $N$, and look at the function:

$$
f(x) = a^x \bmod N.
$$

For the notebook, $N = 15$ and $a = 7$.

Compute the first few values:

```text
x      0   1   2   3   4   5   6   7
7^x    1   7   4   13  1   7   4   13   (mod 15)
```

The values repeat every four steps. That repeating length is the **period**, or order, of $a$ modulo $N$:

$$
r = 4.
$$

If we know that period, the factors fall out by ordinary arithmetic. Since $r$ is even, compute:

$$
7^{r/2} = 7^2 \equiv 4 \pmod{15}.
$$

Take the greatest common divisors (GCDs):

$$
\gcd(4 - 1, 15) = 3,
$$

and:

$$
\gcd(4 + 1, 15) = 5.
$$

So:

```text
15 = 3 x 5
```

The factoring problem has become a period-finding problem.

## Why period-finding is the bottleneck

The function $a^x \bmod N$ is easy to evaluate at any one $x$, while recovering its period efficiently is the difficult part.

For large $N$, the period can be large, and the values can look irregular if you only sample them point by point. A classical machine can compute:

```text
f(0), f(1), f(2), ...
```

but finding the hidden repetition quickly is the hard part. Modern classical factoring algorithms are much more sophisticated than naive period search, but they still do not become polynomial-time factoring algorithms.

Shor's algorithm arranges a quantum computation so that the period is written into phase, then uses a Fourier transform to make that phase measurable:

```text
period in arithmetic -> phase in a quantum state -> measured bit string
```

[Circuit Bench 00: Reading a Quantum Circuit](../../circuit-bench/00-reading-a-quantum-circuit/README.md) supplies the gate, basis, and measurement vocabulary used below if those ideas are new.

## The quantum move is phase estimation

The popular explanation that a quantum computer searches all candidate divisors simultaneously describes the wrong computation. Shor's algorithm estimates a period.

The circuit-level statement is:

> Shor's algorithm uses quantum phase estimation on a modular-multiplication unitary.

For this notebook, we only need three pieces of that statement.

Define a reversible quantum operation, or unitary:

$$
U_a |y\rangle = |ay \bmod N\rangle.
$$

This operation has eigenphases. Those phases contain fractions of the form:

$$
\frac{j}{r},
$$

where $r$ is the period we want.

Quantum phase estimation (QPE) is the circuit pattern that estimates such a phase fraction. It uses a counting register, controlled powers of $U_a$, and an inverse quantum Fourier transform (QFT). For the gate-level version of that pattern, see [Circuit Bench 10: Quantum Phase Estimation](../../circuit-bench/10-quantum-phase-estimation/README.md).

The QFT turns periodic phase structure into a measurement pattern. Applied by itself to a computational-basis state, its output looks uniformly random when measured because the information remains in relative phase. Its role becomes useful inside the larger phase-estimation circuit. [Circuit Bench 09: Quantum Fourier Transform](../../circuit-bench/09-quantum-fourier-transform/README.md) walks through that circuit directly.

The high-level Shor pipeline is:

```text
choose a
build modular multiplication by a mod N
run phase estimation
measure an approximation to j/r
use continued fractions to recover r
use gcd arithmetic to recover factors
```

The quantum computer does the period-finding step. The final extraction of factors is classical.

## Compile one period branch

The [Unit 2 notebook: compiled period-finding for $N = 15$](https://github.com/johnazariah/quantum/blob/main/bottleneck/notebooks/02-cryptography.ipynb) takes the $N = 15$, $a = 7$, $r = 4$ example and compiles one phase-estimation branch into a small circuit.

A scalable modular-exponentiation circuit for arbitrary $N$ is outside its scope; that circuit is the expensive part of a full implementation.

With the arithmetic compiled away, the remaining steps stay visible:

```text
classical reduction
compiled phase-estimation circuit
inverse QFT
continued fractions
gcd post-processing
```

### Section 1: Check the classical period

The notebook begins with the arithmetic.

```python
N = 15
a = 7
```

It computes the values of $7^x \bmod 15$ and verifies the repeating pattern:

```text
1, 7, 4, 13, 1, 7, 4, 13, ...
```

This gives the classical period $r = 4$.

We already know the answer, which gives us ground truth for checking the circuit output.

### Section 2: Compile one phase branch

For $r = 4$, the phase fractions are multiples of:

$$
\frac{1}{4}.
$$

The notebook chooses the branch:

$$
\frac{j}{r} = \frac{1}{4}.
$$

With three counting qubits, the phase-estimation register has:

$$
Q = 2^3 = 8
$$

possible values. The phase $1/4$ corresponds to:

$$
\frac{2}{8},
$$

so the expected measurement peak is the three-bit string:

```text
010
```

Instead of building the full modular-multiplication unitary, the notebook inserts the controlled phases for this branch directly:

```qasm
cu1(phase_angle) q[2], q[3];
cu1(2 * phase_angle) q[1], q[3];
cu1(4 * phase_angle) q[0], q[3];
```

This compiled circuit demonstrates the QPE and inverse-QFT logic after the hard arithmetic has been supplied classically.

### Section 3: Measure the phase

The circuit runs many shots and counts the observed bit strings.

The circuit output is a phase estimate. The dominant bit string should be:

```text
010
```

Interpreted as an integer, that is:

$$
k = 2.
$$

The phase estimate is:

$$
\frac{k}{Q} = \frac{2}{8} = \frac{1}{4}.
$$

Measurement gives a classical bit string, after which the number-theory work resumes.

### Section 4: Recover the period

The notebook uses continued fractions:

```python
frac = Fraction(best_k, Q).limit_denominator(N)
r_candidate = frac.denominator
```

For the clean branch:

$$
\frac{2}{8} = \frac{1}{4},
$$

so the denominator is:

$$
r = 4.
$$

The notebook then checks:

$$
7^4 \equiv 1 \pmod{15}.
$$

The validation step catches unhelpful branches, noisy estimates, and candidate denominators that fail. Shor's algorithm is probabilistic: if a branch does not give a useful period, you try again.

### Section 5: Turn the period into factors

Once the period is recovered, the remaining work is classical.

The notebook returns to classical arithmetic:

```python
x = pow(a, r // 2, N)
factor1 = math.gcd(x - 1, N)
factor2 = math.gcd(x + 1, N)
```

For $N = 15$, $a = 7$, and $r = 4$:

```text
x = 7^2 mod 15 = 4
gcd(4 - 1, 15) = 3
gcd(4 + 1, 15) = 5
```

## The pipeline, end to end

The compiled example exposes the skeleton of Shor's algorithm:

1. Factoring can be reduced to period-finding.
2. Period information can be encoded as quantum phase.
3. Phase estimation can turn that hidden phase into measured bits.
4. Continued fractions can recover the period from those bits.
5. GCD arithmetic can turn the period into factors.

The expensive part of a full implementation is absent: reversible modular exponentiation at cryptographic scale. Error correction, fault-tolerant gate synthesis, layout constraints, and the engineering needed to run Shor's algorithm against RSA-2048 are also outside the notebook.

Those omitted resources separate the factoring theorem from a cryptographic-scale threat.

## Reality check

Shor's algorithm is mathematically settled: a sufficiently large, fault-tolerant quantum computer would break RSA and related discrete-log cryptosystems. The unresolved question is when hardware with the required scale and error correction will exist.

Laboratory demonstrations of Shor-style factoring have stayed tiny, with examples such as 15 and 21.[^martin-lopez] Larger claims often use compiled circuits that bake in so much structure from the answer that they no longer represent scalable factoring.

For RSA-2048, the resource estimates are far beyond today's machines. Gidney and Ekera estimated that factoring a 2048-bit RSA integer in about eight hours would require roughly 20 million noisy physical qubits using surface-code error correction.[^gidney-ekera] Estimates will move as architectures improve; this remains a fault-tolerant-era algorithm.

The migration has already started because of **harvest now, decrypt later**. An adversary can record encrypted traffic today and retain it until a future machine can decrypt it. NIST released its first final post-quantum encryption and signature standards in 2024.[^nist-pqc]

Current quantum computers cannot break RSA. Shor nevertheless changes the long-term security assumption, so systems protecting long-lived information need to migrate before a cryptographically relevant machine arrives.

## Change the phase branch

The clean `010` output comes from one chosen branch. Change it:

Change the phase branch:

```python
target_j = 3
```

The fraction $3/4$ should still reveal denominator 4.

Then try:

```python
target_j = 2
```

That branch gives $1/2$, whose denominator is 2, not the full period. The notebook's validation step should catch that this candidate is not good enough for the factoring post-processing. This is a useful failure, because real Shor runs also have branches that force a retry.

Then inspect the `qpe_circuit` string itself. Trace the three controlled phase gates, then trace the inverse QFT. The lasting lesson is how phase becomes an ordinary bit string that continued fractions can use.

The value of the example is the complete route from factoring to period-finding, phase estimation, continued fractions, and greatest-common-divisor arithmetic. That route is why cryptographers took Shor seriously long before the hardware existed.

[^rsa]: Rivest, Shamir, and Adleman, ["A Method for Obtaining Digital Signatures and Public-Key Cryptosystems"](https://people.csail.mit.edu/rivest/Rsapaper.pdf), Communications of the ACM, 1978.

[^shor]: Peter W. Shor, ["Algorithms for Quantum Computation: Discrete Logarithms and Factoring"](https://doi.org/10.1109/SFCS.1994.365700), 35th Annual Symposium on Foundations of Computer Science, 1994.

[^martin-lopez]: Martin-Lopez et al., ["Experimental realization of Shor's quantum factoring algorithm using qubit recycling"](https://doi.org/10.1038/nphoton.2012.259), Nature Photonics, 2012.

[^gidney-ekera]: Craig Gidney and Martin Ekera, ["How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits"](https://quantum-journal.org/papers/q-2021-04-15-433/), Quantum, 2021.

[^nist-pqc]: NIST, ["NIST Releases First 3 Finalized Post-Quantum Encryption Standards"](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards), 2024.

Next up: [The $2B Molecule](bottleneck-03-drug-discovery.md) — where the hidden period gives way to a quantum system too large to simulate directly.
