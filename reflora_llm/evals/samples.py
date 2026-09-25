"""Sample inputs for evals + the smoke script — realistic recorded-memory shapes.

Each is a RewriteInput with no key_points (so rewrite() generates them), the way a fresh story
arrives from the backend after STT.
"""

from __future__ import annotations

from ..rewrite import RewriteInput

SAMPLES: list[RewriteInput] = [
    RewriteInput(
        title="The day we brought Jack home",
        transcript=(
            "It was a freezing morning in February when we brought Jack home from the hospital. "
            "Grandma had knitted this tiny yellow blanket and we wrapped him up so only his face "
            "showed. The car heater barely worked, so your dad drove about ten miles an hour the "
            "whole way, terrified of every bump. When we got in, the dog wouldn't stop sniffing the "
            "car seat. We just sat on the sofa staring at him for what felt like hours."
        ),
        answers=[
            "I remember your dad's hands were shaking when he buckled the car seat.",
            "The blanket is still in the chest upstairs — that buttery yellow colour.",
        ],
    ),
    RewriteInput(
        title="Nonna's Sunday sauce",
        transcript=(
            "Every Sunday Nonna started the sauce before church. The whole house smelled of garlic "
            "and basil by ten in the morning. She never wrote anything down — a handful of this, a "
            "pinch of that. If you tried to help she'd swat you with the wooden spoon, but she always "
            "let me stir it once, right at the end, for luck."
        ),
        answers=[
            "She kept that spoon for forty years; it was worn flat on one side.",
        ],
    ),
]

# KD-32 guardrails (owner 2026-09-24): spoken self-corrections are EDITS — only the corrected
# fact may reach a key point. Used by the skip-guarded live tests in tests/test_guardrails.py.
CORRECTION_SAMPLES: list[RewriteInput] = [
    RewriteInput(
        title="The beach trip",
        transcript=(
            "That summer we drove all the way to California, sorry, I meant Carolina — North "
            "Carolina, the Outer Banks. Your grandmother packed the same cooler she used every "
            "year and we ate cold chicken on the sand while the kids chased the waves."
        ),
    ),
    RewriteInput(
        title="How we met",
        transcript=(
            "She was born in — no wait, we met in 1962, at the dance hall on Front Street. I "
            "stepped on her foot twice before she agreed to a second song, and we were married "
            "the following spring."
        ),
    ),
]

# KD-32 guardrails (owner 2026-09-24): spoken self-corrections are EDITS — only the corrected
# fact may reach a key point. Used by the skip-guarded live tests in tests/test_guardrails.py.
CORRECTION_SAMPLES: list[RewriteInput] = [
    RewriteInput(
        title="The beach trip",
        transcript=(
            "That summer we drove all the way to California, sorry, I meant Carolina — North "
            "Carolina, the Outer Banks. Your grandmother packed the same cooler she used every "
            "year and we ate cold chicken on the sand while the kids chased the waves."
        ),
    ),
    RewriteInput(
        title="How we met",
        transcript=(
            "She was born in — no wait, we met in 1962, at the dance hall on Front Street. I "
            "stepped on her foot twice before she agreed to a second song, and we were married "
            "the following spring."
        ),
    ),
]

