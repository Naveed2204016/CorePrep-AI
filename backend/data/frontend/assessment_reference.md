# Frontend Assessment Reference

## Semantic HTML & Accessibility
Semantic elements expose structure to browsers and assistive technology. Accessible names, labels, focus order, keyboard operation, and appropriate native controls matter more than ARIA decoration.
## CSS Fundamentals & Layout
Cascade origin, importance, specificity, and source order choose declarations. Flexbox is one-dimensional and Grid is two-dimensional; absolute positioning is not a general layout system.
## JavaScript Fundamentals
Closures retain lexical environment, objects use reference identity, and promises schedule reactions as microtasks. `var`, `let`, and `const` differ in scope and initialization behavior.
## TypeScript
TypeScript checks compile-time structure and does not validate runtime input. Narrowing proves union members, generics preserve relationships, and `any` disables safety.
## DOM & Events
Capture precedes target and bubble phases; delegation handles descendant events through ancestors. DOM updates can trigger style, layout, paint, and compositing work.
## Browser Rendering
HTML builds the DOM and CSS builds the CSSOM before render-tree work. Layout calculates geometry, paint records pixels, and compositing assembles layers.
## HTTP & Web APIs
Fetch resolves on HTTP errors unless code checks status; CORS is browser-enforced permission, not authentication. Cookies have origin, path, security, and same-site rules.
## React Components & Hooks
Rendering must remain pure; state updates schedule new renders. Effects synchronize with external systems and should not replace ordinary derived computation.
## State Management
Keep state near consumers and distinguish client state from remote server state. Duplicated derived state causes inconsistency and unnecessary synchronization.
## Forms & Validation
Client validation improves feedback but server validation remains authoritative. Labels, error association, focus handling, and submission states affect accessibility.
## Routing & Application Architecture
Routes map URLs to UI and data boundaries. Feature organization, lazy loading, error boundaries, and stable ownership reduce coupling.
## Frontend Testing
Test observable behavior rather than component internals. Unit, integration, accessibility, visual, and end-to-end tests balance speed against confidence.
## Web Performance
LCP measures loading, INP responsiveness, and CLS visual stability. Optimize measured bottlenecks using caching, compression, image sizing, splitting, and reduced main-thread work.
## Frontend Security
XSS executes untrusted script, CSRF abuses ambient credentials, and unsafe storage exposes secrets. Output encoding and safe DOM APIs complement content security policy.
## Build Tools & Deployment
Bundlers transform module graphs and optimize assets; environment variables embedded in client bundles are public. Source maps aid debugging but need deliberate exposure policy.
