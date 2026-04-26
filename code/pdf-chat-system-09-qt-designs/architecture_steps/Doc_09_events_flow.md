
## ⚡ User Events

| No.| Event Name               | Description                                                                                   |
| ---| ------------------------ | --------------------------------------------------------------------------------------------- |
| 2  | `upload_pdf_requested`   | Open a file picker dialog box.|
| 3  | `remove_pdf_requested`   | User removes selected PDF |
| 4  | `send_message_requested` | User ask a question to llm based on uploaded PDF and receives answer|
| 5  | `clear_chat_requested`   | Clear all Question and theor answers from UI.|
| 6  | `pdf_file_selected`      | Select a pdf and upload its information in UI.|

---

## Generic Event Flow

1. **Capture user event**
2. **Collect required input**
3. **Validate input**
4. **Run domain operation**
5. **Convert domain result into state data**
6. **Update store/state**
7. **Decide affected UI sections**
8. **Render affected components**
9. **Show status/result**

---

## `Event` : `upload_pdf_requested`

Trigger: User clicks "Upload PDF"

|No | Label        | Description                                                                 |
|-- |--------------|-----------------------------------------------------------------------------|
|1  | Update UI    | Render PDF file picker                                                      |

---

### E-02 · `pdf_loaded`
User selects a valid `.pdf` file from the file picker.

| No | Label | Description |
|---|---|---|
| 1 | Read Data | Read file path return by event |
| 2 | Parse PDF | Extract full text from PDF file using PyMuPDF |
| 3 | Update State | PDF information(text, page count, truncation)|
| 4 | Update State | Clear chat history |
| 5 | Update State | Clear errors |
| 7 | Update UI | Render PDF details |
| 8 | Update UI | Render chat history (empty) |
| 9 | Update UI | Dismiss any previous error |
|10 | Update UI | Render component to ask question |

-----


## `Event` : `pdf_file_selected`

Trigger: User selects a PDF file from the file picker

|No | Label        | Description                                                                 |
|-- |--------------|-----------------------------------------------------------------------------|
|1  | Read Data    | PDF file path                                                               |
|2  | Decide       | If the file is the same as previous, set status message and end flow |
|1  | Validate     | Check and generate errors before text extraction                            |
|3  | Create Obj   | PDFDocument(text, page count, truncation) from PDF                          |
|4  | Update State | Set current document data                                                   |
|5  | Update State | Clear chat history                                                          |
|6  | Update UI    | Render chat history (empty)                                                 |
|7  | Update UI    | Render PDF details                                                          |
|8  | Update UI    | Indicate PDF is loaded (status/message)                                     |

---

## `Event` : `remove_pdf_requested`

Trigger: User clicks "Remove PDF"

|No | Label        | Description                                      |
|---|--------------|--------------------------------------------------|
|1  | Update State | Clear current document                           |
|2  | Update State | Clear chat history                               |
|3  | Update UI    | Render chat history (empty)                      |
|4  | Update UI    | Render PDF section (no PDF selected state)       |
|5  | Update UI    | Disable chat input                               |
|6  | Update UI    | Indicate PDF is removed (status/message)         |

---

## `Event` : `clear_chat_requested`

Trigger: User clicks "Clear conversation"

|No | Label        | Description                              |
|---|--------------|------------------------------------------|
|1  | Update State | Clear chat history                       |
|2  | Update UI    | Render chat history (empty)              |
|3  | Update UI    | Clear chat input                         |
|4  | Update UI    | Indicate chat is cleared (status/message)|
---

## `Event` : `send_message_requested`


Trigger: User submits a message

| Index | Label        | Description                                                                 |
|------:|-------------|-----------------------------------------------------------------------------|
| 1     | Input       | User message text                                                           |
| 2     | Decide      | If message is empty, set status message and end flow                        |
| 3     | Decide      | If no PDF is loaded, set status message and end flow                        |
| 4     | Update State| Add user message to chat history                                            |
| 5     | Update UI   | Render chat history (with user message)                                     |
| 6     | Update UI   | Indicate processing (e.g., "Thinking...")                                   |
| 7     | Invoke LLM  | Generate response using current document and chat history                   |
| 8     | Update State| Add assistant response to chat history                                      |
| 9     | Update UI   | Render chat history (with assistant response)                               |
| 10    | Update UI   | Clear chat input                                                            |
| 11    | Update UI   | Indicate response is ready (status/message)                                 |

---

## 🔄 state change reactions

| Reactions          | Description                                                                 |
| ------------------ | --------------------------------------------------------------------------- |
| `document_changed` | Document updated or cleared → UI updates document panel and input state.    |
| `chat_changed`     | Chat history updated → chat UI re-renders message list.                     |
| `status_changed`   | Status message updated → status bar reflects current operation.             |

---

## ❗ System / Internal Reactions

| Event Name         | Description                                                                 |
| ------------------ | --------------------------------------------------------------------------- |
| `pdf_load_failed`  | PDF loading fails → status updated → UI remains in previous stable state.   |


---