# PDF Chat

A Streamlit application that lets you upload a PDF and have a conversation with its contents using an LLM. Supports two authentication modes: OpenAI API key and ChatGPT OAuth.

---

## Project Structure

```
pdf_chat/
│
├── main.py                         # Entry point and dependency wiring
├── config.py                       # Pydantic BaseSettings — single source of truth
├── requirements.txt
│
├── models/                         # Pure Pydantic data models, no business logic
│   ├── auth.py                     # StoredAuth
│   ├── chat.py                     # Message
│   ├── doc.py                      # ExtractedDoc
│   └── ui.py                       # SidebarEvent
│
├── state/                          # Streamlit session state, split by domain
│   ├── auth_state.py               # auth_mode, oauth_model, login_handle
│   ├── doc_state.py                # doc, doc_hash, uploader_key
│   └── chat_state.py               # history: list[Message]
│
├── controller/                     # Orchestration and control flow
│   ├── app_controller.py           # Main render loop — pure orchestration
│   ├── auth_controller_logic.py    # OAuth polling, login, logout
│   ├── chat_controller_logic.py    # Prompt building, client selection, chat flow
│   └── doc_controller_logic.py     # PDF upload, hash check, truncation
│
├── llm/                            # Transport layers — no business logic
│   ├── openai_client.py            # API key path via OpenAI SDK
│   └── oauth_client.py             # OAuth path via httpx SSE streaming
│
├── services/                       # External integrations
│   ├── auth_service.py             # PKCE OAuth flow, token refresh, persistence
│   └── pdf_service.py              # PDF text extraction with OCR fallback
│
└── ui/                             # Stateless Streamlit rendering
    ├── page.py                     # Page config and title
    ├── sidebar.py                  # Auth panel and session buttons
    ├── pdf_panel.py                # File uploader and metadata display
    └── chat_panel.py               # Chat history, input, and messages
```

---

## Architecture

The app follows a clean layered architecture:

- **Models** define data shapes using Pydantic. No logic, no I/O.
- **State** classes manage `st.session_state` through semantic operations grouped by domain.
- **Services** handle external I/O — OAuth flows and PDF extraction.
- **LLM clients** are pure transport layers. They receive ready-to-send data from the controller and return a reply string.
- **Controller logic** classes own all decisions — which LLM client to use, how to build prompts, how to handle auth events.
- **UI classes** are fully stateless — they receive data as arguments and return user input.
- **AppController** is a thin orchestrator that wires the render order with no business logic.

---

## Authentication Modes

### API Key
Uses `OPENAI_API_KEY` and `OPENAI_MODEL` from your `.env` file. Communicates via the standard OpenAI Python SDK.

### ChatGPT OAuth
Signs in via your ChatGPT account using a PKCE OAuth flow. Opens a browser window for authentication and listens for the callback on `localhost:1455`. Tokens are persisted to `.pdf-chat/auth.json`.

---

## How to Run

### 1. Clone the repository

```bash
git clone <repository-url>
cd pdf_chat
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and set your values:

```env
# Required for API key mode
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# Optional — only needed if using a custom OpenAI-compatible endpoint
OPENAI_BASE_URL=
```

> If you plan to use **ChatGPT OAuth mode only**, you can leave `OPENAI_API_KEY` and `OPENAI_MODEL` blank.

### 5. Install system dependencies (OCR fallback only)

OCR is used automatically when a PDF contains no extractable text (e.g. scanned documents). Skip this step if you only work with text-based PDFs.

**macOS:**
```bash
brew install poppler tesseract
```

**Ubuntu / Debian:**
```bash
sudo apt-get install poppler-utils tesseract-ocr
```

**Windows:**
Install [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases) and [Tesseract for Windows](https://github.com/UB-Mannheim/tesseract/wiki), then add both to your `PATH`.

### 6. Add `__init__.py` files

Python requires an `__init__.py` in each package directory:

```bash
touch models/__init__.py
touch state/__init__.py
touch services/__init__.py
touch llm/__init__.py
touch ui/__init__.py
touch controller/__init__.py
```

### 7. Run the application

```bash
streamlit run main.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## Usage

1. **Choose auth mode** in the sidebar — API key or ChatGPT OAuth.
2. **Upload a PDF** using the file uploader.
3. **Ask questions** about the PDF in the chat input.
4. Use **Clear conversation** to reset chat history.
5. Use **Remove PDF** to unload the current document and start fresh.

---

## Troubleshooting — If `pip install` Fails

If `pip install -r requirements.txt` fails or pip stops working after a previously successful install, the virtual environment is likely corrupted. Recreate it from scratch by running these commands from the project root:

```bash
# Step 1 — navigate to the project root
cd /path/to/pdf_chat

# Step 2 — deactivate the current venv if active
deactivate

# Step 3 — delete the broken venv
rm -rf .venv

# Step 4 — recreate the venv
python3 -m venv .venv

# Step 5 — activate the new venv
source .venv/bin/activate

# Step 6 — install dependencies
pip install -r requirements.txt
```

> **Windows:** replace `source .venv/bin/activate` with `.venv\Scripts\activate` and `rm -rf .venv` with `rmdir /s /q .venv`.

If the install fails again on a specific package, install in two steps to isolate the problem:

```bash
# Core packages
pip install streamlit openai pypdf httpx python-dotenv pydantic pydantic-settings

# OCR packages (optional — only needed for scanned PDFs)
pip install pdf2image pytesseract
```

---

## Notes

- PDFs exceeding the context budget (400,000 characters) are automatically trimmed. A warning is shown when this happens.
- OAuth tokens are stored locally at `.pdf-chat/auth.json` with restricted file permissions (`600`).
- The OAuth callback server runs on port `1455`. Make sure this port is available when signing in.
