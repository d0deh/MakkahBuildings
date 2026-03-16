"""Anthropic API client wrapper with file-based response caching."""
from __future__ import annotations
import os
import json
import hashlib
from pathlib import Path
from anthropic import Anthropic
from ..config import AI_MODEL, AI_MAX_TOKENS, CACHE_DIR


_client: Anthropic | None = None


def get_client() -> Anthropic:
    """Get or create the Anthropic client."""
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY environment variable not set.\n"
                "Set it with: set ANTHROPIC_API_KEY=your-key-here"
            )
        _client = Anthropic(api_key=api_key)
    return _client


def _cache_key(system: str, user: str) -> str:
    """Generate a cache key from prompt content."""
    content = f"{system}|||{user}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def _cache_path(key: str) -> Path:
    """Get the cache file path for a key."""
    CACHE_DIR.mkdir(exist_ok=True)
    return CACHE_DIR / f"{key}.json"


def ask_claude(system: str, user: str, use_cache: bool = True) -> str:
    """Send a prompt to Claude and return the response text.

    Args:
        system: System prompt (role/instructions)
        user: User message (data/question)
        use_cache: If True, cache responses to disk for development

    Returns:
        Claude's response text
    """
    # Check cache
    if use_cache:
        key = _cache_key(system, user)
        cached = _cache_path(key)
        if cached.exists():
            data = json.loads(cached.read_text(encoding="utf-8"))
            return data["response"]

    client = get_client()
    response = client.messages.create(
        model=AI_MODEL,
        max_tokens=AI_MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user}],
    )

    text = response.content[0].text

    # Save to cache
    if use_cache:
        key = _cache_key(system, user)
        _cache_path(key).write_text(
            json.dumps({"system": system[:200], "response": text}, ensure_ascii=False),
            encoding="utf-8",
        )

    return text
