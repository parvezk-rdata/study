# PDF Chat

A PyQT application that lets you upload a PDF and have a conversation with its contents using an LLM. 

Supports authentication modes: OpenAI API key 

---

## Project Structure

```
pdf_chat_app/
│
├── main.py                             # Entry point (starts QApplication)
├── app.py                              # App bootstrap (wires controllers, state, UI)
│
├── controllers/                        # Business logic (no UI code)
│   ├── main_controller.py              # App-level orchestration
│   ├── document_controller.py          # PDF upload, extraction, reset logic
│   └── chat_controller.py              # Chat flow, LLM calls
│
├── components/                         # Pure UI (PyQt widgets)
│   ├── layout/
│   │   └── main_window.py              # Main window (sidebar + chat layout)
│   │
│   ├── document/
│   │   ├── pdf_upload_component.py     # Upload button / file picker
│   │   ├── pdf_info_component.py       # PDF metadata display
│   │   └── pdf_summary_component.py    # (optional future use)
│   │
│   └── chat/
│       ├── chat_history_component.py   # Scrollable message list
│       ├── chat_input_component.py     # Input box + send button
│       └── chat_message_component.py   # Single message renderer (simple text)
│
├── state/                              # Central state management
│   ├── app_state.py                    # Data structure (dataclasses)
│   └── app_state_store.py              # Store + PyQt signals
│
├── services/                           # External logic (pure functions)
│   ├── pdf_extraction_service.py       # wraps extract() logic
│   └── llm_service.py                  # wraps chat() + context fitting
│
├── models/                             # Typed models (optional but clean)
│   ├── chat_models.py
│   └── document_models.py
│
├── assets/                             # (optional) icons, styles later
│
├── .env                                # API key + model config
├── requirements.txt
│
└── README.md

```

---

## Authentication Modes

### API Key
Uses `OPENAI_API_KEY` and `OPENAI_MODEL` from your `.env` file. Communicates via the standard OpenAI Python SDK.

---

## How to Run

### 1. Clone the repository

```bash
git clone <repository-url>
cd /path/to/pdf_chat
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
sudo apt-get install  poppler-utils tesseract-ocr
```

**Windows:**
Install [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases) and [Tesseract for Windows](https://github.com/UB-Mannheim/tesseract/wiki), then add both to your `PATH`.

### 6. Install system dependencies (IMPORTANT)

Fix Qt plugin error:
```
sudo apt update
sudo apt install -y libxcb-cursor0
```

### 7. Run the application

```bash
python3 main.py
```
---

## Usage

1. **Upload a PDF** using the file uploader.
2. **Ask questions** about the PDF in the chat input.
3. Use **Clear conversation** to reset chat history.
4. Use **Remove PDF** to unload the current document and start fresh.

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

---

## Notes

- PDFs exceeding the context budget (400,000 characters) are automatically trimmed. A warning is shown when this happens.