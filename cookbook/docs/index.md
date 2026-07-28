---
hide:
  - navigation
---

<span id="the-quokka-cookbook"></span>

# Circuit Bench

**Quantum circuit notes you can actually run.**

---

## What is this?

A growing collection of self-contained quantum circuit notes — each one explains a concept from the ground up, builds a circuit step by step, and gives you a working [OpenQASM 2.0](https://openqasm.com/) program you can run on your [Quokka](https://www.quokkacomputing.com/).

No framework bloat. No 47 imports. No prerequisites beyond curiosity. Just circuits, explained — then executed.

## Why we're building this

Most quantum computing resources teach you qubits and gates, then leave you stranded somewhere around phase kickback wondering *why you should care*.

We do it the other way around. Each circuit note starts with a **problem** — something concrete and interesting — then builds the quantum circuit that solves it. Theory arrives when it's useful, not when it's scheduled. Phase kickback shows up when it saves you a measurement, not because it's Chapter 3.

The goal is **understanding through doing**. If you can read a `for` loop, you can read a quantum circuit. And if you can run one, you'll understand it better than if you'd read ten pages of formalism.

## What's Quokka?

<div class="grid cards" markdown>

-   :material-cube-outline:{ .lg .middle } **A quantum computer in your hand**

    ---

    [Quokka](https://www.quokkacomputing.com/) is a 30-qubit quantum computing system built by [Eigensystems](https://www.quokkacomputing.com/) in Australia. It's a physical device — a puck that fits in your hand — with a companion [iOS app](https://apps.apple.com/au/app/quokka-quantum/id6754873585) and cloud platform.

    [:octicons-arrow-right-24: www.quokkacomputing.com](https://www.quokkacomputing.com/)

-   :material-file-code-outline:{ .lg .middle } **Standard OpenQASM 2.0**

    ---

    Quokka runs standard [OpenQASM 2.0](https://openqasm.com/) — no proprietary language, no SDK lock-in. Every Circuit Bench program is a plain text `.qasm` file. What you learn here works everywhere.

</div>

<span id="whats-coming"></span>

## Circuit Bench structure

The published notes progress from the fundamentals to algorithms, applications, and advanced techniques. Each note is self-contained and includes a runnable circuit.

| | Circuit Bench section | What you'll learn |
|---|--------|-------------------|
| **Foundations** | Circuit literacy, Bell state, teleportation, Deutsch-Jozsa | Gates, bases, entanglement, measurement, your first quantum speedup |
| **Algorithms and applications** | Bernstein-Vazirani, Simon, Grover, QAOA, VQE, QFT | Oracles, search, optimisation, molecular simulation |
| **Advanced techniques** | Phase estimation, error mitigation, quantum counting | The techniques that power the big algorithms |

!!! tip "How each circuit note works"

    Where a section applies, circuit notes use a shared structure:

    1. **What this circuit does** — the problem and goal, in plain language
    2. **Circuit components or prerequisites** — the required qubits, gates, and prior concepts
    3. **Circuit walkthrough** — the circuit, built incrementally with explanation at every step
    4. **The complete circuit** — the runnable OpenQASM program in one place
    5. **Run it** — execute the circuit, observe the output, and interpret the result
    6. **Analysis and practical notes** — derivations, limitations, connections, and next experiments

## Who is this for?

- **Students** taking a quantum computing course who want a hands-on companion
- **Software engineers** curious about quantum computing but allergic to hype
- **Researchers** who want a quick reference for standard circuits and protocols
- **Anyone** who learns by doing rather than by reading axioms

No physics degree required. We introduce every concept when it's needed, in the context of a working circuit.

## Stay in the loop

New circuit notes appear as the workbooks need them. [Watch the repo on GitHub](https://github.com/johnazariah/quantum) to get notified, or check back here.

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **Learning Path**

    ---

    The full roadmap — what we'll cover and why, in what order.

    [:octicons-arrow-right-24: See the plan](learning-path.md)

-   :material-bookshelf:{ .lg .middle } **References**

    ---

    Textbooks, papers, courses, and talks — curated for going deeper.

    [:octicons-arrow-right-24: Further reading](references.md)

-   :material-github:{ .lg .middle } **Contribute**

    ---

    Found a typo? Want to suggest a circuit note? Every note is a PR away.

    [:octicons-arrow-right-24: GitHub](https://github.com/johnazariah/quantum)

-   :material-cube-outline:{ .lg .middle } **Get a Quokka**

    ---

    The quantum computing puck these circuit notes are built for.

    [:octicons-arrow-right-24: quokkacomputing.com](https://www.quokkacomputing.com/)

</div>

<span id="run-the-recipes-no-hardware-required"></span>

## Run the circuits — no hardware required

You don't need to own a Quokka puck. [Sign up at quokkacomputing.com](https://www.quokkacomputing.com/get-started) to get a Google Colab notebook that connects to one of six cloud Quokkas — paste in any Circuit Bench `.qasm` file, run the cell, and see the results.

!!! note "Other ways to run QASM"
    Every circuit note uses standard OpenQASM 2.0. You can also run the programs for free on:

    - **[IBM Quantum](https://quantum.ibm.com/)** — free account, paste QASM into the Composer, run on simulators or real 127-qubit hardware
    - **[Quirk](https://algassert.com/quirk)** — instant drag-and-drop circuit simulator in the browser (no QASM paste, but great for visual intuition)

    Your learning is portable. What you build here works everywhere.

Every `.qasm` file on the Circuit Bench is a valid OpenQASM 2.0 program. If you outgrow Quokka, the same files run on IBM Quantum, Qiskit, or any other QASM-compatible platform.
