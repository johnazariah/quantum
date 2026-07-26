---
date: 2026-08-10
notebook: https://github.com/johnazariah/quantum/blob/main/bottleneck/notebooks/05-finance.ipynb
categories:
- The Quantum Bottleneck
- Finance
tags:
- Monte Carlo
- quantum amplitude estimation
- option pricing
- phase estimation
authors:
- John Azariah
social:
  linkedin: 'Classical Monte Carlo error falls as 1/sqrt(N), so one more decimal digit costs roughly 100 times as many samples. Quantum amplitude estimation can improve the query scaling to 1/N, provided the quantity is already encoded in a suitable quantum amplitude.


    The notebook prices a European call classically with Black-Scholes and Monte Carlo. Its quantum circuit does something narrower: it reads a compiled three-bit phase for the fraction of eight uniformly weighted price bins above the strike. It does not encode the discounted payoff or build the state-preparation and Grover oracles.


    The possible speedup belongs to oracle queries. Distribution loading, reversible payoff logic, controlled operations, and fault-tolerant depth still determine whether a finance application wins end to end.


    #QuantumComputing #Finance'
  bluesky: 'One more decimal digit in classical Monte Carlo costs about 100 times as many samples. This notebook prices the option classically; its compiled circuit reads the in-the-money fraction on an eight-bin price grid.'
---

# The Convergence Wall

Finance often asks for an average over possible futures. Classical Monte Carlo is the workhorse for that job, but its error falls only as $1/\sqrt{N}$. One more decimal digit of accuracy therefore needs roughly 100 times as many samples.

Unit 5 keeps the option price classical. Its quantum circuit reads a compiled phase for the fraction of eight uniformly weighted price bins above the strike, exposing the amplitude-estimation mechanism after state preparation and oracle construction have been supplied.

<!-- more -->

An option price, a value-at-risk estimate, a stress test, and an exposure calculation all have the same basic shape: define a model for uncertain market moves, run many scenarios, compute the payoff or loss in each scenario, and average.

That is a good reason Monte Carlo is everywhere in finance. It is flexible, model-agnostic, and embarrassingly parallel. If the payoff has path dependence, early exercise, barriers, correlations, or a messy book of instruments, Monte Carlo usually still has a way in.

The catch is convergence.

## Why the last decimal place costs so much

For a European call option, the quantity of interest is an expectation:

$$
V = e^{-rT}\mathbb{E}[\max(S_T - K, 0)].
$$

Here $S_T$ is the stock price at maturity $T$, $K$ is the strike price, and $r$ is the continuously compounded risk-free rate.

The Black-Scholes formula gives a closed-form answer under its assumptions, which makes it a useful benchmark. But the Monte Carlo version is the more general pattern:

1. sample possible terminal prices $S_T$;
2. compute the payoff $\max(S_T - K, 0)$;
3. average the discounted payoff.

If the payoff samples have standard deviation $\sigma$, then the Monte Carlo standard error scales like

$$
\frac{\sigma}{\sqrt{N}},
$$

where $N$ is the number of sampled scenarios. To halve the error, you need roughly four times as many paths. To gain another decimal digit, you need roughly one hundred times as many paths.

Monte Carlo remains flexible and parallel, but its last bit of accuracy is expensive.

## Change the convergence law

Quantum amplitude estimation (QAE) attacks the square-root law. Given coherent access to a state-preparation unitary and the required Grover-style reflections, QAE can estimate an amplitude $a$ with query error scaling like $1/N$ rather than $1/\sqrt{N}$.[^qae]

That is a quadratic improvement in oracle-query complexity.

A finance problem does not arrive as a clean quantum amplitude. A useful QAE pipeline needs problem-specific circuits, often called oracles, for the uncertainty model, payoff function, comparison threshold, and controlled amplification operator. Their construction cost, depth, and approximation error sit outside the $1/N$ query statement.

The companion notebook shows the convergence issue classically, then uses a compiled phase-readout circuit to make the QAE mechanism visible. A production option-pricing oracle is outside its scope.

If the phase-readout part is the unfamiliar piece, [Circuit Bench 10: Quantum Phase Estimation](../../circuit-bench/10-quantum-phase-estimation/README.md) gives the gate-level pattern: controlled powers, an inverse quantum Fourier transform (QFT), and a binary phase estimate.

## What the circuit estimates

The notebook has two separate halves.

First, it prices a simple Black-Scholes call option both analytically and by classical Monte Carlo. Schematically, the convergence loop is:

```python
for n_paths in path_counts:
    estimate = monte_carlo_call_price(n_paths)
    error = abs(estimate - black_scholes_price)
```

Second, it switches to a toy quantum proxy. It divides a price range into eight uniformly weighted bins, marks the bins whose centres are above the strike, and computes the in-the-money fraction. That grid fraction is mapped onto a three-bit phase, and a compiled amplitude-estimation-style circuit reads it out. It is not a market-weighted exercise probability.

The boundary is explicit:

- the notebook uses Black-Scholes and Monte Carlo for the actual option-pricing baseline;
- the quantum circuit estimates the in-the-money fraction on a uniform eight-bin price grid, not a market-weighted probability or the full discounted payoff;
- the amplitude-estimation circuit is compiled from the known proxy value;
- the state-preparation, payoff, and controlled-Grover oracles are not constructed.

The option price remains a classical benchmark. The circuit shows the phase-estimation readout inside QAE after the hard oracle-building work has been compiled away.

## Reality check: pay for the oracle

The asymptotic improvement is real, and a useful finance implementation must still pay for the whole pipeline.

First, the probability distribution must be loaded or generated coherently. If preparing the market model costs too much, the algorithm loses before estimation starts.

Second, the payoff must be encoded reversibly. Real derivatives can have path dependence, discontinuities, early exercise logic, and book-level netting rules. Turning those into quantum circuits is engineering, not notation.

Third, amplitude estimation usually needs deeper controlled circuits than near-term hardware can run reliably. The cleanest version is a fault-tolerant algorithm, not a shallow demonstration circuit.

Once a suitable coherent encoding exists, QAE changes the query scaling of expectation estimation. Practical value depends on building that encoding and its controlled operations cheaply enough for the scaling improvement to survive end to end.

## Follow the convergence

The [companion notebook](https://github.com/johnazariah/quantum/blob/main/bottleneck/notebooks/05-finance.ipynb) lets you compare Black-Scholes, Monte Carlo convergence, and a compiled three-bit amplitude-estimation proxy. For the phase-estimation circuit pattern underneath the proxy, see [Circuit Bench 10 — Quantum Phase Estimation](../../circuit-bench/10-quantum-phase-estimation/README.md).

[^qae]: Brassard et al., ["Quantum Amplitude Amplification and Estimation"](https://doi.org/10.1090/conm/305/05215), *Contemporary Mathematics*, 2002. The quadratic improvement counts calls to the state-preparation and amplification oracles; it is not an end-to-end runtime guarantee.

---

*This is Unit 5 of The Quantum Bottleneck series. Next up: [The Scheduling Nightmare](bottleneck-06-supply-chains.md) — when optimisation means finding a good discrete assignment under competing constraints.*
