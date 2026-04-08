# Market Connectivity Auditor

A Python script that reconciles vendor market data billing (Bloomberg, Refinitiv, ICE) against internal usage logs to identify inactive or zero-usage subscriptions and flag potential cost savings.

## What it does

- Generates sample vendor billing extracts and an internal usage log (replace with real data for production use)
- Merges billing vs. usage data and classifies each subscription as **ACTIVE**, **INACTIVE** (no login in 30+ days), or **NO USAGE**
- Writes actionable CSV reports to a `reports/` folder
- Emails a summary with the reports attached via Gmail SMTP

## Setup

```bash
pip install pandas numpy python-dotenv
cp .env.example .env
# Fill in your Gmail credentials in .env
```

## Configuration

Copy `.env.example` to `.env` and set:

| Variable | Description |
|---|---|
| `EMAIL_USER` | Gmail address to send from |
| `EMAIL_PASS` | Gmail App Password (not your login password) |
| `TARGET_EMAIL` | Recipient address for the audit report |

> Gmail requires an [App Password](https://support.google.com/accounts/answer/185833) if 2FA is enabled.

## Run

```bash
python market_connect_audit.py
```

Reports are saved to `reports/no_usage_report.csv` and `reports/inactive_users_report.csv`.
