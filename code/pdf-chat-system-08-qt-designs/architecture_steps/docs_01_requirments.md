# Chat PDF App — Requirements Document

> This document captures all requirements gathered during Step 01 of the development process.
> For each decision point, the options presented are listed alongside the choice made.

---

## 1. Project Overview

A Python desktop application that lets a user upload a PDF file and have a conversation with its contents using an AI language model. The loaded PDF filename is shown in the UI, and all chat history is held in memory for the duration of the session.

---

## 2. Decision Log

Each question asked during requirements gathering, the options offered, and the choice made.

---

### 2.1 Primary Use Case

**Question:** What's the primary use case?

| Option | Description | Chosen |
|--------|-------------|--------|
| Upload & chat with a single PDF at a time | One PDF loaded at a time; replace to switch | ✅ |
| Upload & chat with multiple PDFs simultaneously | Several PDFs open in parallel, query across all | |
| Both — switch between PDFs or query across them | Single or multi-PDF with switching support | |

**Decision:** Single PDF at a time — keeps the architecture simple and the UX focused.

---

### 2.2 AI / Backend

**Question:** What AI/backend will power the chat?

| Option | Description | Chosen |
|--------|-------------|--------|
| Claude API (Anthropic) | Anthropic's Claude models via API | |
| OpenAI API | OpenAI GPT models via API | ✅ |
| Local model (Ollama etc.) | Offline model, no API key needed | |
| Undecided — suggest best option | Let the assistant recommend | |

**Decision:** OpenAI API — widely supported, straightforward Python SDK, good documentation.

---

### 2.3 Target Platform / Tech Stack

**Question:** What's the target platform / tech stack?

| Option | Description | Chosen |
|--------|-------------|--------|
| React (web app) | Browser-based SPA | |
| Python desktop (Tkinter / PyQt) | Native desktop app via Python GUI framework | ✅ |
| Python web (Streamlit / Gradio) | Python-first web UI, runs in browser | |
| React Native (mobile) | Cross-platform mobile app | |

**Decision:** Python desktop — keeps everything in a single language, no browser or server needed.

---

### 2.4 Python Desktop Framework

**Question:** Which Python desktop framework do you prefer?

| Option | Description | Chosen |
|--------|-------------|--------|
| PyQt5 | Mature, Qt5-based, slightly older API | |
| PyQt6 | Latest Qt6 bindings, modern API | ✅ |
| Tkinter | Built-in standard library, basic widgets | |
| No preference — suggest best | Let the assistant recommend | |

**Decision:** PyQt6 — modern Qt6 bindings, rich widget set, good support for threading.

---

### 2.5 Chat History Persistence

**Question:** Should chat history be persisted?

| Option | Description | Chosen |
|--------|-------------|--------|
| Keep chat history only in memory (lost on close) | Simple; no disk I/O or file management | ✅ |
| Save chat history to disk (persist across sessions) | History survives app restarts | |
| Save both PDF + chat history as a named session | Full session save/restore with a name | |

**Decision:** In-memory only — reduces complexity; acceptable for v1.

---

### 2.6 AI Response Display

**Question:** How should AI responses be displayed?

| Option | Description | Chosen |
|--------|-------------|--------|
| Stream tokens as they arrive (typewriter effect) | Live token streaming, more responsive feel | |
| Show full response at once when ready | Wait for complete response, then display | ✅ |

**Decision:** Full response at once — simpler threading model, no streaming API needed.

---

### 2.7 OpenAI Model

**Question:** Which OpenAI model should be used?

| Option | Description | Chosen |
|--------|-------------|--------|
| GPT-4o (best quality) | Highest capability, higher cost & latency | |
| GPT-4o-mini (faster, cheaper) | Good quality, lower cost, faster responses | ✅ |
| Let user pick model in settings | Runtime model selection in the UI | |

**Decision:** GPT-4o-mini — best balance of quality and cost for a PDF chat use case.

---

### 2.8 PDF-to-AI Strategy

**Question:** How should PDF content be sent to the AI?

| Option | Description | Chosen |
|--------|-------------|--------|
| Send entire PDF text with every message (simple, costly) | Full text in system prompt each call; simple but token-heavy | ✅ |
| Chunk PDF + use vector search / RAG (scalable, accurate) | Embed chunks, retrieve relevant ones per query | |
| Summarise PDF once, chat against summary (fast, lossy) | One-time summary; fast but loses detail | |

**Decision:** Full text per message — simplest implementation for v1; acceptable for typical PDF sizes.

---

### 2.9 Main UI Layout

**Question:** What should the main UI look like?

| Option | Description | Chosen |
|--------|-------------|--------|
| Just a chat window + PDF filename shown | Minimal UI: toolbar with filename, chat area, input box | ✅ |
| Embedded PDF viewer alongside chat | Split pane: rendered PDF on left, chat on right | |
| Separate panel showing extracted PDF text | Raw extracted text panel alongside chat | |

**Decision:** Minimal UI — focused UX, faster to build, easier to maintain.

---

## 3. Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-01 | User can upload exactly one PDF at a time |
| FR-02 | PDF text is extracted and held in memory |
| FR-03 | Loaded PDF filename is displayed in the toolbar/header |
| FR-04 | User types messages in an input box and sends via button or Enter key |
| FR-05 | Full PDF text is included as system context in every API call |
| FR-06 | Entire conversation history is sent with each API call |
| FR-07 | AI response is displayed in full once the API call completes |
| FR-08 | Chat history is in-memory only — lost when the app closes |
| FR-09 | A loading/busy indicator is shown while waiting for the AI response |
| FR-10 | Errors are shown inline in the chat area or via a dialog |
| FR-11 | A "Clear" action resets chat history and unloads the current PDF |

---

## 4. Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NF-01 | Built with **PyQt6** |
| NF-02 | AI powered by **OpenAI GPT-4o-mini** |
| NF-03 | OpenAI API key read from a `.env` file (never hardcoded) |
| NF-04 | API call runs on a **background thread** so the UI never freezes |
| NF-05 | PDF text extracted using **PyMuPDF (fitz)** or **pdfplumber** |

---

## 5. Use Cases

### UC-01 — Load a PDF
User clicks the "Open PDF" button to browse and select a PDF file from disk. The app extracts the full text and stores it in memory. The PDF filename is shown in the header.

### UC-02 — Ask a Question
User types a question in the input field and submits it (button click or Enter key). The app sends the full PDF text + full conversation history + new question to GPT-4o-mini. The response is displayed in the chat window once the API call completes.

### UC-03 — View Conversation History
All prior user messages and AI responses are visible in the chat window in chronological order for the duration of the session.

### UC-04 — Clear / Reset
User clicks "Clear" to wipe the chat history and unload the current PDF, returning the app to its initial state.

### UC-05 — Handle Errors
If no PDF is loaded, the API call fails, or the PDF cannot be parsed, a clear error message is shown in the UI without crashing the app.

---

## 6. Out of Scope (v1)

- Multiple PDFs open simultaneously
- Persisting chat history to disk
- RAG / vector search / chunking strategies
- Streaming token output (typewriter effect)
- Embedded PDF viewer or raw text panel
- Model selection in the UI
