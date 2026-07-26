# The Quantum Bottleneck — Social Hooks

## Post 01: The $50M Delivery Route (Jul 28)

### LinkedIn
Twenty delivery stops can be ordered in 20! ways, about 2.4 quintillion. UPS reports that removing one mile from each driver's daily route can save up to $50 million a year.

The first Quantum Bottleneck post asks what QAOA changes in that kind of combinatorial search. Its companion notebook uses MaxCut on a three-node triangle, where all eight candidates can be scored by hand, then follows the cost phase, mixer, measurement, and classical scoring loop.

Moving from the triangle to a real routing problem adds qubits, constraints, penalty weights, circuit depth, and a classical optimiser, all beyond what this notebook claims to solve.

#QuantumComputing #Logistics

### Bluesky
Twenty delivery stops have about 2.4 quintillion possible orderings. A three-node MaxCut notebook shows how QAOA turns a small version of that search into interference, with all eight candidates checked by hand.

---

## Post 02: The Trapdoor (Aug 1)

### LinkedIn
The notebook factors 15. The problem is the cryptographic machinery that keeps the internet standing. Shor's algorithm threatens RSA not by brute force but by turning factoring into period-finding, and period-finding into phase estimation. This post walks through the circuit, the quantum Fourier transform, and the honest gap between a toy demonstration and a real cryptographic threat.

#QuantumComputing #Cryptography

### Bluesky
Bottleneck 02: The Trapdoor. The notebook factors 15. The problem is RSA. Shor's algorithm turns factoring into period-finding, and the gap between 15 and a real key is the bottleneck.

---

## Post 03: The $2B Molecule (Aug 5)

### LinkedIn
Getting a drug to market costs roughly $2B, and a substantial fraction goes to molecular screening. Before a molecule reaches a clinical trial, we often do not know enough about how its electrons behave. VQE promises to compute electronic structure on a quantum computer, but the gap between a hydrogen molecule on a simulator and a real drug candidate is vast. This post walks through both sides honestly.

#QuantumComputing #DrugDiscovery

### Bluesky
Bottleneck 03: The $2B Molecule. VQE computes electronic structure for drug candidates, but the gap between a hydrogen molecule on a simulator and a real drug is the bottleneck.

---

## Post 04: The Feature Explosion (Aug 8)

### LinkedIn
Machine learning works by moving data into a richer feature space. Quantum machine learning asks: what if the useful feature space is naturally quantum and classically awkward to compute? This post looks at quantum kernels, SVMs, and the dequantisation results that put a ceiling on the quantum speedup claims. The Netflix Prize is still a useful parable.

#QuantumComputing #MachineLearning

### Bluesky
Bottleneck 04: The Feature Explosion. Quantum kernels promise richer feature spaces. Dequantisation results say: not so fast. This post walks through the honest gap.

---

## Post 05: The Convergence Wall (Aug 12)

### LinkedIn
Finance runs on Monte Carlo. Option prices, value-at-risk, stress tests: all computed by averaging over many possible futures. Every extra digit of accuracy quadruples the computation. Quantum amplitude estimation promises a quadratic speedup on that convergence rate. This post runs a small option pricing circuit and asks what stands between a toy demo and a real trading desk.

#QuantumComputing #Finance

### Bluesky
Bottleneck 05: The Convergence Wall. Classical Monte Carlo needs 100x more samples for each extra digit. Quantum amplitude estimation promises quadratic speedup. The bottleneck is everything in between.

---

## Post 06: The Scheduling Nightmare (Aug 15)

### LinkedIn
Assign nurses to shifts. Route trucks through depots. Match jobs to machines. These are not smooth optimisation problems; they are combinatorial, and a decision is yes or no. QAOA encodes them as QUBO problems and searches for the optimal assignment. This post walks through the encoding, the circuit, and the gap between satisfying a few constraints and solving a real scheduling problem.

#QuantumComputing #Optimisation

### Bluesky
Bottleneck 06: The Scheduling Nightmare. Supply chains are webs of discrete choices. QAOA attacks them as QUBO problems. The post walks through the gap between a toy schedule and a real one.

---

## Post 07: The Materials Maze (Aug 19)

### LinkedIn
The materials we care about most are the awkward ones: catalysts, superconductors, battery cathodes. Their behaviour comes from strongly correlated electrons, and that is exactly where classical approximations become fragile. The Hubbard model is the standard test case. This post runs a small quantum simulation and asks how far we are from materials that matter.

#QuantumComputing #MaterialsScience

### Bluesky
Bottleneck 07: The Materials Maze. Strongly correlated electrons make materials hard to simulate classically. The Hubbard model is the test case. This post asks how far we are.

---

## Post 08: The Catalyst Bottleneck (Aug 22)

### LinkedIn
The energy transition needs better catalysts for water splitting, CO2 reduction, nitrogen fixation, and battery chemistry. Catalyst design is an electronic-structure problem in disguise. This final post in The Quantum Bottleneck runs a VQE calculation on a small active space and closes the series with an honest assessment: quantum computing is not a shortcut past chemistry, but it may be the only path through certain problems classical computers cannot reach.

#QuantumComputing #ClimateTech

### Bluesky
Bottleneck 08: The Catalyst Bottleneck. Climate tech needs better catalysts. Catalyst design is electronic structure in disguise. The series closer asks honestly: where does quantum computing fit?
