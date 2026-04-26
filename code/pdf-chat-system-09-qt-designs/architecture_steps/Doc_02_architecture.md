# Step 06: Controller Architecture
---

```
                         ┌──────────────────────┐
                         │  Domain Controller   │
                         └────────────┬─────────┘                
   User Interaction               ▲   │   
           │                      │   │           
           │                      │   │   
           ▼                      │   ▼   
      ┌─────────┐  event    ┌─────┴─────────┐        ┌────────────────────┐
      │Component│ →→→→→→→→→ │Main Controller│ →→→→→→ │Component Controller│
      └─────────┘           └───────────────┘        └─────────┬──────────┘
           ▲                                                   │
           │                                                   │           
           └───────────────────────────────────────────────────┘
```
---

## **Four Types Of Class**

| Class Type | Count | Responsibility |
|---|---|---|
| `Component` | Many | Render UI widgets. Emit signals. Nothing else. |
| `ComponentController` | One per smart component | Handle UI-only actions for their component |
| `DomainController` | One per service/domain | Handle business logic and external services |
| `MainController` | Exactly one | Orchestrate the full event flow across the app |

---

## Component( Key responsibilities )

- Dumb Renderer : Render data it is given via setter methods
- Emit a signal when a user interaction occurs
- Never call the controller directly
- Never read from or write to another component
- Do not make decisions about what happens next
- Do not call any controller method directly
- Do not access application state

---

## ComponentController ( Key responsibilities )

- A non-widget class that **manages one smart component**.
- Owns all UI-level logic for that component
- Expose clean action methods that `MainController` can call
- Manage internal UI state of its component (scroll position, bubble list, visibility)
- Never contain business logic (no PDF parsing, no API calls)
- Never communicate with other `ComponentController`s directly
- One controller per smart component (our app)
---

## DomainController (Key responsibilities)

- A plain class that **handles one domain of business logic or one external service**
- It knows nothing about the UI. Never update the UI directly
- Perform a specific business operation when called
- Return a result or raise a descriptive exception
- Never communicate with other `DomainController`s directly
- Never communicate with other `ComponentController`s directly
---

## MainController (Key responsibilities)

- The **single orchestrator** for the entire application.
- Only class that knows the full sequence of steps for every user event.
- Connect all component signals to handler methods on startup
- Define the complete step-by-step flow for every user event
- Call `DomainController`s for business logic
- Call `ComponentController`s to update the UI
- Handle errors and decide how to surface them
- Do not contain low-level UI code. Delegate to `ComponentController`
- Do not contain business logic (no PDF parsing, no API calls). Delegate to `DomainController`
---


## State Change Decision

### Decision: controller-driven UI updates (not state-driven / reactive)

For this app we chose a **simple controller-driven approach** over a reactive state pattern (like signals on a shared `AppState` object).

This means: **`MainController` explicitly calls `ComponentController` methods to update the UI** after every event. There is no observable state object that components watch automatically.

### Why this approach fits our app

| Factor | Reason |
|---|---|
| Small app | Only 4 user events, 12 components — reactive overhead not justified |
| Linear flows | Each event has a clear, predictable sequence of steps |
| Beginner-friendly | Explicit calls are easier to read, trace, and debug than reactive subscriptions |
| No cross-cutting state | No component needs to react to state it didn't directly cause |

### Rule
> Every UI update in this app is an **explicit method call** made by `MainController` or a `ComponentController`. No component updates itself in response to a shared state object.

---
