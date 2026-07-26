# The Quantum Bottleneck — Social Hooks

## Post 01: The $50M Delivery Route (Jul 28)

### LinkedIn
One mile is not much of a route. Across the UPS fleet, it can be worth up to $50 million a year.

That is where I wanted to begin The Quantum Bottleneck: not with a qubit, but with a problem whose value is obvious and whose search space gets silly very quickly. Twenty delivery stops can be ordered in about 2.4 quintillion ways.

The companion notebook uses a triangle because I want every moving part of QAOA to remain visible. Three nodes give us eight candidate cuts, so we can check every answer by hand, inspect the cost and mixer gates, and compare the samples with random choice.

Then we put the trucks back in. A real routing model adds variables, constraints, penalty weights, circuit depth, a classical optimiser, and some formidable classical competition.

This is the first post in an eight-part series about where quantum algorithms might help, where they plainly do not yet, and what the runnable toy examples actually teach us.

#QuantumComputing #Logistics

### Bluesky
UPS says one mile less per driver per day can save up to $50M a year. I use an eight-solution triangle to keep every QAOA step visible, then put the trucks back in and ask what survives at logistics scale.

---

## Post 02: The Trapdoor (Aug 1)

### LinkedIn
RSA depends on a one-way asymmetry: multiplying two large primes is easy, while recovering them from their product has resisted efficient classical algorithms. Shor's algorithm reduces factoring to period-finding and uses quantum phase estimation to expose the period.

For its runnable example, the notebook works with N=15 and a=7. It compiles one known phase branch into a small circuit, measures the phase, recovers period 4 with continued fractions, and obtains factors 3 and 5 with greatest-common-divisor arithmetic.

Modular exponentiation, error correction, and cryptographic-scale resources are outside this demonstration. Those are the pieces that make breaking RSA a fault-tolerant hardware problem rather than a present-day capability.

#QuantumComputing #Cryptography

### Bluesky
Shor's algorithm factors by finding a period rather than searching candidate divisors. This notebook compiles one known phase branch for N=15, then recovers period 4 and factors 3 and 5 with classical post-processing.

---

## Post 03: The $2B Molecule (Aug 5)

### LinkedIn
Published estimates of developing a new medicine vary widely and can reach several billion dollars once failures and financing costs are included. Better electronic-structure calculations address one part of that risk: predicting molecular energies before expensive experiments.

The runnable example does not model a drug candidate. It runs the variational quantum eigensolver on a reduced two-qubit H2 Hamiltonian at one bond length, measures Z, X, and Y Pauli terms, and compares the energy with exact diagonalisation.

The circuit exposes the complete hybrid loop. Drug-relevant calculations still require molecular integrals, active-space selection, expressive states, many measurements, and a classical chemistry workflow around the quantum solver.

#QuantumComputing #DrugDiscovery

### Bluesky
Drug development can cost billions, but this notebook makes a smaller claim: VQE on a reduced two-qubit H2 Hamiltonian at one bond length. It exposes the measurement loop without presenting a drug simulation.

---

## Post 04: The Feature Explosion (Aug 8)

### LinkedIn
On the notebook's two-dimensional half-moons data, the two-qubit quantum kernel does not beat the classical radial basis function baseline. The result is useful because a large quantum feature space is not evidence of a useful classifier.

The post starts with the Netflix Prize's lesson that representation matters. Its notebook then builds overlap circuits, assembles a kernel matrix from measurement counts, and trains a classical support vector machine.

Any advantage depends on the access model, data-encoding cost, and whether the kernel remains hard to approximate classically. Rigorous separations exist for constructed quantum-data tasks; dequantisation results remove other claimed speedups when classical algorithms receive comparable access.

#QuantumComputing #MachineLearning

### Bluesky
A two-qubit quantum kernel does not beat the classical RBF baseline on this half-moons dataset. The result sets up the real question: when is a quantum similarity useful and classically hard to approximate?

