# The Quantum Bottleneck — Social Hooks

## Post 01: The $50M Delivery Route (Jul 28)

### LinkedIn
One mile is not much of a route. Across the UPS fleet, it can be worth up to $50 million a year.

That is where I wanted to begin The Quantum Bottleneck: not with a qubit, but with a problem whose value is obvious and whose search space gets silly very quickly. Twenty delivery stops can be ordered in about 2.4 quintillion ways.

The companion notebook uses a triangle because I want every moving part of QAOA to remain visible. Three nodes give us eight candidate cuts, so we can check every answer by hand, inspect the cost and mixer gates, and compare the samples with random choice.

Then we put the trucks back in. A real routing model adds variables, constraints, penalty weights, circuit depth, a classical optimiser, and some formidable classical competition.

This is the first post in an eight-part series about where quantum algorithms might help, where they plainly do not yet, and what the runnable toy examples actually teach us.

This first post is dedicated to Dave Fellows: https://www.linkedin.com/in/dave-fellows-3a6b9a17/

My friend, mentor and a boss who stood up for me when no one else would. You encouraged me when I told you I was writing a book on quantum computing, and this is a step in that direction.

#QuantumComputing #Logistics

### Bluesky
UPS says one mile less per driver per day can save up to $50M a year. I use an eight-solution triangle to keep every QAOA step visible, then put the trucks back in and ask what survives at logistics scale.

---

## Post 02: The Trapdoor (Aug 1)

### LinkedIn
Shor's algorithm is usually introduced as the quantum algorithm that factors numbers. I think that description skips the useful move: the circuit estimates a period, and ordinary number theory turns that period into factors.

N=15 and a=7 earn their place because every arithmetic step fits on the page. The notebook compiles one known phase branch, reads 1/4 as 010, recovers period 4 with continued fractions, and obtains 3 and 5 with greatest-common-divisor arithmetic.

At cryptographic scale, all the omitted machinery returns. A real implementation still needs reversible modular exponentiation, error correction, and millions of physical qubits. Factoring 15 is the transparent example; those missing resources are the reason RSA is not falling to today's hardware.

This post is for Simon Middlemiss: https://www.linkedin.com/in/simon-middlemiss-3959b12/

In memory of that glorious talk we did together in Las Vegas in 2019. Truly one of the very best!

#QuantumComputing #Cryptography

### Bluesky
Shor's algorithm is usually introduced as a factoring algorithm. I chose N=15 because it makes the more useful move visible: a quantum circuit exposes a period, then classical arithmetic turns that period into factors.

---

## Post 03: The $2B Molecule (Aug 5)

### LinkedIn
Drug-development estimates can reach several billion dollars, but quantum chemistry owns only part of that bill. I wanted this example to isolate that part rather than let a two-qubit circuit masquerade as a drug-discovery platform.

I use H2 at one bond length because it is the smallest molecule that keeps the complete VQE loop visible. We prepare a trial state, measure the Z, X, and Y terms, reconstruct an energy, and compare it with exact diagonalisation of the same reduced Hamiltonian.

A drug-relevant calculation brings back the pieces this notebook leaves out: molecular integrals, active-space selection, an expressive trial state, a large measurement budget, and the classical chemistry workflow around the quantum solver.

This post is dedicated to Prof Robert Ditchfield: https://faculty-directory.dartmouth.edu/robert-ditchfield

You taught us Quantum Chemistry (Chem 81) in the fall of 1991, and ignited a spark that still burns today! Thank you for being one of my most memorable teachers at Dartmouth!

#QuantumComputing #DrugDiscovery

### Bluesky
I use H2 at one bond length because two qubits expose VQE's measurement loop. It is not a drug simulation; molecular integrals, active-space choice, measurement cost, and the classical chemistry around the solver still matter.

---

## Post 04: The Feature Explosion (Aug 8)

### LinkedIn
The two-qubit quantum kernel and classical RBF baseline both classify 11 of 12 test points. I am keeping the tie because it is the useful result: a quantum feature space does not become valuable merely by being quantum.

The Netflix Prize is still my preferred way into this topic. Machine learning lives or dies by representation, so the notebook builds a feature map, estimates pairwise overlaps from circuits, assembles the kernel matrix, and hands that matrix to a classical support vector machine.

