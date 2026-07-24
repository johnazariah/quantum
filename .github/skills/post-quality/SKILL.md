---
name: post-quality
description: Use before publishing or finalising the BODY of any long-form blog post (or opening a PR that adds/edits one). A reference-grade correctness gate that catches the defects that make a post wrong or confusing for a stranger who lands on it cold, years later, from a search engine or a mid-series social link. Complements authorial-voice (register) and social-hook (the disposable promo layer).
---

# Reference-grade post quality gate

**Philosophy (the author's, and the reason this skill exists).** A blog post is *reference material*. It gets bookmarked, linked, cited, and re-read for years, long after the social hook that announced it has scrolled into oblivion. The hook is a cache — disposable, and we have tooling to backfill and repost it. The post is the source of truth. A buried definition, an overloaded symbol, or a blurred concept is a bug that compounds every time someone new arrives. So it is worth the one-time cost to get a post *right* before it becomes permanent.

**The bar.** A post passes when a competent stranger who arrives **cold** — mid-series, from a search result or a shared link, with none of the earlier posts in their head — is never confused and never misled. If an expert like a careful reviewer would raise an eyebrow, fix it before publishing, not after.

Run every check below against the post body before it ships. Each check lists the failure, why it matters, how to find it, and a real example from this blog.

---

## Check 1 — No use-before-definition

**Rule.** Every term, acronym, and symbol is introduced at or before its first use. The reader never meets a name they have not been given.

**Why.** Reference readers do not read top-to-bottom with faith that it will be explained later; they stop at the first unexplained token.

**How to find it.** For each acronym, grep its first occurrence and confirm the expansion is at or before that line. For symbols, confirm the definition precedes the first appearance in prose (displays that *introduce* a symbol are fine; displays that *use* an undefined one are not).

**Real examples.**
- Part 2 used "VQE" and "QPE" two posts before Part 4 expanded them, and "SVD" was never expanded at all. Fix: gloss on first use — `VQE (the variational quantum eigensolver)`, `SVD (singular value decomposition)`.
- Part 3 named the Pauli matrices *after* the display that already used $X, Y, Z$. Fix: name them as they are introduced.

---

## Check 2 — No overloaded or colliding notation

**Rule.** One symbol, one meaning, across the whole series. If two concepts genuinely need the same glyph, disambiguate one of them.

**Why.** A symbol that means two things is a silent trap: the reader substitutes the wrong meaning and the maths stops making sense, with no visible error to warn them.

**How to find it.** Grep every notation-bearing token across all parts (`\ket`, `|...⟩`, subscripted state labels, single-letter operators) and list each distinct meaning. Any glyph with two meanings is a defect.

**Real example.** `|0⟩` meant both the *ground state* (lowest eigenvector) and the *site-0 computational state* $(1,0)^T$ across the series. The fix was a series-wide decision: energy-ordered eigenstates became `|E₀⟩, |E₁⟩, …`; bare `|0⟩, |1⟩` were reserved strictly for the computational/site basis. Note the trap inside the trap: the obvious `|ψ₀⟩` for the ground state was *already taken* by Part 1's `|ψ(t)⟩ = e^{-iHt}|ψ₀⟩` (the initial state). Always check that your disambiguating symbol is itself free.

---

## Check 3 — Domain precision (say exactly what you mean)

**Rule.** Do not blur two adjacent-but-distinct concepts by using one word for both, especially across a domain boundary.

**Why.** Experts read the precise word. Blurring reads as a category error even when the author understands the distinction perfectly.

**How to find it.** For each load-bearing noun, ask: am I using this in more than one sense? Is there a more precise word for each sense?

**Real examples.**
- "Qubit" was used for both an abstract two-level system (a quantum-mechanics notion) and a physical computing element (a quantum-computing notion). Fix: reserve "qubit" for the physical realisation; use "spin", "site", or "two-level system" for the abstract object; introduce the physical qubit at its true first use.
- Earlier feedback on Part 1 flagged "rotation" used where "unitary" was meant. Same class: name the exact object.

---

## Check 4 — Self-containment

**Rule.** Each post defines its own acronyms and symbols on first use, even if an earlier post in the series already did. Do not rely on the reader having read the previous part.

**Why.** Posts are published on different dates and syndicated individually; a large fraction of readers land mid-series from search or a social link. A forward- or backward-reference for context is welcome; a *dependency* for basic vocabulary is a defect.

**How to find it.** For each acronym/symbol first used in this post, confirm it is either defined here or accompanied by an explicit, linked pointer to where it is defined (`… VQE (see Part 3) …`), not silently assumed.

**Real example.** Part 8 of the Bottleneck series used "VQE" without expanding it, relying on Part 3. Fix: expand on first use in every post, optionally with a link back.

---

## Check 5 — Cross-part consistency

**Rule.** Titles, symbols, terminology, and spelling agree across every part of a series and with any overview/index that lists it.

**Why.** Drift between an overview table and the actual post titles, or between two parts' notation, erodes trust and breaks the reference.

**How to find it.** Diff the series overview/index titles against the actual `# H1` titles. Grep shared symbols across parts to confirm they match. Confirm British spelling throughout (optimisation, colour, behaviour, generalise) and confirm the "next up" teasers name the real next title.

**Real example.** The Bottleneck overview table listed "The Unsimulable Material" and "The Better Catalyst" while the posts were titled "The Materials Maze" and "The Catalyst Bottleneck"; and Part 1 expanded QAOA as American "Optimization" while Part 6 used British "Optimisation". Both fixed.

---

## Check 6 — Real code, real outputs (never fabricate)

**Rule.** Every code block that shows an output, and every quantitative claim drawn from code, must be the genuine result of actually executing that code. Run it, paste exactly what it prints. Never hand-write plausible-looking numbers, sample outputs, or "you'll get something like…" results. If a snippet is illustrative and not meant to be run, show the code only — do not attach a fabricated output block.

**Why.** This is the single fastest way to destroy a technical blog's credibility. A reference reader will copy the code and run it. If the printed autocorrelation, the transition table, or the timing number does not match, every other claim in the post is now suspect. Worse, fabricated outputs are usually invented to fit the narrative the author *wants* — so they quietly encode and "confirm" claims that the real data contradicts. A wrong number is a bug; a wrong number that props up a false thesis is a trap.

**How to find it.** For each code block with a shown result: actually run the code (same seed, same inputs) and diff its output against what the post prints — character for character for text, and to the stated precision for numbers. Confirm the output block would even *appear* (e.g. a dict/Counter with no key for a case does not print a line for it). Then sanity-check the result against theory: does the number match a hand calculation or a known closed form? If code output and narrative disagree, fix whichever is wrong — do not paper over it.

**Real example (the one that created this rule).** A Hidden Structure draft printed autocorrelation values for the Golden Mean process — lag 1 = −0.3340, lag 2 ≈ 0 ("the signal has essentially vanished") — and built its thesis on "autocorrelation is blind to this sequence." Running the actual code gave lag 1 = −0.4917 (≈ the theoretical −0.5) and lag 2 = **+0.2492**: a pronounced decaying oscillation. The outputs were fabricated, and the fabrication concealed that the claim was false — the Golden Mean is first-order Markov, so autocorrelation and bigrams both *do* see its structure. The example itself had to be reframed. None of this survives a reader who runs the code; all of it is caught the moment the author does.

---

## Mechanical pass (fast, run these)

```bash
# 1. Acronym first-use audit (adjust the list per post)
for ac in VQE QPE QAE QUBO QFT SVD SWAP; do
  echo "== $ac =="; grep -n "$ac" <post>.md | head -3; done

# 2. Symbol-collision scan across the whole series
grep -n "\\\\ket" docs/blog/posts/<series>-*.md      # or:  grep -n "|.*⟩"

# 3. Spelling (British)
grep -nE "optimiz|coloriz|behavior|generaliz" docs/blog/posts/<post>.md

# 4. Title vs overview consistency
grep -h "^# " docs/blog/posts/<series>-*.md
# ...diff against the titles in the series index/overview table.
```

## The one test that subsumes them all

Read the post as if you have **never seen the series** and arrived from a search result. The first time you hit a word, symbol, or claim you cannot resolve from what came before it *in this post*, you have found a defect. Fix it, then ship.

## Relationship to the other skills

- **`authorial-voice`** governs *how it sounds* (John's register: dedications, why-before-what, first-person delight). This skill governs *whether it is correct and clear*. A post must pass both.
- **`social-hook`** governs the *disposable* promo layer, with deliberately plainer constraints. Do not apply its bans (no em-dashes, no exclamation) to the post body, and do not apply this reference-grade bar to a 300-character blurb.
