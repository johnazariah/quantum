---
date: 2026-10-27
categories:
  - Mapping Fermions to Qubits
tags:
  - fermionic encodings
  - star-tree theorem
  - SRL framework
  - quantum chemistry
  - original research
authors:
  - John Azariah
social:
  linkedin: 'The SRL framework (2012) derives fermionic encodings by reading index sets off a tree. The star-tree theorem proves this recipe satisfies the canonical anticommutation relations if and only if the tree has depth at most 1 (a star). The proof identifies a single mechanism: on any depth-2 path, the intermediate node cancels in a symmetric difference, creating an identity gap that flips the anticommutation parity from odd to even. Verified exhaustively on all 701 labelled rooted trees for n=1 through 5: exactly n trees pass for each n, and they are exactly the n stars.


    #QuantumComputing #QuantumChemistry'
  bluesky: 'Post 4 completes the encodings series. The star-tree theorem proves the SRL index-set recipe works only for depth-1 trees. A single cancellation mechanism breaks everything deeper. Verified exhaustively on all 701 trees for n=1..5.'
---

# The Star-Tree Theorem: What Breaks and Why

*For the 701 trees that taught us the boundary.*

<!-- more -->

## The question we earned

The [previous post](2026-10-20-three-constructions-in-a-trenchcoat.md) ended with a demonstration: the generic index-set recipe (Construction A) fails for the Fenwick tree — a binary indexed tree from competitive programming that organises $N$ modes into a depth-$\lfloor \log_2 N \rfloor$ structure governed by bit arithmetic — at 8 of 120 anticommutator pairs, while the Bravyi-Kitaev (BK) formula (Construction F) passes all 120. The failure traces to a single mechanism — the symmetric difference $P(j) \triangle \text{Occ}(j)$ "leaks" descendants into the $d_j$ operator at modes where the parity set and occupation set overlap.

But is this failure specific to the Fenwick tree, or does it reveal a general boundary? Could there be some other non-star tree — perhaps a carefully chosen balanced binary tree, or a caterpillar graph — for which Construction A happens to work?

The answer is no. The boundary is sharp, and it is exactly where you would guess after Post 3: stars are the only trees for which the generic recipe produces valid Majorana operators. This is the star-tree theorem.

---

## The theorem

**Star-tree theorem.** Let $T$ be a labelled rooted tree on $N$ nodes, and let $(U, P, \text{Occ})$ be the index sets derived from $T$ by Construction A (the generic recipe: ancestors, remainder $\cup$ children, descendants $\cup$ self). Define the Majorana operators

$$c_j = \bigotimes_{k \in U(j) \cup \{j\}} X_k \;\cdot\; \bigotimes_{k \in P(j)} Z_k,$$

$$d_j = Y_j \;\cdot\; \bigotimes_{k \in U(j)} X_k \;\cdot\; \bigotimes_{k \in (P(j)\, \triangle\, \text{Occ}(j)) \setminus \{j\}} Z_k,$$

where $A \triangle B = (A \setminus B) \cup (B \setminus A)$ denotes the symmetric difference (elements in one set or the other, but not both).

Then these operators satisfy the canonical anticommutation relations (CAR) — that is, $\{c_j, c_k\} = \{d_j, d_k\} = 2\delta_{jk}I$ and $\{c_j, d_k\} = 0$ for all $j, k$ — **if and only if $T$ is a star** (a tree of depth at most 1: one root with all other nodes as direct children).

### What "star" means precisely

A **star tree** on $N$ nodes is a tree where one designated node (the root) has $N - 1$ children, and those children are all leaves. There are exactly $N$ such trees — one for each choice of root. They produce relabellings of the Jordan-Wigner encoding and its parity-encoding dual. No other tree shapes. No other encodings.

---

## The proof: necessity

The interesting direction is necessity: *if $T$ is not a star, the CAR fails*. Every non-star tree has depth at least 2, which means it contains a path of length 2:

$$w \longrightarrow u \longrightarrow v$$