---

## Post 05: The Convergence Wall (Aug 12)

### LinkedIn
Classical Monte Carlo error falls as 1/sqrt(N), so one more decimal digit costs roughly 100 times as many samples. Quantum amplitude estimation can improve the query scaling to 1/N, provided the quantity is already encoded in a suitable quantum amplitude.

The notebook prices a European call classically with Black-Scholes and Monte Carlo. Its quantum circuit does something narrower: it reads a compiled three-bit phase for the fraction of eight uniformly weighted price bins above the strike. It does not encode the discounted payoff or build the state-preparation and Grover oracles.

The possible speedup belongs to oracle queries. Distribution loading, reversible payoff logic, controlled operations, and fault-tolerant depth still determine whether a finance application wins end to end.

#QuantumComputing #Finance

### Bluesky
One more decimal digit in classical Monte Carlo costs about 100 times as many samples. This notebook prices the option classically; its compiled circuit reads the in-the-money fraction on an eight-bin price grid.

---

## Post 06: The Scheduling Nightmare (Aug 15)

### LinkedIn
Two nurses and two shifts need only two bits in this notebook because Nurse B's assignment is implied by Nurse A's. Even here, one hard coverage rule and one soft preference must be combined without letting the penalty weight overwhelm the objective.

The notebook enumerates all four assignments, maps the exact QUBO cost to an Ising Hamiltonian, tunes one QAOA layer classically, and runs the two-qubit circuit. The circuit biases samples towards feasible schedules; it does not guarantee the optimum.

A real roster adds variables, legal and skill constraints, penalty design, and a serious comparison with mixed-integer and constraint-programming solvers.

#QuantumComputing #Optimisation

### Bluesky
A two-bit nurse schedule exposes QUBO penalty design: one hard coverage rule and one soft preference. The notebook maps that cost to a two-qubit QAOA circuit that biases samples towards feasible schedules.

---

## Post 07: The Materials Maze (Aug 19)

### LinkedIn
The materials notebook solves a two-site Hubbard model by exact classical diagonalisation. Its quantum circuit begins only after one known energy has been shifted, rounded onto a three-bit phase grid, and compiled into a phase-estimation readout.

The Hubbard benchmark introduces the competition between electron hopping and on-site repulsion, while the circuit demonstrates how quantum phase estimation turns an eigenphase into measured bits. Controlled evolution under the Hubbard Hamiltonian is not implemented.

Scaling towards useful materials requires a faithful Hamiltonian encoding, state preparation, controlled time evolution, phase precision, error correction, and comparison with tensor-network, Monte Carlo, and embedding methods in the regimes where they work.

#QuantumComputing #MaterialsScience

### Bluesky
This notebook diagonalises a two-site Hubbard model classically, then reads one known energy with compiled three-bit QPE. It demonstrates phase extraction, not quantum simulation of the Hubbard Hamiltonian.

---

## Post 08: The Catalyst Bottleneck (Aug 22)

### LinkedIn
Better catalysts for water splitting, carbon dioxide reduction, nitrogen fixation, and battery chemistry depend on active sites embedded in much larger environments. Quantum embedding gives a quantum computer one focused job: solve the hard active-space Hamiltonian.

The capstone notebook starts after active-space selection and embedding. It runs the variational quantum eigensolver on a precomputed two-qubit effective Hamiltonian, then compares the measured energy with an exact benchmark for that reduced model.

The notebook does not run density functional theory, construct an embedding bath, or simulate a catalyst. A useful quantum contribution depends on the accuracy of that classical interface as well as the state preparation, measurement cost, optimiser, and hardware.

#QuantumComputing #ClimateTech

### Bluesky
Quantum embedding gives a quantum computer a specific job: solve a hard active-space Hamiltonian inside a catalyst model. This two-qubit VQE notebook starts from precomputed inputs; it does not simulate a catalyst.
