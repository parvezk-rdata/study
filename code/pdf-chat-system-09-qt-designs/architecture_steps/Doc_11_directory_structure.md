
# Directory Structure

```
chat_pdf/
│
├── main.py                              # Entry point — creates MainController, starts app
├── .env                                 # API key (not committed to version control)
├── requirements.txt
│
├── core/
│   ├── main_controller.py               # MainController — orchestrates all event flows
│   ├── models/
│   │   ├── domain_models.py             # PDFDocument, ChatMessage
│   │   └── state_models.py              # AppState, AppError, ErrorKind
│   └── bundles/
│       ├── app_controllers.py           # AppControllers frozen dataclass
│       └── domain_controllers.py        # DomainControllers frozen dataclass
│
├── ui/
│   ├── ui_composer.py                   # UIComposer — builds all UI, returns AppControllers bundle
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
└── domain/
    ├── domain_composer.py               # DomainComposer — loads .env, returns DomainControllers bundle
    ├── pdf_service.py                   # PDFService — PyMuPDF text extraction
    └── llm_service.py                   # LLMService — OpenAI API calls
```

---

## Bundle Definitions

```python
# core/bundles/app_controllers.py
@dataclass(frozen=True)
class AppControllers:
    toolbar:    ToolbarController
    status_bar: StatusBarController
    chat_area:  ChatAreaController
    input_bar:  InputBarController

# core/bundles/domain_controllers.py
@dataclass(frozen=True)
class DomainControllers:
    pdf: PDFService
    llm: LLMService
```

---

## File Responsibilities

| File | Contains |
|---|---|
| `main.py` | App entry point. Creates `QApplication`, `MainWindow`, instantiates `MainController` |
| `core/main_controller.py` | All event handlers, signal wiring, `AppState` ownership |
| `core/models/domain_models.py` | `PDFDocument`, `ChatMessage` dataclasses |
| `core/models/state_models.py` | `AppState`, `AppError`, `ErrorKind` enum |
| `core/bundles/app_controllers.py` | `AppControllers` frozen dataclass |
| `core/bundles/domain_controllers.py` | `DomainControllers` frozen dataclass |
| `ui/ui_composer.py` | Builds all components + controllers, returns `AppControllers` bundle |
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
| `domain/domain_composer.py` | Loads `.env`, instantiates domain services, returns `DomainControllers` bundle |
| `domain/pdf_service.py` | PyMuPDF extraction, returns `PDFDocument` or raises `PDFLoadError` |
| `domain/llm_service.py` | Builds OpenAI payload, returns response text or raises `LLMCallError` |