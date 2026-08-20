---
date: 2026-10-06
slug: the-antisymmetry-problem
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
  linkedin: 'Electrons carry a rule that qubits do not: exchange two fermions and the wavefunction changes sign. A qubit register has to be taught that minus sign before it can represent chemistry correctly.


    I wanted to begin this series with H₂ because four spin-orbitals and two electrons are enough to see the whole problem. Jordan-Wigner stores occupation directly and uses a string of Z operators to keep track of fermionic parity. It is beautifully literal, and the bill arrives in the same place: for N modes, the worst-case operator has weight N and the average has weight (N + 1)/2.


    That gives us a correct encoding and the question for the next post: can a prefix-sum data structure from 1994 make the parity bookkeeping logarithmic?


    #QuantumComputing #QuantumChemistry'
  bluesky: 'Electrons carry a rule qubits do not: exchange two fermions and the wavefunction changes sign. Jordan-Wigner teaches that rule with a Z-chain of worst-case weight O(n). I start with H₂ so we can see the cost.'
---

# The Antisymmetry Problem: Why Fermions Need Encoding

*For [Alan Geller](https://www.linkedin.com/in/alan-geller-46934b/), who introduced me to quantum computing, gave me free rein to talk about type theory and DSL design, and first walked me through Jordan-Wigner. This series exists because of that introduction.*

<!-- more -->

## The molecule on the bench

Here is the smallest interesting molecule in quantum chemistry: H₂. Two hydrogen atoms, bonded. Two electrons sharing four spin-orbitals — two spatial orbitals (call them $\sigma$ and $\sigma^*$, the bonding and antibonding orbitals), each available in spin-up and spin-down flavours.

The question a quantum chemist asks is: *what is the ground-state energy of this system?* Electronic energies underpin bond lengths, reaction pathways, and material properties; much of computational chemistry begins here. The full Fock space on four modes has dimension $2^4 = 16$, though number conservation restricts the physical two-electron sector to $\binom{4}{2} = 6$ states. For H₂ we can diagonalise this classically, but H₂ lets us build and check the encoding machinery before scale defeats exact classical methods.

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

A qubit register has distinguishable tensor factors, and local operators on different qubits *commute*: flipping qubit 3 from $\lvert 0\rangle$ to $\lvert 1\rangle$ is a local operation that does not know or care what qubits 0, 1, and 2 are doing. Fermionic creation operators, by contrast, *anticommute*. Creating an electron in mode 3 — where each spin-orbital is one *mode* of the fermionic system — must apply a phase that depends on *how many of the lower modes are already occupied*. The encoding's job is to build that non-local sign structure into the qubit operators.

---

## Counting who's home

### Fock space: the occupation-number picture

Rather than tracking *which* electron is *where* (a bookkeeping nightmare that leads to Slater determinants and antisymmetrisation headaches), we work in *Fock space*. Each mode $j$ is either occupied ($n_j = 1$) or empty ($n_j = 0$). A basis state — an *occupation-number state* — is a binary string:

$$\lvert n_0,\, n_1,\, n_2,\, n_3\rangle, \qquad n_j \in \{0, 1\}.$$

For our H₂ example with $N = 4$ modes, the state $\lvert 1, 1, 0, 0\rangle$ means "modes 0 and 1 are occupied; modes 2 and 3 are empty." The full Fock space has $2^N = 16$ basis states — exactly the dimension of a 4-qubit Hilbert space. The dimensions match because each mode is binary (occupied or empty), so $N$ modes map naturally onto $N$ qubits. The encoding problem is how to make the *operators* respect the same fermionic sign structure.

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

The CAR is the contract. An encoding that satisfies it is a faithful representation of the fermionic operator algebra. An encoding that violates it — even at a single pair $(i, j)$ — is not: spectra computed from Hamiltonians built with the defective operators are no longer guaranteed to match the fermionic problem, even if some eigenvalues may coincidentally agree.

---

## One qubit per mode — what could go wrong?

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

The *Pauli weight* of an operator is the number of qubits it acts on non-trivially (anything other than identity). Weight is a proxy for circuit cost: exponentiating a weight-$w$ Pauli string in a typical parity-ladder implementation requires $O(w)$ entangling gates (roughly $2(w-1)$ CNOTs plus single-qubit basis changes and the rotation). Mode 3 already touches all 4 qubits.

### The cost, honestly

For $N$ modes, the creation operator for mode $j$ has Pauli weight $j + 1$. The worst case is mode $N - 1$, with weight $N$. The average across all modes is $(N + 1) / 2$.

| System | Modes $N$ | Max JW weight | Worst-case JW string |
|--------|:---------:|:-------------:|----------------------|
| H₂ (minimal basis) | 4 | 4 | Weight-4 Pauli string |
| H₂O (STO-3G basis) | 14 | 14 | Weight-14 Pauli string |
| FeMoCo (Reiher et al. active space) | 108 | 108 | Weight-108 Pauli string |
| Large active space | 200 | 200 | Weight-200 Pauli string |

The worst-case weight grows linearly with $N$: mode $N-1$ touches all $N$ qubits, while low-index modes remain lighter. In a straightforward parity-ladder compilation, exponentiating such a string uses $O(N)$ entangling gates. Actual Hamiltonian terms can simplify when Jordan-Wigner strings multiply, and realised depth also depends on compilation, connectivity, scheduling, and ancillas.

---

## Two halves of a whole

There is a cleaner way to state the encoding problem that will serve us well in the posts to come.

### The Majorana decomposition

Every creation operator splits into two Hermitian pieces:

$$a^\dagger_j = \frac{1}{2}(c_j - i\,d_j),$$

where $c_j$ and $d_j$ are the *Majorana operators* for mode $j$. They are their own adjoints ($c_j^\dagger = c_j$, $d_j^\dagger = d_j$) and each squares to the identity ($c_j^2 = d_j^2 = I$). Their anticommutation relations are the Majorana form of the CAR:

$$\{c_j,\, c_k\} = 2\delta_{jk}, \qquad \{d_j,\, d_k\} = 2\delta_{jk}, \qquad \{c_j,\, d_k\} = 0.$$

In words: $2N$ Hermitian operators that pairwise anticommute (except with themselves, where they give $2I$). In the one-qubit-per-mode linear encoding family used in this series, an encoding is fully specified by the images of these $2N$ Majorana generators.

### What JW gives us

Under Jordan-Wigner, the Majorana operators are:

$$c_j = X_j \otimes Z_{j-1} \otimes \cdots \otimes Z_0,$$
$$d_j = Y_j \otimes Z_{j-1} \otimes \cdots \otimes Z_0.$$

Both are single Pauli strings with weight $j + 1$. Within this Pauli-string family, the encoding problem becomes: *find $2N$ Pauli strings satisfying the Majorana anticommutation relations, with the lowest possible weight.* JW achieves weight $O(N)$. Can we do $O(\log N)$?

---

## The logarithmic promise

### A storage-query trade-off

The parity $\bigoplus_{k<j} n_k$ is a single bit. It depends on the joint state of $j$ qubits, but it is still just one bit of information. Must we really read all $j$ qubits to extract it?

Not if we change what the qubits *store*. Instead of raw occupations, suppose each qubit stores a selected partial parity — the XOR of a specific subset of mode occupations. If those subsets are chosen so that any prefix parity can be reconstructed by combining $O(\log N)$ disjoint stored blocks, we can read the parity without touching every lower qubit.

This is the idea behind the *Fenwick tree*, introduced by Peter Fenwick in 1994 for cumulative-frequency tables and now familiar from competitive programming. Each node stores the partial sum of a block whose size is determined by its least-significant set bit. Prefix queries repeatedly clear that bit; point updates repeatedly add it. Bravyi and Kitaev's encoding applies the same storage-query trade-off to fermionic parity.

### What Bravyi and Kitaev proved

In 2002, Bravyi and Kitaev introduced an explicit encoding using a binary partial-sum structure that achieves $O(\log N)$ Pauli weight. Their construction was later recast for electronic-structure work by Seeley, Richard, and Love (SRL, 2012), who expressed it via recursive $\beta$-matrices and the update/parity/flip/remainder index sets ($U$, $P$, $F$, $R$). Havlíček, Troyer, and Whitfield (2017) then made the Fenwick-tree formulation explicit, connecting the lsb-based tree arithmetic directly to the index sets.

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

---

## References

- P. Jordan and E. Wigner, "Über das Paulische Äquivalenzverbot," *Zeitschrift für Physik* **47**, 631–651 (1928). [doi:10.1007/BF01331938](https://doi.org/10.1007/BF01331938)
- S. B. Bravyi and A. Yu. Kitaev, "Fermionic quantum computation," *Annals of Physics* **298**, 210–226 (2002). [doi:10.1006/aphy.2002.6254](https://doi.org/10.1006/aphy.2002.6254), [arXiv:quant-ph/0003137](https://arxiv.org/abs/quant-ph/0003137)
- P. M. Fenwick, "A new data structure for cumulative frequency tables," *Software: Practice and Experience* **24**, 327–336 (1994). [doi:10.1002/spe.4380240306](https://doi.org/10.1002/spe.4380240306)
- J. T. Seeley, M. J. Richard, and P. J. Love, "The Bravyi-Kitaev transformation for quantum computation of electronic structure," *Journal of Chemical Physics* **137**, 224109 (2012). [doi:10.1063/1.4768229](https://doi.org/10.1063/1.4768229), [arXiv:1208.5986](https://arxiv.org/abs/1208.5986)
- V. Havlíček, M. Troyer, and J. D. Whitfield, "Operator locality in the quantum simulation of fermionic models," *Physical Review A* **95**, 032332 (2017). [doi:10.1103/PhysRevA.95.032332](https://doi.org/10.1103/PhysRevA.95.032332), [arXiv:1701.07072](https://arxiv.org/abs/1701.07072)
- M. Reiher, N. Wiebe, K. M. Svore, D. Wecker, and M. Troyer, "Elucidating reaction mechanisms on quantum computers," *Proceedings of the National Academy of Sciences* **114**, 7555–7560 (2017). [doi:10.1073/pnas.1619152114](https://doi.org/10.1073/pnas.1619152114)
