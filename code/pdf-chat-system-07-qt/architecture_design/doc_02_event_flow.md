## 📁 Architecture Overview Of PDF Chat App

| No.| Component Type          | Description                                                                           |
| ---| ----------------------- | ------------------------------------------------------------------------------------- |
| 1  | `MainController`        | Composition root and orchestrator; coordinates all event flows and updates the store. |
| 2  | `Component Controllers` | Event-based UI handlers; update components based on instructions from MainController. |
| 3  | `Components`            | Dumb renderers; only display data and emit user interaction signals.                  |
| 4  | `File Dialog`           | Treated as a component; encapsulates file selection UI as a reusable abstraction.     |
| 5  | `Store`                 | Single source of truth; maintains application state and emits change events.          |
| 6  | `Domain Controllers`    | Handle pure business logic (no UI interaction, no direct store updates).              |

---
## ⚡ Application Lifecycle

| No. | Step Name        | Description                                                        |
| --- | ---------------- | ------------------------------------------------------------------ |
| 1   | `app_initialize` | Initializes controllers, connects signals, and renders initial UI. |


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


# Chat PDF App — High-Level Event Flows

---

## `app_initialize`

1. Start application
2. Create shared application state
3. Create services
4. Create main window
5. Create orchestrator
6. Create domain controllers
7. Create component controllers
8. Connect user events
9. Connect store events
10. Set static UI text
11. Read current state
12. Render initial UI
13. Show ready status

---

## `Event` : `upload_pdf_requested`

Trigger: User clicks "Upload PDF"

|No | Label        | Description                                                                 |
|-- |--------------|-----------------------------------------------------------------------------|
|1  | Update UI    | Render PDF file picker                                                      |

---

## `Event` : `pdf_file_selected`

Trigger: User selects a PDF file from the file picker

|No | Label        | Description                                                                 |
|-- |--------------|-----------------------------------------------------------------------------|
|1  | Input        | PDF file path                                                               |
|2  | Decide       | If the file is the same as the current document, set status message and end flow |
|3  | Create Obj   | Document data (text, page count, truncation) from PDF                       |
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