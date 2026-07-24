---
date: 2026-10-20
categories:
  - Mapping Fermions to Qubits
tags:
  - fermionic encodings
  - Bravyi-Kitaev
  - SRL framework
  - Fenwick tree
  - quantum chemistry
authors:
  - John Azariah
social:
  linkedin: 'The Seeley-Richard-Love paper (2012) presents a unified framework where Jordan-Wigner, Bravyi-Kitaev, and Parity encodings are all derived from trees using the same recipe. This post shows that the unification is illusory. The framework contains two different operator formulas wearing the same notation, and the formula that works for stars (JW, Parity) fails for the Fenwick tree by exactly one qubit at exactly the wrong place. Verified computationally against all 120 anticommutation relations for 8 modes.


    #QuantumComputing #QuantumChemistry'
  bluesky: 'Post 3 in the encodings series. The SRL framework looks like one construction but is actually two formulas in a trenchcoat. The wrong one fails by a single qubit, verified against all 120 anticommutators.'
---

# Three Constructions in a Trenchcoat

*For Jacob Seeley, Martin Richard, and Peter Love — whose 2012 paper gave the field a vocabulary so clean that it took a decade to notice the seam.*

<!-- more -->

## The unified theory that wasn't

In the [previous post](2026-10-13-fenwick-trees-and-bravyi-kitaev.md), we built the Bravyi-Kitaev (BK) encoding from scratch. We derived the three index sets — update $U(j)$, parity $P(j)$, and remainder $R(j) = P(j) \setminus \text{Occ}(j)$ — from the Fenwick tree (a binary indexed tree, originally from competitive programming, whose structure is governed entirely by the least-significant-bit operation $\text{lsb}(k) = k \;\&\; (-k)$). The resulting Majorana operators $c_j$ and $d_j$ — Hermitian operators satisfying the canonical anticommutation relations (CAR) $\{c_j, c_k\} = \{d_j, d_k\} = 2\delta_{jk}I$ and $\{c_j, d_k\} = 0$ — were verified against all 120 relations for 8 modes.

We also noted that the *same* index-set vocabulary — update, parity, occupation — describes Jordan-Wigner (JW) just as naturally: $U(j) = \emptyset$, $P(j) = \{0, \ldots, j-1\}$, $\text{Occ}(j) = \{j\}$. (Here each mode $j$ represents an abstract fermionic site — a spin-orbital in quantum chemistry — and each qubit in the target register stores some combination of occupation information.) This is no accident. In 2012, Seeley, Richard, and Love (SRL) published a paper that presented JW, BK, and the parity encoding as three instances of a single framework. You pick a tree, you read off the sets, you apply the formula, and out come your Majorana operators.

The paper has over 500 citations. It is *the* reference that OpenFermion, Qiskit, and PennyLane cite when implementing BK. And the framework it presents is — genuinely — a beautiful piece of conceptual unification. The vocabulary is right; the descriptions are correct; the three examples all work.

But the framework is hiding something. There are not one but *three* different constructions dressed in the same notation, and only two of them actually produce valid encodings. This post is about catching them in the act.

---

## The promise: one recipe, any tree

### The SRL algorithm

The SRL framework says: given $N$ fermionic modes, choose a labelled rooted tree $T$ on $N$ nodes. Then for each mode $j$, define

$$
\begin{aligned}
U(j) &= \text{ancestors of } j \text{ in } T, \\
P(j) &= \text{remainder}(j) \cup \text{children}(j), \\
\text{Occ}(j) &= \text{descendants of } j \text{ (including } j\text{)},
\end{aligned}
$$

where $\text{remainder}(j)$ collects certain cousins: children of ancestors of $j$ that have index less than $j$ and are not themselves ancestors of $j$.

Then build Majorana operators from these sets. The resulting encoding should satisfy the canonical anticommutation relations (CAR) — the algebraic constraints that make fermions behave like fermions.

The appeal is obvious. Change the tree, change the encoding. A star tree (one root, everything else a leaf) gives JW. A different star gives the parity encoding. The Fenwick tree gives BK. The vocabulary is uniform. The recipe looks universal.

*But what, exactly, is "the formula" that turns sets into operators?*

---

## Where the paths diverge

### The formula for $c_j$

For the $c_j$ Majorana (the "real part" of the ladder operator), there is no ambiguity. Everyone agrees:

$$c_j = \bigotimes_{k \in U(j) \cup \{j\}} X_k \;\cdot\; \bigotimes_{k \in P(j)} Z_k.$$

