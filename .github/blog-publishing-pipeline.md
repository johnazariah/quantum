# Blog publishing and social syndication pipeline: research and design brief

Handoff note for building a blog manager that queues posts, holds their adjoint
social-media hooks, gates them behind human approval, and then publishes the blog
and posts the hooks. Written 2026-07-15. Facts about third-party tools were verified
against their sites/repositories on that date; confirm before relying on them.

## Goal

When a post is written, its LinkedIn post and Bluesky blurb are written at the same
time and travel with it, so the blog publication and the social posts line up on a
schedule without manual reconciliation. A human approves the hooks before anything
goes out.

## What already exists in these repos

- **`social-hook` skill** (`.github/skills/social-hook/SKILL.md`): produces two
  outputs from a post, a longer LinkedIn-style post and a 300-character Bluesky
  blurb. Voice constraints: no em-dashes, no emoji, no choppy sentences, no
  click-bait, matter-of-fact register. This is the "write the adjoint hooks" half.
- **Weekly auto-publish cron** (`.github/workflows/deploy.yml`): `cron: '0 8 * * 2'`
  (Tuesdays 08:00 UTC). The mkdocs blog plugin has `draft_if_future_date: true`, so a
  future-dated post publishes itself the first time a build runs on or after its date.
  This is the "publish the blog on schedule" half.
- **Content schedule** (weekly Tuesdays): Linear Algebra for Fun and Profit Part 1
  (2026-07-14, live) and Part 2 (2026-07-21, written, held as a future draft), then
  The Quantum Bottleneck 01 through 08 on 2026-07-28 through 2026-09-15 (future
  drafts).
- **Main-blog landing page** (`johnazariah.github.io/_layouts/home.html`): a live
  Linear Algebra for Fun and Profit section, plus a still-commented Quantum Bottleneck
  rollout block whose URLs already point at the rescheduled dates.

The missing piece is the middle: a queue, an approval gate, and the syndication step.

## The pattern

This is POSSE (Publish on Own Site, Syndicate Elsewhere): the blog is the source of
truth, and the social posts are syndicated copies. The design below keeps the source
of truth and the approval trail in git, and delegates only the actual posting to a
scheduler.

## Options surveyed (do not build the scheduler from scratch)

### Mixpost (self-hosted, open source)
- `https://mixpost.app`, `https://github.com/inovector/mixpost`.
- Self-hosted via Docker or as a Laravel package. Supports 12 platforms, explicitly
  including LinkedIn and Bluesky.
- Has a built-in approval workflow ("ensure all content meets standards before
  publication"), per-platform post versions, and scheduling. Closest match to the
  "queue and approve" requirement out of the box. Core is open source; Pro is a
  one-time payment.

### Postiz (self-hosted, open source)
- `https://github.com/gitroomhq/postiz-app` (AGPL-3.0, ~33k stars, actively released).
- Self-hosted (NextJS/NestJS/Prisma/Postgres/Temporal/Redis, Docker). Supports
  Bluesky, Mastodon, Discord, X, LinkedIn and others.
- Exposes a public API, a NodeJS SDK, N8N/Make/Zapier integrations, and an agent CLI,
  so a CI step or an agent can push scheduled posts programmatically.

### Typefully (SaaS)
- `https://typefully.com`.
- Supports X, LinkedIn, Bluesky, Threads, Mastodon, Instagram. Not self-hosted.
- Exposes a public API (Bearer keys), an MCP server, and agent skills
  (`https://github.com/typefully/agent-skills`). Because it already holds LinkedIn
  partner access and has an agent interface, an agent can create the LinkedIn post and
  the Bluesky blurb as scheduled drafts for approval, and the LinkedIn gating problem
  below is handled by the vendor.

## The one hard constraint: LinkedIn

- Bluesky (AT Protocol) has an open API. An app password stored as a CI secret plus a
  small script or GitHub Action can post the blurb; fully hands-off is realistic.
- LinkedIn's posting API is gated behind an approved partner app and OAuth. Rolling a
  first-party LinkedIn poster is not worth it. Either use a tool that already holds
  that access (Postiz, Mixpost, Typefully, Buffer), or keep LinkedIn a one-click
  manual step where the tool prepares the exact text.

## Proposed git-native design

1. The `social-hook` skill writes its two outputs into the post front matter, for
   example `linkedin:` and `bluesky:` fields, so the hooks are committed in the same
   change as the post and never drift from it.
2. A publish step, triggered by the existing weekly cron, reads the hooks for any post
   whose date has arrived and whose `status:` is `approved`, then syndicates: Bluesky
   directly via the app-password secret, LinkedIn via the chosen tool or a prepared
   manual post.
3. The approval gate is the `status:` field (`draft` to `approved` to `published`) or,
   if a dashboard is preferred, the scheduler's own approval workflow. A human
   approval is always required before anything posts.
4. All credentials live as repository or CI secrets, never in the repo. Anything that
   posts on the author's behalf holds tokens and causes real external side effects, so
   the human gate and secret storage are non-negotiable.

## Recommendation

- For an owned queue with an approval UI: self-host Mixpost (approval workflow,
  LinkedIn and Bluesky) or Postiz (API and agent CLI).
- For agent-driven with no hosting and working LinkedIn access: Typefully via its API
  or MCP.
- Lowest-risk first increment regardless of the above: a Bluesky auto-post GitHub
  Action on the existing weekly cron, reading a `bluesky:` front-matter field, with
  LinkedIn added through a tool later.

## Open decisions for the implementer

1. Choose a direction: self-hosted OSS (Mixpost or Postiz), SaaS-with-agent
   (Typefully), or start minimal with the Bluesky Action.
2. Confirm whether LinkedIn API/posting access is available, or assume the
   semi-automated (prepare text, manual click) path for LinkedIn.
3. Decide where the queue and approval live: front-matter `status:` in git, or the
   scheduler dashboard.
4. Add `linkedin:` and `bluesky:` front-matter fields to the `social-hook` skill and
   to the post template so hooks are generated in place from now on.

## References

- Mixpost: https://mixpost.app, https://github.com/inovector/mixpost
- Postiz: https://github.com/gitroomhq/postiz-app
- Typefully API and agent skills: https://typefully.com, https://github.com/typefully/agent-skills
- Bluesky / AT Protocol developer docs: https://docs.bsky.app
- POSSE (IndieWeb): https://indieweb.org/POSSE
