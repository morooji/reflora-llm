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



# KD-35 fact-check flags (owner 2026-09-27): the live eval for verify(). Sources = SAMPLES[0]
# ("The day we brought Jack home"); one retelling plants invented facts, one is clean.
# Used by the skip-guarded live tests in tests/test_verify.py.
VERIFY_SOURCE = SAMPLES[0]
VERIFY_KEY_POINTS = [
    "Brought Jack home from the hospital on a freezing February morning",
    "Grandma knitted a tiny yellow blanket; only his face showed",
    "The car heater barely worked; Dad drove about ten miles an hour",
    "Dad's hands shook buckling the car seat",
    "The dog kept sniffing the car seat",
    "They sat on the sofa staring at him for what felt like hours",
    "The blanket is still in the chest upstairs",
]
# Invented: the date "the fourteenth of February", "Aunt Rose", "at Saint Mary's", "eleven pounds".
VERIFY_PLANTED = (
    "It was the fourteenth of February, a freezing morning, when we brought Jack home from "
    "Saint Mary's. Aunt Rose had driven over to see him, and he weighed eleven pounds. Grandma's "
    "tiny yellow blanket was wrapped around him so only his face showed. Your dad crawled along "
    "at ten miles an hour, hands shaking, while the dog sniffed the car seat and we sat on the "
    "sofa just staring at him."
)
VERIFY_PLANTED_FACTS = ["fourteenth of February", "Saint Mary's", "Aunt Rose", "eleven pounds"]
# Clean: paraphrase + mood only — must return [].
VERIFY_CLEAN = (
    "Oh, that freezing February morning! We brought Jack home from the hospital bundled in the "
    "tiny yellow blanket Grandma had knitted, just his little face peeking out. The heater in the "
    "car was useless, so your dad crept along at ten miles an hour, terrified of every bump, his "
    "hands trembling as he buckled the seat. The dog could not stop sniffing that car seat. And "
    "then we simply sat on the sofa and stared at him, for what felt like hours."
)
