# Mapping Fermions to Qubits — Social Hooks

## Post 1: The Antisymmetry Problem (Oct 6)

### LinkedIn
Electrons are not qubits. Their wavefunctions pick up a minus sign whenever two of them swap places, and a quantum computer that ignores that sign structure will simulate the wrong physics. The Jordan-Wigner transform fixes this with a chain of Z operators that tracks parity, but the chain grows linearly with the number of orbitals. For a molecule with 200 active orbitals, every single fermionic operator touches all 200 qubits. This post builds the problem from scratch using hydrogen as a running example, and shows exactly where the cost comes from and why it matters.

#QuantumComputing #QuantumChemistry

### Bluesky
New series on fermionic encodings. Post 1 builds the antisymmetry problem from scratch using hydrogen, derives the Jordan-Wigner transform, and counts the O(n) cost that motivates everything that follows.

---

## Post 2: Fenwick Trees and the Bravyi-Kitaev Encoding (Oct 13)

### LinkedIn
The Jordan-Wigner transform encodes fermions on qubits with a parity chain that touches every lower qubit, giving O(n) operator weight. The Bravyi-Kitaev encoding brings this down to O(log n) by storing partial parities in a binary tree structure borrowed from competitive programming: the Fenwick tree, invented in 1994 for cumulative frequency tables. This post builds the tree from scratch using bit arithmetic, shows what each qubit stores, derives the update and parity sets, and demonstrates verified Majorana operators for 8 modes where the maximum weight is 4 instead of 8.

#QuantumComputing #QuantumChemistry

### Bluesky
Post 2 in the encodings series builds the Bravyi-Kitaev encoding from the Fenwick tree. A data structure from competitive programming gives O(log n) operator weight where Jordan-Wigner needs O(n). All operators verified against the full anticommutation algebra.

---

## Post 3: Three Constructions in a Trenchcoat (Oct 20)

### LinkedIn
The Seeley-Richard-Love paper (2012) presents a unified framework where Jordan-Wigner, Bravyi-Kitaev, and Parity encodings are all derived from trees using the same recipe. This post shows that the unification is illusory. The framework contains two different operator formulas wearing the same notation, and the formula that works for stars (JW, Parity) fails for the Fenwick tree by exactly one qubit at exactly the wrong place. Verified computationally against all 120 anticommutation relations for 8 modes.

#QuantumComputing #QuantumChemistry

### Bluesky
Post 3 in the encodings series. The SRL framework looks like one construction but is actually two formulas in a trenchcoat. The wrong one fails by a single qubit, verified against all 120 anticommutators.

---

## Post 4: The Star-Tree Theorem (Oct 27)

### LinkedIn
The SRL framework (2012) derives fermionic encodings by reading index sets off a tree. The star-tree theorem proves this recipe satisfies the canonical anticommutation relations if and only if the tree has depth at most 1 (a star). The proof identifies a single mechanism: on any depth-2 path, the intermediate node cancels in a symmetric difference, creating an identity gap that flips the anticommutation parity from odd to even. Verified exhaustively on all 701 labelled rooted trees for n=1 through 5: exactly n trees pass for each n, and they are exactly the n stars.

#QuantumComputing #QuantumChemistry

### Bluesky
Post 4 completes the encodings series. The star-tree theorem proves the SRL index-set recipe works only for depth-1 trees. A single cancellation mechanism breaks everything deeper. Verified exhaustively on all 701 trees for n=1..5.
