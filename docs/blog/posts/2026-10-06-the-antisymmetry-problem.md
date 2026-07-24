---
date: 2026-10-06
categories:
  - Mapping Fermions to Qubits
tags:
  - fermionic encodings
  - Jordan-Wigner
  - quantum chemistry
  - second quantisation
authors:
  - John Azariah
social:
  linkedin: 'Electrons are not qubits. Their wavefunctions pick up a minus sign whenever two of them swap places, and a quantum computer that ignores that sign structure will simulate the wrong physics. The Jordan-Wigner transform fixes this with a chain of Z operators that tracks parity, but the chain grows linearly with the number of orbitals. For a molecule with 200 active orbitals, every single fermionic operator touches all 200 qubits. This post builds the problem from scratch using hydrogen as a running example, and shows exactly where the cost comes from and why it matters.


    #QuantumComputing #QuantumChemistry'
  bluesky: 'New series on fermionic encodings. Post 1 builds the antisymmetry problem from scratch using hydrogen, derives the Jordan-Wigner transform, and counts the O(n) cost that motivates everything that follows.'
---

# The Antisymmetry Problem: Why Fermions Need Encoding

*For Peter Love, whose 2012 paper with Seeley and Richard gave the field a vocabulary for this problem — and whose framework turns out to be more subtle than it first appears. This series is, in part, an appreciation of that subtlety.*

<!-- more -->

## The molecule on the bench

Here is the smallest interesting molecule in quantum chemistry: H₂. Two hydrogen atoms, bonded. Two electrons sharing four spin-orbitals — two spatial orbitals (call them $\sigma$ and $\sigma^*$, the bonding and antibonding orbitals), each available in spin-up and spin-down flavours.

The question a quantum chemist asks is: *what is the ground-state energy of this system?* The answer determines bond lengths, reaction rates, material properties — essentially, all of chemistry. For H₂ we can solve this classically (it is a $16 \times 16$ matrix problem), but the point is to build the machinery that scales to systems where classical methods cannot.

In the language of second quantisation, the electronic Hamiltonian is

$$H = \sum_{p,q=0}^{3} h_{pq}\, a^\dagger_p a_q \;+\; \frac{1}{2}\sum_{p,q,r,s=0}^{3} h_{pqrs}\, a^\dagger_p a^\dagger_q a_r a_s,$$

where $a^\dagger_p$ creates an electron in spin-orbital $p$ and $a_q$ removes one from spin-orbital $q$. The coefficients $h_{pq}$ (one-electron integrals: kinetic energy and nuclear attraction) and $h_{pqrs}$ (two-electron integrals: electron-electron repulsion) come from classical computation over the molecular orbitals.

To find the ground-state energy on a quantum computer, we need to represent $H$ as an operator on qubits. That means turning $a^\dagger_p$ and $a_q$ into things built from Pauli matrices. And *that* is where electrons start being difficult.

---

## Electrons are rude

### The swap that costs a sign

Take two distinguishable particles — say a proton and a neutron — in states $\lvert\alpha\rangle$ and $\lvert\beta\rangle$. Their joint state is the product $\lvert\alpha\rangle \otimes \lvert\beta\rangle$. If you swap them, you get $\lvert\beta\rangle \otimes \lvert\alpha\rangle$. The two states are different, and both are perfectly valid.

Electrons are *identical fermions*. Quantum mechanics requires their joint wavefunction to be *antisymmetric* under exchange:

$$\lvert\psi\rangle = \frac{1}{\sqrt{2}}\bigl(\lvert\alpha\rangle \otimes \lvert\beta\rangle \;-\; \lvert\beta\rangle \otimes \lvert\alpha\rangle\bigr).$$

Notice the minus sign. Swap the two particles and the state picks up a factor of $-1$. This is not optional; it is a fundamental property of half-integer-spin particles, and every electron in the universe obeys it.

### Exclusion for free

Set $\alpha = \beta$ in that antisymmetric state and watch what happens:

