"""Summarize prompt — the editable 'Review Story' key points (KD-5, KD-17).

One shared key-points list per story, distilled from the narration transcript and the voice Q&A
answers. Key points, NOT a re-told transcript: short, checkable lines the caregiver edits before
generating the retellings.
"""

from __future__ import annotations

SUMMARIZE_SYSTEM = """\
You distill a recorded family memory into its key points for a caregiver to review and edit.

You are given a narration transcript and, optionally, transcribed answers to follow-up questions.
Produce the shared key points for this memory: the handful of facts, people, places, and moments
that define it — the things every retelling must keep.

Guidelines:
- Key points, not a retelling. Each is one short, plain factual line (a person, the place, what
  happened, why it mattered). No narrative prose, no tone, no embellishment.
- Faithful to what was actually said. Never invent names, dates, or details not in the source.
- Cover the whole memory and merge duplicates across the narration and the answers.
- Aim for roughly 4-8 points, ordered as the memory unfolds.

Return only the key points.\
"""


def build_summarize_user(transcript: str, answers: list[str]) -> str:
    """The user turn: the narration transcript plus any transcribed Q&A answers."""
    parts = ["NARRATION TRANSCRIPT:", transcript.strip() or "(none)"]
    if answers:
        parts.append("")
        parts.append("VOICE Q&A ANSWERS:")
        parts.extend(f"{i}. {a.strip()}" for i, a in enumerate(answers, 1))
    return "\n".join(parts)
