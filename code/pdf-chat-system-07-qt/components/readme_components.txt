
01).  PDFPanelComponent(QVBoxLayout) : QLabel(3), QPushButton(1)


                ┌────────── QWidget :  ( container )  ──────────────┐
                │                                                   │
                │  ┌─── QVBoxLayout [spacing=8, margin=0]──────┐    │
                │  │                                           │    │
                │  │  📝 QLabel        _title_label            │    │
                │  │  📝 QLabel        _file_label             │    │
                │  │  [ QPushButton ]  _upload_button          │    │
                │  │  📝 QLabel        _info_label             │    │
                │  │  [ QPushButton ]  _clear_chat_button      │    │ 
                │  │  [ QPushButton ]  _remove_pdf_button      │    │
                │  │                                           │    │
                │  │  ~ ~ ~ ~ ~ ~ ~  addStretch(1)  ~ ~ ~ ~ ~  │    │
                │  └───────────────────────────────────────────┘    │
                │                                                   │
                └───────────────────────────────────────────────────┘
                  
               
----------------------------------------------------------------------------------------------------
 
02). ChatHistoryComponent(QVBoxLayout) : QScrollArea, QWidget(QVBoxLayout), ChatMessageComponent

        ┌────────── QWidget : ( container )  ────────────────────────────────────────┐
        │                                                                            │
        │  ┌─── QVBoxLayout (_layout) [margins: 0,0,0,0] ─────────────────────────┐  │
        │  │                                                                      │  │
        │  │  ┌─── QScrollArea (_scroll_area) ───────────────────────────────┐    │  │
        │  │  │  setWidgetResizable(True)                                    │    │  │
        │  │  │                                                              │    │  │
        │  │  │  ┌─── QWidget (_container) ───────────────────────────────┐  │    │  │
        │  │  │  │                                                        │  │    │  │
        │  │  │  │  ┌─── QVBoxLayout (_messages_layout) [8px margins] ─┐  │  │    │  │
        │  │  │  │  │  [spacing: 10px]                                 │  │  │    │  │
        │  │  │  │  │                                                  │  │  │    │  │
        │  │  │  │  │  ~ ~ ~ ~ ~ ~ addStretch(1) ~ ~ ~ ~ ~ ~ ~         │  │  │    │  │
        │  │  │  │  │  ┌── ChatMessageComponent ───────────────────┐   │  │  │    │  │
        │  │  │  │  │  │  header_text                              │   │  │  │    │  │
        │  │  │  │  │  │  content_text                             │   │  │  │    │  │
        │  │  │  │  │  └───────────────────────────────────────────┘   │  │  │    │  │
        │  │  │  │  │  ┌── ChatMessageComponent ──────────────────┐    │  │  │    │  │
        │  │  │  │  │  │  header_text                             │    │  │  │    │  │
        │  │  │  │  │  │  content_text                            │    │  │  │    │  │
        │  │  │  │  │  └──────────────────────────────────────────┘    │  │  │    │  │
        │  │  │  │  │  ┌── ChatMessageComponent ──────────────────┐    │  │  │    │  │
        │  │  │  │  │  │  header_text                             │    │  │  │    │  │
        │  │  │  │  │  │  content_text                            │    │  │  │    │  │
        │  │  │  │  │  └──────────────────────────────────────────┘    │  │  │    │  │
        │  │  │  │  │                                                  │  │  │    │  │
        │  │  │  │  └──────────────────────────────────────────────────┘  │  │    │  │
        │  │  │  └────────────────────────────────────────────────────────┘  │    │  │
        │  │  └──────────────────────────────────────────────────────────────┘    │  │
        │  │                                                                      │  │
        │  └──────────────────────────────────────────────────────────────────────┘  │
        │                                                                            │
        └────────────────────────────────────────────────────────────────────────────┘

        _BottomScrollEventFilter (installed on _container)
        ┌─────────────────────────────────────────────────────────┐
        │  Watches for:  Resize / LayoutRequest / Show events     │
        │  Reacts with:  _do_scroll_to_bottom()                   │
        └─────────────────────────────────────────────────────────┘

        scroll_to_bottom() fires _do_scroll_to_bottom() 3 times:
        ├── QTimer  0ms   (immediate, next event loop tick)
        ├── QTimer  50ms  (after layout settles)
        └── QTimer 150ms  (after rendering fully completes)


              