$$\frac{1}{\sqrt{2}}\bigl(\lvert\alpha\rangle \otimes \lvert\alpha\rangle - \lvert\alpha\rangle \otimes \lvert\alpha\rangle\bigr) = 0.$$

The state vanishes. Two electrons *cannot* occupy the same spin-orbital. That is the Pauli exclusion principle — not an extra rule, but a consequence of the minus sign.

### Why this is a problem for simulation

A qubit register is *symmetric*. Flipping qubit 3 from $\lvert 0\rangle$ to $\lvert 1\rangle$ is a local operation: it does not know or care what qubits 0, 1, and 2 are doing. But creating an electron in mode 3 must apply a phase that depends on *how many of the lower modes are already occupied*. The encoding's job is to build that non-local sign structure into the qubit operators.

---

## Counting who's home

### Fock space: the occupation-number picture

Rather than tracking *which* electron is *where* (a bookkeeping nightmare that leads to Slater determinants and antisymmetrisation headaches), we work in *Fock space*. Each mode $j$ is either occupied ($n_j = 1$) or empty ($n_j = 0$). A basis state — an *occupation-number state* — is a binary string:

$$\lvert n_0,\, n_1,\, n_2,\, n_3\rangle, \qquad n_j \in \{0, 1\}.$$

For our H₂ example with $N = 4$ modes, the state $\lvert 1, 1, 0, 0\rangle$ means "modes 0 and 1 are occupied; modes 2 and 3 are empty." The full Fock space has $2^N = 16$ basis states — exactly the dimension of a 4-qubit Hilbert space. That coincidence is what makes quantum simulation possible.

### Creation, annihilation, and the parity phase

The creation operator $a^\dagger_j$ and annihilation operator $a_j$ add and remove electrons from mode $j$:

$$a^\dagger_j \lvert \ldots, 0_j, \ldots\rangle = (-1)^{\sum_{k<j} n_k}\, \lvert \ldots, 1_j, \ldots\rangle,$$
$$a_j \lvert \ldots, 1_j, \ldots\rangle = (-1)^{\sum_{k<j} n_k}\, \lvert \ldots, 0_j, \ldots\rangle.$$

The crucial ingredient is the *parity phase* $(-1)^{\sum_{k<j} n_k}$: the sign depends on the total occupation of all modes with index less than $j$. This is what enforces antisymmetry. Creating an electron in mode 3 when modes 0 and 1 are occupied gives $(-1)^2 = +1$; if only mode 0 is occupied, it gives $(-1)^1 = -1$. The encoding must reproduce this dependence exactly.

---

## The contract

Any fermion-to-qubit encoding must produce operators that satisfy the *canonical anticommutation relations* (the CAR):

$$\{a_i,\, a^\dagger_j\} \;\equiv\; a_i\, a^\dagger_j + a^\dagger_j\, a_i \;=\; \delta_{ij},$$
$$\{a_i,\, a_j\} = \{a^\dagger_i,\, a^\dagger_j\} = 0.$$

Here $\delta_{ij}$ is the Kronecker delta (1 if $i = j$, 0 otherwise) and $\{A, B\} = AB + BA$ is the *anticommutator*. These relations encode everything: the exclusion principle ($a^\dagger_j a^\dagger_j = 0$), the correct counting statistics, and the sign structure under exchange.

The CAR is the contract. An encoding that satisfies it simulates fermions correctly. An encoding that violates it — even at a single pair $(i, j)$ — simulates something else entirely, and every energy eigenvalue it produces is wrong.

---

## One qubit per electron — what could go wrong?

The occupation-number basis looks identical to a qubit computational basis: $\lvert 1, 0, 1, 0\rangle$ in Fock space maps to $\lvert 1010\rangle$ on a qubit register. So let qubit $j$ store the occupation of mode $j$. Easy!

The states map perfectly. The *operators* do not.

