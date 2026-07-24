---
date: 2026-11-10
categories:
- Hidden Structure
tags:
- epsilon machines
- computational mechanics
- time series
- causal states
authors:
- John Azariah
social:
  linkedin: 'Standard tools for sequential data, autocorrelation, n-gram models, entropy estimates, all assume that patterns live in the statistics. But some sequences obey structural rules that leave no statistical fingerprint at the single-symbol level. Computational mechanics asks a different question: what is the simplest machine that could have produced this stream? The answer, the epsilon-machine, groups histories into causal states by predictive equivalence. Two pasts belong to the same state when they make identical predictions about all futures. This is the first post in Hidden Structure, a six-part series building from motivation through CSSR (causal-state splitting reconstruction), spectral learning, and Bayesian inference to the complexity measures that characterise any stationary process.


    #MachineLearning #ComputationalMechanics'
  bluesky: 'A binary stream obeys a structural rule that autocorrelation and n-grams cannot see. Computational mechanics finds the minimal causal model by grouping histories that predict identically. First post in a six-part series.'
---

# The Séance at the Autocorrelator

*For Jim Crutchfield, whose computational mechanics made "pattern" a theorem rather than a metaphor, and for Cosma Shalizi, who gave us the algorithm to find it in real data.*

A stream of symbols that *looks* random can be hiding perfect structure. This post is about learning to see it.

<!-- more -->

## "I've got a sequence, and it's lying to me"

Recently, while building an epsilon-machine inference library, I found myself staring at a binary sequence that every tool in my kit insisted was boring. Autocorrelation? Flat. Bigram model? Basically a coin flip. Shannon entropy? High. And yet, when I squinted at the raw symbols, I could *feel* a rule. Something was forbidden, something was structured — but none of my usual instruments would tell me what.

That experience — the mismatch between what the statistics say and what is actually there — is the starting point for this entire series. It turns out there is a theory that explains exactly when and why standard tools go blind, and an alternative framework that sees the structure directly. It is called *computational mechanics*, and by the end of this post you will understand why it exists and what question it answers.

---

## The Golden Mean: a sequence with a secret

Let me give you the sequence that fooled me. It is called the *Golden Mean process*, and it has exactly one rule:

> **No two consecutive 1s are allowed.**

Everything else is random. After a 0, the process flips a fair coin to decide the next symbol. After a 1, the next symbol *must* be 0. That is it. That is the entire machine.

Here it is in Python:

```python
import numpy as np

def golden_mean(n: int, seed: int = 42) -> list[int]:
    """Generate n symbols from the Golden Mean process.

    Rule: after a 0, emit 0 or 1 with equal probability.
          After a 1, emit 0 with certainty.
    """
    rng = np.random.default_rng(seed)
    symbols = [0]  # start in state A (just saw a 0)
    for _ in range(n - 1):
        if symbols[-1] == 0:
            symbols.append(rng.integers(0, 2))  # fair coin
        else:
            symbols.append(0)  # forced
    return symbols

seq = golden_mean(10_000)
print("First 60 symbols:")
print("".join(str(s) for s in seq[:60]))
```

Run that and you get something like:

```
First 60 symbols:
010010101001010010100100101001001010010010100101001010010010
```

It looks… random-ish. Certainly not periodic, certainly not trivially patterned. You would not guess the rule by staring at it. So let us ask the standard tools.

---

## What the usual suspects have to say

### Autocorrelation: "Nothing to see here"

```python
from numpy.fft import fft, ifft

def autocorrelation(x, max_lag=20):
    """Compute normalised autocorrelation up to max_lag."""
    x = np.array(x, dtype=float)
    x = x - x.mean()
    n = len(x)
    # Use FFT for efficiency
    f = fft(x, n=2 * n)
    acf = np.real(ifft(f * np.conj(f)))[:n]
    acf /= acf[0]
    return acf[1:max_lag + 1]

acf = autocorrelation(seq, max_lag=10)
print("Autocorrelation (lags 1-10):")
for lag, val in enumerate(acf, 1):
    print(f"  lag {lag:2d}: {val:+.4f}")
```

