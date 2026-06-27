"""Reflora LLM rewrite — turn a recorded memory into 5 retellings + key points.

Input: the narration transcript + voice Q&A answers (+ the story's key points and optional
per-version steering — tone / focus). Output: 5 versions (different tone/length) and the
shared key-points summary. Uses Claude.

This is the `llm` component of the Reflora pipeline; the backend (reflora-backend) orchestrates
and calls this. Contract/decisions live in the hub: reflora-claude/docs/ (KD-22, Backend-API-Spec).
NOTE: do NOT hardcode a Claude model/tier from memory — choose it against the live reference.
"""

from dataclasses import dataclass

# The 5 tone presets (mirror VARIANT_TONES in the UI / Backend-API-Spec).
TONES = ["warm", "short", "playful", "reflective", "poetic"]


@dataclass
class RewriteInput:
    title: str
    transcript: str                 # STT of the narration
    answers: list[str]              # STT of the voice Q&A answers
    key_points: list[str]           # the story's shared key points (empty -> generate)
    focus: list[str] | None = None  # optional steering hints (single-version regen)


@dataclass
class Version:
    tone: str
    transcript: str                 # the rewritten narration for this version


@dataclass
class RewriteOutput:
    key_points: list[str]
    versions: list[Version]         # len == 5 (one per tone)


def rewrite(inp: RewriteInput) -> RewriteOutput:
    """Produce 5 retellings + key points. TODO: implement with Claude (tier TBD via live reference)."""
    raise NotImplementedError("Wire up the Claude call here — see reflora-claude/docs.")
