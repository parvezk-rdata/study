

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