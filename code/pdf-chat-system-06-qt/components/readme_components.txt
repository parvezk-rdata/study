
01). PDFSummaryComponent (Components/document)

┌────────── QWidget (Box or panel)──────────┐
│                                           │
│        [8px padding all around]           │
│                                           │
│  ┌─── QVBoxLayout ─────────────────────┐  │
│  │                                     │  │
│  │                                     │  │
│  │  📝 QLabel : " message "            │  │
│  │                                     │  │
│  │                                     │  │
│  │                                     │  │
│  └─────────────────────────────────────┘  │
│                                           │
└───────────────────────────────────────────┘

----------------------------------------------------------------------------------------------------

02). PDFInfoComponent (Components/document)

┌────────── QWidget (Box or panel)──────────┐
│                                           │
│        [8px padding all around]           │
│                                           │
│  ┌─── QVBoxLayout ─────────────────────┐  │   <-- 0 margin
│  │                                     │  │
│  │                                     │  │
│  │  📝 QLabel : " message "            │  │   <-- 8px gap between widgets
│  │                                     │  │
│  │  📝 QLabel : " message "            │  │
│  │                                     │  │
│  │                                     │  │
│  └─────────────────────────────────────┘  │
│                                           │
└───────────────────────────────────────────┘


── Before PDF loaded ──              ── After PDF loaded ──
                                    (only if truncated=True)
┌──────────────────────┐         ┌──────────────────────────────┐
│ PDF Info             │         │ PDF Info                     │
│                      │         │                              │
│ No PDF loaded        │         │ Pages: 12                    │
└──────────────────────┘         │ Method: pdfminer             │
                                 │ Characters: 45,231           │
                                 │                              │
                                 │ Warning: PDF exceeds...      │
                                 └──────────────────────────────┘
                                         

----------------------------------------------------------------------------------------------------
 03). PDFUploadComponent

┌────────── QWidget (box or panel) ─────────┐
│                                           │
│        [8px padding all around]           │
│                                           │
│  ┌─── QVBoxLayout ─────────────────────┐  │
│  │                                     │  │   <-- 0 margin
│  │  📝 QLabel : " message "            │  │
│  │                                     │  │
│  │  📝 QLabel : " message "            │  │   <-- 8px gap between widgets
│  │                                     │  │
│  │  📝 QPushButton                     │  │
│  │                                     │  │
│  └─────────────────────────────────────┘  │
│                                           │
└───────────────────────────────────────────┘


   Before Upload                         After Upload                            
  ┌─────────────────────────────────┐   ┌─────────────────────────────────┐     
  │  PDF  (bold 14px)               │   │  PDF  (bold 14px)               │     
  │                                 │   │                                 │     
  │  No PDF selected                │   │  report.pdf                     │     
  │                                 │   │                                 │     
  │  [ Upload PDF ]                 │   │  [ Upload PDF ]                 │     
  └─────────────────────────────────┘   └─────────────────────────────────┘     


----------------------------------------------------------------------------------------------------
 04). PDFUploadComponent