"""Tests for app.rewrite — offline unit tests (fake client) + a skip-guarded real smoke.

The unit tests inject a fake Anthropic client whose messages.parse(...) returns a
SimpleNamespace(parsed_output=<schema instance>), and assert both the request shape (correct model
per call, adaptive thinking, output_format set, no banned sampling params) and the parsed_output ->
dataclass mapping. The real smoke runs only when ANTHROPIC_API_KEY is set.
"""

from __future__ import annotations

import os
from types import SimpleNamespace

import pytest

from reflora_llm.rewrite import (
    KeyPoints,
    RewriteInput,
    RewriteOutput,
    RewriteResult,
    TONES,
    Version,
    VersionItem,
    rewrite,
    summarize,
)

BANNED_PARAMS = ("temperature", "top_p", "top_k", "budget_tokens")


class FakeMessages:
    """Captures every parse() request and returns a preset parsed_output."""

    def __init__(self, parsed_output):
        self._parsed_output = parsed_output
        self.calls: list[dict] = []

    def parse(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(parsed_output=self._parsed_output)


class FakeClient:
    def __init__(self, parsed_output):
        self.messages = FakeMessages(parsed_output)


def _result(tones):
    return RewriteResult(
        key_points=["Brought Jack home in February", "Grandma's yellow blanket"],
        versions=[VersionItem(tone=t, text=f"{t} retelling") for t in tones],
    )


def test_rewrite_request_shape_and_mapping():
    client = FakeClient(_result(TONES))
    inp = RewriteInput(title="t", transcript="x", key_points=["a", "b"], tones=list(TONES))

    out = rewrite(inp, client=client)

    # key points provided -> a single parse() call (no summarize)
    assert len(client.messages.calls) == 1
    kw = client.messages.calls[0]
    assert kw["model"] == "claude-opus-4-8"
    assert kw["thinking"] == {"type": "adaptive"}
    assert kw["output_config"]["effort"] == "high"
    assert kw["output_format"] is RewriteResult
    for banned in BANNED_PARAMS:
        assert banned not in kw

    # parsed_output -> dataclasses
    assert isinstance(out, RewriteOutput)
    assert out.key_points == ["Brought Jack home in February", "Grandma's yellow blanket"]
    assert all(isinstance(v, Version) for v in out.versions)
    assert [v.tone for v in out.versions] == list(TONES)
    assert [v.transcript for v in out.versions] == [f"{t} retelling" for t in TONES]
    assert len(out.versions) == len(inp.tones)


def test_rewrite_single_version_regen_passes_steering():
    client = FakeClient(_result(["playful"]))
    inp = RewriteInput(
        title="t",
        transcript="x",
        key_points=["a"],
        tones=["playful"],
        focus=["funnier", "the dog"],
        spoken_note="make it about the dog sniffing the car seat",
    )

    out = rewrite(inp, client=client)

    assert len(out.versions) == 1 == len(inp.tones)
    assert out.versions[0].tone == "playful"
    # focus hints + spoken note flow into the user turn
    user = client.messages.calls[0]["messages"][0]["content"]
    assert "funnier" in user
    assert "sniffing the car seat" in user


def test_empty_key_points_triggers_summarize():
    """No key_points -> summarize (Sonnet) runs first, then rewrite (Opus) reuses its output."""
    captured: list[dict] = []

    class TwoStepMessages:
        def parse(self, **kwargs):
            captured.append(kwargs)
            if kwargs["output_format"] is KeyPoints:
                return SimpleNamespace(parsed_output=KeyPoints(key_points=["generated point"]))
            return SimpleNamespace(parsed_output=_result(TONES))

    class TwoStepClient:
        def __init__(self):
            self.messages = TwoStepMessages()

    inp = RewriteInput(title="t", transcript="some narration", tones=list(TONES))  # no key_points
    out = rewrite(inp, client=TwoStepClient())

    assert len(captured) == 2
    # 1) summarize call
    assert captured[0]["output_format"] is KeyPoints
    assert captured[0]["model"] == "claude-sonnet-4-6"
    assert captured[0]["thinking"] == {"type": "adaptive"}
    assert captured[0]["output_config"]["effort"] == "medium"
    # 2) rewrite call, with the generated key points threaded into its user turn
    assert captured[1]["output_format"] is RewriteResult
    assert captured[1]["model"] == "claude-opus-4-8"
    assert "generated point" in captured[1]["messages"][0]["content"]
    assert len(out.versions) == 5


def test_summarize_request_shape():
    client = FakeClient(KeyPoints(key_points=["one", "two"]))

    points = summarize("narration text", ["an answer"], client=client)

    assert points == ["one", "two"]
    kw = client.messages.calls[0]
    assert kw["model"] == "claude-sonnet-4-6"
    assert kw["thinking"] == {"type": "adaptive"}
    assert kw["output_config"]["effort"] == "medium"
    assert kw["output_format"] is KeyPoints
    for banned in BANNED_PARAMS:
        assert banned not in kw
    user = kw["messages"][0]["content"]
    assert "narration text" in user
    assert "an answer" in user


@pytest.mark.skipif(not os.environ.get("ANTHROPIC_API_KEY"), reason="real API key required")
def test_real_smoke():
    from reflora_llm.evals.samples import SAMPLES

    out = rewrite(SAMPLES[0])
    assert len(out.versions) == 5
    assert [v.tone for v in out.versions] == TONES
    assert out.key_points and all(p.strip() for p in out.key_points)
    assert all(v.transcript.strip() for v in out.versions)
