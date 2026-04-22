"""
The three things the alien can do: record knowledge, reorganize it, and ask questions.
All side effects (file I/O, terminal I/O) live here.
"""

from pathlib import Path

from pydantic import BaseModel

KNOWLEDGE_BASE = Path("memory") / "knowledge_base.md"


class EncyclopediaEntry(BaseModel):
    title: str
    category: str  # e.g. "flora", "fauna", "physics", "culture", "language"
    content: str


def write_entry(entry: EncyclopediaEntry) -> str:
    """Append a formatted entry to the knowledge base file."""
    KNOWLEDGE_BASE.parent.mkdir(exist_ok=True)

    text = f"\n## {entry.title}\n**Category:** {entry.category}\n\n{entry.content}\n"

    with KNOWLEDGE_BASE.open("a") as f:
        f.write(text)

    return f"Entry '{entry.title}' written to the encyclopedia."


def reorganize(new_content: str) -> str:
    """Overwrite the knowledge base with the reorganized content."""
    assert KNOWLEDGE_BASE.exists(), "Nothing to reorganize — the encyclopedia is empty."
    KNOWLEDGE_BASE.write_text(new_content)
    return "Encyclopedia reorganized."


def ask(question: str) -> str:
    """Print the question to the terminal and wait for a human to answer."""
    print(f"\n  [The alien asks]: {question}")
    answer = input("  [Your answer]:   ").strip()
    return answer
