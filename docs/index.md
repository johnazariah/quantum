---
hide:
  - navigation
---

# Quantum

*Making quantum leaps in understanding.*

*I'm **John Azariah** — a lifelong student interested in mathematics, physics, and quantum computing, bringing three decades of software engineering and functional programming to get a better understanding of what makes the universe tick.*

*This is the quantum computing companion to [my main blog](https://johnazariah.github.io), which covers functional programming, software engineering, and language design.*

---

## Series

### Linear Algebra for Fun and Profit

The linear algebra behind quantum computing and machine learning. Each post builds from first principles with a single running example you can check by hand.

- [How to Raise *e* to a Matrix (and Why You'd Want To)](blog/2026/07/14/how-to-raise-e-to-a-matrix-and-why-youd-want-to/) — the matrix exponential solves the Schrödinger equation, and the result is a rotation rather than a stretch.
- [Where Eigenvalues Pay Rent](blog/2026/07/17/where-eigenvalues-pay-rent/) — three industries, three matrices, three ways the same linear algebra pays rent.
- [The Eigensolver Zoo](blog/2026/07/21/the-eigensolver-zoo/) — every eigensolver is a function of the operator; this post surveys the classical half.
- [What a Difference *i* Makes](blog/2026/07/24/what-a-difference-i-makes/) — insert a factor of *i* and stretch becomes rotation. The quantum eigensolvers.

### The Quantum Bottleneck

In *The Quantum Bottleneck*, I begin with problems that already cost industries real money, then follow each one down to the mathematical obstruction and the circuit proposed to address it. Every post has a runnable notebook and a reality check against the classical methods and hardware limits that remain.

- [The $50M Delivery Route](blog/2026/07/27/the-50m-delivery-route/) — UPS can save up to $50 million a year by removing one mile from each driver's daily route. We use a three-node MaxCut problem to inspect the complete QAOA loop before putting the trucks back in.
- [The Trapdoor](blog/2026/07/29/the-trapdoor/) — Shor's algorithm does not search for factors. A compiled phase-estimation example exposes a period, then ordinary number theory turns that period into 3 and 5.
- [The $2B Molecule](blog/2026/08/03/the-2b-molecule/) — a two-qubit H₂ example keeps the complete VQE measurement loop visible without pretending to be a drug-discovery platform.
- [The Feature Explosion](blog/2026/08/05/the-feature-explosion/) — a quantum overlap kernel and a classical radial-basis-function kernel tie at 11/12 on the same small dataset. The negative result is the useful result.
- [The Convergence Wall](blog/2026/08/10/the-convergence-wall/) — classical Monte Carlo prices the option; a compiled quantum circuit shows the phase-readout mechanism behind amplitude estimation, with the unbuilt oracles left visible.
- [The Scheduling Nightmare](blog/2026/08/12/the-scheduling-nightmare/) — two binary decisions are enough to inspect the QUBO-to-Ising-to-QAOA pipeline and see how faithfully a circuit can optimise the wrong model.
- [Series overview and companion notebooks](bottleneck/) — the full eight-part path, publishing every Monday and Wednesday through 19 August.
- [Circuit Bench](circuit-bench/) — thirteen circuit notes with diagrams, OpenQASM, expected output, and gate-by-gate explanations for the machinery used throughout the series.

Next up: **The Materials Maze** on 17 August — a two-site Hubbard benchmark, followed by a deliberately visible handoff into compiled quantum phase estimation.

### From Saturday to Co-Author

How a functional programmer went from "what is QAOA?" on a Saturday morning to co-author on a quantum computing paper, eight weeks later. Written in Julia and grounded in functional programming.

1. [Saturday](https://johnazariah.github.io/2026/05/29/saturday-to-coauthor-01-saturday.html)
2. [The Fold Under the Tree](https://johnazariah.github.io/2026/06/01/saturday-to-coauthor-02-the-fold-under-the-tree.html)
3. [Three Gradients in One Codebase](https://johnazariah.github.io/2026/06/04/saturday-to-coauthor-03-three-gradients-in-one-codebase.html)
4. [The Walls](https://johnazariah.github.io/2026/06/08/saturday-to-coauthor-04-the-walls.html)
5. [The Algebra That Runs Itself](https://johnazariah.github.io/2026/06/11/saturday-to-coauthor-05-the-algebra-that-runs-itself.html)
6. [Eighteen Hundred Reasons](https://johnazariah.github.io/2026/06/15/saturday-to-coauthor-06-eighteen-hundred-reasons.html)
7. [Learning from the Masters](https://johnazariah.github.io/2026/06/18/saturday-to-coauthor-07-learning-from-the-masters.html)
8. [Fourteen](https://johnazariah.github.io/2026/06/22/saturday-to-coauthor-08-fourteen.html)
9. [The Collaborator That Never Sleeps](https://johnazariah.github.io/2026/06/25/saturday-to-coauthor-09-the-collaborator-that-never-sleeps.html)
10. [What Language Taught Us About Mathematics](https://johnazariah.github.io/2026/06/29/saturday-to-coauthor-10-what-language-taught-us-about-mathematics.html)
