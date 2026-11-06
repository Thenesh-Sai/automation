# LaunchPoint — Application Inventory

**Discovery date:** 2026-11-06  
**Environment:** DEV (`launchpoint-ui.dev.siloverse.space`)  
**Discovery status:** Verified (UI) · API contracts Not Verified (no OpenAPI JSON) · DB Not Accessible  

## 1. Application purpose

Siloverse LaunchPoint is the SSO gateway and launcher for Aurora regional enclaves and applications (Aurora Command Center path, AVR, Relativity, AGI, CaseTime, Reveal, CoreECI handoff).

## 2. Entry / authentication (FE557 / Sign Out)

| Item | Observation | Status |
| :--- | :--- | :--- |
| Identity URL | `https://identity.dev.siloverse.space/` | Verified |
| Sign-in fields | Username (email), Password, Remember my username, Continue to LaunchPoint | Verified |
| Valid login | Lands on `/home` as Rachel Torres | Verified |
| Session cookie names observed | `user_cookie`, `siloverse_theme` (domain `.siloverse.space`) | Verified (names only) |
| User Profile menu | User Statistics & Analytics; Add / Manage Enterprise Users; **Sign Out** | Verified |
| Profile identity text | “Rachel Torres”, `rachel.torres@consilio.com` | Verified |
| Unauthenticated LaunchPoint | Session error + “Go to sign in” | Verified (prior session) |

**Not verified yet:** exact invalid-password message text; session expiry timeout duration; enterprise user admin screens.

## 3. Home Dock (FE588)

| Element | Notes | Status |
| :--- | :--- | :--- |
| Heading | “Aurora Launchpoint” | Verified |
| App launch tiles | Open Aurora Command Center; Open Aurora Verity Review; Open Relativity; Open AGI; CaseTime/Reveal about only | Verified |
| Aurora Pulse feed | Filters: All, News, Insight, Release, Project, Data handled, Milestone | Verified |
| Theme toggle | Switch to Light Mode | Verified |
| Give Feedback | Present | Verified |

## 4. Aurora navigation (supporting LaunchPoint ↔ apps)

| Route | Screen | Key controls | Status |
| :--- | :--- | :--- | :--- |
| `/aurora/instances` | Regional enclaves | Search; Open Aurora US/UK/CA/AU/HK | Verified |
| `/aurora/aurora-us/clients` | Client directory | Search; Domain/Tier filters; Grid/List; pagination | Verified |
| `/aurora/aurora-us/clients/{id}/projects` | Project portfolio | Table/Card; Open project; Show workspace | Verified |
| `/aurora/aurora-us/projects/{code}` | Project detail | CoreECI Enabled metrics; Profile/Intake/Processing modals; AVR workspace tile | Verified |
| `/avr/workspaces` | AVR workspace directory | Search; Instance/Client filters; sort; page size; Launch Workspace modal | Verified |

### AVR Launch Workspace modal (verified fields)

- Workspace name, Workspace ID (e.g. 539), Client, Matter, Matter number (A30022), Instance (`aurora-us`)
- Launching as: name, email, **System Admin**
- Actions: Close, Launch Workspace → Connecting… → opens `https://avr.dev.siloverse.space/`

## 5. Config.js (public)

```js
window.__LAUNCH_CONFIG__ = {
  avrUrl: "https://avr.dev.siloverse.space",
  coreeciUrl: "https://coreeci.dev.siloverse.space",
  sgiUrl: "https://sgi-ui.dev.siloverse.space",
  // apiBaseUrl / identityUrl empty in published config
  cookieDomain: ".siloverse.space"
};
```

## 6. API discovery (LaunchPoint)

| Probe | Result | Status |
| :--- | :--- | :--- |
| `/swagger/index.html` | Returns SPA HTML shell, not OpenAPI | Not Verified |
| `/swagger/v1/swagger.json` | Not available as JSON | Not Verified |
| Network XHR inventory | Browser resource list showed static assets; live API base empty in config | Not Verified |

**Rule for Phase 5:** Do not invent LaunchPoint API endpoints until captured via authenticated network traces or provided OpenAPI.

## 7. Modules / features inventory

| Application | Module | Feature | Subfeature | UI screen | Related API | DB entity | Role | Dependencies | Discovery status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| LaunchPoint | Authentication | Sign In | FE557 | Identity UI | Not Verified | Not Accessible | Any | Identity host | Verified UI |
| LaunchPoint | Authentication | Sign Out | — | User Profile | Not Verified | Not Accessible | Signed-in | Session cookie | Verified UI control |
| LaunchPoint | Home Dock | Home | FE588 | `/home` | Not Verified | Not Accessible | Signed-in | SSO | Verified UI |
| LaunchPoint | Aurora | Regions | — | `/aurora/instances` | Not Verified | Not Accessible | Signed-in | — | Verified UI |
| LaunchPoint | Aurora | Clients | — | `/aurora/{region}/clients` | Not Verified | Not Accessible | Signed-in | Region | Verified UI |
| LaunchPoint | Aurora | Projects | — | client projects / project detail | Not Verified | Not Accessible | Signed-in | Client | Verified UI |
| LaunchPoint | AVR Gateway | Workspaces | — | `/avr/workspaces` | Not Verified | Not Accessible | System Admin observed | AVR URL | Verified UI |
| LaunchPoint | CoreECI Gateway | Project telemetry | — | project detail CoreECI cards | Not Verified | Not Accessible | Signed-in | CoreECI URL | Verified UI |
| LaunchPoint | Admin | Manage Enterprise Users | — | Profile menu | Not Verified | Not Accessible | Unknown RBAC | — | Partially Verified (entry only) |
