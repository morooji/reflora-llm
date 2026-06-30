"""Smoke test: run summarize() + rewrite() against the REAL Claude API.

Requires ANTHROPIC_API_KEY. From the repo root:

    python scripts/smoke.py

Prints the generated key points and the 5 retellings for the first sample memory.
"""

from __future__ import annotations

import os
import sys

# Allow `python scripts/smoke.py` from the repo root (no install needed).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.evals.samples import SAMPLES  # noqa: E402
from app.rewrite import rewrite, summarize  # noqa: E402


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

    print(f"\nOK: {len(out.versions)} versions, tones = {[v.tone for v in out.versions]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
