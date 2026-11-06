# Known Issues / Limitations (Not necessarily defects)

| ID | Area | Issue | Impact on automation | Status |
| :--- | :--- | :--- | :--- | :--- |
| LIM-001 | API | No OpenAPI/Swagger JSON on UI hosts | Cannot generate verified API clients | Blocked |
| LIM-002 | API | `apiBaseUrl` / `VITE_API_BASE_URL` empty in public config | Unknown backend hosts | Blocked |
| LIM-003 | CoreECI | Project handoff control not found; full module UI not entered this session | CoreECI UI POM incomplete | Blocked |
| LIM-004 | DB | RDS 1433 reachable but no credentials/schema | Data tests blocked | Blocked |
| LIM-005 | AVR | FE397 / FE399 / FE748 not visible on reviewed document | Cannot assert those subfeatures yet | Not Verified |
| LIM-006 | AVR Docs | Grid empty until Search clicked | Tests must click Search explicitly | Observed behaviour |
| LIM-007 | Security | Destructive/perf testing on shared DEV not authorized | Limit to non-destructive checks | Policy |