where $w$ is a grandparent, $u$ is a parent, and $v$ is a grandchild. We will show that $\{d_w, c_v\} \neq 0$, violating the CAR (which requires this anticommutator to vanish since $w \neq v$).

### Step 1: What $c_v$ looks like at positions $w$ and $u$

Since $w$ and $u$ are both ancestors of $v$, they both belong to $U(v)$. The $c_v$ operator has $X$ at every position in $U(v) \cup \{v\}$. Therefore:

- $c_v$ has $X$ at position $w$
- $c_v$ has $X$ at position $u$

### Step 2: What $d_w$ looks like at position $u$ — the cancellation

Node $u$ is a **child** of $w$, so $u \in \text{children}(w) \subseteq P(w)$.

Node $u$ is also a **descendant** of $w$, so $u \in \text{Occ}(w)$.

Therefore $u \in P(w) \cap \text{Occ}(w)$. In the symmetric difference $P(w) \triangle \text{Occ}(w)$, elements that appear in *both* sets cancel. Node $u$ cancels.

Node $u$ is not an ancestor of $w$ (it is below $w$), so $u \notin U(w)$.

**Result:** $d_w$ has **identity** at position $u$. The operator "forgets" about node $u$ entirely.

### Step 3: What $d_w$ looks like at position $v$

Node $v$ is a grandchild of $w$ — a descendant but *not* a direct child. So $v \in \text{Occ}(w)$ but $v \notin \text{children}(w)$. Is $v$ in the remainder of $w$? No — remainder collects children of ancestors of $w$, and $v$ is below $w$, not above.

Therefore $v \in \text{Occ}(w) \setminus P(w)$. In the symmetric difference, elements in $\text{Occ}$ but not $P$ survive. So $v \in (P(w) \triangle \text{Occ}(w)) \setminus \{w\}$ (assuming $v \neq w$, which it is since $v$ is a grandchild).

**Result:** $d_w$ has $Z$ at position $v$.

### Step 4: What $d_w$ looks like at position $w$

By construction, $d_w$ has $Y$ at its own position $w$.

### Step 5: Count the anticommuting positions

| Position | $d_w$ | $c_v$ | Anticommutes? |
|:--------:|:-----:|:-----:|:-------------:|
| $w$ | $Y$ | $X$ | **Yes** — different non-identity Paulis |
| $u$ | $I$ | $X$ | No — identity commutes with everything |
| $v$ | $Z$ | $X$ | **Yes** — different non-identity Paulis |

Two anticommuting positions. An **even** count. For the operators to anticommute, we need an **odd** count.

**Therefore $\{d_w, c_v\} \neq 0$.** The CAR is violated. $\square$

### The mechanism in one sentence

> The intermediate node $u$ is both a child and a descendant of its parent $w$. The symmetric difference $P(w) \triangle \text{Occ}(w)$ cancels anything in both sets, so $u$ vanishes from $d_w$. This creates an identity gap at position $u$, which should have contributed an anticommuting position (since $c_v$ has $X$ there). The gap flips the parity from odd to even, breaking anticommutation.

---

## A concrete counterexample

Here is the balanced ternary tree on 8 nodes, which makes the failure vivid:

```
        4
      / | \
     1   3   6
    /   /   / \
   0   2   5   7
```

The depth-2 path $4 \to 6 \to 7$ triggers the theorem. Concretely:

**For grandparent $w = 4$ (the root):**

- $U(4) = \emptyset$
- $P(4) = \{1, 3, 6\}$ (all three children)
- $\text{Occ}(4) = \{0, 1, 2, 3, 4, 5, 6, 7\}$ (all descendants — it is the root)
- $P(4) \cap \text{Occ}(4) = \{1, 3, 6\}$ — *all* children are also descendants!
- $(P \triangle \text{Occ}) \setminus \{4\} = \{0, 2, 5, 7\}$
- $d_4 = $ `ZIZIYZIZ`

Note: $d_4$ has **identity at position 6**. Node 6 was cancelled.

