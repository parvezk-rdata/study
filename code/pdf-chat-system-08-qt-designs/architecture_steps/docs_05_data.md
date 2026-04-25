

# Chat PDF — Step 05: Component Data Needs

> **Project**: Chat PDF Desktop App  
> **Stack**: PyQt6 + OpenAI GPT-4o-mini  
> **Step**: 05 of 16 — For each component, identify what data it needs to display correctly

---

## Consolidated Field Summary

All unique data fields across all 12 components:

| # | Field | Type | Consumed By |
|---|-------|------|-------------|
| 1 | `pdf_filename` | `str \| None` | `PdfFileLabel` |
| 2 | `pdf_loaded` | `bool` | `ClearButton`, `ChatWidget`, `InputBar` |
| 3 | `messages` | `list[Message]` | `ChatWidget` |
| 4 | `is_busy` | `bool` | `UploadButton`, `ChatWidget`, `InputBar` |
| 5 | `error_message` | `str \| None` | `ErrorStatusBar` |
| 6 | `role` | `"user" \| "ai"` | `MessageBubble` |
| 7 | `content` | `str` | `MessageBubble`, `ErrorBubble` |
| 8 | `input_text` | `str` | `MessageInput`, `SendButton` |
| 9 | `is_enabled` | `bool` | `MessageInput`, `SendButton` (derived, passed from `InputBar`) |

**Total: 9 unique fields** across 12 components.

---

## 📂 Project Structure

```
MainWindow  (QMainWindow)  🟣 smart
├── Toolbar zone
│   ├── UploadButton       🟢 dumb
│   ├── PdfFileLabel       🟢 dumb
│   └── ClearButton        🟢 dumb
│
├── ErrorStatusBar         ⚪ shared / conditional
│
├── ChatWidget             🟣 smart
│   ├── EmptyStateWidget   🟢 dumb
│   ├── MessageBubble      🟢 dumb  (user & ai variants)
│   ├── TypingIndicator    ⚪ shared / conditional
│   └── ErrorBubble        ⚪ shared / conditional
│
└── InputBar               🟣 smart
    ├── MessageInput       🟢 dumb
    └── SendButton         🟢 dumb

```


## Data Per Component

### Zone 1 — Toolbar

| Component | Field | Type | Purpose |
|-----------|-------|------|---------|
| `UploadButton` | `is_busy` | `bool` | Disabled while an API call is in-flight |
| `PdfFileLabel` | `pdf_filename` | `str \| None` | Shown as filename badge; `None` shows "No PDF loaded" |
| `ClearButton` | `pdf_loaded` | `bool` | Enabled only when a PDF is loaded |

---

### Zone 2 — Status Bar

| Component | Field | Type | Purpose |
|-----------|-------|------|---------|
| `ErrorStatusBar` | `error_message` | `str \| None` | Text to display in the bar; `None` = widget is hidden |

---

### Zone 3 — Chat Area

| Component | Field | Type | Purpose |
|-----------|-------|------|---------|
| `ChatWidget` | `messages` | `list[Message]` | Full ordered conversation history to render |
| `ChatWidget` | `is_busy` | `bool` | Whether to show `TypingIndicator` at the bottom |
| `ChatWidget` | `pdf_loaded` | `bool` | Whether to show `EmptyStateWidget` or message list |
| `EmptyStateWidget` | *(none)* | `—` | Static widget — no dynamic data needed |
| `MessageBubble` | `role` | `"user" \| "ai"` | Controls alignment and background colour |
| `MessageBubble` | `content` | `str` | The message text to render inside the bubble |
| `TypingIndicator` | *(none)* | `—` | Shown/hidden by parent; self-animates |
| `ErrorBubble` | `content` | `str` | Error message text to display inline in chat |

---

### Zone 4 — Input Bar

| Component | Field | Type | Purpose |
|-----------|-------|------|---------|
| `InputBar` | `pdf_loaded` | `bool` | Enables/disables the entire input bar |
| `InputBar` | `is_busy` | `bool` | Disables Send button while request is in-flight |
| `MessageInput` | `is_enabled` | `bool` | Passed down from `InputBar` |
| `MessageInput` | `input_text` | `str` | Current typed text; cleared on submit |
| `SendButton` | `is_enabled` | `bool` | Passed down from `InputBar` |
| `SendButton` | `input_text` | `str` | Non-empty = enabled; empty = disabled |

---

## Key Observations

**`pdf_loaded`, `is_busy`, and `messages` are consumed by multiple components** across different zones. This is a strong signal that they belong to shared app-level state owned by `MainWindow`, not by any individual component.

**`EmptyStateWidget` and `TypingIndicator` need no data.** They are purely visibility-controlled — shown or hidden by their parent `ChatWidget` based on its own state.

**`is_enabled` is a derived field**, not a raw state value. `InputBar` computes it from `pdf_loaded` and `is_busy` and passes it down to `MessageInput` and `SendButton`.

**`role` and `content` are instance-level fields** — they belong to each individual `MessageBubble` instance and come from the `Message` model, not from global app state.

**`error_message` is separate from `messages`** — PDF load errors are not part of the conversation history and live in their own field driving `ErrorStatusBar`.

---

## The `Message` Model (preliminary)

`ChatWidget` consumes a `list[Message]`. Based on the fields needed by `MessageBubble` and `ErrorBubble`, the `Message` model needs at minimum:

```python
@dataclass
class Message:
    role: str       # "user" | "ai" | "error"
    content: str    # text to display
```

> Full state modelling will be covered in **Step 07 — Model the state using appropriate classes/models**.

---

*Chat PDF — Design Documentation | Step 05 of 16*