---
name: social-hook
description: Use when creating a short social-media hook for LinkedIn and Bluesky (300 characters) to promote a blog post or article. Produces a non-clickbait, matter-of-fact blurb with no em-dashes, no emoji, and no choppy short sentences.
---

# Social hook for LinkedIn and Bluesky

Use this skill to turn a published post into a single short promotional blurb that can be pasted on LinkedIn and Bluesky. The output is deliberately plain: it states what the piece is and what the reader will get, and it does not tease.

## Inputs

- The target post (a file path, a URL, or the text). Read it first and find the single most interesting true statement it makes. That statement is the hook. Do not invent a curiosity gap; the honest, specific idea is more compelling than a tease.

## Hard constraints

Every one of these is required. A hook that violates any of them is not done.

1. **300 characters maximum**, counting everything, including the link if it is inline. Bluesky enforces 300 characters including the URL, so treat 300 as a hard ceiling for both platforms.
2. **No em-dashes.** Use commas, semicolons, or colons, or restructure the sentence. En-dashes are allowed only for numeric ranges.
3. **No emoji** and no decorative symbols.
4. **No short, choppy sentences.** Write complete, measured sentences. Do not use one-word sentences, sentence fragments, or a staccato rhythm.
5. **Not click-baity.** No curiosity-gap phrasing, no "you won't believe", no false urgency, no superlatives, no hype. Name the topic and the concrete angle or payoff plainly.
6. **Matter-of-fact register**, precise and unhurried, consistent with the author's voice.

## Character budget

A full blog URL can be roughly 100 characters. If the link is inline, keep the prose near 180 to 200 characters so the total stays under 300. Prefer to keep the URL out of the character-counted text where the platform allows it:

- **LinkedIn:** paste the link on its own; LinkedIn renders a preview card, so the 300 applies to the prose.
- **Bluesky:** attach the link as a card in the composer rather than pasting the raw URL, so the URL does not consume the budget; if the URL must be inline, count it toward the 300.

## Hashtags

Optional and minimal. Use at most two, and only if they read as descriptive topic labels rather than promotion. If they push the total over 300 or read as spam, leave them out.

## Process

1. Read the post and extract the single specific, true idea worth leading with.
2. Draft a blurb that names the topic and the concrete angle, in one or two complete sentences.
3. Count the characters of the final string, including the URL if inline. Trim until the total is at most 300.
4. Run the checklist below and fix anything that fails.
5. Return the hook, its exact character count, and a note on where the link goes for each platform.

## Self-check before returning

- Character count is at most 300, including any inline URL.
- Contains no em-dash and no emoji.
- Sentences are complete and measured, with no fragments and no staccato.
- Reads as a plain description, not a tease or a boast.
- The claim is accurate to the post and specific, not vague.

## Worked example

For a post that derives, from first principles, why quantum time evolution is a rotation:

> A first-principles account of what it means to raise e to a matrix, and why quantum time evolution turns out to be a rotation rather than a stretch. One two-by-two example, checkable by hand, carries the whole argument.

That blurb is 231 characters, has no em-dash or emoji, uses two complete sentences, and describes the piece without teasing. The link is added by the platform's preview or link card.
