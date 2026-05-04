

```

mcp_servers/
│
└── pdf_reader/
    ├── main.py                     # Entry point
    ├── requirements.txt
    │
    ├── server/
    │   └── pdf_reader_server.py   # FastMCP setup + tool registration
    │
    ├── tools/
    │   └── extract_pdf_text_tool.py   # MCP tool (validation + orchestration)
    │
    ├── services/
    │   ├── pdf_reader.py          # Pure extraction (PyMuPDF)
    │   └── pdf_validator.py       # Path + file validation
    │
    ├── models/
    │   ├── request/
    │   │   └── extract_pdf_text_request.py
    │   │
    │   └── response/
    │       └── extract_pdf_text_response.py
    │
    └── conf/
        └── settings.py

```