# Reflora — LLM rewrite service (`reflora-llm`)

> ⚠️ **ALWAYS read the Reflora overview first, before doing anything in this repo:**
> **`../reflora-claude/docs/00-Reflora-Overview.md`** (the central hub —
> sibling folder `../reflora-claude`), then KD-22 in `docs/Key-Decisions.md`. Don't skip it.

This repo is the **LLM component** of the Reflora pipeline: it turns a recorded memory — the narration
**transcript** + the voice **Q&A answers** — into the **5 retellings** (different tone/length) plus the
shared **key-points** summary, using **Claude**. The backend (`reflora-backend`) orchestrates and calls
this; this repo owns the prompts, the rewrite logic, and the quality evals.

## Shared knowledge lives in the central hub — read it first
> **`../reflora-claude`**
> - Start at **`docs/00-Reflora-Overview.md`** (the index).
> - **`docs/Key-Decisions.md` → KD-22** — the 5-version pipeline and the tones.
> - **`docs/Backend-API-Spec.md`** — the `Version`/`VariantChange` shapes (tone / voiceId / focus),
>   key points, and where this slots into the generation job.
> - **`docs/System-Architecture.md`** — this is the `C·LLM` component; buy-heavy pipeline.

Keep design/decisions canonical **in the hub** (don't copy them here). Update the hub when they change.

## Scope (just this component)
- **In:** `title`, narration `transcript`, `answers[]`, current `key_points[]`, optional per-version
  `focus[]` hints. **Out:** 5 `Version`s (tones: warm / short / playful / reflective / poetic) +
  `key_points`. See `app/rewrite.py` for the contract.
- Single-version regen applies one tone + focus; full generation produces all 5.

## Model choice
Use **Claude**. **Do NOT hardcode a model/tier from memory** — pick it against the **live** model/
pricing reference (the `claude-api` skill) when implementing, judged by quality/cost on real samples.

## Structure
```
app/rewrite.py   the core contract (RewriteInput → RewriteOutput)
app/prompts/     prompt templates
app/evals/       quality checks on real samples
app/main.py      optional FastAPI service (or import rewrite() as a library)
```

## Status
**Scaffold only — do not build it out yet.** Initiated for structure; the next phase wires up Claude.
