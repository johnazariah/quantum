# About

## What is Quantum Workbooks?

Two tracks of quantum computing teaching material — unified by one philosophy: **start with the problem, not the qubit**.

**The Circuit Bench** is a collection of self-contained quantum circuit notes. Each one explains a concept from the ground up, builds a circuit step by step, and gives you a working program you can run on [Quokka](https://www.quokkacomputing.com/) or any OpenQASM-compatible platform.

**The Quantum Bottleneck** companion notebooks are runnable worked examples for the upcoming book of the same name. Each notebook implements a quantum algorithm in the context of the industry problem it was designed to solve — from delivery route optimisation to catalyst design for carbon capture.

## Who made this?

[John Azariah](https://github.com/johnazariah) — PhD candidate at the Centre for Quantum Software & Information, University of Technology Sydney, and one of the original designers of Microsoft's Q# quantum programming language. He believes the best way to learn quantum computing is to run quantum circuits, not to stare at axioms.

## The teaching philosophy

Most resources teach quantum computing **bottom-up**: start with linear algebra, define qubits, prove properties of gates, build up to algorithms. By the time you reach anything interesting, you've forgotten why you started.

We teach **problem-down**: start with something you want to compute, figure out what circuit solves it, and learn the theory because you need it — not because it's on a syllabus.

Every concept in the Circuit Bench is introduced **at the point where it's useful**, in the context of a working circuit. Phase kickback isn't Chapter 3; it shows up when it saves you a measurement. The QFT isn't a standalone topic; it appears when it solves a problem.

## Why Quokka?

[Quokka](https://www.quokkacomputing.com/) runs standard OpenQASM 2.0. That means:

- **No SDK lock-in.** The circuits are the code. No `import qiskit` boilerplate.
- **Tactile learning.** A physical device makes the abstract concrete.
- **Portable knowledge.** Every `.qasm` file works on any QASM-compatible platform.

Quokka is built by [Eigensystems](https://www.quokkacomputing.com/) in Australia.

## Contributing

This is an open-source project. If you find a bug, want to improve an explanation, or have an idea for a new circuit note:

- **Bug or typo?** Open an [issue](https://github.com/johnazariah/quantum/issues)
- **New circuit note?** Open a [pull request](https://github.com/johnazariah/quantum/pulls)
- **Question?** Start a [discussion](https://github.com/johnazariah/quantum/discussions)

## License

MIT. Use these materials however you like.
