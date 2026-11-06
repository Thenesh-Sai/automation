# Confirmed Defects (Discovery Phase)

Only defects that were **reproduced** during live inspection are listed.

---

### DEF-CORE-001

| Field | Value |
| :--- | :--- |
| Defect ID | DEF-CORE-001 |
| Application | LaunchPoint (CoreECI telemetry surface) / CoreECI |
| Feature ID | Related to Intake / processing telemetry (adjacent to FE137+ project ops) |
| Summary | Intake Audit modal displays Storage Allocation fields instead of intake audit logs |
| Environment | DEV — LaunchPoint project A30020 / A30022 |
| Preconditions | Signed in as rachel.torres@consilio.com; open Aurora US project detail with CoreECI Enabled |
| Steps to reproduce | 1. Open `https://launchpoint-ui.dev.siloverse.space/aurora/aurora-us/projects/A30022` (or A30020). 2. Click **Intake Audit**. 3. Read modal body. |
| Expected result | Intake audit log entries / intake-specific telemetry for the project |
| Actual result | Modal titled “Intake Audit Logs” shows Allocated ESI Ingest Storage, Extracted Text & Metadata DB, TIFF/PDF Production Cache, Total Managed Footprint — same content as Project Profile / View Details |
| Severity | Medium |
| Priority | P2 |
| Evidence | Live UI observation 2026-11-06; body text captured during discovery |
| Reproducibility | Yes (observed on A30020 and A30022) |
| Related test case | TBD after Phase 4 case IDs assigned |

---

No other defects are confirmed at this time. Observations that are **not** confirmed defects (empty search before clicking Search on AVR Documents, CoreECI project gate without handoff) are application behaviours pending requirements confirmation.
