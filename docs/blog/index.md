# Start here: quantum computing, problem first

Most quantum computing explanations begin with a qubit.

This blog usually will not.

The goal here is to teach real quantum computing from the direction in which people encounter real problems: delivery routes, cryptography, drug discovery, machine learning, finance, supply chains, materials, and climate. We start with the bottleneck, build the smallest runnable notebook that exposes the structure, and introduce the quantum machinery only when the problem asks for it.

That does not mean skipping the foundations. It means earning them.

## What these posts are for

Each post is a companion to a runnable workbook. The post gives you the orientation: what problem we are studying, why the classical version runs into trouble, what quantum idea enters, and what the notebook is actually demonstrating.

The notebook is the lab bench. It keeps the moving parts visible: circuit construction, calls to the backend, measurements, post-processing, and the classical checks that keep the example honest.

This is part of a larger project called *The Quantum Bottleneck*, but the blog is not trying to be the long-form version in miniature. It is a public companion path: enough context to understand the notebooks, enough honesty to know what they do not prove, and enough structure to see why the examples matter.

## How to read the series

Start anywhere that interests you, but the first path is:

1. [The $50M Delivery Route](posts/bottleneck-01-logistics.md) — QAOA for a tiny MaxCut instance, motivated by logistics.
2. [The Trapdoor](posts/bottleneck-02-cryptography.md) — Shor's algorithm as period-finding, motivated by public-key cryptography.
3. [The $2B Molecule](posts/bottleneck-03-drug-discovery.md) — VQE as a way to estimate molecular energy.

Each post follows the same rhythm:

```text
problem -> bottleneck -> quantum idea -> notebook -> reality check
```

When a notebook uses a toy example, you will see that called out clearly. When an algorithm depends on fault-tolerant hardware before it becomes industrially useful, you will see that called out too. The point is not to make quantum computing sound inevitable. The point is to make the structure visible.

## Where the Circuit Bench fits

The [Circuit Bench](../circuit-bench/index.md) is the side path for circuit literacy and circuit machinery: gates, Bloch-sphere intuition, measurement bases, Bell states, teleportation, Grover search, the Quantum Fourier Transform, phase estimation, VQE, QAOA, quantum counting, and error mitigation.

You do not need to read the Circuit Bench before reading the Bottleneck posts. The main path here is application-first. But when a post meets a circuit primitive that deserves a closer look, it will point to the relevant circuit note.

Think of it this way:

- **The Bottleneck posts** explain why a quantum idea appears.
- **The notebooks** let you run the idea.
- **The Circuit Bench** lets you slow down and inspect the circuit machinery.

That is the promise of this space: problem-first, runnable, and honest.
