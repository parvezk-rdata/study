

## Domain Models

### `PDFDocument`

| Field | Type | Description |
|---|---|---|
| `filename` | `str` | Display name e.g. `annual_report_2024.pdf` |
| `full_text` | `str` | Full extracted text sent as system context |

---

### `ChatMessage`

| Field | Type | Description |
|---|---|---|
| `role` | `str` | `"user"` or `"assistant"` |
| `content` | `str` | Message text |

---

## State Models

### `AppState`

| Field | Type | Description |
|---|---|---|
| `pdf` | `PDFDocument \| None` | `None` = no PDF loaded |
| `messages` | `list[ChatMessage]` | Full conversation history (in-memory) |
| `is_loading` | `bool` | `True` while waiting for API response |
| `error` | `AppError \| None` | Current active error, or `None` |

---

### `AppError`

| Field | Type | Description |
|---|---|---|
| `kind` | `ErrorKind` | `PDF_LOAD` or `API_FAILURE` or `EMPTY_QUERY` |
| `message` | `str` | Human-readable error text shown in UI |

---

### `ErrorKind` (Enum)

| Value | Display Location | Description |
|---|---|---|
| `PDF_LOAD` | `StatusBarComponent` banner | Shown when PDF fails to load |
| `API_FAILURE` | `ChatAreaComponent` inline red bubble | Shown when OpenAI API call fails |
| `EMPTY_QUERY` | `ChatAreaComponent` inline red bubble | Shown when user sends empty message |
