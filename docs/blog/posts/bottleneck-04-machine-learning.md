---
date: 2026-08-05
notebook: https://github.com/johnazariah/quantum/blob/main/bottleneck/notebooks/04-machine-learning.ipynb
categories:
- The Quantum Bottleneck
- Machine Learning
tags:
- quantum kernels
- SVM
- feature maps
- dequantisation
authors:
- John Azariah
social:
  linkedin: 'On the notebook''s two-dimensional half-moons data, the two-qubit quantum kernel does not beat the classical radial basis function baseline. The result is useful because a large quantum feature space is not evidence of a useful classifier.


    The post starts with the Netflix Prize''s lesson that representation matters. Its notebook then builds overlap circuits, assembles a kernel matrix from measurement counts, and trains a classical support vector machine.


    Any advantage depends on the access model, data-encoding cost, and whether the kernel remains hard to approximate classically. Rigorous separations exist for constructed quantum-data tasks; dequantisation results remove other claimed speedups when classical algorithms receive comparable access.


    #QuantumComputing #MachineLearning'
  bluesky: 'A two-qubit quantum kernel does not beat the classical RBF baseline on this half-moons dataset. The result sets up the real question: when is a quantum similarity useful and classically hard to approximate?'
---

# The Feature Explosion

The two-qubit quantum kernel in the companion notebook does not beat its classical radial basis function baseline on the half-moons data. That result is useful: a feature space does not become valuable merely by being quantum.

The Netflix Prize remains a good parable. Recommendation quality depended on finding representations that exposed useful structure in sparse, noisy data, then comparing them against strong baselines.

<!-- more -->

The problem was not simply to recommend films. It was to infer preference from users, items, ratings, histories, and all the interactions between them.

That is a familiar machine-learning move. When a problem is not linearly separable in the data we can see, we map it into a richer space where the separating surface may become simple. The cost is that richer spaces can become enormous.

Classical machine learning has a beautiful workaround: the **kernel trick**. Instead of explicitly constructing a feature vector $\phi(x)$, compute only the similarity

$$
K(x, x') = \langle \phi(x), \phi(x') \rangle .
$$

Support vector machines (SVMs) use those pairwise similarities to find a separating boundary. As long as $K(x, x')$ is cheap to evaluate, the feature space can be large without being explicitly stored.

The bottleneck appears when the similarity itself becomes the hard part.

## When similarity becomes expensive

High dimension alone is not the obstruction; kernel methods deliberately create high-dimensional spaces. The cost lies in accessing their geometry efficiently.

A kernel method needs a kernel matrix. The straightforward implementation in the notebook compares every training point with every other training point, requiring $m^2$ circuit evaluations for $m$ examples. Symmetry can remove nearly half of those evaluations for the square training matrix, but the scaling remains quadratic.

A practical kernel method must answer three questions:

- can I encode the data into that space;
- can I compute the pairwise similarities;
- can I do both without smuggling in an even harder classical problem?

Quantum kernels live at that boundary.

## Use a quantum state as the feature map

A quantum feature map prepares a state $|\phi(x)\rangle$ from classical data $x$. The associated kernel is the overlap between two prepared states:

$$
K(x, x') = |\langle \phi(x') | \phi(x) \rangle|^2 .
$$

Operationally, this is a circuit experiment. Prepare $U_\phi(x)|00\rangle$, apply the inverse of $U_\phi(x')$, and measure the probability of returning to $|00\rangle$. If the circuit vocabulary is new, [Circuit Bench 00](../../circuit-bench/00-reading-a-quantum-circuit/README.md) explains gates, unitary rotations, and measurement before you meet them inside the kernel circuit.

The hybrid workflow is:

1. encode each data point with a quantum feature-map circuit;
2. estimate $K(x_i, x_j)$ from measurement counts;
3. assemble the kernel matrix;
4. train a classical SVM using that precomputed kernel.

The quantum device supplies the kernel estimates, and a classical SVM trains on the resulting matrix.

## Build the kernel, then compare it

The notebook builds a small quantum-kernel workflow:

- generate a two-dimensional half-moons dataset;
- encode each point into a two-qubit feature map using rotations and entanglement;
- estimate the kernel matrix by running overlap circuits;
- train a classical SVM on that quantum kernel;
- compare it with a classical radial basis function (RBF) kernel SVM.

Schematically, the kernel circuit has the following form. The notebook itself constructs the corresponding OpenQASM strings rather than Python gate objects:

```python
def kernel_circuit(x, xp):
    return U_phi(x) + U_phi_adjoint(xp) + measurement
```

The measured probability of `00` is the estimated overlap. Repeating that for every pair of training points gives the matrix passed to `SVC(kernel='precomputed')`.

On this fixed data split, the ideal overlap kernel and the classical RBF baseline each classify 11 of the 12 test points. The notebook estimates each overlap from finite shots, so individual runs can move with sampling noise. The comparison supplies a working quantum-kernel pipeline, not evidence of an advantage.

## Reality check: the classical baseline fights back

Quantum machine learning is one of the easiest areas to oversell, because the words line up too neatly: quantum state spaces are large, machine learning likes large feature spaces, therefore quantum computers should help. The middle step is where the work is.

Rigorous separations do exist on constructed learning tasks when the learner has direct quantum access to quantum data.[^quantum-learning] That access model does not automatically describe recommender systems, medical classifiers, or language models built from classical records.

Dequantisation results show the other side. Under length-squared sampling access, classical algorithms can match quantum-inspired performance for tasks such as principal-component analysis and supervised clustering, removing an exponential separation under those assumptions.[^dequantisation] The access model is part of the claim.

The largest practical obstacle is often **data loading**. If a million classical features require a million gates to encode, the quantum feature map may lose before the kernel is ever measured. Quantum advantage is more plausible when the data is already quantum, when the feature map is compact, or when the classical simulation of the kernel circuit is genuinely hard.

The notebook asks a narrower question: can a quantum circuit define and estimate a useful similarity measure? Its half-moons comparison answers the engineering question and leaves the advantage question open.

## Compare the kernels

The [companion notebook](https://github.com/johnazariah/quantum/blob/main/bottleneck/notebooks/04-machine-learning.ipynb) lets you compare a two-qubit quantum kernel with a classical RBF kernel on the same toy dataset.

[^quantum-learning]: Huang et al., ["Quantum advantage in learning from experiments"](https://doi.org/10.1126/science.abn7293), *Science*, 2022. The separation concerns constructed tasks with quantum experimental access, not arbitrary classical datasets.
[^dequantisation]: Chia et al., ["Sampling-Based Sublinear Low-Rank Matrix Arithmetic Framework for Dequantizing Quantum Machine Learning"](https://doi.org/10.1145/3549524), *Journal of the ACM*, 2022.

---

*This is Unit 4 of The Quantum Bottleneck series. Next up: [The Convergence Wall](bottleneck-05-finance.md) — where expectation estimation meets the Monte Carlo square-root law.*
