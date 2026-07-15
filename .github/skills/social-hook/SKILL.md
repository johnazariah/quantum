---
name: social-hook
description: Use when creating social-media promotion for a blog post or article. Produces two outputs, a longer LinkedIn-style post and a 300-character Bluesky blurb, both non-clickbait and matter-of-fact, with no em-dashes, no emoji, and no choppy short sentences.
---

# Social promotion for LinkedIn and Bluesky

Use this skill to turn a published post into two ready-to-paste artifacts: a longer LinkedIn-style post, and a 300-character blurb for Bluesky. Both are deliberately plain: they state what the piece is and what the reader will get, and they do not tease. The two share one voice; they differ only in length and shape.

## Inputs

- The target post (a file path, a URL, or the text). Read it first and find the single most interesting true statement it makes. That statement is the hook. Do not invent a curiosity gap; the honest, specific idea is more compelling than a tease.

## Shared constraints (both outputs)

Every one of these is required. An output that violates any of them is not done.

1. **No em-dashes.** Use commas, semicolons, or colons, or restructure the sentence. En-dashes are allowed only for numeric ranges.
2. **No emoji** and no decorative symbols.
3. **No short, choppy sentences.** Write complete, measured sentences. Do not use one-word sentences, sentence fragments, or a staccato rhythm.
4. **Not click-baity.** No curiosity-gap phrasing, no "you won't believe", no false urgency, no superlatives, no hype. Name the topic and the concrete angle or payoff plainly.
5. **Matter-of-fact register**, precise and unhurried, consistent with the author's voice.
6. **One honest idea leads.** Find the single most interesting true statement the post makes and lead with it. The specific idea is more compelling than a tease.

## The two outputs

### 1. LinkedIn post

A short, complete post, not a teaser. Structure it as a few single-idea paragraphs separated by blank lines:

- **Opening (carries the fold).** LinkedIn truncates at roughly 200 characters behind a "see more" link, so the first sentence or two must name the topic and the concrete angle on their own.
- **Body.** One to three short paragraphs that develop the specific idea and say what the reader will get. Naming the running example or the concrete payoff is good; padding is not.
- **Close.** A plain pointer to the piece. Put the link on its own line at the end, or note that it goes in the first comment, since LinkedIn tends to favour posts that keep the outbound link out of the body.

Length: aim for roughly 600 to 1300 characters of prose. The hard platform ceiling is 3000; do not approach it. Keep it tight enough to read in one pass.

### 2. Bluesky blurb

The 300-character version, a single measured blurb that distils the LinkedIn opening to its sharpest true statement.

- **300 characters maximum**, counting everything, including the link if it is inline. Bluesky enforces 300 characters including the URL, so treat 300 as a hard ceiling.
- Prefer to keep the URL out of the counted text: attach it as a link card in the composer rather than pasting the raw URL. If the URL must be inline, count it toward the 300.
- One or two complete sentences.

## Where the link goes

A full blog URL can be roughly 100 characters. On **LinkedIn**, paste the link on its own line at the end, or put it in the first comment; the 300-character limit does not apply, and the platform renders a preview card. On **Bluesky**, attach the link as a card in the composer so the URL does not consume the 300-character budget; if it must be inline, count it toward the 300.

## Hashtags

Optional and minimal. Use at most two, and only if they read as descriptive topic labels rather than promotion. If they push the total over 300 or read as spam, leave them out.

## Process

1. Read the post and extract the single specific, true idea worth leading with.
2. Draft the **LinkedIn post**: open with that idea in the first two sentences, develop it in one to three short paragraphs, and close with a plain pointer to the piece.
3. Distil the same idea into the **Bluesky blurb** of one or two complete sentences. Count its characters, including the URL if inline, and trim until the total is at most 300.
4. Run the checklist below against both outputs and fix anything that fails.
5. Return both outputs, the Bluesky blurb's exact character count, and a note on where the link goes for each platform.

## Self-check before returning

Both outputs:

- Contain no em-dash and no emoji.
- Sentences are complete and measured, with no fragments and no staccato.
- Read as a plain description, not a tease or a boast.
- The claim is accurate to the post and specific, not vague.

LinkedIn post:

- The first two sentences name the topic and angle on their own, before the fold.
- The body is a few single-idea paragraphs, tight enough to read in one pass.

Bluesky blurb:

- Character count is at most 300, including any inline URL.

## Worked example

For a post that derives, from first principles, why quantum time evolution is a rotation:

**LinkedIn post:**

> Raising e to a matrix looks like a notation trick, but it is the step that makes quantum time evolution computable, and the result is a rotation rather than a stretch.
>
> The post starts from the scalar exponential, builds the spectral theorem, and arrives at the propagator that advances a quantum state in time. A single two-by-two Hermitian matrix carries the whole argument, and every step can be checked by hand.
>
> The reward is a clean geometric picture. A Hermitian operator stretches space along its eigenvectors; the same operator inside an exponential with an imaginary exponent rotates instead, which is exactly why total probability is conserved.
>
> Full post: https://johnazariah.github.io/quantum-workbooks/blog/2026/07/14/how-to-raise-e-to-a-matrix-and-why-youd-want-to/

That post leads with the idea before the fold, develops it in three measured paragraphs, has no em-dash or emoji, and does not tease.

**Bluesky blurb (231 characters):**

> A first-principles account of what it means to raise e to a matrix, and why quantum time evolution turns out to be a rotation rather than a stretch. One two-by-two example, checkable by hand, carries the whole argument.

That blurb is 231 characters, uses two complete sentences, and describes the piece without teasing. The link is attached as a Bluesky link card, not counted.
