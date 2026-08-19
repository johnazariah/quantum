# Mapping Fermions to Qubits — Social Hooks

## Post 1: The Antisymmetry Problem (Oct 6)

### LinkedIn
Electrons carry a rule that qubits do not: exchange two fermions and the wavefunction changes sign. A qubit register has to be taught that minus sign before it can represent chemistry correctly.

I wanted to begin this series with H₂ because four spin-orbitals and two electrons are enough to see the whole problem. Jordan-Wigner stores occupation directly and uses a string of Z operators to keep track of fermionic parity. It is beautifully literal, and the bill arrives in the same place: for N modes, the worst-case operator has weight N and the average has weight (N + 1)/2.

That gives us a correct encoding and the question for the next post: can a prefix-sum data structure from 1994 make the parity bookkeeping logarithmic?

#QuantumComputing #QuantumChemistry

### Bluesky
Electrons carry a rule qubits do not: exchange two fermions and the wavefunction changes sign. Jordan-Wigner teaches that rule with a Z-chain of worst-case weight O(n). I start with H₂ so we can see the cost.

---

## Post 2: Fenwick Trees and the Bravyi-Kitaev Encoding (Oct 13)

### LinkedIn
The Jordan-Wigner parity chain from Post 1 has an obvious information-theoretic weakness: parity is a single bit, but JW reads it by touching every qubit below the target. Competitive programmers solved exactly this class of problem in 1994 with the Fenwick tree, a data structure that answers prefix-sum queries in O(log n) time using nothing but bit manipulation.

I build the tree from scratch in this post, derive the three index sets that determine the Bravyi-Kitaev encoding, and verify every Majorana operator against the full anticommutation algebra for eight modes. The maximum operator weight drops from 8 (JW) to 4 (BK), and the mechanism is pure tree arithmetic.

#QuantumComputing #QuantumChemistry

### Bluesky
Parity is one bit, so why does Jordan-Wigner read every qubit below the target? The Fenwick tree, a prefix-sum structure from 1994, answers in O(log n). I build the Bravyi-Kitaev encoding from it and verify all the anticommutators.

---

## Post 3: Three Constructions in a Trenchcoat (Oct 20)

### LinkedIn
Seeley, Richard, and Love published a 2012 paper that seemed to unify three fermionic encodings (Jordan-Wigner, Bravyi-Kitaev, and Parity) into a single recipe: pick a tree, read off index sets, build operators. The vocabulary is beautiful and the notation is clean, which is probably why it took a decade to notice that the recipe is actually two different formulas wearing the same symbols.

I trace the divergence to a single qubit position where the symmetric difference and set difference disagree. For star-shaped trees the two formulas coincide; for the Fenwick tree they do not, and 8 of 120 anticommutator pairs break. The failure is not numerical noise; it is a structural gap in the framework.

#QuantumComputing #QuantumChemistry

### Bluesky
The SRL framework (2012) unifies three fermionic encodings under one tree-based recipe. It turns out the recipe contains two formulas in the same notation, and they disagree at exactly the qubit positions where the Fenwick tree has depth.

---

## Post 4: The Star-Tree Theorem (Oct 27)

### LinkedIn
I wanted to know whether the SRL framework fails only for the Fenwick tree or for every tree deeper than a star, so I enumerated all 701 labelled rooted trees on up to five nodes and tested each one. The answer turns out to be clean: the generic index-set recipe satisfies the canonical anticommutation relations if and only if the tree has depth at most 1. The proof identifies a single mechanism. On any path of length two, the intermediate node cancels in a symmetric difference, leaving an identity gap that flips the anticommutation count from odd to even.

That is the star-tree theorem: stars work, everything deeper breaks, and the reason is the same every time.

#QuantumComputing #QuantumChemistry

### Bluesky
I enumerated all 701 labelled rooted trees on up to 5 nodes. The SRL index-set recipe passes the canonical anticommutation relations if and only if the tree is a star. One cancellation mechanism breaks every deeper tree.