This is the operator that flips qubit $j$ and propagates the update while reading the parity. It works the same way in JW, in BK, and in the parity encoding. No controversy here.

### The formula for $d_j$ — and here's the fork

For the $d_j$ Majorana (the "imaginary part"), there are *two different recipes* that the SRL paper uses without ever quite distinguishing them.

**Recipe A (the generic formula):**

$$d_j^{(A)} = Y_j \;\cdot\; \bigotimes_{k \in U(j)} X_k \;\cdot\; \bigotimes_{k \in (P(j)\; \triangle\; \text{Occ}(j)) \setminus \{j\}} Z_k,$$

where $\triangle$ denotes the *symmetric difference* — elements in one set or the other, but not both.

**Recipe F (the BK formula):**

$$d_j^{(F)} = Y_j \;\cdot\; \bigotimes_{k \in U(j)} X_k \;\cdot\; \bigotimes_{k \in P(j) \setminus \text{Occ}(j)} Z_k.$$

The only difference: Recipe A uses the symmetric difference $P(j) \triangle \text{Occ}(j)$. Recipe F uses the set difference $P(j) \setminus \text{Occ}(j)$.

These are different operations! The symmetric difference $A \triangle B = (A \setminus B) \cup (B \setminus A)$ includes elements from *both* directions — things in $P$ but not $\text{Occ}$, *and* things in $\text{Occ}$ but not $P$. The set difference $P \setminus \text{Occ}$ includes only the first direction.

*When do these two recipes give the same answer?* Precisely when $P(j) \cap \text{Occ}(j) = \emptyset$ — i.e., when the parity set and the occupation set have no elements in common. In that case, $P \triangle \text{Occ} = P \cup \text{Occ}$, and after removing $j$ (which lives in $\text{Occ}$), both recipes reduce to the same set of $Z$ positions.

### The star-tree guarantee

For a star tree — the kind that gives JW or the parity encoding — every non-root node is a leaf. Leaves have no descendants besides themselves, so $\text{Occ}(j) = \{j\}$. And since $j \notin P(j)$ by construction (a node is never its own cousin), we get $P(j) \cap \text{Occ}(j) = \emptyset$ for every $j$.

Both recipes agree. Both work. The framework looks unified.

### The Fenwick tree breaks the symmetry

The Fenwick tree has depth $\lfloor \log_2 N \rfloor$. Internal nodes have subtrees — their $\text{Occ}(j)$ set extends well below them, potentially reaching into their own parity set. For $N = 8$:

| Mode $j$ | $P(j)$ | $\text{Occ}(j)$ | $P \cap \text{Occ}$ |
|:---------:|:-------:|:----------------:|:--------------------:|
| 0 | $\emptyset$ | $\{0\}$ | $\emptyset$ |
| 1 | $\{0\}$ | $\{0, 1\}$ | $\{0\}$ |
| 2 | $\{1\}$ | $\{2\}$ | $\emptyset$ |
| 3 | $\{1, 2\}$ | $\{0, 1, 2, 3\}$ | $\{1, 2\}$ |
| 4 | $\{3\}$ | $\{4\}$ | $\emptyset$ |
| 5 | $\{3, 4\}$ | $\{4, 5\}$ | $\{4\}$ |
| 6 | $\{5\}$ | $\{6\}$ | $\emptyset$ |
| 7 | $\{3, 5, 6\}$ | $\{0, 1, 2, 3, 4, 5, 6, 7\}$ | $\{3, 5, 6\}$ |

Four modes (1, 3, 5, 7) have non-empty overlap. These are the non-leaf nodes in the Fenwick tree — exactly the modes with subtrees larger than themselves. At these modes, Recipe A and Recipe F produce *different operators*.

---

## The tell: mode 3

Let me show you exactly where this breaks. Mode $j = 3$ in the 8-mode Fenwick tree has:

- $U(3) = \{7\}$ (one ancestor: the root)
- $P(3) = \{1, 2\}$ (the prefix-query path)
- $\text{Occ}(3) = \{0, 1, 2, 3\}$ (the subtree of node 3)
- $P(3) \cap \text{Occ}(3) = \{1, 2\}$ — both parity elements are *also* descendants!

**Recipe A** computes $Z$ positions as $(P \triangle \text{Occ}) \setminus \{j\}$:

$$P(3) \triangle \text{Occ}(3) = \{1, 2\} \triangle \{0, 1, 2, 3\} = \{0, 3\}.$$

