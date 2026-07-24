---
date: 2026-10-13
categories:
  - Mapping Fermions to Qubits
tags:
  - fermionic encodings
  - Bravyi-Kitaev
  - Fenwick tree
  - quantum chemistry
authors:
  - John Azariah
social:
  linkedin: 'The Jordan-Wigner transform encodes fermions on qubits with a parity chain that touches every lower qubit, giving O(n) operator weight. The Bravyi-Kitaev encoding brings this down to O(log n) by storing partial parities in a binary tree structure borrowed from competitive programming: the Fenwick tree, invented in 1994 for cumulative frequency tables. This post builds the tree from scratch using bit arithmetic, shows what each qubit stores, derives the update and parity sets, and demonstrates verified Majorana operators for 8 modes where the maximum weight is 4 instead of 8.


    #QuantumComputing #QuantumChemistry'
  bluesky: 'Post 2 in the encodings series builds the Bravyi-Kitaev encoding from the Fenwick tree. A data structure from competitive programming gives O(log n) operator weight where Jordan-Wigner needs O(n). All operators verified against the full anticommutation algebra.'
---

# Fenwick Trees and the Bravyi-Kitaev Encoding

*For Peter Fenwick (1943–2022), whose 1994 paper on "A New Data Structure for Cumulative Frequency Tables" found an afterlife in quantum chemistry that he probably never anticipated.*

<!-- more -->

## Where we left off

In the [previous post](2026-10-06-the-antisymmetry-problem.md), we established that simulating fermions on qubits requires encoding the parity phase $(-1)^{\sum_{k<j} n_k}$ into our qubit operators. The Jordan-Wigner (JW) transform does this with a chain of $Z$ operators on every qubit below $j$, giving Pauli weight $j + 1$ — which means $O(N)$ weight for $N$ modes.

We ended with a question: the parity of modes $0$ through $j-1$ is a single bit of information. Can we recover it by reading fewer than $j$ qubits? The answer involves a data structure that has nothing to do with physics.

---

## A prefix-sum problem in disguise

### What parity actually asks for

The parity $\bigoplus_{k=0}^{j-1} n_k$ is a *prefix XOR*: the exclusive-or of all occupation numbers below mode $j$. In Jordan-Wigner, each qubit stores one occupation number directly ($q_k = n_k$), so computing the prefix XOR requires reading all $j$ qubits — one by one, XOR them up. That is the $O(N)$ cost.

But prefix sums are a solved problem in computer science! The insight behind the Bravyi-Kitaev (BK) encoding is this: if we store *partial parities* in the qubits instead of raw occupation numbers, we can recover any prefix XOR by reading only $O(\log N)$ qubits. The data structure that makes this work is the Fenwick tree.

### The idea: store smarter, query faster

Instead of qubit $j$ storing just $n_j$, let each qubit store the XOR of a *range* of occupation numbers. Organise the ranges so that any prefix can be assembled from at most $\lceil\log_2 N\rceil$ of them. Then the parity query touches only $O(\log N)$ qubits, and the operator weight drops accordingly.

---

## The Fenwick tree from scratch

### Origin story

In 1994, Peter Fenwick published "A New Data Structure for Cumulative Frequency Tables" in *Software: Practice and Experience*. His problem was humble: maintain an array of counters that supports both *point updates* (increment counter $j$) and *prefix queries* (sum of counters $0$ through $j$), each in $O(\log N)$ time. The solution — now called a Fenwick tree or binary indexed tree (BIT) — became a staple of competitive programming.

The connection to quantum chemistry is that our problem has exactly the same shape. "Point update" = changing the occupation of mode $j$ (which updates certain qubits). "Prefix query" = computing the parity $\bigoplus_{k<j} n_k$ (which reads certain qubits). If both operations touch $O(\log N)$ positions, the resulting encoding has $O(\log N)$ weight.

### The one bit trick that runs the show

The entire Fenwick tree is governed by a single operation: extracting the *least significant bit* of an integer.

