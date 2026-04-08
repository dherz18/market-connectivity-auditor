# Sample Inputs

These files represent the two data sources the script reconciles:

**Vendor billing extracts** (`bloomberg_extract.csv`, `refinitiv_extract.csv`, `ice_extract.csv`) — one row per employee subscription, with the flat monthly cost per vendor. In production these would come directly from vendor billing feeds or account management portals.

**Internal usage log** (`internal_usage_logs.csv`) — one row per employee/system pair, recording the last login timestamp pulled from the firm's internal entitlement or SSO system.
