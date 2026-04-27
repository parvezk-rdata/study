# Directory Structure
> Note : the name domain is being replaced with services

```
chat_pdf/
│
├── main.py                              # Entry point — creates QApplication, MainWindow, 
│                                          MainController
├── .env                                 # API key (not committed to version control)
├── requirements.txt
│
├── app/
│   ├── main_controller.py               # MainController — orchestrates all event flows
│   └── models/
│       ├── services/
│       │   ├── pdf_document.py          # PDFDocument dataclass
│       │   └── chat_message.py          # ChatMessage dataclass
│       └── state/
│           ├── app_state.py             # AppState dataclass
│           └── app_error.py             # AppError dataclass, ErrorKind enum
│
├── ui/
│   ├── ui_composer.py                   # UIComposer — builds all UI, returns UIBundle
│   ├── ui_bundle.py                     # UIBundle frozen dataclass
│   ├── toolbar/
│   │   ├── toolbar_component.py         # ToolbarComponent [SMART]
│   │   └── toolbar_controller.py        # ToolbarController
│   ├── status_bar/
│   │   ├── status_bar_component.py      # StatusBarComponent [SMART]
│   │   └── status_bar_controller.py     # StatusBarController
│   ├── chat_area/
│   │   ├── chat_area_component.py       # ChatAreaComponent [SMART]
│   │   ├── chat_area_controller.py      # ChatAreaController
│   │   └── widgets/
│   │       ├── message_bubble_widget.py # MessageBubbleWidget [DUMB]
│   │       ├── loading_bubble_widget.py # LoadingBubbleWidget [DUMB]
│   │       └── placeholder_widget.py   # PlaceholderWidget [DUMB]
│   └── input_bar/
│       ├── input_bar_component.py       # InputBarComponent [SMART]
│       └── input_bar_controller.py      # InputBarController
│
├── services/
│   ├── service_composer.py              # ServiceComposer — instantiates services, returns ServiceBundle
│   ├── service_bundle.py                # ServiceBundle frozen dataclass
│   ├── pdf_service.py                   # PDFService — PyMuPDF text extraction
│   └── llm_service.py                   # LLMService — OpenAI API calls
│
├── config/
│   └── settings.py                      # Loads .env, exposes OPENAI_API_KEY and config constants
│
└── utils/                               # Shared helpers (empty for now)
```

---

## File Responsibilities

| File | Contains |
|---|---|
| `main.py` | App entry point. Creates `QApplication`, `MainWindow`, instantiates `MainController` |
| `app/main_controller.py` | All event handlers, signal wiring, `AppState` ownership |
| `app/models/services/pdf_document.py` | `PDFDocument` dataclass |
| `app/models/services/chat_message.py` | `ChatMessage` dataclass |
| `app/models/state/app_state.py` | `AppState` dataclass |
| `app/models/state/app_error.py` | `AppError` dataclass, `ErrorKind` enum |
| `ui/ui_bundle.py` | `UIBundle` frozen dataclass — holds refs to all component controllers |
| `ui/ui_composer.py` | Builds all components + controllers, returns `UIBundle` |
| `ui/toolbar/toolbar_component.py` | Toolbar UI — Upload button, filename label, Clear button |
| `ui/toolbar/toolbar_controller.py` | File picker, filename display, Clear button state |
| `ui/status_bar/status_bar_component.py` | Error banner UI — icon, message label, dismiss button |
| `ui/status_bar/status_bar_controller.py` | Show/hide error banner |
| `ui/chat_area/chat_area_component.py` | Scrollable chat area UI — bubble container |
| `ui/chat_area/chat_area_controller.py` | Bubble management, scroll, placeholder, loading indicator |
| `ui/chat_area/widgets/message_bubble_widget.py` | Single message bubble [DUMB] |
| `ui/chat_area/widgets/loading_bubble_widget.py` | Animated `• • •` loading bubble [DUMB] |
| `ui/chat_area/widgets/placeholder_widget.py` | Empty state icon + hint text [DUMB] |
| `ui/input_bar/input_bar_component.py` | Input field + Send button UI |
| `ui/input_bar/input_bar_controller.py` | Read input, clear input, enable/disable |
| `services/service_bundle.py` | `ServiceBundle` frozen dataclass — holds refs to all services |
| `services/service_composer.py` | Instantiates all services, returns `ServiceBundle` |
| `services/pdf_service.py` | PyMuPDF extraction, returns `PDFDocument` or raises `PDFLoadError` |
| `services/llm_service.py` | Builds OpenAI payload, returns response text or raises `LLMCallError` |
| `config/settings.py` | Loads `.env` via python-dotenv, exposes `OPENAI_API_KEY` constant |
| `utils/` | Shared helpers — empty for now |