$$\text{lsb}(k) = k \;\&\; (-k)$$

In binary, this isolates the lowest set bit. The result determines the "responsibility range" of node $k$ — how many elements it covers:

| $k$ | Binary | $\text{lsb}(k)$ | Range width |
|-----|--------|:--------:|:-----------:|
| 1 | 0001 | 1 | 1 |
| 2 | 0010 | 2 | 2 |
| 3 | 0011 | 1 | 1 |
| 4 | 0100 | 4 | 4 |
| 5 | 0101 | 1 | 1 |
| 6 | 0110 | 2 | 2 |
| 7 | 0111 | 1 | 1 |
| 8 | 1000 | 8 | 8 |

Node $k$ (1-indexed) is responsible for elements in the range $[k - \text{lsb}(k) + 1,\; k]$. Node 4 covers elements 1–4; node 6 covers elements 5–6; node 7 covers only element 7.

### The tree structure

The *parent* of node $k$ is $k + \text{lsb}(k)$:

```
parent(1) = 1 + 1 = 2
parent(2) = 2 + 2 = 4
parent(3) = 3 + 1 = 4
parent(4) = 4 + 4 = 8 (root)
parent(5) = 5 + 1 = 6
parent(6) = 6 + 2 = 8 (root)
parent(7) = 7 + 1 = 8 (root)
```

This gives the tree (drawn with 1-indexed nodes):

```
            8
          / | \
         4  6  7
        / \ |
       2  3 5
       |
       1
```

Or re-drawn to show the depth structure clearly (0-indexed for modes):

```
Level 0 (root):          7
                       / | \
Level 1:             3   5   6
                   / |   |
Level 2:         1   2   4
                 |
Level 3:         0
```

The depth is $\lfloor\log_2 N\rfloor$ — at most 3 levels for 8 nodes.

---

## What each qubit stores

Here is the critical departure from Jordan-Wigner. In JW, qubit $j$ stores $n_j$ directly. In BK, qubit $j$ stores the XOR of all occupation numbers in its responsibility range:

| Qubit (0-indexed) | Stores | Interpretation |
|:-:|--------|------|
| 0 | $n_0$ | Just mode 0 |
| 1 | $n_0 \oplus n_1$ | Parity of modes 0–1 |
| 2 | $n_2$ | Just mode 2 |
| 3 | $n_0 \oplus n_1 \oplus n_2 \oplus n_3$ | Parity of modes 0–3 |
| 4 | $n_4$ | Just mode 4 |
| 5 | $n_4 \oplus n_5$ | Parity of modes 4–5 |
| 6 | $n_6$ | Just mode 6 |
| 7 | $n_0 \oplus n_1 \oplus \cdots \oplus n_7$ | Parity of all 8 modes |

The pattern: nodes at odd positions store single occupations; nodes at powers of 2 store progressively wider parities; the root stores the total parity of the entire system.

---

## The three operations

### 1. Prefix query — the parity set P(j)

To compute $\bigoplus_{k<j} n_k$, walk *down* from position $j$, subtracting $\text{lsb}$ at each step:

$$j \;\to\; j - \text{lsb}(j) \;\to\; \cdots \;\to\; 0.$$

Each visited node contributes one term of the prefix XOR. The set of visited nodes (converted to 0-indexed) is the *parity set* $P(j)$.

For mode 6 (1-indexed position 6): $6 \to 4 \to 0$. So $P(6) = \{5, 3\}$ (0-indexed nodes 5 and 3). Reading qubits 5 and 3 gives $n_4 \oplus n_5$ and $n_0 \oplus \cdots \oplus n_3$, whose XOR is the parity of modes 0–5 — exactly what we need.

The path length is at most $\lfloor\log_2 N\rfloor$, so $|P(j)| \leq \lfloor\log_2 N\rfloor$.

### 2. Point update — the update set U(j)

