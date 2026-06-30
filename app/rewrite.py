"""Reflora LLM rewrite — turn a recorded memory into 5 retellings + the shared key points.

Two callables (the backend's drop-in seam):
- summarize(transcript, answers) -> key points        the editable Review-Story summary (KD-5)
- rewrite(RewriteInput) -> RewriteOutput              the 5 retellings (KD-22) + shared key points (KD-17)

Uses Claude via the official `anthropic` SDK. Model tiers live in app/config.py (chosen against the
live claude-api reference, not from memory). Deterministic JSON via messages.parse(output_format=...).
The backend (reflora-backend) calls this; the contract lives in the hub (reflora-claude/docs).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from pydantic import BaseModel

from .config import (
    REWRITE_EFFORT,
    REWRITE_MAX_TOKENS,
    REWRITE_MODEL,
    SUMMARIZE_EFFORT,
    SUMMARIZE_MAX_TOKENS,
    SUMMARIZE_MODEL,
    THINKING,
    get_client,
)
from .prompts.rewrite import REWRITE_SYSTEM, build_rewrite_user
from .prompts.summarize import SUMMARIZE_SYSTEM, build_summarize_user

# The 5 tone presets (mirror VARIANT_TONES in the UI / Backend-API-Spec, KD-22).
TONES = ["warm", "short", "playful", "reflective", "poetic"]


# --- I/O contract (keeps the backend seam a drop-in) ---
@dataclass
class RewriteInput:
    title: str
    transcript: str
    answers: list[str] = field(default_factory=list)
    key_points: list[str] = field(default_factory=list)            # empty -> generate
    tones: list[str] = field(default_factory=lambda: list(TONES))  # 5 for generate; [one] for regen
    focus: list[str] | None = None                                 # per-version steering (regen)
    spoken_note: str | None = None                                 # transcribed spoken note (regen)


@dataclass
class Version:
    tone: str
    transcript: str                                                # this version's rewritten narration


@dataclass
class RewriteOutput:
    key_points: list[str]
    versions: list[Version]                                        # len == len(inp.tones)


# --- Structured-output schemas (drive messages.parse(output_format=...)) ---
class KeyPoints(BaseModel):
    key_points: List[str]


class VersionItem(BaseModel):
    tone: str
    text: str


class RewriteResult(BaseModel):
    key_points: List[str]
    versions: List[VersionItem]


def summarize(transcript: str, answers: Optional[List[str]] = None, *, client=None) -> List[str]:
    """Distill the narration (+ answers) into the editable key-points summary (KD-5)."""
    client = client or get_client()
    resp = client.messages.parse(
        model=SUMMARIZE_MODEL,
        max_tokens=SUMMARIZE_MAX_TOKENS,
        thinking=THINKING,
        output_config={"effort": SUMMARIZE_EFFORT},
        output_format=KeyPoints,
        system=SUMMARIZE_SYSTEM,
        messages=[{"role": "user", "content": build_summarize_user(transcript, answers or [])}],
    )
    return list(resp.parsed_output.key_points)


def rewrite(inp: RewriteInput, *, client=None) -> RewriteOutput:
    """Produce one retelling per requested tone + the shared key points (KD-22, KD-17).

    Uses inp.key_points if provided, else generates them via summarize(); always returns key points.
    Pass one tone in inp.tones for a single-version regen, all five (default) for a full generation.
    """
    client = client or get_client()
    key_points = (
        list(inp.key_points)
        if inp.key_points
        else summarize(inp.transcript, inp.answers, client=client)
    )

    resp = client.messages.parse(
        model=REWRITE_MODEL,
        max_tokens=REWRITE_MAX_TOKENS,
        thinking=THINKING,
        output_config={"effort": REWRITE_EFFORT},
        output_format=RewriteResult,
        system=REWRITE_SYSTEM,
        messages=[{"role": "user", "content": build_rewrite_user(inp, key_points)}],
    )
    result = resp.parsed_output
    versions = [Version(tone=v.tone, transcript=v.text) for v in result.versions]
    return RewriteOutput(key_points=list(result.key_points) or key_points, versions=versions)
