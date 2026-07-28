# Circuit Bench

**Quantum circuit notes you can actually run.**

```bash
git clone https://github.com/johnazariah/quantum
cd quantum/cookbook
```

Pick a circuit note. Read why it matters. Run it on your [Quokka](https://www.quokkacomputing.com/).

## What is this?

A collection of self-contained quantum circuit notes, each built around a real problem and a working [OpenQASM 2.0](https://openqasm.com/) circuit that runs on [Quokka](https://www.quokkacomputing.com/) — a 30-qubit quantum computing system designed for education and exploration.

No framework boilerplate. No 47 imports. Just circuits, explained.

## Circuit notes

| # | Circuit note | What you'll learn |
|---|--------|-------------------|
| 00 | [Reading a Quantum Circuit](recipes/00-reading-a-quantum-circuit/) | Gates, Bloch sphere, unitary rotations, measurement bases |
| 01 | [Bell State](recipes/01-bell-state/) | Entanglement, measurement correlation |
| 02 | [Teleportation](recipes/02-teleportation/) | Classical feedback, the teleportation protocol |
| 03 | [Deutsch-Jozsa](recipes/03-deutsch-jozsa/) | Oracles, quantum speedup, interference |
| 04 | [Bernstein-Vazirani](recipes/04-bernstein-vazirani/) | Hidden string discovery in one query |
| 05 | [Simon's Problem](recipes/05-simons-problem/) | Hidden periods and Fourier sampling |
| 06 | [Grover's Search](recipes/06-grovers-search/) | Unstructured search and amplitude amplification |
| 07 | [QAOA for MaxCut](recipes/07-qaoa-maxcut/) | Variational optimisation on a graph |
| 08 | [VQE for H2](recipes/08-vqe-h2/) | Quantum chemistry and measurement workflows |
| 09 | [Quantum Fourier Transform](recipes/09-quantum-fourier-transform/) | Fourier structure on a quantum register |
| 10 | [Quantum Phase Estimation](recipes/10-quantum-phase-estimation/) | Eigenphase extraction |
| 11 | [Error Mitigation (ZNE)](recipes/11-error-mitigation-zne/) | Noise scaling and extrapolation |
| 12 | [Quantum Counting](recipes/12-quantum-counting/) | Counting solutions with Grover and QPE |

## How to use this repo

Each note lives in its own directory under `recipes/`:

```
recipes/01-bell-state/
├── README.md        # The explanation — why it matters, how it works
├── bell.qasm        # The circuit — paste into quokka or run from CLI
└── expected.txt     # What you should see
```

Read the README, run the `.qasm` file, compare with `expected.txt`.

## Prerequisites

- A [Quokka](https://www.quokkacomputing.com/) puck, or the Quokka app ([iOS](https://apps.apple.com/au/app/quokka-quantum/id6754873585))
- Curiosity

That's it. Every circuit is a standard OpenQASM 2.0 file — paste it into your Quokka and run. Linear algebra and quantum mechanics are introduced *as needed*, in context, inside each note.

## Contributing

Found a bug in a circuit note? Want to suggest a new one? Open an issue or PR.

## License

MIT
