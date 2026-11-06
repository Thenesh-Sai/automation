# CoreECI — Application Inventory

**Discovery date:** 2026-11-06  
**Environment:** DEV (`coreeci.dev.siloverse.space`)  
**Discovery status:** Partially Verified  

## 1. Application purpose (meta description — verified)

> Enterprise legal technology platform for early case investigation, client search term reports, document tagging, and export to review.

## 2. Access model

| Observation | Status |
| :--- | :--- |
| Unauthenticated → “You are not signed in” + Go to LaunchPoint | Verified |
| Authenticated without project → “No project selected” + Back to LaunchPoint | Verified |
| Direct `/project/A30020` or query/hash project params **do not** open workspace without handoff | Verified |
| LaunchPoint project page shows **CoreECI Enabled** + document/load metrics | Verified |
| Working launch handoff into full CoreECI modules | **Not Verified** in this session (no dedicated Launch CoreECI control found on project page; telemetry modals only) |

## 3. Config.js (public)

```js
window.__COREECI_CONFIG__ = {
  VITE_API_BASE_URL: "",
  VITE_LAUNCHPOINT_URL: "",
  VITE_COOKIE_DOMAIN: "",
  VITE_USE_MOCK_SEARCH: ""
};
```

Implication: published API base empty; search may use mock mode (`VITE_USE_MOCK_SEARCH`). Treat backend API contracts as **Not Verified** until network capture during a successful project session.

## 4. Client-side data keys observed (prior authenticated CoreECI session)

LocalStorage key **names** (values summarized, not pasted as secrets):

| Key | Entity shape (field names observed) | Status |
| :--- | :--- | :--- |
| `core_eci_loads_v5` | LoadKey, LoadName, ProjectId, DocumentCount, Status, LoadedAt, Description | Verified structure |
| `core_eci_documents_v5` | DocumentCode, DocumentName, DocumentType, FileSize, Custodian, DateSent, ProjectId, LoadKey, Tags, TagFieldAssignments, Summary, ContentText, Snippets | Verified structure |
| `core_eci_reports_v5` | ReportCode, ReportName, ProjectId, Scope, LoadKey, SearchCriteria, DocumentsMatched, TotalMatches, Status, ExecutedBy | Verified structure |
| `core_eci_tags_v5` / `core_eci_tag_fields_v5` | TagName, Color, CategoryName, Description | Verified structure |
| `core_eci_exports_v5` | ExportCode, ExportName, ExportDestination, ExportType, TagName, Status, TotalVolume | Verified structure |

**Sample verified entities (A30022 seed):** LoadKey `1001`, DocumentCode `87687014`, ReportCode `STR-001`, ExportCode `EXP-001`.

Export destinations observed in data: `Relativity Review Platform`, `AVR Review Gateway`.

## 5. LaunchPoint-side CoreECI telemetry (project A30022 / A30020)

| Control | Behaviour | Status |
| :--- | :--- | :--- |
| CoreECI Enabled badge | Visible on project header | Verified |
| Total Documents / Most Recent Load Date / CoreECI Active | Displayed | Verified |
| Project Profile | Modal: ESI ingest, extracted text DB, TIFF/PDF cache, footprint | Verified |
| View Details | Storage Allocation Breakdown (same storage fields) | Verified |
| Intake Audit | Modal title “Intake Audit Logs” but body showed **same storage fields** as Profile | **Defect candidate** (see Defects) |
| Processing in Progress / Summary | Modals open | Partially Verified |

## 6. Feature inventory vs supplied Feature IDs

| Feature ID | Feature | UI evidence | API | DB | Discovery status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| FE137 | Search Term Reports | Data model + LP release notes; create UI not opened this session | Not Verified | Not Accessible | Partially Verified |
| FE163 | Hit List | DocumentsMatched / snippets fields in report+document model | Not Verified | Not Accessible | Partially Verified |
| FE239 | Document Tagging | Tags / TagFieldAssignments categories incl. Relativity/AVR/privilege/trade secret | Not Verified | Not Accessible | Partially Verified |
| FE278 | Export Creation | Exports model; destinations Relativity/AVR | Not Verified | Not Accessible | Partially Verified |
| FE297 | Package Manifest | Not observed as labeled “Manifest” in CoreECI this session (AVR Production has Manifest) | Not Verified | Not Accessible | Not Verified in CoreECI UI |
| — | Custodian Timeline | Mentioned in LaunchPoint pulse (“CoreECI adds custodian timeline view”) | Not Verified | Not Accessible | Partially Verified (announcement only) |

## 7. Blockers for full CoreECI UI automation

1. Need confirmed **Launch CoreECI** handoff control / deep-link contract from LaunchPoint.  
2. Need authenticated network capture of real API calls (Swagger returns HTML SPA, not OpenAPI).  
3. DB credentials required for SQL validation against RDS.
