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
