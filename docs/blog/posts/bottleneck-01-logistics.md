---
date: 2026-07-27
notebook: https://github.com/johnazariah/quantum/blob/main/bottleneck/notebooks/01-logistics.ipynb
categories:
- The Quantum Bottleneck
- Optimisation
tags:
- QAOA
- MaxCut
- combinatorial optimisation
authors:
- John Azariah
social:
  linkedin: |
    One mile is not much of a route. Across the UPS fleet, it can be worth up to $50 million a year.

    That is where I wanted to begin The Quantum Bottleneck: not with a qubit, but with a problem whose value is obvious and whose search space gets silly very quickly. Twenty delivery stops can be ordered in about 2.4 quintillion ways.

    The companion notebook uses a triangle because I want every moving part of QAOA to remain visible. Three nodes give us eight candidate cuts, so we can check every answer by hand, inspect the cost and mixer gates, and compare the samples with random choice.

    Then we put the trucks back in. A real routing model adds variables, constraints, penalty weights, circuit depth, a classical optimiser, and some formidable classical competition.

    This is the first post in an eight-part series about where quantum algorithms might help, where they plainly do not yet, and what the runnable toy examples actually teach us.

    #QuantumComputing #Logistics
  bluesky: 'UPS says one mile less per driver per day can save up to $50M a year. I use an eight-solution triangle to keep every QAOA step visible, then put the trucks back in and ask what survives at logistics scale.'
---

# The $50M Delivery Route

*Dedicated to my friend, mentor and a boss who stood up for me when no one else would, Dave Fellows. You encouraged me when I told you I was writing a book on quantum computing, and this is a step in that direction.*

UPS reports that removing one mile from each driver's daily route can save up to **$50 million a year**.[^ups-orion] At fleet scale, a route planner can create real value without proving it has found the perfect route; a repeatable improvement is enough.

Even a route with only 20 stops admits

$$
20! = 2,432,902,008,176,640,000
$$

possible orderings, before time windows, vehicle capacity, driver hours, or traffic enter the model.

The notebook reduces the optimisation machinery to **MaxCut** on a triangle: three nodes, three edges, and eight colourings. We can enumerate every candidate, inspect every gate, and compare the circuit's samples with uniform random choice.

<!-- more -->

The transfer to routing is structural: encode discrete decisions, turn the objective and constraints into a cost operator, alternate cost and mixer operations, then measure and score candidate solutions. The price of that transfer is also concrete. Real instances need far more variables, carefully weighted constraint penalties, deeper circuits, and a classical optimiser around the quantum circuit.

The exact enumeration program is easy to describe: generate every route, compute every distance, and keep the shortest. Its running time makes it useless long before the model becomes realistic.

The triangle strips those domain constraints away and leaves a complete circuit example whose inputs and outputs fit on the page.

## The shape under the logistics

The travelling-salesman problem, vehicle routing, nurse rostering, circuit placement, portfolio selection, and MaxCut all share a shape:

1. There are many discrete decisions.
2. The value of one decision depends on other decisions.
3. You can score any one proposed answer.
4. You cannot score every proposed answer once the instance gets large.

For MaxCut, the decisions are wonderfully bare. Each graph node gets a bit:

```text
0 = one side of the cut
1 = the other side of the cut
```

An edge is "cut" when its endpoints have different bits. So for a triangle with nodes `0`, `1`, and `2`, the bit string `001` means nodes 0 and 1 are on one side, node 2 is on the other. Two of the three edges cross the cut, so the cut value is 2.

There are only eight bit strings for a triangle:

```text
000  001  010  011  100  101  110  111
```

The notebook enumerates all eight. For three nodes, brute force gives us ground truth: we can compute the exact answer before asking whether the quantum circuit produces a useful distribution.

For a triangle, the best possible cut value is 2. You cannot cut all three edges because a triangle has an odd cycle: once two edges cross the cut, the third edge necessarily lands inside one side. So the six bit strings with one bit different from the other two are optimal; `000` and `111` are the bad ones.