Removing $j = 3$: the $Z$ set is $\{0\}$.

So $d_3^{(A)} = Z_0 \cdot I_1 \cdot I_2 \cdot Y_3 \cdot I_4 \cdot I_5 \cdot I_6 \cdot X_7$ — written as a Pauli string: `ZIIYIIIX`.

**Recipe F** computes $Z$ positions as $P \setminus \text{Occ}$:

$$P(3) \setminus \text{Occ}(3) = \{1, 2\} \setminus \{0, 1, 2, 3\} = \emptyset.$$

So $d_3^{(F)} = I_0 \cdot I_1 \cdot I_2 \cdot Y_3 \cdot I_4 \cdot I_5 \cdot I_6 \cdot X_7$ — Pauli string: `IIIYIIIX`.

One operator has a $Z$ at qubit 0. The other does not. That single qubit is the difference between a valid encoding and a broken one.

### The broken anticommutator

Consider the pair $\{d_0, d_3\}$. The CAR demands these anticommute (equal zero, since $0 \neq 3$). With the operators:

- $d_0 = $ `YXIXIIIX` (same in both recipes, since $P(0) = \emptyset$)
- $d_3^{(A)} = $ `ZIIYIIIX` (Recipe A)

Position by position:

| Qubit | $d_0$ | $d_3^{(A)}$ | Commutes? |
|:-----:|:-----:|:------:|:---------:|
| 0 | $Y$ | $Z$ | **Anticommutes** |
| 1 | $X$ | $I$ | Commutes (identity) |
| 3 | $X$ | $Y$ | **Anticommutes** |
| 7 | $X$ | $X$ | Commutes (same) |

Two anticommuting positions. An even number means the operators *commute* — they produce $+1$ instead of $-1$ when multiplied in opposite order. The CAR requires an odd number for anticommutation. **Recipe A fails.**

Now with Recipe F:

| Qubit | $d_0$ | $d_3^{(F)}$ | Commutes? |
|:-----:|:-----:|:------:|:---------:|
| 0 | $Y$ | $I$ | Commutes (identity) |
| 3 | $X$ | $Y$ | **Anticommutes** |
| 7 | $X$ | $X$ | Commutes (same) |

One anticommuting position — odd. **Recipe F satisfies the CAR.**

The mechanism is almost embarrassingly simple. The symmetric difference "leaks" qubit 0 into $d_3$ because $0 \in \text{Occ}(3) \setminus P(3)$ — it is a descendant of mode 3 but not in mode 3's parity path. This leaked qubit creates an extra anticommuting position with $d_0$, flipping the parity from odd (correct) to even (broken).

---

## The full damage

This is not a one-off. For the 8-mode Fenwick tree, Recipe A fails at exactly 8 anticommutator pairs:

| Failing pair | Cause |
|:------------:|:-----:|
| $\{d_0, d_3\}$ | Mode 3 has $P \cap \text{Occ} \neq \emptyset$ |
| $\{d_1, d_7\}$ | Mode 7 has $P \cap \text{Occ} \neq \emptyset$ |
| $\{d_2, d_7\}$ | Same root cause |
| $\{d_4, d_7\}$ | Same root cause |
| $\{c_0, d_3\}$ | Cross-type, same mechanism |
| $\{c_1, d_7\}$ | Cross-type |
| $\{c_2, d_7\}$ | Cross-type |
| $\{c_4, d_7\}$ | Cross-type |

All 8 failures involve modes 3 or 7 — the two modes whose $P \cap \text{Occ}$ overlaps are largest ($\{1, 2\}$ and $\{3, 5, 6\}$ respectively). Recipe F — the set-difference formula that defines the remainder as $R(j) = P(j) \setminus \text{Occ}(j)$ — passes all 120 checks without incident.

---

## Same sets, different formula

I want to be very precise about what is happening here, because it is easy to mischaracterise.

The *index sets* $U(j)$, $P(j)$, and $\text{Occ}(j)$ are the *same* whether you compute them from the tree structure (ancestors, prefix-query path, subtree) or from bit arithmetic (the Fenwick formulas). The tree topology and the bit tricks agree perfectly. There is no discrepancy in the sets.

The discrepancy is in the *operator construction rule* — the formula that turns those sets into Pauli strings. Recipe A uses symmetric difference. Recipe F uses set difference. For star trees they coincide. For the Fenwick tree they diverge, and Recipe A breaks.

This means the SRL "framework" is actually two things:

