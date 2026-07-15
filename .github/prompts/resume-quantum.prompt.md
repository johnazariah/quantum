---
description: "Resume work in quantum after the cookbook/bottleneck repo reorg"
name: "Resume Quantum"
argument-hint: "What should we work on next?"
agent: "agent"
model: "GPT-5 (copilot)"
---

Resume work in this repository as if you are taking over from a previous successful session.

Start by reading these files:
- [repo handoff](../copilot-instructions.md)
- [root README](../../README.md)
- [MkDocs config](../../mkdocs.yml)
- [cookbook README](../../cookbook/README.md)
- [bottleneck README](../../bottleneck/README.md)
- [deploy workflow](../workflows/deploy.yml)

Assume the following is already true unless the repository has changed since the last push:
- The GitHub repository was renamed from `johnazariah/quokka-cookbook` to `johnazariah/quantum`.
- The public repo was reorganized at commit `24aa408` into two top-level surfaces:
  - `cookbook/` for the existing Quokka recipe material
  - `bottleneck/` for runnable companions exported from *The Quantum Bottleneck*
- Root `mkdocs.yml` now uses `docs_dir: cookbook/docs`.
- The current Pages build still serves the cookbook site from the repo root.
- `bottleneck/` contains eight notebooks, a local `requirements.txt`, and `scripts/notebook_smoke_test.py`.
- These validations succeeded after the reorg:
  - `mkdocs build --strict`
  - `python bottleneck/scripts/notebook_smoke_test.py`

Working assumptions:
- `quantum-bottleneck` remains the authoritative manuscript repo; `bottleneck/` here is only the runnable export surface.
- Keep notebook code transparent and pedagogy-first.
- Preserve the cookbook site while integrating Bottleneck material incrementally.
- Do not reflatten the repo unless explicitly asked.

When resuming:
1. Confirm current git status and recent commits.
2. Re-read the files above before making assumptions.
3. Prioritize the user's new request over any default roadmap.
4. If no concrete request is supplied, propose the highest-value next step from this shortlist:
   - add an umbrella landing page that exposes both `cookbook/` and `bottleneck/`
   - decide how cookbook branding should appear inside the umbrella repo
   - tighten Pages navigation so the cookbook structure is intentionally exposed
   - formalize how future Bottleneck notebook exports should be synced from the manuscript repo

Keep the first response short: summarize the recovered state, name the next action, then start doing the work.