# Step 11 — Components and Component Controllers

---

## Components and their Controllers

| Component | Controller | Smart / Dumb |
|---|---|---|
| `ToolbarComponent` | `ToolbarController` | Smart |
| `StatusBarComponent` | `StatusBarController` | Smart |
| `ChatAreaComponent` | `ChatAreaController` | Smart |
| `InputBarComponent` | `InputBarController` | Smart |
| `PlaceholderWidget` | — | Dumb |
| `MessageBubbleWidget` | — | Dumb |
| `LoadingBubbleWidget` | — | Dumb |

---

## `ToolbarController`

| Method | Description |
|---|---|
| `get_file_path()` | Open native file picker filtered to `.pdf`, return selected path or `None` if cancelled |
| `show_pdf_details(filename)` | Render PDF filename label in toolbar |
| `enable_clear()` | Enable the Clear button |
| `disable_clear()` | Disable the Clear button |

---

## `StatusBarController`

| Method | Description |
|---|---|
| `show_error(message)` | Show error banner with message text |
| `hide()` | Hide the status bar |

---

## `ChatAreaController`

| Method | Description |
|---|---|
| `show_placeholder()` | Show empty state placeholder (icon + hint text) |
| `hide_placeholder()` | Hide placeholder |
| `add_user_bubble(text)` | Render a right-aligned user message bubble |
| `add_assistant_bubble(text)` | Render a left-aligned assistant message bubble |
| `add_error_bubble(message)` | Render an inline red error bubble |
| `show_loading()` | Show `• • •` loading bubble |
| `hide_loading()` | Hide loading bubble |
| `clear_bubbles()` | Remove all message bubbles from chat area |
| `scroll_to_bottom()` | Scroll chat area to latest message |

---

## `InputBarController`

| Method | Description |
|---|---|
| `get_text()` | Read and return current text from input field |
| `clear_input()` | Clear the input field |
| `enable()` | Enable input field and Send button |
| `disable()` | Disable input field and Send button |