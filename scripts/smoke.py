"""Smoke test: run summarize() + rewrite() against the REAL Claude API.

Needs reflora_llm installed (`pip install .`) and ANTHROPIC_API_KEY set:

    python scripts/smoke.py

Prints the generated key points, the 5 retellings, and their fact-check flags for the first sample memory.
"""

from __future__ import annotations

import os

from reflora_llm import rewrite, summarize, verify
from reflora_llm.evals.samples import SAMPLES


def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY to run the smoke test.")
        return 1

    sample = SAMPLES[0]
    print(f"# {sample.title}\n")

    print("## summarize() — key points")
    for p in summarize(sample.transcript, sample.answers):
        print(f"  - {p}")

    print("\n## rewrite() — 5 retellings + shared key points")
    out = rewrite(sample)
    print(f"\nkey points ({len(out.key_points)}):")
    for p in out.key_points:
        print(f"  - {p}")
    for v in out.versions:
        print(f"\n--- {v.tone} ---")
        print(v.transcript)

    print("\n## verify() — KD-35 fact-check flags on the 5 retellings")
    flags = verify(sample.transcript, sample.answers, out.key_points, [v.transcript for v in out.versions])
    for v, fl in zip(out.versions, flags):
        print(f"  {v.tone}: {len(fl)} flag(s)" + "".join(f"\n     - \"{f.text}\" — {f.note}" for f in fl))

    print(f"\nOK: {len(out.versions)} versions, tones = {[v.tone for v in out.versions]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
