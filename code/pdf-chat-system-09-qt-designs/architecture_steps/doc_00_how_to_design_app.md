
To build a "Chat PDF" App and following is the workflow steps. we will discuss  and complete one step at a time till we complete the code. Use python, openai key

### 🧭 GUI App Development Workflow

01. **Gather requirements**  - Define use cases, expected functionality, functional and non-functional requirements, and make initial architectural decisions.

02. **Define controller architecture(roles of):**  
   
    - MainController  
    - ComponentController  
    - DomainController  
    - Components  

    Also define communication via signals and whether state change trigger events or not(state-driven UI updates)

03. **Design GUI pages on paper**  
    Decide how many pages/screens are needed and what each page does.

04. **Group UI widgets into application components**  
   
    - Identify application components needed for each GUI page.  
    - UI Widgets are basic elements(Button, Input).  
    - Application components are UI units built using widgets, just like react components we make. 

05. **Design component hierarchy**  - Decide parent/child relationships and smart vs dumb components.

06. **For each application component, prepare a table:**  
   
    - Type: Input / Output / Static  
    - Data required for rendering  
    - Data type  
    - Domain data or UI state  
    - Mapping to models  

    Note : Table needs to be prepared for  application component and not for UI widgets.

07. **Derive models from component data**  
    - Domain models  
    - State models  

08. List all user events that can occur across the app. Each use case typically maps to one or more user events.

09. **Define event flow for each event** - Describe step-by-step what happens when each event occurs.

10. **Identify domain controllers** - Determine business logic and external service handlers.

11. **Assign responsibilities to**  
    - MainController  
    - ComponentController  
    - DomainController  
    - Components  

12. **Define directory structure**  - Organize the application into logical folders and modules.

13. **Implement UI components** - Build application components based on the GUI design.

14. **Create MainController skeleton** - Add one method per user event.

15. **Document event logic inside methods**   - Add comments describing event flow steps.

16. **Identify methods in domain_controllers and component_controllers**  - Add comments describing task to be done.

17. **Implement**  
    - DomainControllers  
    - MainController  
    - ComponentControllers  
    - Final component wiring if any

---

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