When the occupation of mode $j$ changes, every qubit whose stored range includes mode $j$ must be updated. These are the *ancestors* of node $j+1$ in the Fenwick tree — reached by *adding* $\text{lsb}$ repeatedly:

$$(j+1) \;\to\; (j+1) + \text{lsb}(j+1) \;\to\; \cdots$$

until you exceed $N$. The 0-indexed result is the *update set* $U(j)$.

For mode 0 (1-indexed node 1): $1 \to 2 \to 4 \to 8$. So $U(0) = \{1, 3, 7\}$. When $n_0$ changes, qubits 1, 3, and 7 all need flipping (they all store parities that include $n_0$).

Again, path length $\leq \lfloor\log_2 N\rfloor$, so $|U(j)| \leq \lfloor\log_2 N\rfloor$.

### 3. Occupation query — the flip set Occ(j)

To determine whether mode $j$ is occupied, we need to isolate $n_j$ from the partial parities. Qubit $j$ stores $\bigoplus_{k \in [j+1-\text{lsb}(j+1),\; j]} n_k$ — a range that always includes $n_j$ but may include other modes too. The *occupation set* (or "flip set") $\text{Occ}(j)$ is the set of qubits whose stored values XOR together to give just $n_j$:

$$\text{Occ}(j) = \{j+1-\text{lsb}(j+1),\;\ldots,\;j\} \quad\text{(0-indexed)}.$$

For mode 3: $\text{Occ}(3) = \{0, 1, 2, 3\}$ (because qubit 3 stores the parity of modes 0–3, and to isolate $n_3$ you need to cancel the contribution of modes 0–2 using qubits 0–2).

For mode 0: $\text{Occ}(0) = \{0\}$ (qubit 0 stores $n_0$ directly — no cancellation needed).

---

## Building the Majorana operators

Now we assemble the encoding. A fermion-to-qubit encoding is specified by its *Majorana operators* $c_j$ and $d_j$ — two Hermitian Pauli strings per mode that combine to form the creation operator $a^\dagger_j = \frac{1}{2}(c_j - i\,d_j)$. They must satisfy the canonical anticommutation relations (the CAR):

$$\{c_j, c_k\} = 2\delta_{jk}, \quad \{d_j, d_k\} = 2\delta_{jk}, \quad \{c_j, d_k\} = 0.$$

The BK Majorana operators are built from two additional pieces:

- The *remainder set* $R(j) = P(j) \setminus \text{Occ}(j)$: elements in the parity set that are *not* in the occupation set.

The formulas:

$$c_j = X_j \;\cdot\; \bigotimes_{k \in U(j)} X_k \;\cdot\; \bigotimes_{k \in P(j)} Z_k,$$

$$d_j = Y_j \;\cdot\; \bigotimes_{k \in U(j)} X_k \;\cdot\; \bigotimes_{k \in R(j)} Z_k.$$

The $c_j$ operator flips qubit $j$ and all update qubits (propagating the occupation change), while applying $Z$ at the parity qubits (computing the sign). The $d_j$ operator does the same update propagation but uses the *remainder* for its phase — encoding the occupation information differently.

### The verified scoreboard (n = 8)

Here are the actual Majorana operators, computed and verified against all 120 anticommutation relations:

| Mode $j$ | $c_j$ | $d_j$ | Weight of $c_j$ | Weight of $d_j$ |
|:-:|:------:|:------:|:-------:|:-------:|
| 0 | `XXIXIIIX` | `YXIXIIIX` | 4 | 4 |
| 1 | `ZXIXIIIX` | `IYIXIIIX` | 4 | 3 |
| 2 | `IZXXIIIX` | `IZYXIIIX` | 4 | 4 |
| 3 | `IZZXIIIX` | `IIIYIIIX` | 4 | 2 |
| 4 | `IIIZXXIX` | `IIIZYXIX` | 4 | 4 |
| 5 | `IIIZZXIX` | `IIIZIYIX` | 4 | 3 |
| 6 | `IIIZIZXX` | `IIIZIZYX` | 4 | 4 |
| 7 | `IIIZIZZX` | `IIIIIIIY` | 4 | 1 |