**For grandchild $v = 7$:**

- $U(7) = \{6, 4\}$ (ancestors)
- $P(7) = \{1, 3, 5\}$
- $c_7 = $ `IZIZXZXX`

Note: $c_7$ has **$X$ at position 6** (since 6 is an ancestor of 7).

**The failing anticommutator $\{d_4, c_7\}$:**

| Qubit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|:-----:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| $d_4$ | $Z$ | $I$ | $Z$ | $I$ | $Y$ | $Z$ | $I$ | $Z$ |
| $c_7$ | $I$ | $Z$ | $I$ | $Z$ | $X$ | $Z$ | $X$ | $X$ |
| | — | — | — | — | anti | same | — | anti |

Anticommuting positions: 4 ($Y$ vs $X$) and 7 ($Z$ vs $X$). Count: **2 (even)**. The operators commute instead of anticommuting. The CAR is violated.

Position 6 — where $d_4$ has $I$ and $c_7$ has $X$ — is the gap. If node 6 had *not* cancelled, $d_4$ would have $Z$ at position 6, giving three anticommuting positions (odd), and the CAR would hold.

---

## The proof: sufficiency

Stars work — and the argument is clean. In a star with root $r$ and leaves $\ell_1, \ldots, \ell_{N-1}$:

For any leaf $j$:
$$U(j) = \{r\}, \quad P(j) = \{\ell_k : k < j\}, \quad \text{Occ}(j) = \{j\}.$$

Since $j \notin P(j)$ (a node is never a sibling of itself with smaller index) and $\text{Occ}(j) = \{j\}$, we have $P(j) \cap \text{Occ}(j) = \emptyset$. The symmetric difference and set difference agree. No cancellation occurs.

For two distinct leaves $j < k$:

- $c_j$ has $X$ at positions $\{j, r\}$ and $Z$ at $P(j) = \{\ell_m : m < j\}$
- $c_k$ has $X$ at positions $\{k, r\}$ and $Z$ at $P(k) = \{\ell_m : m < k\}$
- At position $r$: $X$ vs $X$ — commutes (same Pauli)
- At position $j$: $X$ vs $Z$ — **anticommutes** (since $j < k$ means $j \in P(k)$)
- No other position has non-identity in both operators

Exactly one anticommuting position. Odd. The anticommutation relation holds.

All other Majorana pairs ($d_j$ vs $d_k$, $c_j$ vs $d_k$) work by the same counting argument — the root provides a commuting shared position, and a single leaf provides the unique anticommuting position. Stars have exactly the right structure to make the count odd every time.

---

## The exhaustive census

We do not rely on the proof alone. Every labelled rooted tree for $N = 1$ through $5$ has been enumerated and tested computationally, checking all anticommutation relations symbolically:

| $N$ | Total trees ($N^{N-1}$) | Pass CAR | Stars | Match? |
|:---:|:-----------------------:|:--------:|:-----:|:------:|
| 1 | 1 | 1 | 1 | ✓ |
| 2 | 2 | 2 | 2 | ✓ |
| 3 | 9 | 3 | 3 | ✓ |
| 4 | 64 | 4 | 4 | ✓ |
| 5 | 625 | 5 | 5 | ✓ |

**701 trees. Exactly $N$ pass for each $N$. They are exactly the $N$ stars.** No accidental successes. No borderline cases. The boundary is binary: star or broken.

---

## What the theorem does *not* say

Precision matters here. The star-tree theorem says something specific, and the temptation to over-read it is real. Let me be explicit about boundaries.

**It does NOT say "BK is wrong."** BK uses Construction F (the set-difference formula), not Construction A (the symmetric-difference formula). BK is correct — we verified it in [Post 2](2026-10-13-fenwick-trees-and-bravyi-kitaev.md).

