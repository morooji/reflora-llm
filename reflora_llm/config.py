"""Model/tier choice + client construction for the Reflora LLM rewrite.

Model IDs and effort were chosen against the LIVE claude-api reference (not from memory):
- summarize -> claude-sonnet-4-6 @ effort "medium": cheap, factual key-points extraction (KD-5).
- rewrite   -> claude-opus-4-8  @ effort "high":   the creative 5-version retelling (KD-22).

Both calls use adaptive thinking. Do NOT pass temperature / top_p / top_k / budget_tokens —
all four are removed on Opus 4.8 and return 400 (the same surface applies to Sonnet 4.6 here).
max_tokens are kept under the SDK's non-streaming guard (it trips above ~21K for these models),
so the rewrite (16K) and summary (4K) run non-streaming; raise + switch to streaming if needed.
"""

from __future__ import annotations

import anthropic

# --- Summary call (the editable Review-Story key points, KD-5) ---
SUMMARIZE_MODEL = "claude-sonnet-4-6"
SUMMARIZE_EFFORT = "medium"
SUMMARIZE_MAX_TOKENS = 4000

# --- Rewrite call (the 5 retellings, KD-22) ---
REWRITE_MODEL = "claude-opus-4-8"
REWRITE_EFFORT = "high"
REWRITE_MAX_TOKENS = 16000  # non-streaming-safe; stream if raised much higher

# Adaptive thinking on both calls (no fixed budget_tokens — removed on Opus 4.8).
THINKING = {"type": "adaptive"}


def get_client() -> anthropic.Anthropic:
    """Default Anthropic client — reads ANTHROPIC_API_KEY from the environment."""
    return anthropic.Anthropic()
