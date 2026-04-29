# Working Memory

## Purpose

This file is for mutable context that future Codex sessions should reuse and maintain.

## Current understanding

- Project type: local PyQt6 desktop app.
- Core use case: load a PDF, ask questions about its text, show chat-style answers.
- Main orchestration path: `main.py` -> `MainController` -> `UIComposer` + `ServiceComposer`.
- State model: one loaded PDF, chat history, loading flag, and error string.

## Explanation guidance for future sessions

- Start explanations from `app/main_controller.py` unless the user asks for a narrower area.
- Explain the app in terms of event flow, not just folders.
- Connect UI actions to service calls and state changes whenever possible.
- Use `architecture_design/` and `architecture_steps/` as supporting references, not as source-of-truth over code.

## Known repo notes

- `.codex_memory/` is the durable repo-local memory directory for future Codex sessions.
- `.codex` could not be used because it already exists as a locked empty file in this environment.
- `.gitignore` does not currently exclude `.codex_memory/`, so these notes are versionable unless changed later.
- `rg` is not installed in this environment; use `find`, `sed`, and similar tools when needed.

## What to update after future work

- Add corrected architecture notes if the code evolves.
- Record user preferences for how explanations should be written.
- Note major gaps between design docs and implementation.
- Remove stale assumptions once verified or disproved.

## Pending detail to capture later

- More precise summaries of the individual UI controllers and service implementations.
- Whether `OPENAI_MODEL` has a safe default inside the LLM service layer.
- Whether any background threading or async behavior exists deeper in the stack.