Maximum weight: **4** (compared to JW's maximum of **8** for the same number of modes).

Every one of the 120 anticommutators $\{c_j, c_k\}$, $\{d_j, d_k\}$, and $\{c_j, d_k\}$ has been verified to equal zero for $j \neq k$ (or $2I$ for $j = k$). These are not approximations — the canonical anticommutation relations are satisfied exactly.

---

## The H₂ comparison

Continuing with our 4-mode hydrogen molecule from Post 1:

| Mode $j$ | $U(j)$ | $P(j)$ | $c_j$ (BK) | $d_j$ (BK) | Max weight (BK) | Max weight (JW) |
|:-:|:-:|:-:|:----:|:----:|:-:|:-:|
| 0 | $\{1, 3\}$ | $\{\}$ | `XXIX` | `YXIX` | 3 | 1 |
| 1 | $\{3\}$ | $\{0\}$ | `ZXIX` | `IYIX` | 3 | 2 |
| 2 | $\{3\}$ | $\{1\}$ | `IZXX` | `IZYX` | 3 | 3 |
| 3 | $\{\}$ | $\{1,2\}$ | `IZZX` | `IIIY` | 3 | 4 |

BK maximum weight for $N = 4$: **3**. JW maximum: **4**. 

For this toy problem, the savings are modest — one fewer qubit touched in the worst case. But the scaling tells the real story:

| $N$ modes | JW max weight | BK max weight | Ratio |
|:---------:|:---:|:---:|:---:|
| 4 | 4 | 3 | 75% |
| 8 | 8 | 4 | 50% |
| 16 | 16 | 5 | 31% |
| 64 | 64 | 7 | 11% |
| 256 | 256 | 9 | 3.5% |

The BK weight grows as $\lceil\log_2 N\rceil + 1$. For 256 modes, JW touches all 256 qubits in the worst case; BK touches at most 9. That is the difference between a feasible circuit and an impossible one.

---

## Why the tree shape matters

The logarithmic scaling is not magic — it is a direct consequence of the tree's depth. The Fenwick tree on $N$ nodes has depth $\lfloor\log_2 N\rfloor$. Both the update path (walking up to the root) and the prefix-query path (walking down to zero) traverse at most this many levels. Since the parity set and update set are these paths, their sizes are bounded by $\lfloor\log_2 N\rfloor$, and so is the operator weight.

A deeper tree would give larger sets; a shallower tree would give smaller ones but fewer modes. The Fenwick tree hits the sweet spot: it supports $N$ modes with depth $O(\log N)$, using only bit arithmetic to navigate.

This raises a natural question: could we use *other* tree structures — perhaps balanced binary trees, ternary trees, or something else — and get the same or better scaling? The Seeley-Richard-Love paper (2012) implied yes: they presented a framework where *any* tree gives an encoding. The next post examines that claim carefully, and finds that it is rather less general than it appears.

---

## What we built

Starting from the prefix-sum problem identified in Post 1, we have:

1. **Connected** the parity-encoding problem to the classical Fenwick tree data structure.
2. **Built** the tree from scratch using the $\text{lsb}(k) = k \;\&\; (-k)$ operation.
3. **Derived** three index sets — update $U(j)$, parity $P(j)$, and remainder $R(j)$ — from tree paths.
4. **Constructed** Majorana operators $c_j$ and $d_j$ from these sets.
5. **Verified** all 120 anticommutation relations for 8 modes (computationally, not by assertion).
6. **Demonstrated** the weight scaling: $O(\log N)$ versus JW's $O(N)$.

The Bravyi-Kitaev encoding works. The Fenwick tree delivers on the logarithmic promise. But the framework that presented it — the SRL index-set formalism — has a subtlety lurking beneath its apparent generality. Three encodings, three trees, one vocabulary... but are they really three instances of one construction?

*Next time: Three Constructions in a Trenchcoat.*