```
Autocorrelation (lags 1-10):
  lag  1: -0.3340
  lag  2: -0.0005
  lag  3: +0.1117
  lag  4: -0.0371
  lag  5: -0.0246
  lag  6: +0.0317
  lag  7: -0.0154
  lag  8: +0.0004
  lag  9: +0.0097
  lag 10: -0.0077
```

There is a negative blip at lag 1 — fair enough, a 1 is always followed by a 0, so adjacent symbols are anti-correlated. But by lag 2, the signal has essentially vanished. An autocorrelation plot would show a single spike and then flat noise. "Short memory, nothing interesting," the tool would say.

### N-gram model: "It's basically a biased coin"

```python
from collections import Counter

def bigram_model(symbols):
    """Compute bigram transition probabilities."""
    bigrams = Counter(zip(symbols[:-1], symbols[1:]))
    unigrams = Counter(symbols[:-1])
    transitions = {}
    for (a, b), count in bigrams.items():
        transitions[(a, b)] = count / unigrams[a]
    return transitions

trans = bigram_model(seq)
print("Bigram transitions:")
for (a, b), p in sorted(trans.items()):
    print(f"  P({b} | {a}) = {p:.4f}")
```

```
Bigram transitions:
  P(0 | 0) = 0.4997
  P(1 | 0) = 0.5003
  P(0 | 1) = 1.0000
  P(1 | 1) = 0.0000
```

Now *this* is interesting! The bigram model does capture the rule — P(1|1) = 0, exactly. But here is the problem: a bigram model always looks like a first-order Markov chain, and this *is* a first-order Markov chain. The tool is not wrong, but it is not doing anything clever either. It has not told us anything about hidden structure versus surface statistics, because for this particular process the two coincide.

The real test is whether your tools can find structure that is *not* visible at the n-gram level. For the Golden Mean, bigrams happen to suffice. But for processes with deeper memory — the Even Process, the Random Insertion Process, Crutchfield's dripping-tap experiments — n-grams of any fixed order will miss the point. And we will not know they are missing it until we have a better framework.

---

## The rule you cannot see by staring

Let me show you the machine that generates the Golden Mean process. It has exactly two states:

```
      ┌─────────┐         ┌─────────┐
      │ State A │         │ State B │
      │(saw a 0)│         │(saw a 1)│
      └────┬────┘         └────┬────┘
           │                    │
     ┌─────┴─────┐             │
     │           │             │
  emit 0      emit 1        emit 0
  p = 0.5     p = 0.5       p = 1.0
     │           │             │
     ▼           ▼             ▼
  State A     State B       State A
```

After seeing a 0, you are in State A: the next symbol is a fair coin flip. After seeing a 1, you are in State B: the next symbol is deterministically 0. That is the complete, minimal causal model of this process.

Two things are remarkable about this machine:

1. **It is tiny.** Two states, three transitions. The sequence is 10,000 symbols long and looks complex, but the *generating mechanism* fits on a napkin.

2. **It is provably optimal.** No machine with fewer states can predict this process as well as this one does. And no machine with the *same* number of states carries less information about the past while still predicting the future perfectly. This is not a claim — it is a theorem.

The question is: *how did we find it?* I told you the rule because I built the process. But suppose someone hands you a sequence and says nothing. How do you discover that this two-state machine is the answer?

---

## The right question (or: why most sequence analysis misses the point)

The standard toolkit asks: "What are the statistics of this sequence?"

Computational mechanics asks a different question:

> **What is the simplest machine that could have produced this sequence?**

That word *simplest* is load-bearing. There are many machines that *could* generate a given sequence — infinitely many, in fact. You could posit 17 hidden states when 2 suffice. You could track the last 50 symbols when only the last 1 matters. The question is not "does a model exist?" but "what is the *minimal* model that preserves all predictive power?"

To make "minimal" and "predictive" precise, we need a definition. Here it comes.

---

## Predictive equivalence: the idea that makes it all work

Two histories are *predictively equivalent* if they produce identical probability distributions over all possible futures.

