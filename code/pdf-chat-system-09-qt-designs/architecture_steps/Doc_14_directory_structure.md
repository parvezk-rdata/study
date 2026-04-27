# Step 13 — Directory Structure

```
chat_pdf/
│
├── main.py                        # Entry point — creates QApplication, MainWindow, MainController
├── .env                           # OpenAI API key (not committed to version control)
├── requirements.txt               # All dependencies
│
├── controllers/
│   ├── __init__.py
│   ├── main_controller.py         # MainController — orchestrates all event flows
│   │
│   ├── component_controllers/
│   │   ├── __init__.py
│   │   ├── toolbar_controller.py      # ToolbarController
│   │   ├── status_bar_controller.py   # StatusBarController
│   │   ├── chat_area_controller.py    # ChatAreaController
│   │   └── input_bar_controller.py    # InputBarController
│   │
│   └── domain_controllers/
│       ├── __init__.py
│       ├── pdf_service.py             # PDFService — PyMuPDF text extraction
│       └── llm_service.py             # LLMService — OpenAI API calls
│
├── components/
│   ├── __init__.py
│   ├── toolbar_component.py           # ToolbarComponent — Upload, filename, Clear
│   ├── status_bar_component.py        # StatusBarComponent — error banner
│   ├── chat_area_component.py         # ChatAreaComponent — scrollable bubble area
│   ├── input_bar_component.py         # InputBarComponent — text input + Send
│   │
│   └── widgets/
│       ├── __init__.py
│       ├── message_bubble_widget.py   # MessageBubbleWidget — single chat bubble (dumb)
│       ├── loading_bubble_widget.py   # LoadingBubbleWidget — • • • indicator (dumb)
│       └── placeholder_widget.py      # PlaceholderWidget — empty state (dumb)
│
├── models/
│   ├── __init__.py
│   ├── domain_models.py               # PDFDocument, ChatMessage
│   └── state_models.py                # AppState, AppError, ErrorKind
│
└── utils/
    ├── __init__.py
    └── config.py                      # Load .env, expose OPENAI_API_KEY
```

---

## File Responsibilities

| File | Contains |
|---|---|
| `main.py` | App entry point. Creates `QApplication`, `MainWindow`, instantiates `MainController` |
| `main_controller.py` | All event handlers, signal wiring, `AppState` ownership |
| `toolbar_controller.py` | File picker, filename display, Clear button state |
| `status_bar_controller.py` | Show/hide error banner |
| `chat_area_controller.py` | Bubble management, scroll, placeholder, loading indicator |
| `input_bar_controller.py` | Read input, clear input, enable/disable |
| `pdf_service.py` | PyMuPDF extraction, returns `PDFDocument` or raises `PDFLoadError` |
| `llm_service.py` | Builds OpenAI payload, returns response text or raises `LLMCallError` |
| `domain_models.py` | `PDFDocument`, `ChatMessage` dataclasses |
| `state_models.py` | `AppState`, `AppError`, `ErrorKind` enum |
| `config.py` | Loads `.env`, exposes `OPENAI_API_KEY` constant |