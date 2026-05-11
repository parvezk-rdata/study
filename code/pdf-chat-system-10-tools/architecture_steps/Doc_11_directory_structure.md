# Directory Structure
> Note: the codebase now uses the word `services` instead of `domain`.

```


root(chat pdf app)/
│
├── main.py                              # Entry point — creates QApplication, MainWindow, 
│                                          MainController
├── requirements.txt
├── __init__.py
│
├── app/
│   ├── __init__.py
│   ├── main_controller.py                # MainController:  orchestrates all event flows
│   │
│   ├── event_handlers/
│   │   ├── __init__.py
│   │   ├── pdf/
│   │   │   ├── __init__.py
│   │   │   ├── upload_pdf_handler.py     # Full PDF upload flow
│   │   │   └── remove_pdf_handler.py     # PDF removal
│   │   │
│   │   ├── chat/
│   │   │   ├── __init__.py
│   │   │   ├── send_message_handler.py   # Single chat with llm 
│   │   │   └── clear_chat_handler.py     # Clear all chats
│   │   │
│   │   └── ui/
│   │       ├── __init__.py
│   │       └── theme_changed_handler.py  # Stub — receives theme_name, will apply it
│   │
│   └── models/
│       ├── __init__.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── pdf_document.py                 # PDFDocument dataclass
│       │   │
│       │   └── llm_transaction/
│       │       └── chat_message.py           # ChatMessage
│       │
│       └── state/
│            ├── __init__.py
│            ├── app_state.py              # AppState dataclass
│            ├── app_state_store.py        # future/planned only. app is without store.
│            └── app_error.py              # future/planned only. app is without AppError
│   
├── ui/
│   ├── __init__.py
│   ├── ui_composer.py                   # UIComposer — builds all UI, returns UIBundle
│   ├── ui_bundle.py                     # UIBundle frozen dataclass
│   │
│   ├── toolbar/
│   │   ├── __init__.py
│   │   ├── toolbar_component.py         # ToolbarComponent 
│   │   ├── toolbar_controller.py        # ToolbarController
│   │   └── widgets/
│   │       ├── __init__.py
│   │       ├── upload_button_widget.py
│   │       ├── filename_label_widget.py
│   │       ├── clear_button_widget.py
│   │       └── theme_combo_widget.py
│   │
│   ├── file_picker/
│   │   ├── __init__.py
│   │   ├── file_picker.py                   # FilePickerComponent  
│   │   └── file_picker_controller.py        # FilePickerController
│   │
│   ├── status_bar/
│   │   ├── __init__.py
│   │   ├── status_bar_component.py      # StatusBarComponent 
│   │   └── status_bar_controller.py     # StatusBarController
│   │
│   ├── chat_area/
│   │   ├── __init__.py
│   │   ├── chat_area_component.py       # ChatAreaComponent 
│   │   ├── chat_area_controller.py      # ChatAreaController
│   │   └── widgets/
│   │       ├── __init__.py
│   │       ├── message_bubble_widget.py # MessageBubbleWidget
│   │       └── placeholder_widget.py    # PlaceholderWidget 
│   │
│   └── input_bar/
│       ├── __init__.py
│       ├── input_bar_component.py       # InputBarComponent 
│       ├── input_bar_controller.py      # InputBarController
│       └── widgets/
│           ├── __init__.py
│           ├── button_widget.py 
│           └── text_input_widget.py
│
├── services/
│   ├── __init__.py
│   ├── service_composer.py              # ServiceComposer — instantiates controllers and 
│   │                                      services, config, returns ServiceBundle
│   ├── service_bundle.py                # ServiceBundle frozen dataclass
│   │                                      holds PDFController, LLMController
│   ├── document_extractors/
│   │   |
│   │   ├── text
│   │   |   └── plain
|   |   |       ├── controller.py
|   |   |       ├── service.py
|   |   |       ├── request.py
|   |   |       ├── response.py
|   |   |       └── __init__.py  
│   │   |                                     
│   │   └── pdf/
|   |       └── pymupdf/
|   |           ├── controller.py
|   |           ├── service.py
|   |           ├── request.py
|   |           ├── response.py
|   |           └── __init__.py                            
│   │                                      
│   │  
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── llm_controller.py            # LLMController — receives LLMRequest,  
│   │   │                                  calls LLMService, returns LLMResponse
│   │   ├── llm_service.py               # LLMService: raw OpenAI API call, simple types only
│   │   ├── request.py                   # LLMRequest: send to llm controller by main controller
│   │   ├── response.py                  # LLMResponse: returned by llm controller to main controller
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── openai_formatter.py       # OpenAIFormatter class
│   │
│   └── mcp/
│       ├── __init__.py
│       ├── tool_registry.py              # MCPToolRegistry(returns list of tools)
|       |
│       ├── clients/
│       |   ├── __init__.py
│       |   ├── client_async.py           # classes: MCPConnectionClient
│       |   └── client_sync.py            # classes: SyncConnection
|       |
|       ├── controller.py                 # MCPToolController
│       ├── models/
│       │   ├── __init__.py
│       │   └── mcp_tool_definition.py    # classes : ToolParameter, ToolDefinition 
|       |
│       └── tools_json/
│           ├── tool_get_directory.json   # tool definition : get working directory path
│           ├── tool_list_pdfs.json       # tool definition : get list of pdfs in dir
│           └── tool_read_pdf.json        # tool definition : get content of pdf
│
├── conf/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── appConfig.py                  # shared/global config
│   │   ├── openAI.py                     # LLM-specific
│   │   ├── mcp.py                        # MCP-specific
│   │   └── config_bundle.py              # aggregates all settings
│   │
│   └── env/                              # NO __init__.py — contains only .env files
│       ├── .env.app                      # shared/global config 
│       ├── .env.openAI.example           # example of file .env.openAI
│       ├── .env.openAI                   # LLM-specific
│       └── .env.mcp                      # MCP Server
│
├── styles/                               # NO __init__.py — contains only .qss files
│
└── utils/ 
      └── __init__.py


```