The classical problem now has three explicit parts:

```text
bit string -> candidate solution
cut value  -> score
best score -> optimisation target
```

QAOA keeps that candidate representation and score, then changes the distribution from which we sample candidates.

If circuit words like gate, basis, or measurement are new, start with [Circuit Bench 00: Reading a Quantum Circuit](../../circuit-bench/00-reading-a-quantum-circuit/README.md). If you want the first two-qubit example before the QAOA circuit appears, [Circuit Bench 01: The Bell State](../../circuit-bench/01-bell-state/README.md) is the side path: Hadamard, CNOT, measurement correlation, and why changing measurement basis matters. You do not need either note first, but they are there when those primitives deserve a closer look.

## Superposition is only the start

A common explanation of quantum search says:

> A quantum computer tries all answers at once.

The QAOA circuit does begin by placing the qubits into a superposition of all eight triangle colourings. Measuring at that point, however, returns a uniformly random bit string. Superposition prepares the candidate states; **interference** creates the useful bias.

A quantum algorithm is useful when it arranges the computation so that unwanted possibilities cancel and wanted possibilities reinforce. The possibilities being "present" is not enough. Their amplitudes have to be made to interfere in the right way before measurement.

QAOA, the **Quantum Approximate Optimisation Algorithm**, is one attempt to do that for optimisation problems. It offers no guarantee of the optimum and no escape from NP-hardness. It produces a probability distribution over candidate answers, with parameters chosen so that good answers appear more often than they would under uniform random sampling.

For this notebook, the test is concrete: do the chosen angles shift probability away from `000` and `111` and towards the six cuts with score 2?

## Turn the cut into an operator

QAOA represents the objective as an operator that is diagonal in the computational basis. Each candidate bit string is then an eigenstate, and its score is the corresponding eigenvalue.

For MaxCut, the key operator is Pauli-$Z$.

You only need one fact about it:

```text
Z on |0> gives +1
Z on |1> gives -1
```

Now look at an edge between nodes `i` and `j`.

If the two bits are the same, $Z_i Z_j$ gives $+1$.

If the two bits are different, $Z_i Z_j$ gives $-1$.

The expression

$$
\frac{1 - Z_i Z_j}{2}
$$

is an edge-cut detector. It evaluates to 0 when the edge is not cut, and 1 when it is cut.

Sum that expression over every edge and you have turned the graph into an operator:

$$
C = \sum_{(i,j)\in E} \frac{1 - Z_i Z_j}{2}.
$$

Here $C$ is a score to maximise. Ground-state formulations instead use $-C$ as an energy to minimise. The identity term in $C$ contributes only a global phase, so the notebook drops it and absorbs the remaining sign and factor into its angle convention. Under that convention, each edge compiles to CNOT-$R_Z(2\gamma)$-CNOT. Changing the sign or factor changes the numerical optimum for $\gamma$.

Each colouring is now a computational-basis state whose cut value can be written into relative phase. The same structural move returns later when molecules, schedules, and materials become operators.

## What the circuit actually does

The notebook builds a depth-1 QAOA circuit for the triangle. Depth 1 means one round of the two QAOA moves:

```text
cost, then mix
```

Two angles control that round. The cost angle $\gamma$ sets the edge phases; the mixer angle $\beta$ controls how far amplitude moves between neighbouring bit strings. The notebook uses values tuned for this graph and this gate convention:

$$
\gamma = 1.264491043069892,
\qquad
\beta = 0.3063052837250049.
$$

There are four stages in the circuit.

### 1. Start with every colouring equally likely

The circuit begins with Hadamard gates:

```qasm
h q[0];
h q[1];
h q[2];
```

Each Hadamard takes a qubit that starts as `0` and puts it into an equal superposition of `0` and `1`. Three Hadamards on three qubits create an equal superposition of the eight possible colourings.