The harder question comes after the circuit runs. Any advantage depends on data-loading cost, the access model, and whether a classical algorithm can approximate the same kernel. The dequantisation results belong in the main argument, not in small print.

#QuantumComputing #MachineLearning

### Bluesky
The quantum kernel and classical RBF baseline both classify 11 of 12 points. I kept the tie because it forces the right question: is the quantum similarity useful, cheap to encode, and genuinely hard to approximate?

---

## Post 05: The Convergence Wall (Aug 12)

### LinkedIn
One more decimal digit in classical Monte Carlo costs roughly 100 times as many samples. That convergence law is why quantum amplitude estimation attracts so much attention in finance.

I leave the option price on the classical side in this notebook. Black-Scholes and Monte Carlo supply the real pricing comparison; the compiled quantum circuit reads only the in-the-money fraction on eight uniformly weighted price bins. Calling that quantum option pricing would hide the state-preparation, payoff, and Grover oracles we have not built.

The possible 1/N scaling counts oracle queries. Distribution loading, reversible payoff logic, controlled operations, and fault-tolerant depth still decide whether anything improves back on the trading desk.

#QuantumComputing #Finance

### Bluesky
One more decimal digit in Monte Carlo costs about 100 times as many samples. I leave the option price classical; the compiled quantum circuit reads only an eight-bin fraction because the real pricing oracles are not built.

---

## Post 06: The Scheduling Nightmare (Aug 15)

### LinkedIn
I kept the roster to two nurses and two shifts so all four assignments fit on one page. That is enough to expose the modelling problem: one hard coverage rule, one soft preference, and a penalty weight that can quietly overwhelm the objective.

The notebook enumerates every assignment, derives the exact QUBO and Ising coefficients, tunes one QAOA layer classically, and runs the two-qubit circuit. QAOA biases the samples towards feasible schedules; it does not certify the optimum.

A badly written QUBO will be optimised faithfully, which is not much comfort to the person writing next month's roster. Real scheduling brings back legal rules, skills, fairness, thousands of variables, and formidable mixed-integer and constraint-programming baselines.

#QuantumComputing #Optimisation

### Bluesky
I kept the roster to two nurses and two shifts so all four assignments fit on one page. The QUBO exposes one hard rule, one soft preference, and a warning: the circuit will faithfully sample the model we actually wrote.

---

## Post 07: The Materials Maze (Aug 19)

### LinkedIn
The materials notebook does two different jobs, and I leave the seam visible. First, exact classical diagonalisation supplies the singlet-sector spectrum of a half-filled two-site Hubbard model. Then one known energy is shifted onto a three-bit grid and read by compiled quantum phase estimation.

That circuit demonstrates binary phase extraction. It does not implement controlled evolution under the Hubbard Hamiltonian, so calling it a quantum materials simulation would erase the most expensive step.

For a useful material, state preparation, controlled time evolution, phase precision, error correction, and the modelling around the active space all return. Tensor networks, quantum Monte Carlo, and embedding methods remain the classical competition wherever their assumptions hold.

#QuantumComputing #MaterialsScience

### Bluesky
I leave the seam visible in this materials notebook: exact diagonalisation supplies a two-site Hubbard energy, then compiled QPE reads that known phase. The circuit demonstrates phase extraction, not Hubbard simulation.

---

## Post 08: The Catalyst Bottleneck (Aug 22)

### LinkedIn
I am ending The Quantum Bottleneck with embedding because it gives the quantum solver a bounded job inside a scientific workflow. A catalyst is too large to hand to one device, but its hardest correlated orbitals can sometimes be isolated as an active space.

The notebook begins after a classical calculation has selected that space and supplied a two-qubit effective Hamiltonian. VQE prepares a trial state, measures its Pauli terms, and compares the resulting energy with an exact benchmark for the same reduced model.

The surrounding chemistry has not disappeared. Active-space choice, the environment, self-consistency, measurement cost, and hardware errors still determine whether the quantum correction means anything for a real catalyst.

#QuantumComputing #ClimateTech

### Bluesky
I end the series with embedding because it gives the quantum solver a bounded job inside a catalyst workflow. The two-qubit notebook starts from a precomputed active-space Hamiltonian; it does not simulate the catalyst.