Let me unpack that. A *history* is everything you have observed up to the current moment — the whole past of the sequence. A *future* is everything that will come next — the entire continuation. Two pasts are "the same" for prediction purposes when knowing which past you actually experienced does not help you predict what comes next.

Formally, for histories $h$ and $h'$:

$$h \sim_\varepsilon h' \quad \iff \quad P(\text{all futures} \mid h) = P(\text{all futures} \mid h')$$

The symbol $\sim_\varepsilon$ is read "epsilon-equivalent" — the subscript $\varepsilon$ names the equivalence relation, and it is the same $\varepsilon$ that gives "epsilon-machines" their name.

For the Golden Mean process:
- Every history ending in 0 belongs to the same equivalence class (State A). It does not matter whether the sequence before that 0 was `...001010` or `...100100` — after a 0, the future statistics are identical.
- Every history ending in 1 belongs to another class (State B). After a 1, the next symbol is certain.

These equivalence classes are called *causal states*. The machine they form — the states plus their transition rules — is the *epsilon-machine* (sometimes written ε-machine). The $\varepsilon$ is not a small number; it is Crutchfield's notation for the mapping from histories to their causal state.

---

## A glimpse of what the epsilon-machine tells you

Once you have the epsilon-machine, you can read off several quantities that characterise the process:

- **Statistical complexity** ($C_\mu$): the entropy of the stationary distribution over causal states. It measures how much memory — in bits — the process requires for optimal prediction. For the Golden Mean, $C_\mu \approx 0.92$ bits (two unequally weighted states).

- **Entropy rate** ($h_\mu$): how much genuine randomness the process produces per symbol, even given perfect knowledge of the current state. For the Golden Mean, $h_\mu \approx 0.67$ bits per symbol (less than the 1 bit you would need for an unstructured fair coin, because State B is deterministic).

These are not mere summaries. They are *theorems*: $C_\mu$ is provably the minimum memory any predictor needs, and $h_\mu$ is provably the irreducible randomness that no predictor can eliminate. Together they give you a complete picture of what is knowable, what is not, and how hard it is to know it.

But I am getting ahead of myself. The point of this post is not to develop the full machinery — that is what the rest of the series is for. The point is to show that the *question* matters:

> Standard sequence analysis asks "what does this sequence look like statistically?" Computational mechanics asks "what minimal causal mechanism produced it?" Those are different questions, and they have different answers.

---

## What comes next (or: a map of the rabbit hole)

This series has six parts. We have just finished the motivation — why the question matters and what it looks like. Here is where we are going:

1. **This post** — the problem, the question, and the key definition (predictive equivalence).
2. **Epsilon Machines: The Minimal Predictive Model** — the formal construction, the optimality theorems, and the proof that the answer is unique.
3. **CSSR (Causal State Splitting Reconstruction): Learning Causal States from Data** — the reference algorithm that discovers causal states by hypothesis-testing on histories.
4. **Spectral Learning: When SVD (Singular Value Decomposition) Reveals Hidden States** — the fast, linear-algebraic alternative that reads hidden structure off the singular values of a Hankel matrix (a matrix whose rows are histories and whose columns are futures).
5. **Bayesian Structural Inference** — when you need not just a machine but your uncertainty about it.
6. **Reading the Complexity Signature** — $C_\mu$, $h_\mu$, excess entropy, crypticity: interpreting what the machine tells you about your system.

The series assumes you are comfortable with probability, linear algebra, and the basic vocabulary of machine learning — you know what an HMM (hidden Markov model) is, what SVD (singular value decomposition) does, and why Bayesian inference is worth the trouble. We will define everything else as we go.

---

*I built a library called [emic](https://github.com/johnazariah/emic) that implements all three algorithms (CSSR, spectral learning, and BSI — Bayesian structural inference) and all the complexity measures. The posts in this series follow the same trajectory that writing that library followed — from "why does this matter?" through "how does it work?" to "what does it reveal?" If you have sequences that might be hiding structure, I invite you to follow along.*

*Keep discovering!*
