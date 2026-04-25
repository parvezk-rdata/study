# Chat PDF — Step 03: Component Identification

> **Project**: Chat PDF Desktop App  
> **Stack**: PyQt6 + OpenAI GPT-4o-mini  
> **Step**: 03 of 16 — Identify the components needed for each GUI page

---

## Component Types

| Type | Meaning |
|------|---------|
| 🟣 Smart | Stateful — owns and manages state, reacts to events |
| 🟢 Dumb | Presentational — receives data as input, emits signals only |
| ⚪ Shared | Conditional / reused across multiple states |

---

## Zone Breakdown

The single application window is divided into **4 zones**. Each zone and its components are described below.

---

### Zone 1 — Toolbar

Always visible at the top of the window.

| Component | Type | Qt Base Class | Responsibility |
|-----------|------|---------------|----------------|
| `UploadButton` | 🟢 Dumb | `QPushButton` | Triggers the file-open dialog. Always enabled. |
| `PdfFileLabel` | 🟢 Dumb | `QLabel` | Displays the loaded PDF filename as a badge, or "No PDF loaded" placeholder text when empty. |
| `ClearButton` | 🟢 Dumb | `QPushButton` | Triggers the clear/reset action. Disabled when no PDF is loaded; enabled once a PDF is loaded. |

---

### Zone 2 — Status Bar *(conditionally visible)*

Sits between the toolbar and the chat area. Hidden by default; shown only when a PDF fails to load.

| Component | Type | Qt Base Class | Responsibility |
|-----------|------|---------------|----------------|
| `ErrorStatusBar` | ⚪ Shared | `QFrame` | Displays a red warning strip with an error message and a dismiss (✕) button. Shown on PDF load failure; hidden on dismiss or successful PDF load. |

---

### Zone 3 — Chat Area

The main content region. Scrollable. Switches between empty state and active conversation.

| Component | Type | Qt Base Class | Responsibility |
|-----------|------|---------------|----------------|
| `ChatWidget` | 🟣 Smart | `QScrollArea` | Owns and renders the full message list. Manages scroll position (auto-scrolls to bottom on new message). Switches between `EmptyStateWidget` and message bubbles. |
| `EmptyStateWidget` | 🟢 Dumb | `QWidget` | Centred icon + prompt text shown when no PDF is loaded and no messages exist. |
| `MessageBubble` | 🟢 Dumb | `QFrame` | Single reusable bubble widget. Accepts `role` (`user` \| `ai`) to switch alignment and colour. User variant: right-aligned, blue background. AI variant: left-aligned, neutral background. |
| `TypingIndicator` | ⚪ Shared | `QWidget` | Animated 3-dot widget. Shown while an API call is in-flight; hidden once the response arrives. |
| `ErrorBubble` | ⚪ Shared | `QFrame` | Red left-aligned bubble injected into the chat stream when an API or network error occurs. |

---

### Zone 4 — Input Bar

Always visible at the bottom of the window. Fully disabled until a PDF is loaded.

| Component | Type | Qt Base Class | Responsibility |
|-----------|------|---------------|----------------|
| `InputBar` | 🟣 Smart | `QWidget` | Parent container for the input field and send button. Owns the enabled/disabled state of both children together. Emits a `message_submitted` signal. |
| `MessageInput` | 🟢 Dumb | `QTextEdit` | Multi-line text entry field. Clears itself after submission. Enter key triggers send (Shift+Enter for newline). |
| `SendButton` | 🟢 Dumb | `QPushButton` | Triggers message submission. Disabled while a request is in-flight to prevent double-sends. |

---

## Full Component List (Summary)

| # | Component | Zone | Type | Qt Base Class |
|---|-----------|------|------|---------------|
| 1 | `UploadButton` | Toolbar | 🟢 Dumb | `QPushButton` |
| 2 | `PdfFileLabel` | Toolbar | 🟢 Dumb | `QLabel` |
| 3 | `ClearButton` | Toolbar | 🟢 Dumb | `QPushButton` |
| 4 | `ErrorStatusBar` | Status Bar | ⚪ Shared | `QFrame` |
| 5 | `ChatWidget` | Chat Area | 🟣 Smart | `QScrollArea` |
| 6 | `EmptyStateWidget` | Chat Area | 🟢 Dumb | `QWidget` |
| 7 | `MessageBubble` | Chat Area | 🟢 Dumb | `QFrame` |
| 8 | `TypingIndicator` | Chat Area | ⚪ Shared | `QWidget` |
| 9 | `ErrorBubble` | Chat Area | ⚪ Shared | `QFrame` |
| 10 | `InputBar` | Input Bar | 🟣 Smart | `QWidget` |
| 11 | `MessageInput` | Input Bar | 🟢 Dumb | `QTextEdit` |
| 12 | `SendButton` | Input Bar | 🟢 Dumb | `QPushButton` |

**Total: 12 components** — 2 smart, 7 dumb, 3 shared/conditional.

---

## Visibility Rules

| Component | Default State | Shown When | Hidden When |
|-----------|--------------|------------|-------------|
| `ErrorStatusBar` | Hidden | PDF fails to load | User dismisses it / new PDF loads successfully |
| `EmptyStateWidget` | Visible | No PDF loaded, no messages | PDF is loaded |
| `TypingIndicator` | Hidden | API call in-flight | Response received / error occurs |
| `ErrorBubble` | N/A | API or network error | — (stays in chat history) |
| `ClearButton` | Disabled | — | PDF is not loaded |
| `InputBar` (+ children) | Disabled | — | PDF is not loaded |
| `SendButton` | Enabled | — | API call in-flight |

---

## Notes

- `MessageBubble` is a **single component with two variants** (`user` and `ai`), not two separate classes. The `role` parameter controls alignment, colour, and corner rounding.
- `InputBar` is a **smart wrapper** — it is the single source of truth for whether the input area is active. `MessageInput` and `SendButton` never manage their own enabled state independently.
- `ChatWidget` is responsible for **auto-scroll** — every time a new bubble or the `TypingIndicator` is added, it scrolls to the bottom.
- `ErrorBubble` is **not dismissible** — it becomes part of the permanent conversation history so the user can see which message triggered the failure.

---

*Chat PDF — Design Documentation | Step 03 of 16*
