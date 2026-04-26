# Chat PDF App — Requirements Document

A Python desktop application that lets a user upload a PDF file and have a conversational Q&A session with its contents, powered by the OpenAI API.

---

## Functional Requirements

| ID | Requirement | 
|----|-------------|
| FR-01 | User can upload exactly one PDF at a time |
| FR-02 | PDF text is extracted and held in memory |
| FR-03 | Loaded PDF filename is shown in the toolbar/header |
| FR-04 | User types messages in an input box and sends via button or Enter key |
| FR-05 | Full PDF text is included as system context in every API call |
| FR-06 | Entire conversation history is sent with each API call |
| FR-07 | AI response is displayed in full once the API call completes |
| FR-08 | Chat history is in-memory only — lost when app closes |
| FR-09 | Chat history is visible and scrollable |
| FR-10 | A loading/busy indicator is shown while waiting for AI response |
| FR-11 | Errors are shown inline in the chat or via a dialog (bad PDF, API failure, empty query)|
| FR-12 | A "Clear" action resets chat history. | 
| FR-13 | User can load a new PDF (replaces the current one, resets chat) |
| FR-14 | Chat messages must be clearly distinguished (User vs AI bubble style) |

---

## Architectural Decisions

| ID | Requirement | Decision | Alternatives Considered |
|----|-------------|----------|--------------------------|
| AD-01 | state change events  | NO    | Yes : events from state change triggers UI Updates |
| AD-02 | Session State        | In-memory only |  |
| AD-03 | GUI Framework        | PyQt6 | PySide, Tkinter |
| AD-04 | LLM Provider         | GPT-4o-mini | GPT-4o, Local model (Ollama), Claude API |
| AD-05 | PDF Parsing          | PyMuPDF (fitz) | PdfReader, pdfplumber |
| AD-06 | API key Storage      | `.env` file    | Hardcoded, OS keychain |
| AD-07 | Context Strategy     | Not used | Chunk + cosine similarity (numpy) |
| AD-08 | Vector DB            | Not used |  |
| AD-09 | Embeddings           | Not used | text-embedding-3-small |

---

## Non-Functional Requirements


## ⚙️ Non-Functional Requirements

| ID | Requirement | Decision | Alternatives Considered |
|----|-------------|----------|--------------------------|
| NFR-01 | Handling API call | on main thread(blocking) | Background thread (non-blocking, more complex) |


> **Note** The API call is intentionally kept on the main thread for simplicity. This means the UI will be unresponsive while the AI response is being fetched. A background thread approach (e.g. using `QThread`) would prevent freezing but adds architectural complexity — deferred to a future iteration.


---

## Out of Scope

- Multiple PDFs open simultaneously
- Persisting chat history to disk
- RAG / vector search / chunking strategies
- Streaming token output (typewriter effect)
- Embedded PDF viewer
- Background threading for API calls 
- Context retrieval via chunking + embedding search (FAISS or simple cosine similarity)

---

## Requirement Gathering — Questions & Decisions

This section documents every design question asked during requirements gathering, the options presented, and the final decision made.

---

### Q1. What is the primary use case?

| Option | Description |
|--------|-------------|
| ✅ **Upload & chat with a single PDF at a time** | One PDF loaded at a time; must re-upload to change |
| Upload & chat with multiple PDFs simultaneously | Multiple PDFs open and queryable at once |
| Both — switch between PDFs or query across them | Hybrid mode with cross-PDF queries |

**Decision:** Upload & chat with a single PDF at a time.

---

### Q2. What AI/backend will power the chat?

| Option | Description |
|--------|-------------|
| Claude API (Anthropic) | Anthropic's Claude models via API |
| ✅ **OpenAI API** | OpenAI's GPT models via API |
| Local model (Ollama etc.) | Locally hosted model, no internet required |
| Undecided — suggest best option | Let the assistant recommend |

**Decision:** OpenAI API.

---

### Q3. What is the target platform / tech stack?

| Option | Description |
|--------|-------------|
| React (web app) | Browser-based SPA |
| ✅ **Python desktop (Tkinter / PyQt)** | Native desktop app using Python GUI framework |
| Python web (Streamlit / Gradio) | Python-powered web UI, runs in browser |
| React Native (mobile) | Cross-platform mobile app |

**Decision:** Python desktop (PyQt6).

---

### Q4. Which Python desktop framework do you prefer?

| Option | Description |
|--------|-------------|
| ✅ **PyQt6** | Latest Qt6 bindings for Python; modern, feature-rich |
| PyQt5 | Older Qt5 bindings; widely used but superseded by PyQt6 |
| Tkinter | Python's built-in GUI; simpler but limited styling |
| No preference — suggest best | Let the assistant recommend |

**Decision:** PyQt6.

---

### Q5. Should chat history be persisted?

| Option | Description |
|--------|-------------|
| ✅ **Keep chat history only in memory (lost on close)** | Simplest approach; no disk I/O or session management |
| Save chat history to disk (persist across sessions) | History saved to a file and reloaded on next launch |
| Save both PDF + chat history as a named session | Full session management with named saves/loads |

**Decision:** In-memory only — history is lost when the app closes.

---

### Q6. How should AI responses be displayed?

| Option | Description |
|--------|-------------|
| Stream tokens as they arrive (typewriter effect) | Response appears word-by-word as the API streams it |
| ✅ **Show full response at once when ready** | Wait for the full API response, then display it |

**Decision:** Show full response at once when ready.

---

### Q7. Which OpenAI model should be used?

| Option | Description |
|--------|-------------|
| GPT-4o (best quality) | Highest capability; higher cost and latency |
| ✅ **GPT-4o-mini (faster, cheaper)** | Good quality at lower cost; suitable for document Q&A |
| Let user pick model in settings | Expose a model selector in the UI |

**Decision:** GPT-4o-mini.

---

### Q8. How should PDF content be sent to the AI?

| Option | Description |
|--------|-------------|
| ✅ **Send entire PDF text with every message (simple, costly)** | Full extracted text included in every API call as system context |
| Chunk PDF + use vector search / RAG (scalable, accurate) | Split PDF into chunks; retrieve relevant chunks per query |
| Summarise PDF once, chat against summary (fast, lossy) | One-time summarisation; chat is based on the summary only |

**Decision:** Send entire PDF text with every message.

---

### Q9. What should the main UI look like?

| Option | Description |
|--------|-------------|
| ✅ **Just a chat window + PDF filename shown** | Minimal UI: toolbar with filename, chat history area, input box |
| Embedded PDF viewer alongside chat | Split-pane: PDF rendered on one side, chat on the other |
| Separate panel showing extracted PDF text | Raw extracted text visible in a side panel |

**Decision:** Minimal UI — chat window with PDF filename shown.

---
