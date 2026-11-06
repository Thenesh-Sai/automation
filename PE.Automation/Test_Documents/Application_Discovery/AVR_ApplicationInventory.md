# AVR — Application Inventory

**Discovery date:** 2026-11-06  
**Environment:** DEV (`https://avr.dev.siloverse.space/`)  
**Workspace inspected:** A30022 — Acme Freight & Supply Chain Contract Dispute (Workspace ID 539, Instance aurora-us)  
**User role observed:** System Admin  
**Discovery status:** Verified (major modules) · API Not Verified · DB Not Accessible  

## 1. Access model

| Observation | Status |
| :--- | :--- |
| Direct AVR root without project → “No project selected” | Verified |
| Launch from LaunchPoint `/avr/workspaces` → Launch Workspace modal → Connecting… | Verified |
| Config public: `window.__AVR_CONFIG__ = {"AVR_PII_URL":""}` | Verified |
| Cookie names: `siloverse_theme`, `user_cookie`; local key `avr_theme`, `avr_assignment_mirror_v2` | Verified (names) |
| Meta description lists multi-role workflows, allocation, coding, search/filter, production | Verified |

## 2. Module navigation (verified)

| Module | Purpose observed |
| :--- | :--- |
| Dashboard | Review Summary, Production Overview, Coding analytics, Assignment Summary |
| Assignments | Create/edit assignments, reviewers, instructions, security/keyword groups |
| Documents | Search/filter/allocate/unallocate matter documents |
| Reviews | Document viewer + Review Coding Panel |
| Release to Production | Packages, eligibility search, Manifest |
| Tags and Folders | Present in nav (screen not deeply exercised) |
| Keyword Groups | Present in nav (screen not deeply exercised) |

Header: Switch project, System Admin role chip, Toggle Theme, User Profile, Skip to content.

## 3. Dashboard metrics (A30022)

| Metric | Value observed |
| :--- | ---: |
| Total Matter Docs | 22 |
| Assigned to Batches | 1 |
| Unassigned Pool | 21 |
| Pending Reviews | 1 |
| Completed Reviews | 0 |
| Released / Draft / Eligible / Packages | 0 |
| Responsiveness | Uncoded 22 (100%) |

CTAs: Assign Documents, Release to Production, Manage Reviewers.

## 4. Assignments (FE749 / FE750 / FE751)

### List
- Create Assignment
- Search by assignment name, ID, or description
- Status filter: All / Open / In Review / Completed / Suspended
- Columns: Assignment, Reviewers, Configuration, Status, Action (Edit)
- Sample rows:
  - Shipment Tracking & Delivery Scan Review (`88259553`) — Open — 4 reviewers — Needs setup
  - Inventory Variance and Customs Review (`88259554`) — In Review
  - Data Integrity Second-Level Review (`88259555`) — Open

### Create Assignment wizard (verified sections)
1. Assignment details — name* , description  
2. Reviewers — search + checkboxes (Carlos Gomez, Elena Petrova, Lena Fischer, Mateo Alvarez)  
3. Review instructions  
4. Security group & keyword groups — Security group combobox (Default / External / QC / Privileged); custom keyword group name/keywords; Add group; series colours  
5. Cancel / Create Assignment (disabled until required fields satisfied)

## 5. Documents / allocation (FE448–FE457, FE437, FE443)

Requires explicit **Search** to populate grid (empty state before search).

| Control | Options / behaviour |
| :--- | :--- |
| Search documents | Keyword / Enter; “Search index: 22 active matter documents” |
| Keyword group | Select a keyword group |
| Review Status | ALL, Unassigned, Pending, In Progress, Completed |
| Custodian | Javier Morales, Li Wei, Carlos Méndez |
| Batch Assignment | Unassigned Only + three assignment IDs |
| Responsiveness | Responsive / Not Responsive / Technical Issue |
| Privilege | Privileged Only / Not Privileged |
| File Type | form_packet, change_history, document_markup, chat_export, mixed_correspondence, email_thread, field_log, transaction_ledger |
| Allocate / Unallocate Selected | Present; disabled at 0 selection |
| Grid columns | Doc ID, Subject/Title, Type, Custodian, Status, Reviewer, Batch, Keywords, Coding, Tags |

Sample Doc ID: `10479141` — Pending — Carlos Gomez — Shipment Tracking batch.

## 6. Reviews / coding (FE394–FE399, FE747, FE748)

Viewer for `LOG-06_006_form_packet.pdf` (Doc `10479141`):
- Assignment selector
- Protocol Instructions
- Views: Native / Text / Images / Translation
- **Review Coding Panel**
  1. Responsiveness * (Responsive / Not Responsive / Technical Issue) → FE394  
  2. Confidentiality * (Confidential / Not Confidential) → FE395  
  3. Privilege * (Privileged / Not Privileged) → FE396  
  5. Reviewer Remarks + Hot Doc  
  - Save Draft / Complete Review → FE747  

| Subfeature | Status |
| :--- | :--- |
| FE397 Select Privilege Type | **Not Verified** on this screen (no privilege-type control visible before selecting Privileged) |
| FE399 Document Tags on coding panel | **Not Verified** (step “4” missing in labels; Tags module exists separately) |
| FE748 AI-assisted Review | **Not Verified** (no AI control observed on this document) |

## 7. Release to Production (FE531 / FE533 / FE538)

| Control | Observation | Feature map |
| :--- | :--- | :--- |
| New production package | Present | FE531 |
| Search packages + status filter (Draft / Validated / Released / Failed validation) | Present | — |
| Open / Manifest | Present (disabled with no selection) | Manifest related |
| Find production documents (expand) | Search by ID/title/filename/custodian/package | FE533 |
| Copy: verify eligibility / jurisdiction formats | Present in page description | FE538 |
| AI Validation – Summary of Packages | **Not Verified** as labeled control | Not Verified |

## 8. API discovery (AVR)

| Probe | Result | Status |
| :--- | :--- | :--- |
| `avr.dev.siloverse.space/swagger/*` | HTML SPA responses, not OpenAPI JSON | Not Verified |
| Live XHR endpoint catalogue | Not captured this session | Not Verified |

## 9. Feature discovery matrix

| Feature ID | Functionality | Discovery status |
| :--- | :--- | :--- |
| FE749 | Create Assignment | Verified |
| FE750 | Add Reviewers | Verified (create form) |
| FE751 | View Assigned Reviewers | Partially Verified (count on list; Manage Reviewers CTA) |
| FE448 | Choose Assignment | Verified (Reviews + Documents batch filters) |
| FE449 | Choose Reviewer | Partially Verified (reviewer shown; allocate flow not completed) |
| FE443 | Select Documents for Assignment | Verified (select + Allocate Selected) |
| FE457 | Open in Review | Partially Verified (Reviews opens pending doc) |
| FE437 | Search Documents | Verified |
| FE394 | Set Responsiveness | Verified |
| FE395 | Set Confidentiality | Verified |
| FE396 | Set Privilege | Verified (boolean) |
| FE397 | Select Privilege Type | Not Verified |
| FE399 | Select Document Tags | Not Verified on coding panel |
| FE747 | Submit Review | Verified (Complete Review control) |
| FE748 | AI-assisted Review | Not Verified |
| FE531 | Create New Package | Verified (New production package) |
| FE533 | Select Documents for Production | Partially Verified (finder UI) |
| FE538 | Check for Eligibility | Partially Verified (copy + filters; not executed) |
| — | AI Validation summary | Not Verified |
