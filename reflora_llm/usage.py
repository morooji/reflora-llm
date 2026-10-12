"""Token-usage capture (KD-37 per-family AI cost tracking).

The public calls return parsed dataclasses only; the token counts live on the SDK response. Rather
than change every return type, callers wrap a block:

    with capture_usage() as calls:
        out = rewrite(inp)
    for c in calls:  # one UsageRecord per Claude call made inside the block (summarize, rewrite, verify)
        print(c.kind, c.model, c.input_tokens, c.output_tokens)

Implemented with a contextvar so nested/concurrent callers never see each other's calls. Outside a
capture block recording is a no-op. Never raises: a missing/odd `usage` object records zeros.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass


@dataclass
class UsageRecord:
    kind: str  # "summarize" | "rewrite" | "verify"
    model: str
    input_tokens: int
    output_tokens: int
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0


_sink: ContextVar[list[UsageRecord] | None] = ContextVar("reflora_llm_usage_sink", default=None)


@contextmanager
def capture_usage() -> Iterator[list[UsageRecord]]:
    """Collect one UsageRecord per Claude call made inside the block."""
    records: list[UsageRecord] = []
    token = _sink.set(records)
    try:
        yield records
    finally:
        _sink.reset(token)


def _int(value) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def record_usage(kind: str, model: str, response) -> None:
    """Called by summarize()/rewrite()/verify() right after messages.parse(). No-op outside a
    capture block; tolerant of fakes that carry no `usage`."""
    sink = _sink.get()
    if sink is None:
        return
    usage = getattr(response, "usage", None)
    sink.append(
        UsageRecord(
            kind=kind,
            model=str(getattr(response, "model", None) or model),
            input_tokens=_int(getattr(usage, "input_tokens", 0)),
            output_tokens=_int(getattr(usage, "output_tokens", 0)),
            cache_read_input_tokens=_int(getattr(usage, "cache_read_input_tokens", 0)),
            cache_creation_input_tokens=_int(getattr(usage, "cache_creation_input_tokens", 0)),
        )
    )
