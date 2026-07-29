# Circuit Bench

All circuit notes in one place. Each one is self-contained: pick whatever interests you, or follow the [Learning Path](../learning-path.md) for a structured progression.

New notes will appear as the workbooks need them. [Watch the repo](https://github.com/johnazariah/quantum) to get notified.

## Find the circuit files

Every note has a **Files on the bench** section with direct links to its runnable OpenQASM 2.0 program, expected output, and circuit diagram where one is available.

In the repository, those files live together under [`cookbook/recipes/`](https://github.com/johnazariah/quantum/tree/main/cookbook/recipes):

```text
cookbook/recipes/01-bell-state/
├── README.md       # the circuit note
├── bell.qasm       # the runnable circuit
├── expected.txt    # the result to compare against
└── circuit.png     # the circuit diagram
```

Some notes need more than one circuit. Circuit Bench 00 compares three one-qubit programs, Circuit Bench 03 has constant and balanced oracles, and Circuit Bench 11 has three noise scales. Their file lists make those roles explicit.

## Run a circuit

1. Open a circuit note and choose a `.qasm` file from **Files on the bench**.
2. Load or paste it into the [Quokka](https://www.quokkacomputing.com/) app or cloud notebook, or another runner that accepts OpenQASM 2.0.
3. Start with 1024 shots unless the note says otherwise. Deterministic circuits should concentrate on one result; probabilistic circuits should approach the stated distribution.
4. Compare the result with `expected.txt` and the note's **Run it** section. Compare the pattern, not exact shot counts.
5. Check the runner's bit-string convention before interpreting a result. Some tools print the highest-index classical bit first; the notes state the register order when it matters.

The [Getting Started](https://johnazariah.github.io/quantum/getting-started/) page walks through the Quokka setup and a first Bell-state run.

## Extend and experiment

Treat each committed `.qasm` file as a reference circuit. Copy it before changing it, then use the same loop for every experiment:

1. **Predict** what should change in the output and why.
2. **Change one thing**: one gate, angle, oracle term, measurement basis, or repetition count.
3. **Run under the same conditions**, including the same number of shots.
4. **Compare** with the reference output.
5. **Explain** the difference in terms of state preparation, phase, interference, or measurement.

A small record is enough:

| Change | Prediction | Observed result | Explanation |
|---|---|---|---|
| One controlled modification | What should move or stay fixed? | Counts or probabilities | Which circuit mechanism caused it? |

Each note ends with experiments chosen for that circuit. They are deliberately small: the point is to isolate a mechanism, not to turn a teaching circuit into an advantage claim.

---

## Foundations

The fundamentals: one to three qubits, a handful of gates, and the first circuits where quantum behaviour becomes visible.

| # | Circuit note | Qubits | Key concept | Status |
|---|--------|--------|-------------|--------|
| 00 | [Reading a Quantum Circuit](00-reading-a-quantum-circuit/README.md) | 1 | Gates, Bloch sphere, unitary rotation, measurement bases | ✅ Published |
| 01 | [Bell State](01-bell-state/README.md) | 2 | Entanglement, measurement correlation | ✅ Published |
| 02 | [Teleportation](02-teleportation/README.md) | 3 | Classical feedback, the teleportation protocol | ✅ Published |
| 03 | [Deutsch-Jozsa](03-deutsch-jozsa/README.md) | 3 | Oracles, phase kickback, quantum speedup | ✅ Published |

---

## Algorithms and applications

Optimisation, simulation, and search: the circuits where quantum algorithms start to show their structure.

| # | Circuit note | Qubits | Key concept | Status |
|---|--------|--------|-------------|--------|
| 04 | [Bernstein-Vazirani](04-bernstein-vazirani/README.md) | 4 | Hidden string discovery in one query | ✅ Published |
| 05 | [Simon's Problem](05-simons-problem/README.md) | 4 | Hidden period, exponential speedup | ✅ Published |
| 06 | [Grover's Search](06-grovers-search/README.md) | 3 | Unstructured search, quadratic speedup | ✅ Published |
| 07 | [QAOA for MaxCut](07-qaoa-maxcut/README.md) | 3 | Combinatorial optimisation, variational methods | ✅ Published |
| 08 | [VQE for H₂](08-vqe-h2/README.md) | 2 | Quantum chemistry, molecular simulation | ✅ Published |
| 09 | [Quantum Fourier Transform](09-quantum-fourier-transform/README.md) | 3 | Fourier analysis on a quantum register | ✅ Published |

---

## Advanced techniques

Phase estimation, quantum counting, and the techniques that power the big algorithms.

| # | Circuit note | Qubits | Key concept | Status |
|---|--------|--------|-------------|--------|
| 10 | [Quantum Phase Estimation](10-quantum-phase-estimation/README.md) | 4 | Eigenvalue extraction, precision measurement | ✅ Published |
| 11 | [Error Mitigation (ZNE)](11-error-mitigation-zne/README.md) | 2 | Zero-noise extrapolation, practical noise reduction | ✅ Published |
| 12 | [Quantum Counting](12-quantum-counting/README.md) | 4 | Counting solutions without finding them | ✅ Published |
