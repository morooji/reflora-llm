"""reflora_llm — turn a recorded memory into 5 retellings + shared key points (Claude).

The public API the backend imports in-process:

    from reflora_llm import rewrite, summarize, verify, capture_usage, RewriteInput, RewriteOutput, Version, Flag, TONES

Importing this package constructs no client and needs no ANTHROPIC_API_KEY — get_client()
is called lazily inside summarize()/rewrite()/verify(). See reflora_llm/rewrite.py for the contract.
"""

from __future__ import annotations

from .rewrite import (
    TONES,
    RewriteInput,
    RewriteOutput,
    Version,
    rewrite,
    summarize,
)
from .usage import UsageRecord, capture_usage
from .verify import Flag, verify

__all__ = [
    "TONES",
    "Flag",
    "RewriteInput",
    "RewriteOutput",
    "UsageRecord",
    "Version",
    "capture_usage",
    "rewrite",
    "summarize",
    "verify",
]
