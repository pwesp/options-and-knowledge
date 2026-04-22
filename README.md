# Options and Knowledge (OaK)

An alien lands on a foreign planet and tries to learn how to survive — by asking questions, taking notes, and chasing every new thing it encounters.

This is a small, student-friendly demo of Richard Sutton's [OaK architecture](https://www.youtube.com/watch?v=gEbbGyNkR2U) (Options and Knowledge), built with [pydantic_ai](https://ai.pydantic.dev) and [Ollama](https://ollama.com). The alien runs entirely on a local LLM — no API keys needed.

---

## What it does

You feed the alien observations through your terminal. It reads, thinks, and can:

- **Record** what it learns in a structured knowledge base (`memory/knowledge_base.md`)
- **Ask you questions** when it wants to understand something better
- **Reorganize** its knowledge base when things get messy

The key idea from OaK: when the alien encounters something new, it doesn't just log it — it tries to *re-experience* it by asking follow-up questions. Novelty drives curiosity, curiosity drives learning.

---

## Prerequisites

- [Ollama](https://ollama.com) installed and running
- The model pulled:

```bash
ollama pull gemma4:e4b
```

- Conda (for environment setup)

---

## Installation

```bash
conda create -n oak python=3.13
conda activate oak
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu130
pip install -r requirements.txt
```

---

## Run

```bash
conda activate oak
python awaken_alien.py
```

You'll see a `[World]:` prompt. Type anything — describe something about the world, tell the alien a fact, or just say hello. The alien will respond, and may ask you questions back.

```
The alien awakens...

[World]: There is a creature here with four legs and soft fur. It made a sound at me.

  [The alien asks]: What kind of sound did it make?
  [Your answer]:   A low rumbling sound, almost like a purr.

[Alien]: Fascinating. I have recorded this creature in my encyclopedia...
```

The knowledge base is written to `memory/knowledge_base.md` and grows over the session. It is prepended to every message so the alien always has its full memory in context.

---

## Project structure

```
awaken_alien.py      # Entry point — start here
src/
  agent.py           # The alien: model setup and tool registration
  tools.py           # What the alien can do: write, reorganize, ask
  prompts/
    system.md        # The alien's identity and instructions
memory/
  knowledge_base.md  # Built up at runtime (created on first write)
```

---

## Changing the model

Edit the model name in `src/agent.py`:

```python
OpenAIChatModel("gemma4:e4b", ...)  # swap this for any model in `ollama list`
```

Any Ollama model works. Larger models will use the tools more reliably.
