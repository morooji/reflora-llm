"""KD-37: capture_usage() collects one record per Claude call, scoped to the block."""

from __future__ import annotations

from types import SimpleNamespace

from reflora_llm import TONES, RewriteInput, capture_usage, rewrite, summarize, verify
from reflora_llm.rewrite import KeyPoints, RewriteResult, VersionItem
from reflora_llm.verify import VerifyResult, VersionFlags


class Client:
    """Fake whose parse() answers by output_format and carries a usage object."""

    def __init__(self):
        self.messages = self

    def parse(self, **kw):
        fmt = kw["output_format"]
        if fmt is KeyPoints:
            out, model, i, o = KeyPoints(key_points=["k"]), "claude-sonnet-4-6", 100, 20
        elif fmt is RewriteResult:
            out = RewriteResult(
                key_points=["k"], versions=[VersionItem(tone=t, text=f"{t} x") for t in TONES]
            )
            model, i, o = "claude-opus-4-8", 1000, 800
        else:
            out, model, i, o = (
                VerifyResult(versions=[VersionFlags(flags=[])] * 5),
                "claude-sonnet-5",
                700,
                60,
            )
        return SimpleNamespace(
            parsed_output=out,
            model=model,
            usage=SimpleNamespace(
                input_tokens=i,
                output_tokens=o,
                cache_read_input_tokens=0,
                cache_creation_input_tokens=5,
            ),
        )


def test_capture_collects_every_call_in_order():
    client = Client()
    with capture_usage() as calls:
        out = rewrite(RewriteInput(title="t", transcript="x", tones=list(TONES)), client=client)
        verify("x", [], out.key_points, [v.transcript for v in out.versions], client=client)
    assert [(c.kind, c.model, c.input_tokens, c.output_tokens) for c in calls] == [
        ("summarize", "claude-sonnet-4-6", 100, 20),
        ("rewrite", "claude-opus-4-8", 1000, 800),
        ("verify", "claude-sonnet-5", 700, 60),
    ]
    assert calls[0].cache_creation_input_tokens == 5


def test_outside_a_block_nothing_is_recorded_and_blocks_are_isolated():
    client = Client()
    summarize("x", client=client)  # no sink → no error
    with capture_usage() as outer:
        summarize("x", client=client)
        with capture_usage() as inner:
            summarize("x", client=client)
        summarize("x", client=client)
    assert len(inner) == 1 and len(outer) == 2


def test_fake_without_usage_records_zeros():
    class Bare:
        def __init__(self):
            self.messages = self

        def parse(self, **kw):
            return SimpleNamespace(parsed_output=KeyPoints(key_points=["k"]))

    with capture_usage() as calls:
        summarize("x", client=Bare())
    assert calls[0].input_tokens == 0 and calls[0].model == "claude-sonnet-4-6"
