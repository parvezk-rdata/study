

```

mcp-server/
├── README.md
├── main.py
├── requirements.txt
│
├── server/
│   └── pdf_reader_server.py
│
└── tools/
    │
    ├── extract_pdf_text/
    |   ├── .env
    │   ├── request.py
    │   ├── response.py
    │   ├── pdf_reader.py
    │   ├── pdf_validator.py
    │   ├── settings.py
    │   ├── controller.py
    │   ├── tool.py
    │   └── test.py
    │
    ├── get_working_directory/
    |   ├── .env
    │   ├── response.py
    │   ├── settings.py
    │   ├── controller.py
    │   ├── tool.py
    │   └── test.py
    │
    ├── list_pdfs_in_directory/
    |   ├── .env
    │   ├── request.py
    │   ├── response.py
    │   ├── directory_scanner.py
    │   ├── settings.py
    │   ├── controller.py
    │   ├── tool.py
    │   └── test.py
    │
    └── read_pdf_content/
        ├── .env
        ├── request.py
        ├── response.py
        ├── pdf_reader.py
        ├── pdf_validator.py
        ├── settings.py
        ├── controller.py
    │   ├── tool.py
    │   └── test.py


```

## File Responsibilities

| File | Contains |
|---|---|
| `main.py` | Entry point. Starts the MCP server by importing and running the FastMCP instance. |
| `server/pdf_reader_server.py` | Creates FastMCP instance, registers MCP tools, and exposes them to MCP runtime. |
| `tools/extract_pdf_text_tool.py` | MCP-facing adapter. Validates request input, calls controller, returns Pydantic response (auto-serialized by FastMCP). |
| `controllers/extract_pdf_text_controller.py` | Orchestrates the use case. Validates PDF path, calls services, builds success/error response models. |
| `services/pdf_validator.py` | Validates PDF file path, extension, size, and existence. Returns error message or None. |
| `services/pdf_reader.py` | Reads PDF file using PyMuPDF and returns raw text and page count. |
| `models/request/extract_pdf_text_request.py` | Pydantic request model. Validates incoming MCP tool input (`pdf_path`). |
| `models/response/extract_pdf_text_response.py` | Pydantic response models. Defines success and error response structures returned by controller and tool. |
| `conf/settings.py` | Application configuration. Contains server name, file size limits, allowed extensions, and environment loading. |