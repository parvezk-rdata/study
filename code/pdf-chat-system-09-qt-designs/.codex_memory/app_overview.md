# App Overview

## What this app is

This repository contains a PyQt6 desktop app for chatting with the contents of a PDF using an OpenAI model.

Entry point:

- `main.py` creates the `QApplication`, applies the QSS theme, creates a `QMainWindow`, and hands control to `MainController`.

## Main runtime flow

1. `main.py` creates the window and calls `MainController(window)`.
2. `app/main_controller.py` builds the UI through `UIComposer().build(window)`.
3. `app/main_controller.py` builds services through `ServiceComposer().build()`.
4. `MainController` stores runtime state in `AppState`.
5. User actions from toolbar, status bar, and input bar are bound to controller handlers.

## Architecture shape

The code is organized around four layers:

- `app/`: top-level orchestration and app state.
- `ui/`: Qt widgets/components and thin UI controllers.
- `services/`: PDF loading and LLM access.
- `config/`: environment-backed settings.

There are also design/reference docs under `architecture_design/` and `architecture_steps/`.

## Key classes

- `MainController`: central coordinator for user events, state updates, and UI/service calls.
- `UIComposer`: builds the main window layout and returns a `UIBundle` of UI controllers.
- `ServiceComposer`: builds and wires the PDF and LLM service controllers.
- `AppState`: stores loaded PDF, message history, loading state, and current error.

## User interaction flow

### Upload PDF

- Toolbar triggers `_on_upload_clicked()`.
- File picker is opened by the toolbar controller.
- `_load_pdf(file_path)` calls `self._svc.pdf.load(file_path)`.
- On success, the controller stores the PDF, clears chat state, clears old errors, updates the toolbar, resets the chat area, and enables input.
- On failure, the status bar shows an error and input remains disabled.

### Ask a question

- Input bar triggers `_on_send_clicked()`.
- Empty input creates a chat-area error bubble.
- Valid input becomes a `ChatMessage(role="user", content=text)`.
- UI enters loading mode and disables input.
- `LLMTransaction` is created from loaded PDF text, prior message history, and the new user message.
- `self._svc.llm.ask(transaction)` calls the LLM layer.
- On success, both user and assistant messages are stored and rendered, then input is re-enabled and cleared.
- On failure, loading is cleared, an error bubble is added, and input is re-enabled.

### Clear chat

- Toolbar triggers `_on_clear_clicked()`.
- Message history and current error are cleared.
- Chat bubbles are removed.
- Placeholder is shown again.
- Status bar error is hidden.

## Important files

- `main.py`
- `app/main_controller.py`
- `app/models/state/app_state.py`
- `ui/ui_composer.py`
- `ui/ui_bundle.py`
- `services/service_composer.py`
- `services/pdf/pdf_controller.py`
- `services/llm/llm_controller.py`
- `config/settings.py`

## Configuration

Runtime settings are loaded from `.env` by `config/settings.py`.

Required:

- `OPENAI_API_KEY`

Expected by current setup:

- `OPENAI_MODEL`

## Current code characteristics

- The app appears to be synchronous; PDF loading and LLM calls run directly from controller handlers.
- Error messages shown to the user are simplified and generic.
- `MainController` is the best place to start for broad code explanations.
