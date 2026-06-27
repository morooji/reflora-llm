"""Optional FastAPI wrapper so the backend can call this over HTTP.
(Or import `rewrite()` from app.rewrite as a library.) See README.
"""

from fastapi import FastAPI

app = FastAPI(title="Reflora LLM (rewrite)", version="0.0.1")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# POST /rewrite -> 5 versions + key points (mount once app/rewrite.py is implemented).
