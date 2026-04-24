## 📁 Architecture Overview

| Component Type          | Description                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------- |
| `MainController`        | Composition root and orchestrator; coordinates all event flows and updates the store. |
| `Component Controllers` | Event-based UI handlers; update components based on instructions from MainController. |
| `Components`            | Dumb renderers; only display data and emit user interaction signals.                  |
| `File Dialog`           | Treated as a component; encapsulates file selection UI as a reusable abstraction.     |
| `Store`                 | Single source of truth; maintains application state and emits change events.          |
| `Domain Controllers`    | Handle pure business logic (no UI interaction, no direct store updates).              |

---



pdf_chat_app/
│
├── main.py
│   # imports PDFChatApplication from app.py and starts the app
│
├── app.py
│   # imports MainWindow, MainController, AppStateStore, LLMService, PDFExtractionService
│
├── controllers/
│   ├── main_controller.py
│   │   # imports MainWindow, FileDialogComponent, PDFController, LLMController,
│   │   # PDFPanelController, ChatHistoryController, ChatInputController,
│   │   # AppStateStore, ChatMessage, DocumentInfo
│   │
│   ├── controller_results.py
│   │   # imports DocumentInfo (for result dataclasses like PDFLoadResult, LLMChatResult)
│   │
│   ├── domain_controllers/
│   │   ├── llm_controller.py
│   │   │   # imports LLMService, ChatMessage, DocumentInfo, LLMChatResult
│   │   │
│   │   └── pdf_controller.py
│   │       # imports PDFExtractionService, LLMService, DocumentInfo, PDFLoadResult
│   │
│   └── component_controllers/
│       ├── pdf_panel_controller.py
│       │   # imports PDFPanelComponent
│       │
│       ├── chat_history_controller.py
│       │   # imports ChatHistoryComponent
│       │
│       ├── chat_input_controller.py
│       │   # imports ChatInputComponent
│       │
│       └── file_dialog_controller.py
│           # imports FileDialogComponent
│
├── components/
│   ├── layout/
│   │   └── main_window.py
│   │       # imports PDFPanelComponent, ChatHistoryComponent, ChatInputComponent
│   │
│   ├── document/
│   │   └── pdf_panel_component.py
│   │       # imports QWidget, QLabel, QPushButton, QVBoxLayout, pyqtSignal
│   │
│   ├── chat/
│   │   ├── chat_history_component.py
│   │   │   # imports QWidget, QScrollArea, QVBoxLayout, QTimer, QEvent,
│   │   │   # ChatMessageComponent
│   │   │
│   │   ├── chat_input_component.py
│   │   │   # imports QWidget, QLineEdit, QPushButton, QHBoxLayout, pyqtSignal
│   │   │
│   │   └── chat_message_component.py
│   │       # imports QWidget, QLabel, QVBoxLayout
│   │
│   └── system/
│       └── file_dialog_component.py
│           # imports QWidget, QFileDialog, pyqtSignal
│
├── state/
│   ├── app_state.py
│   │   # defines AppState dataclass (document, chat_history, status_message)
│   │
│   └── app_state_store.py
│       # imports AppState, emits signals (document_changed, chat_changed, status_changed)
│
├── services/
│   ├── llm_service.py
│   │   # handles OpenAI/LLM API calls
│   │
│   └── pdf_extraction_service.py
│       # handles PDF parsing + OCR extraction
│
├── models/
│   ├── chat_models.py
│   │   # defines ChatMessage dataclass
│   │
│   └── document_models.py
│       # defines DocumentInfo dataclass
│
├── requirements.txt
│   # lists dependencies (PyQt6, OpenAI, etc.)
│
└── .env
    # stores API keys and environment variables