At this point, every bit string has probability $1/8$.

Nothing has been optimised yet. We have only prepared the search space.

### 2. Imprint the cost as phase

For each graph edge, the notebook emits the same three-gate pattern. For edge `(0, 1)` with the fixed $\gamma$ above:

```qasm
cx q[0], q[1];
rz(2.528982) q[1];
cx q[0], q[1];
```

The first CNOT computes whether the two endpoint bits agree or differ, storing that parity temporarily in the target qubit. The $R_Z$ rotation then applies a phase depending on that parity. The second CNOT uncomputes the parity so the qubits go back to representing the original colouring.

The edge block restores the visible bit string and changes its relative phase. Measurement immediately after the cost step would still produce a uniform distribution; the mixer must turn those phase differences into probability differences.

### 3. Mix neighbouring colourings

The mixer applies an $R_X$ rotation to every qubit:

```qasm
rx(0.612611) q[0];
rx(0.612611) q[1];
rx(0.612611) q[2];
```

An $R_X$ rotation partially moves amplitude between `0` and `1` on a qubit. On the full bit string, that means amplitude can flow between colourings that differ by one bit flip.

This resembles trying a neighbouring solution in local search, except the movement is coherent. The amplitudes carry the phases from the cost step, so contributions arriving from different neighbouring colourings can add or cancel.

For the triangle, that interference suppresses `000` and `111`, the two colourings that cut no edges, and amplifies the six colourings that cut two edges. The circuit is not inspecting each answer and choosing the best one. The cost phase and mixer have been arranged so that amplitudes interfere differently around good and bad colourings.

### 4. Measure, score, repeat

At the end, the circuit measures:

```qasm
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
```

A single shot returns one candidate bit string. The notebook therefore runs the circuit many times, counts the outcomes, computes the cut value for each one, and estimates the expected cut value of the distribution:

```text
one shot       -> one candidate solution
many shots     -> an empirical distribution
cut function   -> score each sample
average score  -> quality of the chosen angles
```

Poor angles leave the distribution close to random. Better angles concentrate more probability on high-scoring cuts.

For the same circuit viewed directly on the Circuit Bench, see [QAOA for MaxCut](../../circuit-bench/07-qaoa-maxcut/README.md). The post you are reading explains why this circuit belongs in the logistics story; the Circuit Bench note is the more direct gate-by-gate version.

## Walking through the notebook

Open the notebook here:

[Unit 1 notebook: QAOA for MaxCut](https://github.com/johnazariah/quantum/blob/main/bottleneck/notebooks/01-logistics.ipynb)

The notebook keeps the exact baseline, circuit construction, sampling, scoring, and parameter sweep explicit. You should be able to see every moving part.

### Section 1: Define the graph

The graph is the triangle:

```python
n_qubits = 3
edges = [(0, 1), (0, 2), (1, 2)]
```

Then the notebook defines the scoring function:

```python
def cut_value(bitstring: str, edges: list) -> int:
    return sum(1 for i, j in edges if bitstring[i] != bitstring[j])
```

This is the classical problem, with no quantum mechanics anywhere near it. Given a proposed colouring, count the edges whose endpoints differ.

The notebook then enumerates all eight bit strings, establishing ground truth before we run the quantum circuit.

### Section 2: Build the QAOA circuit

The function `qaoa_qasm` writes OpenQASM 2.0 as a string.

That may look low-level if you are used to polished SDKs, but it is exactly what we want pedagogically. The code does not hide the circuit behind a library object. You can see:

- the Hadamards that prepare the uniform superposition;
- one CNOT-$R_Z$-CNOT block per edge;
- one $R_X$ mixer rotation per qubit;
- the final measurements.

The notebook uses fixed, pre-optimised parameters for the triangle:

```python
gamma_opt = 1.264491043069892
beta_opt = 0.3063052837250049
```

These values are tuned for this small graph and the stated gate convention; they are not universal QAOA constants. The later parameter sweep shows why angle choice matters.

### Section 3: Run on Quokka

The notebook sends the QASM program to a cloud Quokka and receives measurement counts.

The interesting output is not just "did we get the best bit string?" There are six best bit strings for the triangle, all with cut value 2. The question is whether the circuit shifts probability mass toward those six and away from `000` and `111`.

The bar chart colours optimal outcomes differently from suboptimal ones. This is the moment where the circuit becomes more than a diagram: you can see the distribution produced by interference.

The notebook then computes:

```python
expected_cut = sum(
    cut_value(k, edges) * results[k] / total_shots
    for k in results
)
```

That expected cut value is the quantity the classical optimiser would try to improve in a full QAOA workflow.

### Section 4: Sweep the parameter landscape

The parameter sweep makes the hybrid nature of QAOA visible. The notebook runs a grid of circuits over $\gamma$ and $\beta$ and records the expected cut value at each point. The heatmap is the landscape a classical optimiser would have to navigate.

For a larger problem, we would use a classical optimiser rather than sweep every point.

The complete hybrid loop is:

```text
choose angles
run quantum circuit
measure samples
compute average cut value
choose better angles
repeat
```

The quantum circuit is the function the classical optimiser queries.

That distinction will matter again in the VQE workbook. QAOA and VQE look like different algorithms, but structurally they are cousins: parameterised quantum circuit inside, classical optimiser outside.

### Section 5: Compare with random sampling

The final comparison uses uniform random sampling. This is a meaningful baseline for the triangle because six of its eight states are optimal: random sampling reaches an optimal cut with probability $3/4$ and has expected cut value $1.5$. The tuned circuit should concentrate still more probability on the six cuts with value 2.

## Back to the trucks

The notebook establishes the mechanics:

1. A combinatorial optimisation problem can be encoded as a Hamiltonian.
2. The Hamiltonian can be compiled into circuit operations.
3. The cost can be written into quantum phase.
4. A mixer can turn phase differences into measurement bias.
5. Samples from the circuit can be scored classically.
6. A classical optimiser can use those scores to tune the quantum circuit.

It does not establish an advantage for delivery routing, or even for large MaxCut instances. Industrial vehicle-routing problems already have mixed-integer methods, decomposition techniques, local search, and specialised heuristics. A useful QAOA result must compare against serious implementations of those methods while also paying for the quantum encoding, repeated measurements, and parameter tuning.

Routing also changes the circuit. Every decision variable needs a representation; capacity, timing, and assignment rules need constraints or a constraint-preserving mixer; and additional QAOA rounds add depth. Today's shallow, noisy hardware has not demonstrated that full pipeline at industrial scale.

## What to try next

If you run the notebook, do not just run it top to bottom and close the tab. Change it.

Change the graph:

```python
n_qubits = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
```

Change $\gamma$ and $\beta$ and watch the distribution flatten or sharpen.

Increase the parameter-sweep resolution and see how noisy the heatmap becomes when each circuit uses fewer shots.

Then extend the QASM builder to depth 2: cost, mixer, cost, mixer, with four angles instead of two. Deeper circuits are more expressive, but they are harder to tune and more vulnerable to noise.

The larger Quantum Bottleneck project goes further into the logistics motivation and the QAOA advantage debate. The workbook gives you the thing you can touch: a graph, a Hamiltonian, a circuit, a sampler, and a distribution that is no longer uniform.

For a first workbook, one fully exposed triangle is enough.

[^ups-orion]: See the ORION case summary in Delen, ["Analytics Success Story: UPS's ORION Project"](https://www.informit.com/articles/article.aspx?p=2992600&seqNum=6), which reports that reducing one mile per driver per day over a year can save UPS up to $50 million.

Next up: [The Trapdoor](bottleneck-02-cryptography.md) — where a hidden period replaces the search landscape, and "cost and mix" gives way to "Fourier and measure."
