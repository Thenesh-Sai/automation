# SQL repositories

Live SQL access is gated by `Database.Enabled` and credentials via environment variables:

- `SILOVERSE_DB_ENABLED=true`
- `SILOVERSE_DB_USER`
- `SILOVERSE_DB_PASSWORD`
- `SILOVERSE_DB_NAME`

Host defaults to `aurora.cr068iswih5c.ap-south-1.rds.amazonaws.com:1433`.

Schema-specific repositories will be added only after tables are verified.
