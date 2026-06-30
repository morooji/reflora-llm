# reflora-llm

The **LLM rewrite** component of Reflora — Python + **Claude**. Turns a recorded memory (narration
transcript + voice Q&A answers) into the **5 retellings** (different tone/length) and the shared
**key-points** summary. The backend (`reflora-backend`) calls this; this repo owns the prompts,
rewrite logic, and evals.

> **Design & contract live in the central hub**, not here:
> `../reflora-claude/docs/` — start at `docs/00-Reflora-Overview.md`; see **KD-22** + `Backend-API-Spec.md`.
> See `CLAUDE.md` for the pointer.

## Scope
In: title, narration transcript, answers, key points, optional focus hints.
Out: 5 versions (warm / short / playful / reflective / poetic) + key points. See `app/rewrite.py`.

## Structure
```
app/rewrite.py   core contract     app/prompts/  templates
app/main.py      optional service  app/evals/    quality checks
pyproject.toml
```

## Status
**Rewrite implemented** (branch `llm-rewrite`). `summarize()` + `rewrite()` call Claude via the
official SDK (`messages.parse`, structured output): **Sonnet 4.6** @ medium for the key points,
**Opus 4.8** @ high for the 5 retellings (tiers verified against the live reference, not memory).
Offline unit tests + a skip-guarded real smoke (`scripts/smoke.py`, needs `ANTHROPIC_API_KEY`).
Wiring this into the backend (library vs HTTP) and full evals are separate slices.