---

## File Responsibilities — Entry Point + App Layer

| File | Contains |
|---|---|
| main.py | App entry point. Calls configure_logging(), creates QApplication, MainWindow, instantiates MainController. |
| utils/logger.py | configure_logging() — configures Python logging to stdout with timestamp and level prefix. Call once at startup. |
| app/main_controller.py | Slim orchestrator. Builds UI, services, and state. Instantiates all event handlers. Wires signals to handler methods via _bind_signals. Owns AppState. |
| app/event_handlers/pdf/upload_pdf_handler.py | Handles the full PDF upload flow. Opens the file picker on upload click, calls PDFService via PDFController, updates AppState, refreshes toolbar, chat area, and input bar. Handles PDFLoadError and surfaces it to the status bar. |
| app/event_handlers/pdf/remove_pdf_handler.py | Handles PDF removal. Clears state.pdf, resets message history and error, empties the chat area, and disables input. |
| app/event_handlers/chat/send_message_handler.py | Handles a single chat turn. Builds LLMRequest from state (with or without PDF text). Runs the agentic loop: calls LLMController, executes MCP tool calls via MCPToolController, feeds results back, repeats until a final answer or error. Saves user + assistant messages to AppState and updates the UI. |
| app/event_handlers/chat/clear_chat_handler.py | Handles chat clear. Resets message history and error in AppState, empties the chat area, hides the status bar, and disables input. |
| app/event_handlers/ui/theme_changed_handler.py | Stub handler for theme switching. Receives a theme_name string and will apply it to the app stylesheet when implemented. |

## File Responsibilities — App Layer — Models

| File | Contains |
|---|---|
| app/models/services/pdf_document.py | PDFDocument dataclass — holds full_text and metadata for an uploaded PDF. |
| app/models/services/llm_transaction/chat_message.py | ChatMessage dataclass — a single role + content pair stored in AppState.messages. |
| app/models/state/app_state.py | AppState dataclass — holds state.pdf (optional PDFDocument), state.messages (chat history), and state.error. |
| app/models/state/app_state_store.py | Future/planned only. |
| app/models/state/app_error.py | Future/planned only. |

## File Responsibilities — UI Layer

| File | Contains |
|---|---|
| ui/ui_composer.py | UIComposer — builds all components and controllers, returns UIBundle. |
| ui/ui_bundle.py | UIBundle frozen dataclass — holds refs to all component controllers. |
| ui/toolbar/toolbar_component.py | Toolbar UI — Upload button, filename label, Clear button. |
| ui/toolbar/toolbar_controller.py | Filename display, Clear button state, signal binding. |
| ui/toolbar/widgets/upload_button_widget.py | Upload button widget. |
| ui/toolbar/widgets/filename_label_widget.py | Filename label widget — displays name of currently loaded PDF. |
| ui/toolbar/widgets/clear_button_widget.py | Clear button widget. |
| ui/toolbar/widgets/theme_combo_widget.py | Theme selector dropdown widget. |
| ui/file_picker/file_picker.py | FilePickerComponent. |
| ui/file_picker/file_picker_controller.py | Opens PDF picker dialog. |
| ui/status_bar/status_bar_component.py | Error banner UI — icon, message label, dismiss button. |
| ui/status_bar/status_bar_controller.py | Show/hide error banner. |
| ui/chat_area/chat_area_component.py | Scrollable chat area UI — bubble container. |
| ui/chat_area/chat_area_controller.py | Bubble management, scroll, placeholder. |
| ui/chat_area/widgets/message_bubble_widget.py | Single message bubble. |
| ui/chat_area/widgets/placeholder_widget.py | Empty state icon and hint text. |
| ui/input_bar/input_bar_component.py | Input field and Send button UI. |
| ui/input_bar/input_bar_controller.py | Read input, clear input, enable/disable. |
| ui/input_bar/widgets/button_widget.py | Send button widget. |
| ui/input_bar/widgets/text_input_widget.py | Text input widget. |