**It does NOT say "you cannot encode with non-star trees."** Construction B (the path-based method of Steudtner & Wehner, Jiang et al., and Miller's Bonsai) works for *all* trees. You can build valid encodings from balanced binary trees, ternary trees, or any other topology — you just cannot do it with the SRL index-set recipe.

**It does NOT say "the update/parity/occupation vocabulary is useless."** The vocabulary correctly *describes* any valid encoding. What fails is the claim that the vocabulary is *constructive* — that you can mechanically derive a valid encoding by reading sets off an arbitrary tree.

**It DOES say:**

1. The generic tree-to-operator recipe (Construction A) produces valid results only for trivial tree shapes.
2. The SRL "unification" of JW and BK under one framework is a conflation of two genuinely different constructions.
3. The field's migration from index-set methods to path-based methods (2018 onward) was structurally necessary, not merely a preference.

---

## Why stars are special — the geometric picture

There is an elegant way to see why depth 1 is the hard boundary.

In a star, every non-root node has exactly **one** ancestor (the root) and **zero** descendants (it is a leaf). This means:

- $U(j)$ is trivial: just $\{r\}$ for leaves, $\emptyset$ for the root.
- $\text{Occ}(j)$ is trivial: just $\{j\}$ for leaves.
- $P(j)$ collects only siblings — nodes at the *same* depth.

There is no way for a node to be simultaneously in another node's parity set *and* its occupation set, because parity collects siblings (same depth) while occupation collects descendants (deeper). In a star, "same depth" and "deeper" never overlap for any pair.

The moment a tree has depth 2, some node has both a parent (putting it in its parent's parity set, as a child) and grandchildren (putting it in its grandparent's occupation set, as a descendant). This dual membership is what the symmetric difference cancels, and what the cancellation breaks.

---

## The landscape after the theorem

Where does this leave us? The three constructions from Post 3 now have rigorous status:

| Construction | Domain | Role |
|:------------:|:------:|:----:|
| **A** (index-set, symmetric diff) | Stars only | Descriptive vocabulary; not a generator |
| **F** (Fenwick, set diff) | Fenwick tree | Bespoke formula for one tree |
| **B** (path-based) | All trees | The universal constructive method |

The SRL paper's contribution remains valuable: it gave us the *vocabulary* (update, parity, occupation, remainder) and it made BK *implementable*. What the star-tree theorem adds is the missing characterisation: the vocabulary describes, but does not construct. New encodings — for balanced trees, ternary trees, hardware-native topologies — must be derived via Construction B.

---

## What we built across this series

Starting from the bare antisymmetry constraint in [Post 1](2026-10-06-the-antisymmetry-problem.md), we have:

1. **Established** that fermion-to-qubit encodings exist because antisymmetry can be tracked by parity phases, and that the Jordan-Wigner $Z$-chain is the simplest but costliest ($O(N)$ weight) solution.

2. **Built** the Bravyi-Kitaev encoding from the Fenwick tree data structure, achieving $O(\log N)$ weight with all 120 anticommutators verified computationally ([Post 2](2026-10-13-fenwick-trees-and-bravyi-kitaev.md)).

3. **Unmasked** the SRL framework as a conflation of three constructions — one generic recipe (symmetric difference) that works only for stars, one bespoke formula (set difference) that works for the Fenwick tree, and one universal method (path-based) that the field quietly migrated to ([Post 3](2026-10-20-three-constructions-in-a-trenchcoat.md)).

4. **Proved** — here, now — that the generic recipe's failure is not accidental but structural: the symmetric-difference cancellation of intermediate nodes on depth-$\geq 2$ paths is the unique mechanism, and it triggers on every non-star tree. Verified exhaustively on all 701 trees for $N = 1$ through $5$.

The encoding problem is not closed — there are questions about optimal weight, hardware-connectivity-aware tree selection, and whether Construction F can be generalised beyond Fenwick — but the *framework* question is settled. The index-set recipe is a description language, not a construction method. The path-based approach is the constructive foundation. And the Fenwick tree remains a beautiful, singular object — the one non-star tree for which someone found a bespoke formula that works, three decades before anyone proved why the generic one couldn't.

*Keep counting the anticommutators.*