----------------------------------------------------------------------------------------------------

03). ChatInputComponent

        ┌────────── QWidget : ( container )  ────────────────────────────────────────┐
        │                                                                            │
        │  ┌─── QHBoxLayout [margins: 0,0,0,0] [spacing: 8px] ────────────────────┐  │
        │  │                                                                      │  │
        │  │  ┌─── QLineEdit  ────────────────────────────────┐──────────────┐    │  │
        │  │  │  stretch=1 (fill available space)             │ QPushButton  │    │  │
        │  │  │                                               │ stretch=0    │    │  │
        │  │  └───────────────────────────────────────────────┘──────────────┘    │  │
        │  │                                                      original size   │  │
        │  └──────────────────────────────────────────────────────────────────────┘  │
        └────────────────────────────────────────────────────────────────────────────┘

  Signals:
  ├── _send_button.clicked   ──┐
  │                            ├──► _emit_send() ──► send_requested.emit(input.text())
  └── _input.returnPressed   ──┘

               
----------------------------------------------------------------------------------------------------
 
04). ChatMessageComponent

                ┌────────── QWidget : ( container )  ───────────────────────┐
                │                                                           │
                │  ┌─── QVBoxLayout  [margins: 8,8,8,8] [spacing: 4px]───┐  │
                │  │                                                     │  │
                │  │  📝 QLabel wordWrap = True                          │  │
                │  │     "You"  /  "Assistant"                           │  │
                │  │                                                     │  │
                │  │            [4px gap]                                │  │
                │  │                                                     │  │
                │  │  📝 QLabel wordWrap = True                          │  │
                │  │     Question / LLM Response                         │  │
                │  │                                                     │  │
                │  └─────────────────────────────────────────────────────┘  │
                └───────────────────────────────────────────────────────────┘

                One ChatMessageComponent = one message bubble:
                ┌───────────────────────────────┐
                │  You                          │  ← _header_label
                │  What is PyQt6?               │  ← _content_label
                └───────────────────────────────┘
                ┌───────────────────────────────┐
                │  Assistant                    │  ← _header_label
                │  PyQt6 is a Python binding... │  ← _content_label
                └───────────────────────────────┘
 
----------------------------------------------------------------------------------------------------
 
05).
┌────────── QMainWindow : [1100 x 700] ────────────────────────────────────┐
│                                                                          │
│  ┌─── QHBoxLayout ────────────────────────────────────────────────────┐  │
│  │                                                                    │  │
│  │  ┌─ QFrame [290px] [stretch=0]───┐ ┌─── QWidget [stretch=1] ─────┐ │  │
│  │  │                               │ │                             │ │  │
│  │  │┌─── PDFPanelComponent ─────┐  │ │  ┌─ ChatHistoryComponent ─┐ │ │  │
│  │  ││                           │  │ │  │                        │ │ │  │
│  │  ││                           │  │ │  │       [stretch=1]      │ │ │  │
│  │  ││                           │  │ │  │                        │ │ │  │
│  │  │└───────────────────────────┘  │ │  │                        │ │ │  │
│  │  │                               │ │  │                        │ │ │  │
│  │  │~ ~ ~ ~ addStretch(1) ~ ~ ~    │ │  └────────────────────────┘ │ │  │
│  │  │                               │ │                             │ │  │
│  │  │                               │ │  ┌─ ChatInputComponent ───┐ │ │  │                             
│  │  │                               │ │  │      [stretch=0]       │ │ │  │
│  │  │                               │ │  └────────────────────────┘ │ │  │
│  │  │                               │ │                             │ │  │
│  │  └───────────────────────────────┘ └─────────────────────────────┘ │  │
│  │                                                                    │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘




