# Mapping Fermions to Qubits — Social Hooks

## Post 1: The Antisymmetry Problem (Oct 6)

### LinkedIn
Electrons are not qubits. Their wavefunctions pick up a minus sign whenever two of them swap places, and a quantum computer that ignores that sign structure will simulate the wrong physics. The Jordan-Wigner transform fixes this with a chain of Z operators that tracks parity, but the chain grows linearly with the number of orbitals. For a molecule with 200 active orbitals, every single fermionic operator touches all 200 qubits. This post builds the problem from scratch using hydrogen as a running example, and shows exactly where the cost comes from and why it matters.

#QuantumComputing #QuantumChemistry

### Bluesky
New series on fermionic encodings. Post 1 builds the antisymmetry problem from scratch using hydrogen, derives the Jordan-Wigner transform, and counts the O(n) cost that motivates everything that follows.
