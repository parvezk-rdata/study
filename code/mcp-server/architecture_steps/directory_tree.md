

```

mcp-server/
├── README.md
├── main.py
├── requirements.txt
│
├── conf/
│   └── settings.py
│
├── controllers/
│   └── extract_pdf_text_controller.py
│
├── models/
│   ├── request/
│   │   └── extract_pdf_text_request.py
│   └── response/
│       └── extract_pdf_text_response.py
│
├── server/
│   └── pdf_reader_server.py
│
├── services/
│   ├── pdf_reader.py
│   └── pdf_validator.py
│
├── tools/
│   └── extract_pdf_text_tool.py
│
├── utils/
│   └── result.py
│
├── architecture_steps/
│   ├── correct_directory_tree.md
│   ├── directory_tree.md
│   ├── diagrams/
│   │   ├── d_01_mcp_flow.svg
│   │   └── mcp_controller_architecture.svg
│   └── flow/
│
└── zz_test/
    ├── test_doc.pdf
    ├── test_doc.txt
    └── test_extract.py


```

```
get_documents_directory
    input: none
    output: directory path

list_pdfs_in_directory
    input: directory_path
    output: list of PDF files

read_pdf_content
    input: pdf_path
    output: PDF text

search_pdf_content
    --> returns only relevant pages/chunks from one or more PDFs
    
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