If we try to build $a^\dagger_j$ as a simple qubit flip — the operator $\lvert 1\rangle\langle 0\rvert$ acting on qubit $j$ — we get something that changes the occupation correctly but ignores the parity phase. It commutes with operators on other qubits instead of anticommuting. The CAR fails, and we are no longer simulating fermions.

We need an operator that:

1. **Flips** qubit $j$ from $\lvert 0\rangle$ to $\lvert 1\rangle$ (the occupation change),
2. **Applies a sign** $(-1)^{\sum_{k<j} n_k}$ depending on the state of other qubits (the parity), and
3. **Annihilates** the state if qubit $j$ is already $\lvert 1\rangle$ (the exclusion principle).

Requirement 2 makes the operator *non-local*: it must inspect other qubits. The question — the one this entire series is about — is: *how many* other qubits does it need to inspect?

---

## Jordan and Wigner's Z-chain

### The idea (1928!)

Jordan and Wigner's solution is beautifully direct. Store the occupation of mode $j$ in qubit $j$ (as we wanted), and handle the parity with a chain of Pauli $Z$ operators on every qubit below $j$:

$$a^\dagger_j \;=\; \frac{1}{2}(X_j - iY_j) \;\otimes\; Z_{j-1} \otimes Z_{j-2} \otimes \cdots \otimes Z_0.$$

Here $X_j$, $Y_j$, $Z_j$ are the Pauli matrices acting on qubit $j$, and $I_j$ (identity) is implicit on all qubits not listed. The combination $Q^+_j \equiv \frac{1}{2}(X_j - iY_j)$ is the *qubit raising operator*: it maps $\lvert 0\rangle_j \to \lvert 1\rangle_j$ and sends $\lvert 1\rangle_j$ to the zero vector (not a valid state — this is requirement 3).

### Why the Z-chain works

The Pauli $Z$ has eigenvalues $+1$ on $\lvert 0\rangle$ and $-1$ on $\lvert 1\rangle$. So $Z_k$ acting on qubit $k$ contributes $(-1)^{n_k}$ to the product. The full chain gives:

$$Z_{j-1}\, Z_{j-2}\, \cdots\, Z_0 \;=\; (-1)^{n_{j-1} + n_{j-2} + \cdots + n_0} \;=\; (-1)^{\sum_{k<j} n_k}.$$

That is exactly the parity phase the CAR demands. The Jordan-Wigner (JW) transform is the most literal possible encoding: it stores occupation directly and handles parity by reading every lower qubit.

### The H₂ scoreboard

For our 4-mode hydrogen molecule, the four creation operators under JW are:

| Mode $j$ | $a^\dagger_j$ (Jordan-Wigner) | Pauli weight |
|-----------|-------------------------------|:------------:|
| 0 | $\frac{1}{2}(X_0 - iY_0)$ | 1 |
| 1 | $\frac{1}{2}(X_1 - iY_1) \otimes Z_0$ | 2 |
| 2 | $\frac{1}{2}(X_2 - iY_2) \otimes Z_1 \otimes Z_0$ | 3 |
| 3 | $\frac{1}{2}(X_3 - iY_3) \otimes Z_2 \otimes Z_1 \otimes Z_0$ | 4 |

The *Pauli weight* of an operator is the number of qubits it acts on non-trivially (anything other than identity). It determines circuit depth: each non-identity Pauli in the string costs roughly one two-qubit gate to implement. Mode 3 already touches all 4 qubits.

### The cost, honestly

For $N$ modes, the creation operator for mode $j$ has Pauli weight $j + 1$. The worst case is mode $N - 1$, with weight $N$. The average across all modes is $(N + 1) / 2$.

| System | Modes $N$ | Max JW weight | What that means |
|--------|:---------:|:-------------:|----------------|
| H₂ (minimal basis) | 4 | 4 | Fine — toy problem |
| H₂O (6-31G basis) | 14 | 14 | Starting to hurt |
| FeMoCo (active space) | 56 | 56 | Deep circuits |
| Large active space | 200 | 200 | Impractical |

