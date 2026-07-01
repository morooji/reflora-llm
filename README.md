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
Out: 5 versions (warm / short / playful / reflective / poetic) + key points. See `reflora_llm/rewrite.py`.

Consumed **as a library** (installed with `pip install .`, imported in-process by the backend):
`from reflora_llm import rewrite, summarize, RewriteInput, RewriteOutput, Version, TONES`.

## Structure
```
reflora_llm/rewrite.py   core contract + public API   reflora_llm/prompts/  templates
reflora_llm/config.py    model tiers + get_client()   reflora_llm/evals/    samples
scripts/smoke.py  tests/  pyproject.toml
```

## Status
**Rewrite implemented** (branch `llm-rewrite`). `summarize()` + `rewrite()` call Claude via the
official SDK (`messages.parse`, structured output): **Sonnet 4.6** @ medium for the key points,
**Opus 4.8** @ high for the 5 retellings (tiers verified against the live reference, not memory).
Offline unit tests + a skip-guarded real smoke (`scripts/smoke.py`, needs `ANTHROPIC_API_KEY`).
Wiring this into the backend (library vs HTTP) and full evals are separate slices.
