

### Workflow

01. Gather requirements — define use cases and expected functionality
02. Decide if we want state changes to trigger events or not(state-driven UI updates).
03. Design GUI pages on paper. Deide how many pages and what they will do.
04. Identify the components needed for each GUI page
05. Design the component hierarchy — decide which components are smart vs dumb, and their parent/child relationships
06. Identify the data needed and what components are affected by it.
07. Model the data — define domain models  (e.g. Message, PdfDocument)
08. Model the data — define state models   (e.g. AppState)
09. Map that data to application state
10. List all user events that can occur across the app. Each use case typically maps to one or more user events.
11. For each event, define the steps that will happen (refer: Generic Event Flow)
12. Identify domain controllers needed to handle business logic or external services
13. Identify directory structure for the app.
14. Write components based on the GUI design
15. Write main_controller with one blank method per event
16. Inside each blank method, add comments describing the steps from step 10
17. Decide which tasks belong to component_controllers and which belong to domain_controllers
18. Implement method bodies, starting with domain_controllers, then main_controller, then component_controllers


## Smart vs Dumb Components

| | 🟣 Smart Component | 🟢 Dumb Component |
|---|---|---|
| **Owns state?** | Yes — holds and manages its own state | No — receives data from parent |
| **Qt signals** | Emits AND reacts to signals | Emits signals only (never listens) |
| **Business logic** | May contain some UI-level logic | None — only renders what it's given |
| **Talks to parent** | Yes — via signals upward | Yes — via signals upward only |
| **Reusability** | Low — tied to app context | High — works anywhere |
| **Examples in our app** | `ChatWidget`, `InputBar` | `MessageBubble`, `SendButton`, `PdfFileLabel` |
| **PyQt6 equivalent** | Widget that connects slots internally | Widget that just emits signals + paints |
| **Who decides appearance?** | Itself, based on its own state | Its parent, by passing in data |

> **Simple rule of thumb:** if a component *knows* something about the app, it's smart. If it just *shows* something it was told, it's dumb.

---

### Key Principle
> This follows a **top-down, outside-in** philosophy — design intent before implementation, which scales well for larger apps.