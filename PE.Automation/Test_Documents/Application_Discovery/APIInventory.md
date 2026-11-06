# API Inventory

**Rule:** No endpoint is automated until listed here as **Verified**.

## Probe summary (2026-11-06)

| URL probed | HTTP | Content-Type | Status |
| :--- | ---: | :--- | :--- |
| https://avr.dev.siloverse.space/swagger/v1/swagger.json | 200 | text/html | Not Verified (SPA HTML, not OpenAPI) |
| https://avr.dev.siloverse.space/swagger/swagger.json | 200 | text/html | Not Verified |
| https://avr.dev.siloverse.space/api | 200 | text/html | Not Verified |
| https://coreeci.dev.siloverse.space/swagger/index.html | 200 | text/html | Not Verified |
| https://coreeci.dev.siloverse.space/swagger/v1/swagger.json | 200 | text/html | Not Verified |
| https://identity.dev.siloverse.space/swagger/index.html | 200 | text/html | Not Verified |
| https://launchpoint-ui.dev.siloverse.space/swagger/index.html | 200 | text/html | Not Verified |

## Published config API bases

| App | Config key | Value observed | Status |
| :--- | :--- | :--- | :--- |
| LaunchPoint | `apiBaseUrl` / `identityUrl` | empty string | Not Verified |
| CoreECI | `VITE_API_BASE_URL` | empty string | Not Verified |
| AVR | `AVR_PII_URL` | empty string | Not Verified |

## Verified API contracts

| App | Method | Endpoint | Auth | Schema | Status codes | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| — | — | — | — | — | — | **None verified yet** |

## Next discovery actions (required before API automation)

1. Capture authenticated DevTools Network log while exercising LaunchPoint, CoreECI, AVR.  
2. Obtain OpenAPI/Swagger from backend hosts (if separate from UI hosts).  
3. Document each call: method, path, query, request/response JSON, status codes.  
4. Only then generate `Siloverse.Api` endpoint clients.
