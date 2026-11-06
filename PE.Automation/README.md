# PE.Automation

Enterprise Playwright + NUnit automation framework for **LaunchPoint**, **CoreECI**, and **AVR**.

## Phase status

| Phase | Status |
| :--- | :--- |
| 1 Discovery | Complete (see `Test_Documents/Application_Discovery`) |
| 2 Solution + UI foundation (Verified features) | **In progress / this scaffold** |
| 3–7 | Pending after Phase 2 build validation |

## Solution layout

- `src/Siloverse.Configuration` — appsettings + DI
- `src/Siloverse.Models` — DTOs
- `src/Siloverse.Api` — API clients (**no invented business endpoints**)
- `src/Siloverse.UI` — Playwright page objects (Verified features)
- `src/Siloverse.Infrastructure` — in-memory + SQL probe
- `tests/Siloverse.Tests.UI`
- `tests/Siloverse.Tests.Api`
- `tests/Siloverse.Tests.Integration`
- `tests/Siloverse.Tests.Data`

## Prerequisites

- .NET 8 SDK
- PowerShell
- Credentials via environment variables (never commit secrets)

```powershell
$env:SILOVERSE_USERNAME = "rachel.torres@consilio.com"
$env:SILOVERSE_PASSWORD = "<password>"
# Optional SQL (SSMS registered servers had no saved RDS login):
$env:SILOVERSE_DB_ENABLED = "true"
$env:SILOVERSE_DB_USER = "<sql-user>"
$env:SILOVERSE_DB_PASSWORD = "<sql-password>"
$env:SILOVERSE_DB_NAME = "<database-name>"
```

## Build

```powershell
cd PE.Automation
dotnet restore
dotnet build PE.Automation.sln
pwsh bin/Debug/net8.0/playwright.ps1 install chromium
# Or:
dotnet build tests/Siloverse.Tests.UI/Siloverse.Tests.UI.csproj
pwsh tests/Siloverse.Tests.UI/bin/Debug/net8.0/playwright.ps1 install
```

## Run tests (Visual Studio Test Explorer or CLI)

```powershell
# Data / in-memory (no browser credentials required)
dotnet test tests/Siloverse.Tests.Data --filter "Category=InMemory"

# API host smoke (no invented business APIs)
dotnet test tests/Siloverse.Tests.Api

# UI verified features (requires SILOVERSE_USERNAME/PASSWORD)
dotnet test tests/Siloverse.Tests.UI --filter "Category=Smoke"

# Integration journeys
dotnet test tests/Siloverse.Tests.Integration --filter "Category=Smoke"
```

## Database note

Host `aurora.cr068iswih5c.ap-south-1.rds.amazonaws.com:1433` is reachable.  
Windows/SSMS integrated auth failed (`untrusted domain`). No SQL username/password was found in SSMS registered servers. Live schema discovery remains **Blocked** until credentials are provided.

## Test cases

CSV workbooks under `Test_Documents/Test_Cases/` (LaunchPoint, CoreECI, AVR, combined).
