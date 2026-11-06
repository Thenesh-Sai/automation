# Feature Inventory (Master)

Maps supplied Feature IDs to discovery status. This is the reference for Phase 4–5 automation scope.

Legend: **Verified** · **Partially Verified** · **Not Verified** · **Not Accessible** · **Blocked**

| Feature ID | Application | Module | Feature / Subfeature | Discovery status | Automation readiness |
| :--- | :--- | :--- | :--- | :--- | :--- |
| FE557 | LaunchPoint | Authentication | Sign In | Verified (UI) | UI ready; API Blocked |
| — | LaunchPoint | Authentication | Sign Out | Verified (UI control) | UI ready; API Blocked |
| FE588 | LaunchPoint | Home Dock | View home + user info | Verified | UI ready |
| FE137 | CoreECI | Search Term Reports | Create / enter terms / view / manage tags | Partially Verified | Blocked (project handoff + API) |
| FE163 | CoreECI | Hit List | Documents matching search terms | Partially Verified | Blocked |
| FE239 | CoreECI | Document Tagging | Tag add/remove/persist | Partially Verified | Blocked |
| FE278 | CoreECI | Export Creation | Create/filter/sort/view exports | Partially Verified | Blocked |
| FE297 | CoreECI | Package Manifest | Manifest table for export package | Not Verified in CoreECI | Blocked |
| FE749 | AVR | Reviewer Management | Create Assignment | Verified | UI ready; API Blocked |
| FE750 | AVR | Reviewer Management | Add Reviewers | Verified | UI ready; API Blocked |
| FE751 | AVR | Reviewer Management | View Assigned Reviewers | Partially Verified | UI partial |
| FE448 | AVR | Document Allocation | Choose Assignment | Verified | UI ready |
| FE449 | AVR | Document Allocation | Choose Reviewer | Partially Verified | UI partial |
| FE443 | AVR | Document Allocation | Select Documents | Verified | UI ready |
| FE457 | AVR | Document Allocation | Open in Review | Partially Verified | UI partial |
| FE437 | AVR | Document Allocation | Search Documents | Verified | UI ready |
| FE394 | AVR | Review Documents | Set Responsiveness | Verified | UI ready |
| FE395 | AVR | Review Documents | Set Confidentiality | Verified | UI ready |
| FE396 | AVR | Review Documents | Set Privilege | Verified | UI ready |
| FE397 | AVR | Review Documents | Select Privilege Type | Not Verified | Blocked pending UI proof |
| FE399 | AVR | Review Documents | Select Document Tags | Not Verified on coding panel | Blocked pending UI proof |
| FE747 | AVR | Review Documents | Submit Review (Complete Review) | Verified | UI ready |
| FE748 | AVR | Review Documents | AI-assisted Review | Not Verified | Blocked |
| — | AVR | Production | AI Validation summary | Not Verified | Blocked |
| FE531 | AVR | Production | Create New Package | Verified | UI ready |
| FE533 | AVR | Production | Select Documents for Production | Partially Verified | UI partial |
| FE538 | AVR | Production | Check for Eligibility | Partially Verified | UI partial |

## Cross-app dependencies (verified)

```
Identity SSO → LaunchPoint session (user_cookie)
LaunchPoint → AVR workspace launch (project context)
LaunchPoint → CoreECI project gate (project context required; launch control TBD)
LaunchPoint project page ↔ CoreECI telemetry cards
CoreECI export destinations reference Relativity + AVR (data model)
AVR ↔ LaunchPoint theme/cookie domain .siloverse.space
```

## Counts

| Metric | Count |
| :--- | ---: |
| Supplied feature rows in this matrix | 26 |
| Verified | 12 |
| Partially Verified | 9 |
| Not Verified | 5 |
| Ready for UI automation (Verified) | 12 |
| Blocked for API automation | All (0 verified endpoints) |
| Blocked for DB automation | All (no credentials/schema) |
