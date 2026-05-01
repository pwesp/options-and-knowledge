"""
The two things the alien can do: record knowledge and reorganize it.
All side effects (file I/O) live here.
"""

from pathlib import Path

from pydantic import BaseModel

KNOWLEDGE_BASE = Path("memory") / "knowledge_base.md"


class EncyclopediaEntry(BaseModel):
    title: str
    category: str  # "observation", "hypothesis" (if X then Y), or "option" (to achieve X, do Y)
    content: str
    conditions: str | None = None  # when does this apply / what triggers it


def write_entry(entry: EncyclopediaEntry) -> str:
    """Append a formatted entry to the knowledge base file."""
    KNOWLEDGE_BASE.parent.mkdir(exist_ok=True)

    conditions_line = f"\n**Conditions:** {entry.conditions}" if entry.conditions else ""
    text = f"\n## {entry.title}\n**Category:** {entry.category}{conditions_line}\n\n{entry.content}\n"

    with KNOWLEDGE_BASE.open("a") as f:
        f.write(text)

    return f"Entry '{entry.title}' written to the encyclopedia."


def reorganize(new_content: str) -> str:
    """Overwrite the knowledge base with the reorganized content."""
    assert KNOWLEDGE_BASE.exists(), "Nothing to reorganize — the encyclopedia is empty."
    KNOWLEDGE_BASE.write_text(new_content)
    return "Encyclopedia reorganized."
