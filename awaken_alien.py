"""
Entry point. Runs the terminal loop: feed the alien observations, let it think and ask questions.
"""

from pydantic_ai.messages import ModelMessage

from src.agent import alien
from src.tools import KNOWLEDGE_BASE


def build_message(observation: str) -> str:
    """
    Prepend the current encyclopedia to the observation so the alien
    always sees its full memory alongside whatever is new.
    """
    if KNOWLEDGE_BASE.exists() and KNOWLEDGE_BASE.stat().st_size > 0:
        memory = KNOWLEDGE_BASE.read_text().strip()
        return f"## Your encyclopedia\n\n{memory}\n\n---\n\n## New information\n\n{observation}"
    # No encyclopedia yet — just pass the raw observation
    return observation


def main() -> None:
    print("The alien awakens...\n")

    history: list[ModelMessage] = []

    while True:
        try:
            observation = input("\n[World]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nThe alien sleeps.")
            break

        if not observation:
            continue

        message = build_message(observation)
        result = alien.run_sync(message, message_history=history)

        print(f"\n[Alien]: {result.output}")

        # Accumulate history so the alien remembers the conversation
        history += result.new_messages()


if __name__ == "__main__":
    main()
