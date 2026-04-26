# Step 12 — Identify MainController

---

## Responsibilities

- Single orchestrator for the entire application
- Holds `AppState` — the only place state is read and written
- Connects all component signals to handler methods on startup
- Calls `DomainController` methods for business logic
- Calls `ComponentController` methods to update the UI
- Handles all errors and decides how to surface them

---

## Signal Connections (wired on startup)

| Signal | Source Component | Handler Method |
|---|---|---|
| Upload PDF clicked | `ToolbarComponent` | `on_upload_pdf_requested()` |
| Clear clicked | `ToolbarComponent` | `on_chat_cleared()` |
| Status bar dismissed | `StatusBarComponent` | `on_status_bar_dismissed()` |
| Send clicked / Enter pressed | `InputBarComponent` | `on_message_send_requested()` |

---

## Handler Methods

| Method | Mapped Event | Description |
|---|---|---|
| `on_upload_pdf_requested()` | E-01 | Open file picker |
| `on_pdf_loaded(file_path)` | E-02 | Parse PDF, update state, update UI |
| `on_status_bar_dismissed()` | E-03 | Clear error state, hide status bar |
| `on_message_send_requested()` | E-04 | Validate input, call LLM, update state, update UI |
| `on_chat_cleared()` | E-05 | Clear state and reset chat UI |

---

## Error Handlers

| Method | Mapped Error | Description |
|---|---|---|
| `on_pdf_load_failed(message)` | `pdf_load_failed` | Store error, show status bar banner |
| `on_api_call_failed(message)` | `api_call_failed` | Store error, show inline red bubble |
| `on_empty_query_submitted()` | `empty_query_submitted` | Store error, show inline red bubble |

---

## What MainController does NOT do

| Concern | Delegated to |
|---|---|
| Open file picker | `ToolbarController` |
| Extract PDF text | `PDFService` |
| Call OpenAI API | `LLMService` |
| Render bubbles, show/hide widgets | `ComponentControllers` |