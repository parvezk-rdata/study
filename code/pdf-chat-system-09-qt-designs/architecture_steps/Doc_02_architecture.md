> Step 06: Controller Architecture
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

## **Six Types Of Class**

| Class Type | Count | Responsibility |
|---|---|---|
| `Component` | Many | Render UI widgets. Emit signals. Nothing else. |
| `ComponentController` | One per smart component | Handle UI-only actions for their component |
| `DomainController` | One per service/domain | Handle business logic and external services |
| `MainController` | Exactly one | Orchestrate the full event flow across the app |
| `UIComposer` | Exactly one | Create `MainWindow`, instantiate and lay out all components, create all `ComponentControllers`, return `AppControllers` bundle |
| `DomainComposer` | Exactly one | Instantiate all domain services, load API key from `.env`, return `DomainControllers` bundle |

---

## Bundles (frozen dataclasses)

| Class | Type | Fields |
|---|---|---|
| `AppControllers` | `@dataclass(frozen=True)` | one field for each component controller |
| `DomainControllers` | `@dataclass(frozen=True)` | one field for each domain controller |

---


## MainController responsibilities

```
MainController
   |
   ├── Initialize Application
   |     |
   |     ├── call UIComposer → get AppControllers
   |     |
   |     ├── call DomainComposer → get DomainControllers
   |     |
   |     └── store references
   |
   ├── Define Event Handling Methods
   |     |
   |     ├── one method per user/system event
   |     |
   |     ├── Inside each event handler:
   |     |     |
   |     |     ├── Orchestrate Flow Between Controllers
   |     |     |
   |     |     ├── Handle Cross-Component Updates
   |     |     |
   |     |     ├── Call Domain Controllers (business logic)
   |     |     |
   |     |     └── Update UI via Component Controllers
   |
   ├── Bind Events to Handlers
   |     |
   |     └── connect UI signals → MainController methods
   |
   ├── Manage Application State (High-Level)
   |     |
   |     └── shared/global state only
   |
   ├── Error Handling & Routing
   |     |
   |     └── catch errors inside event handlers and route to UI
   |
   ├── Manage App Lifecycle
   |     |
   |     ├── initialize
   |     |    
   |     ├── reset
   |     |     
   |     └── shutdown (optional)
   |
   └── Coordinate Async / Long Tasks (if any)
         └── threads, loading states, etc.
```

## Component( Key responsibilities )

- Dumb Renderer : receive data and update UI
- Create UI Elements
- Build Layout
- Emit a external signal when a user interaction occurs
- Handle internal signals (scrolling, focus, hover, animations)
- Manage Internal UI State
- Never call the controller directly
- Never read from or write to another component
- do not decide what happens after an event
- Do not call any controller method directly
- do not interact with other components
- do not access global/application state

---

## ComponentController ( Key responsibilities )

- A non-widget class that **manages one smart component**.
- One controller per smart component (our app)
- Contains only operation methods that are called during event handling 
- there can be one or more methods corrosponding to an event.
- Owns all UI-level logic for that component
- Manage internal UI state of its component
- Acts as the bridge between MainController and the Component
- Ensures the component remains dumb and passive
- Never contain business logic
- Never communicate with other `ComponentController`s directly
---

## DomainController (Key responsibilities)

- A plain class that **handles one domain of business logic or one external service**
- Contains only operation methods that are called during event handling
- It knows nothing about the UI. Never update the UI directly
- Perform a specific business operation when called
- Return a result or raise a descriptive exception
- Communicates only via MainController
- Never communicate with other `DomainController`s directly
- Never communicate with other `ComponentController`s directly
---

## UIComposer (Key responsibilities)

- A plain class that **builds the entire UI** 
- single place where all components and component controllers are created
- Creates `MainWindow` and adds all components to it with correct layout
- Instantiates all `ComponentControllers` and passes each one its component
- Returns refrences of all component controllers as a frozen bundle
- Main controller need it get refrences of all component controllers 

---

## DomainComposer (Key responsibilities)

- A plain class that **builds all domain services** 
- the single place where all domain controllers are created
- Loads the settings from `.env` file at startup
- Instantiates all `DomainControllers`
- Returns refrences of all domain controllers as a frozen bundle
- Main controller need it get refrences of all domain controllers 

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
