"""
The alien agent: model setup and tool registration.
"""

from pathlib import Path

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

from .tools import EncyclopediaEntry, ask, reorganize, write_entry

_system_prompt = (Path(__file__).parent / "prompts" / "system.md").read_text()

alien: Agent = Agent(
    OpenAIChatModel("gemma4:e4b", provider=OllamaProvider(base_url="http://localhost:11434/v1")),
    system_prompt=_system_prompt,
)


@alien.tool_plain
def record_in_encyclopedia(entry: EncyclopediaEntry) -> str:
    """Save a piece of knowledge to the encyclopedia with a title, category, and description."""
    return write_entry(entry)


@alien.tool_plain
def reorganize_encyclopedia(reorganized_content: str) -> str:
    """Rewrite the full encyclopedia in a cleaner, better-organized form. Pass the complete new content as a string."""
    return reorganize(reorganized_content)


@alien.tool_plain
def ask_question(question: str) -> str:
    """Ask a question and receive an answer. Use this to probe deeper into anything new or surprising."""
    return ask(question)
