

### Workflow

01. Gather requirements — define use cases and expected functionality
02. Design GUI pages on paper
03. Identify the components needed for each GUI page
04. Design the component hierarchy — decide which components are smart vs dumb, and their parent/child relationships
05. For each component, identify what data it needs to display correctly
06. Represent that data as state — each piece of component data becomes a member of the app state
07. Model the state using appropriate classes/models
08. Decide if any events should fire reactively on state change
09. List all user events that can occur across the app. Each use case typically maps to one or more user events.
10. For each event, define the steps that will happen (refer: Generic Event Flow)
11. Identify domain controllers needed to handle business logic or external services
12. Write components based on the GUI design
13. Write main_controller with one blank method per event
14. Inside each blank method, add comments describing the steps from step 10
15. Decide which tasks belong to component_controllers and which belong to domain_controllers
16. Implement method bodies, starting with domain_controllers, then main_controller, then component_controllers


---

### Key Principle
> This follows a **top-down, outside-in** philosophy — design intent before implementation, which scales well for larger apps.