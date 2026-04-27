# Step 13 — Directory Structure

```

chat_pdf/
│
├── main.py                          # Entry point — creates MainController, starts app
│
├── .env                             # API key (not committed to version control)
├── requirements.txt
│
├── controllers/
│   ├── main_controller.py           # MainController — orchestrates all event flows
│   ├── ui_composer.py               # UIComposer — builds UI, returns AppControllers bundle
│   └── domain_composer.py           # DomainComposer — loads .env, returns DomainControllers bundle
│
├── components/
│   ├── toolbar_component.py         # ToolbarComponent [SMART]
│   ├── status_bar_component.py      # StatusBarComponent [SMART]
│   ├── chat_area_component.py       # ChatAreaComponent [SMART]
│   ├── input_bar_component.py       # InputBarComponent [SMART]
│   └── widgets/
│       ├── message_bubble_widget.py # MessageBubbleWidget [DUMB]
│       ├── loading_bubble_widget.py # LoadingBubbleWidget [DUMB]
│       └── placeholder_widget.py   # PlaceholderWidget [DUMB]
│
├── component_controllers/
│   ├── toolbar_controller.py        # ToolbarController
│   ├── status_bar_controller.py     # StatusBarController
│   ├── chat_area_controller.py      # ChatAreaController
│   └── input_bar_controller.py      # InputBarController
│
├── domain/
│   ├── pdf_service.py               # PDFService — PyMuPDF text extraction
│   └── llm_service.py               # LLMService — OpenAI API calls
│
├── models/
│   ├── domain_models.py             # PDFDocument, ChatMessage
│   └── state_models.py              # AppState, AppError, ErrorKind
│
└── bundles/
    ├── app_controllers.py           # AppControllers frozen dataclass
    └── domain_controllers.py        # DomainControllers frozen dataclass

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