1. **A descriptive vocabulary** for encoding schemes — you can always *describe* any valid encoding by specifying its $(U, P, \text{Occ})$ triples. This is correct and useful.

2. **A constructive recipe** that supposedly generates valid encodings from trees — apply the generic formula, get working operators. This only works for stars.

The descriptive vocabulary is fine. BK can be *described* in terms of update, parity, and occupation sets. But BK was not *generated* by the generic recipe. Its operators were derived separately, using a different formula (set difference instead of symmetric difference), specifically tuned to the Fenwick tree's algebraic structure.

---

## Three constructions, unmasked

So what are the "three constructions in a trenchcoat"? Here they are, stated plainly:

### Construction A — the generic index-set recipe

- **Input:** Any labelled rooted tree $T$
- **Method:** Derive $(U, P, \text{Occ})$ from tree structure; build operators using symmetric difference
- **Domain of validity:** Star trees only (depth $\leq 1$)
- **Produces:** JW, parity encoding, and trivial relabellings thereof

### Construction F — the Fenwick-specific formula

- **Input:** The Fenwick tree (specifically)
- **Method:** Derive $(U, P, \text{Occ})$ from bit arithmetic; build operators using set difference ($R = P \setminus \text{Occ}$)
- **Domain of validity:** The Fenwick tree
- **Produces:** The Bravyi-Kitaev encoding

### Construction B — the path-based method

- **Input:** Any rooted tree (including ternary trees)
- **Method:** Assign Paulis along root-to-leaf *paths*, not at individual *positions*
- **Domain of validity:** Universal — works for all trees
- **Produces:** All known encodings, including JW, BK, and ternary-tree variants
- **References:** Steudtner & Wehner (2018), Jiang et al. (2020), Miller et al. "Bonsai" (2023)

The SRL paper presents A and F as a single method — same vocabulary, same code structure, different tree input. But they are fundamentally different: A uses a generic formula that breaks for deep trees, while F uses a Fenwick-specific formula that happens to share the same vocabulary.

Construction B, developed later by other groups, is the one that actually delivers on the original promise of "any tree gives an encoding." It works by assigning Paulis along entire root-to-leaf paths rather than position by position, which avoids the symmetric-difference cancellation entirely.

---

## The quiet migration

There is a telling pattern in the literature. Here is a partial timeline:

| Year | Paper | Construction used |
|------|-------|:-----------------:|
| 2012 | Seeley, Richard, Love | A + F (conflated) |
| 2015 | Tranter et al. | A/F (follows SRL) |
| 2018 | Steudtner & Wehner | **B** |
| 2020 | Jiang et al. | **B** |
| 2023 | Miller et al. (Bonsai) | **B** |

Every major encoding paper since 2018 uses Construction B — the path-based method. None of them uses Construction A (the generic index-set recipe). And none of them explains *why* they switched. They just... use a different method. The field migrated from A to B without anyone formally documenting that A doesn't work for deep trees.

The star-tree theorem — which the next post proves — provides the formal explanation for this migration.

---

## What we found

Starting from the SRL framework's elegant promise, we have:

1. **Identified** two distinct operator formulas (symmetric difference vs. set difference) hiding behind one vocabulary.
2. **Shown** that the formulas agree for star trees (where $P \cap \text{Occ} = \emptyset$) but diverge for the Fenwick tree (where they overlap at internal nodes).
3. **Verified** computationally that the symmetric-difference formula (Recipe A) fails 8 of 120 anticommutator pairs for 8 modes, while the set-difference formula (Recipe F) passes all 120.
4. **Traced** the failure to a single mechanism: the symmetric difference "leaks" descendants into the $d_j$ operator, creating an extra anticommuting position that flips the parity from odd (correct) to even (broken).
5. **Named** the three constructions that the SRL paper conflates, and noted the field's quiet migration to the one (Construction B) that actually works universally.

The BK encoding is correct — we verified that in Post 2. The SRL description of BK is correct — the index-set vocabulary accurately describes what BK does. What is *not* correct is the implication that BK is an instance of a general "tree-to-encoding" recipe. BK has its own formula, derived specifically for the Fenwick tree, and that formula differs from the generic recipe at precisely the modes where the tree has depth.

This raises a natural question: is there something *provably* special about stars? Is it coincidence that the generic recipe works for depth-1 trees and fails for everything deeper, or is there a theorem?

There is. And it is cleaner than you might expect.

*Next time: The Star-Tree Theorem — why depth one is the hard boundary, and how a single grandchild breaks everything.*
