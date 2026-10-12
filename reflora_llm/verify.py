"""KD-35 fact-check flags — the separate verification pass after the rewrite.

    verify(transcript, answers, key_points, versions) -> list[list[Flag]]

One list per retelling, in the order given. A Flag is a phrase quoted VERBATIM from that retelling
that states a concrete fact absent from the sources, plus a one-line note. An empty list = clean.

Structured output via messages.parse (like rewrite()). After parsing, every flag is checked in code:
a flag whose text is not an exact substring of its retelling is dropped (the app highlights the
phrase inside the retelling, so verbatim is a hard guarantee, not a hope). The model's own count of
retellings is also enforced — a short/long answer is padded/truncated to len(versions).
"""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel

from .config import THINKING, VERIFY_EFFORT, VERIFY_MAX_TOKENS, VERIFY_MODEL, get_client
from .prompts.verify import VERIFY_SYSTEM, build_verify_user
from .usage import record_usage

MAX_FLAG_WORDS = 20  # the prompt asks for ~12; anything far longer is a paraphrase, not a quote


@dataclass
class Flag:
    text: str  # verbatim excerpt of the retelling
    note: str  # one short line, e.g. "not in the recording"


# --- Structured-output schema (drives messages.parse(output_format=...)) ---
class FlagItem(BaseModel):
    text: str
    note: str


class VersionFlags(BaseModel):
    flags: list[FlagItem]


class VerifyResult(BaseModel):
    versions: list[VersionFlags]


def _keep(flag: FlagItem, retelling: str) -> Flag | None:
    """Verbatim guard: keep only non-empty excerpts that occur exactly in the retelling."""
    text = flag.text.strip()
    if not text or text not in retelling or len(text.split()) > MAX_FLAG_WORDS:
        return None
    return Flag(text=text, note=flag.note.strip() or "not in the recording")


def verify(
    transcript: str,
    answers: list[str] | None,
    key_points: list[str] | None,
    versions: list[str],
    *,
    client=None,
) -> list[list[Flag]]:
    """Flag the phrases in each retelling that state a fact absent from the sources (KD-35).

    `versions` are the retelling TEXTS in version order; the result is aligned to them.
    """
    if not versions:
        return []
    client = client or get_client()
    resp = client.messages.parse(
        model=VERIFY_MODEL,
        max_tokens=VERIFY_MAX_TOKENS,
        thinking=THINKING,
        output_config={"effort": VERIFY_EFFORT},
        output_format=VerifyResult,
        system=VERIFY_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": build_verify_user(
                    transcript, list(answers or []), list(key_points or []), list(versions)
                ),
            }
        ],
    )
    record_usage("verify", VERIFY_MODEL, resp)
    parsed = list(resp.parsed_output.versions)[: len(versions)]
    parsed += [VersionFlags(flags=[])] * (len(versions) - len(parsed))  # pad a short answer

    out: list[list[Flag]] = []
    for entry, retelling in zip(parsed, versions):
        kept = [f for f in (_keep(item, retelling) for item in entry.flags) if f is not None]
        # de-duplicate identical excerpts (keep first note)
        seen: set[str] = set()
        out.append([f for f in kept if not (f.text in seen or seen.add(f.text))])
    return out
