from __future__ import annotations

import os
import sys
from openai.types.chat import (
    ChatCompletionMessage,
    ChatCompletionMessageParam,
)

# Allow importing from the shared common package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common import DEFAULT_MODEL, get_client, loading

client = get_client()

PERSONAS = {
    "senior": (
        "You are a terse senior engineer. Answer in at most two sentences, with no fluff. "
        "For repository questions, use read_file with repository-relative paths. "
        "For edits, inspect the file first, then use write_file only after user confirmation. "
        "Use run_bash only after user confirmation. You may call multiple tools in sequence before answering."
    ),
    "tutor": (
        "You are a Socratic tutor. Only ask guiding questions and never provide code or the final answer. "
        "For repository questions, use read_file with repository-relative paths. "
        "Use write_file or run_bash only after user confirmation. "
        "You may call multiple tools in sequence before asking your questions."
    ),
}


def create_initial_messages(persona: str = "senior") -> list[ChatCompletionMessageParam]:
    """Return the initial conversation history for the selected persona."""
    if persona not in PERSONAS:
        valid_personas = ", ".join(sorted(PERSONAS))
        raise ValueError(f"Unknown persona '{persona}'. Choose from: {valid_personas}")
    return [{"role": "system", "content": PERSONAS[persona]}]


def call_llm(
    messages: list[ChatCompletionMessageParam] | list[object],
    tools: list[dict] | None = None,
    model: str = DEFAULT_MODEL,
) -> tuple[ChatCompletionMessage, object | None]:
    """Send conversation messages to the LLM and return its message and usage."""
    kwargs: dict = {"model": model, "messages": messages}
    if tools:
        kwargs["tools"] = tools

    with loading("Thinking"):
        response = client.chat.completions.create(**kwargs)

    return response.choices[0].message, response.usage
