# Database Inventory

## Host provided

| Property | Value | Status |
| :--- | :--- | :--- |
| Hostname | `aurora.cr068iswih5c.ap-south-1.rds.amazonaws.com` | Provided |
| Resolved IP (discovery workstation) | 35.154.58.61 | Verified |
| TCP 1433 (SQL Server) | **Open** (`TcpTestSucceeded = True`) | Verified |
| TCP 5432 (PostgreSQL) | Closed | Verified |
| TCP 3306 (MySQL) | Closed | Verified |
| Engine inference | **Microsoft SQL Server** (port 1433) | Partially Verified |
| Database name(s) | Unknown | Not Accessible |
| Username / password | Not provided | Not Accessible |
| Schema / tables / PKs / FKs | Unknown | Not Accessible |
| Stored procedures | Unknown | Not Accessible |

## Connectivity attempts (Phase 2)

| Attempt | Result |
| :--- | :--- |
| TCP 1433 | Open |
| `sqlcmd -E` (Windows Integrated) | **Failed**: `Login failed. The login is from an untrusted domain and cannot be used with Integrated authentication.` |
| SSMS Registered Servers (`RegSrvr17.xml`) | Groups only; **no saved RDS connection / credentials** |
| SQL username/password | **Not provided** by stakeholder yet |

Inventing table names would violate anti-hallucination rules.

## Implications for Phase 5/6

| Work item | Status |
| :--- | :--- |
| `Siloverse.Infrastructure` SQL repositories | Scaffold interfaces only until schema verified |
| In-memory repositories | Allowed for isolated unit-style tests; **must not** be claimed as real DB testing |
| Live data tests (`Siloverse.Tests.Data`) | **Blocked** pending: DB name, SQL auth, read-only account, schema diagram |

## Required from stakeholders

1. SQL authentication (or Windows/AAD) for a **non-production** read account.  
2. Database name(s) mapped to LaunchPoint / CoreECI / AVR.  
3. Schema export or ER diagram for tables touched by supplied Feature IDs.  
4. Confirmation that automated tests may insert/cleanup in a dedicated test schema.
