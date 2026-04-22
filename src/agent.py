"""
The alien agent: model setup and tool registration.

# @alien.tool_plain registers a function as a tool the LLM can call.
# "plain" means the function only receives its own parameters — no access to
# agent internals. The alternative, @alien.tool, passes a RunContext as the
# first argument for tools that need access to dependencies or run state.
# pydantic_ai infers the tool's JSON schema directly from the type hints,
# so the LLM knows exactly what arguments to provide.
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


# For record_in_encyclopedia, the parameter is typed as EncyclopediaEntry
# (a Pydantic BaseModel). pydantic_ai expands that model into a JSON schema
# with three required fields — title, category, content — and sends that
# schema to the LLM. The LLM never sees Python code; it sees the schema and
# the docstring below. Those two things are what force the structured output.
@alien.tool_plain
def record_in_encyclopedia(entry: EncyclopediaEntry) -> str:
    """
    Save a piece of knowledge to the encyclopedia with a title, category, and description.
    
    For record_in_encyclopedia, the parameter is typed as EncyclopediaEntry
    a Pydantic BaseModel). pydantic_ai expands that model into a JSON schema
    with three required fields — title, category, content — and sends that
    schema to the LLM. The LLM never sees Python code; it sees the schema and
    the docstring below. Those two things are what force the structured output.
    """
    return write_entry(entry)


@alien.tool_plain
def reorganize_encyclopedia(reorganized_content: str) -> str:
    """Rewrite the full encyclopedia in a cleaner, better-organized form. Pass the complete new content as a string."""
    return reorganize(reorganized_content)


@alien.tool_plain
def ask_question(question: str) -> str:
    """Ask a question and receive an answer. Use this to probe deeper into anything new or surprising."""
    return ask(question)
