# Options and Knowledge (OaK)

An alien lands on a foreign planet and tries to learn how to survive — by asking questions, taking notes, and chasing every new thing it encounters.

This is a student-friendly demo of Richard Sutton's [OaK architecture](https://www.youtube.com/watch?v=gEbbGyNkR2U), built with [pydantic_ai](https://ai.pydantic.dev) and [Ollama](https://ollama.com). Runs entirely on a local LLM — no API keys needed.

The key idea from OaK: when the alien encounters something new, it doesn't just log it — it tries to *re-experience* it by asking follow-up questions. Novelty drives curiosity, curiosity drives learning.

---

## Prerequisites

**Ollama** — download and install from [ollama.com/download](https://ollama.com/download), then pull the model:

```bash
ollama pull gemma4:e4b
```

**Conda** — used to create the Python environment.

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

You'll see a `[World]:` prompt. Describe something, tell the alien a fact, or just say hello. It will respond and may ask you questions back.

```
The alien awakens...

[World]: There is a creature here with four legs and soft fur. It made a sound at me.

  [The alien asks]: What kind of sound did it make?
  [Your answer]:   A low rumbling sound, almost like a purr.

[Alien]: Fascinating. I have recorded this creature in my encyclopedia...
```

The knowledge base grows in `memory/knowledge_base.md` and is prepended to every message so the alien always has its full memory in context.

---

## How it works

```
  You type an observation
          │
          ▼
  Current encyclopedia prepended
  to the message as context
          │
          ▼
  ┌───────────────────┐
  │     LLM (Ollama)  │  ◄── system prompt (alien identity + tool descriptions)
  └────────┬──────────┘
           │  decides to call a tool
           ▼
  ┌─────────────────────────────────────────┐
  │  record_in_encyclopedia(entry)          │  writes a structured entry to memory/
  │  reorganize_encyclopedia(new_content)   │  rewrites memory/ in place
  │  ask_question(question)                 │  blocks, reads your answer from terminal
  └─────────────────────────────────────────┘
           │  tool result returned to LLM
           ▼
  LLM produces final response
          │
          ▼
  [Alien]: ...  →  loop back to [World]:
```

Tools are registered with `@alien.tool_plain` — a method on the `Agent` object that tells pydantic_ai which functions the LLM is allowed to call. pydantic_ai inspects the type hints and generates a JSON schema for each tool, which is sent to the LLM alongside the docstring. **The LLM never sees Python code** — only the schema and the docstring.

The `plain` in `tool_plain` means the function only receives its own parameters. The alternative, `@agent.tool`, passes a `RunContext` as the first argument for tools that need access to agent internals.

The `EncyclopediaEntry` parameter on `record_in_encyclopedia` is a Pydantic `BaseModel`. pydantic_ai expands it into a schema with three required fields (`title`, `category`, `content`), which is what forces the LLM to produce structured output rather than free-form text.

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
OpenAIChatModel("gemma4:e4b", ...)  # swap for any model in `ollama list`
```

Larger models will use the tools more reliably.
