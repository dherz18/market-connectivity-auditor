# Market Connectivity Auditor

A Python tool for auditing market data subscriptions across vendors (Bloomberg, Refinitiv, ICE), reconciling billing against actual usage, and flagging inactive or zero-usage entitlements to surface cost savings opportunities.

Built to demonstrate the kind of automated, scalable audit processes relevant to market connectivity and technology operations roles at proprietary trading firms.

## What it does

- Ingests vendor billing extracts and internal usage logs
- Merges billing against usage data and classifies each subscription: **ACTIVE**, **INACTIVE** (no login in 30+ days), or **NO USAGE**
- Generates actionable CSV reports in a `reports/` folder
- Emails a summary with the reports attached via Gmail SMTP

## Setup

```bash
pip install pandas numpy python-dotenv
cp .env.example .env
# Fill in your credentials in .env
```

## Configuration

| Variable | Description |
|---|---|
| `EMAIL_USER` | Gmail address to send from |
| `EMAIL_PASS` | Gmail App Password |
| `TARGET_EMAIL` | Recipient for the audit report |

> Gmail requires an [App Password](https://support.google.com/accounts/answer/185833) if 2FA is enabled.

## Run

```bash
python market_connect_audit.py
```

Reports are saved to `reports/no_usage_report.csv` and `reports/inactive_users_report.csv`.

## Sample data

The [`samples/`](samples/) folder contains example inputs and outputs so you can see exactly what the script works with before running it:

- [`samples/vendor_inputs/`](samples/vendor_inputs/) — vendor billing extracts (Bloomberg, Refinitiv, ICE) and internal usage log
- [`samples/report_outputs/`](samples/report_outputs/) — generated inactive/no-usage reports and a sample audit email

## Extending for production

The sample data generation at the top of the script is a stand-in for real vendor extracts. In production, replace that section with actual file ingestion from your vendor billing feeds and internal entitlement system exports. The reconciliation and reporting logic below it requires no changes.
