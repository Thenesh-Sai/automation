# PE.Automation — Test Documents

This folder holds discovery, planning, execution and maintenance artefacts for the Siloverse automation framework covering **LaunchPoint**, **CoreECI** and **AVR**.

## Phase status

| Phase | Status | Notes |
| :--- | :--- | :--- |
| Phase 1 – Application Discovery | **Complete** | Inventories under Application_Discovery |
| Phase 2 – Architecture / Solution | **Complete (build green)** | `PE.Automation.sln` builds; UI foundation for Verified features |
| Phase 3 – Framework foundation | Partially complete | Browser fixture, DI, API clients (no invented endpoints), in-memory repos |
| Phase 4 – Feature test design | Not started | |
| Phase 5 – Automation implementation | Not started | |
| Phase 6 – Execution / defects | Not started | |
| Phase 7 – Final validation | Not started | |

## Environment inspected

| App | URL | Status |
| :--- | :--- | :--- |
| LaunchPoint UI | https://launchpoint-ui.dev.siloverse.space | Verified (authenticated) |
| Identity | https://identity.dev.siloverse.space | Verified (sign-in) |
| CoreECI | https://coreeci.dev.siloverse.space | Partially Verified (gate + prior session data) |
| AVR | https://avr.dev.siloverse.space | Verified (project A30022 launched) |
| RDS host | `aurora.cr068iswih5c.ap-south-1.rds.amazonaws.com` | Port **1433 open** (SQL Server). Credentials **Not Accessible** |

## Test account used for discovery

- User display: Rachel Torres
- Email: rachel.torres@consilio.com
- Observed role in AVR launch modal: **System Admin**

Credentials are **not** stored in this repository. Supply via user secrets / CI variables only.