The weight never shrinks relative to $N$. Jordan-Wigner's parity chain scales with the total number of modes, regardless of the molecule's local structure. For large systems, this linear overhead dominates the circuit depth.

---

## Two halves of a whole

There is a cleaner way to state the encoding problem that will serve us well in the posts to come.

### The Majorana decomposition

Every creation operator splits into two Hermitian pieces:

$$a^\dagger_j = \frac{1}{2}(c_j - i\,d_j),$$

where $c_j$ and $d_j$ are the *Majorana operators* for mode $j$. They are their own adjoints ($c_j^\dagger = c_j$, $d_j^\dagger = d_j$) and each squares to the identity ($c_j^2 = d_j^2 = I$). Their anticommutation relations are the Majorana form of the CAR:

$$\{c_j,\, c_k\} = 2\delta_{jk}, \qquad \{d_j,\, d_k\} = 2\delta_{jk}, \qquad \{c_j,\, d_k\} = 0.$$

In words: $2N$ Hermitian operators that pairwise anticommute (except with themselves, where they give $2I$). Any encoding is fully specified by its Majorana operators.

### What JW gives us

Under Jordan-Wigner, the Majorana operators are:

$$c_j = X_j \otimes Z_{j-1} \otimes \cdots \otimes Z_0,$$
$$d_j = Y_j \otimes Z_{j-1} \otimes \cdots \otimes Z_0.$$

Both are single Pauli strings with weight $j + 1$. The encoding problem, restated: *find $2N$ Pauli strings satisfying the Majorana anticommutation relations, with the lowest possible weight.* JW achieves weight $O(N)$. Can we do $O(\log N)$?

---

## The logarithmic promise

### An information-theoretic hint

The parity $\bigoplus_{k<j} n_k$ is a single bit. It depends on the joint state of $j$ qubits, but it is still just one bit of information. Must we really read all $j$ qubits to extract it?

Consider a *binary tree* on $N$ nodes. Any leaf-to-root path has length $O(\log N)$. If intermediate nodes store *partial parities* — say, node $k$ stores the parity of its subtree — then the parity of any prefix can be assembled by reading $O(\log N)$ nodes along one root-to-leaf path. The same bit of information, recovered from fewer lookups.

This is the intuition behind the *Fenwick tree* (Fenwick, 1994) — a data structure from competitive programming that computes prefix sums in $O(\log N)$ operations. And it is the structure that Seeley, Richard, and Love (2012) connected to quantum chemistry, giving us the Bravyi-Kitaev encoding.

### What Bravyi and Kitaev proved

In 2002, Bravyi and Kitaev showed that a fermion-to-qubit encoding with $O(\log N)$ Pauli weight *exists*. The proof was abstract and hard to implement directly. It took a decade for Seeley, Richard, and Love (SRL, 2012) to turn the existence proof into an explicit, algorithmic construction based on the Fenwick tree.

That construction — how a data structure from 1994 solves a physics problem from 1928 — is the subject of the next post.

---

## Where we stand

We have established five things:

1. **The physics.** Electrons are antisymmetric under exchange; the minus sign is non-negotiable.
2. **The algebra.** The canonical anticommutation relations (the CAR) encode the full sign structure. Any encoding must satisfy them exactly.
3. **The naive attempt.** Mapping occupation numbers directly to qubit states works for the *basis* but fails for the *operators* — you lose the parity phase.
4. **The JW solution.** A Z-chain computes parity by reading every lower qubit. Correct, simple, but $O(N)$ weight per operator.
5. **The gap.** Parity is one bit distributed across many qubits. Tree structures can recover it in $O(\log N)$ lookups. The Bravyi-Kitaev encoding exploits this.

The molecule on the bench is the same — H₂, four spin-orbitals, two electrons. But next time, we will organise those four qubits into a tree, and watch the operator weights shrink.

*Keep encoding!*