## File Responsibilities — Services — PDF

| File | Contains |
|---|---|
| services/pdf/pdf_controller.py | PDFController — receives file path, calls PDFService, returns PDFDocument. |
| services/pdf/pdf_service.py | PDFService — raw PyMuPDF text extraction, simple types only. |

## File Responsibilities — Services — LLM

| File | Contains |
|---|---|
| services/llm/llm_controller.py | LLMController — receives LLMRequest and available tools list. Calls LLMService.call_with_tool_list(), parses the raw message, and returns LLMResponse (answer, tool_calls, or error). |
| services/llm/llm_service.py | LLMService — raw OpenAI API calls. call() for plain messages; call_with_tool_list() for tool-enabled requests. Returns model_dump() of the assistant message. |
| services/llm/llm_request.py | LLMRequest — builds and owns running_messages: [system_prompt] + chat_history + [user_question]. add_message() appends assistant tool-call messages; add_tool_result() appends tool result messages. |
| services/llm/llm_response.py | LLMResponse — holds final_answer, tool_calls, or error. Convenience checks: has_answer(), has_tool_calls(), has_error(). |
| services/llm/utils/openai_formatter.py | OpenAIFormatter — formats ChatMessage to dict; formats list of ToolDefinition into OpenAI function-calling schema. |

## File Responsibilities — Services — MCP

| File | Contains |
|---|---|
| services/mcp/controller.py | MCPToolController — generic controller for all MCP tool calls. Receives tool name and arguments, delegates to SyncConnection, always returns a plain dict (parsed result or structured error). Never raises exceptions. |
| services/mcp/tool_registry.py | MCPToolRegistry — loads all ToolDefinition objects from tools_json directory. Returns list of ToolDefinition via getAllMCPTools(). |
| services/mcp/models/mcp_tool_definition.py | ToolParameter and ToolDefinition Pydantic models — define the shape of each MCP tool exposed to the LLM. |
| services/mcp/clients/client_async.py | MCPConnectionClient — async MCP client. Probes TCP before connecting (_probe_tcp) to prevent anyio/asyncio teardown crash. Manages streamablehttp_client context and ClientSession lifecycle. |
| services/mcp/clients/client_sync.py | SyncConnection — wraps MCPConnectionClient in asyncio.run(). Exposes synchronous run(tool_name, arguments). Tracks connected, tool_called, and closed status for error diagnosis. |
| services/mcp/tools_json/tool_get_directory.json | Tool definition JSON — get_documents_directory: returns the working documents directory path. No input parameters. |
| services/mcp/tools_json/tool_list_pdfs.json | Tool definition JSON — list_pdfs_in_directory: returns list of PDF file paths in a given directory. Input: directory_path. |
| services/mcp/tools_json/tool_read_pdf.json | Tool definition JSON — read_pdf_content: returns full extracted text from a PDF. Input: pdf_path. |

## File Responsibilities — Services — Wiring

| File | Contains |
|---|---|
| services/service_composer.py | ServiceComposer — instantiates PDFService, PDFController, SyncConnection, MCPToolController, LLMService, LLMController (with formatted tool list). Returns ServiceBundle. |
| services/service_bundle.py | ServiceBundle frozen dataclass — holds refs to PDFController, LLMController, and MCPToolController. |

## File Responsibilities — Configuration

| File | Contains |
|---|---|
| conf/settings/config_bundle.py | AppSettings — aggregates AppConfig, OpenAIConfig, and MCPConfig into a single settings object. |
| conf/settings/appConfig.py | AppConfig — Pydantic settings loaded from conf/env/.env.app. Holds app_name. |
| conf/settings/openAI.py | OpenAIConfig — Pydantic settings loaded from .env.openAI. Holds api_key, model, llm_temperature, llm_max_tokens. |
| conf/settings/mcp.py | MCPConfig — Pydantic settings loaded from .env.mcp. Holds mcp_server_url. |
| conf/env/.env.app | Environment values for shared app settings used by AppConfig. |
| conf/env/.env.openAI | Environment values for OpenAI settings used by OpenAIConfig. |
| conf/env/.env.openAI.example | Example OpenAI environment file template. |
| conf/env/.env.mcp | Environment values for MCP server settings used by MCPConfig. Holds MCP_SERVER_URL. |


----


## Models
  - Use Pydantic only at boundaries where data comes from outside. Use dataclass for internal app models.
  - Use Pydantic if data comes from: JSON files, .env/config validation, external request/response formats
