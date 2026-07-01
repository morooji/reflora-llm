"""reflora_llm — turn a recorded memory into 5 retellings + shared key points (Claude).

The public API the backend imports in-process:

    from reflora_llm import rewrite, summarize, RewriteInput, RewriteOutput, Version, TONES

Importing this package constructs no client and needs no ANTHROPIC_API_KEY — get_client()
is called lazily inside summarize()/rewrite(). See reflora_llm/rewrite.py for the contract.
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

__all__ = [
    "rewrite",
    "summarize",
    "RewriteInput",
    "RewriteOutput",
    "Version",
    "TONES",
]
