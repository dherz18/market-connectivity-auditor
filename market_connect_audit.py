import pandas as pd
import numpy as np
import os
import smtplib
from datetime import datetime, timedelta
from pathlib import Path
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()


# Configuration & directory setup
os.makedirs('vendor_data', exist_ok=True)
os.makedirs('reports', exist_ok=True)
data_dir = Path('vendor_data')
reports_dir = Path('reports')

EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASS = os.environ.get('EMAIL_PASS')
TARGET_EMAIL = os.environ.get('TARGET_EMAIL')

# Sample data generation — swap these out for real vendor extracts in production
trader_ids = [f"TRDR_{i:03d}" for i in range(1, 51)]

vendors = {
    'bloomberg': {'cost': 2500, 'ids': trader_ids[0:25]},
    'refinitiv': {'cost': 1800, 'ids': trader_ids[20:40]},
    'ice': {'cost': 2200, 'ids': trader_ids[35:50]}
}

for name, info in vendors.items():
    pd.DataFrame({
        'Employee_ID': info['ids'],
        'Vendor': name.upper(),
        'Monthly_Cost': info['cost']
    }).to_csv(data_dir / f'{name}_extract.csv', index=False)

usage_records = []
for t_id in trader_ids:
    for system in ['BLOOMBERG', 'REFINITIV', 'ICE']:
        if np.random.random() > 0.2:  # ~80% usage rate
            last_date = datetime.now() - timedelta(days=np.random.randint(0, 45))
            usage_records.append({'Employee_ID': t_id, 'System': system, 'Last_Login': last_date})

pd.DataFrame(usage_records).to_csv('internal_usage_logs.csv', index=False)

# Ingest & reconcile vendor billing against internal usage
usage_data = pd.read_csv('internal_usage_logs.csv')
usage_data['Last_Login'] = pd.to_datetime(usage_data['Last_Login'])

vendor_files = list(data_dir.glob('*.csv'))
all_subs = pd.concat([pd.read_csv(f) for f in vendor_files], ignore_index=True)

audit_df = pd.merge(
    all_subs,
    usage_data,
    how='left',
    left_on=['Employee_ID', 'Vendor'],
    right_on=['Employee_ID', 'System']
)

audit_df.drop(columns=['System'], inplace=True)
audit_df['Days_Inactive'] = (datetime.now() - audit_df['Last_Login']).dt.days

audit_df['Status'] = audit_df.apply(
    lambda x: 'NO USAGE' if pd.isna(x['Last_Login'])
    else ('INACTIVE' if x['Days_Inactive'] >= 30 else 'ACTIVE'),
    axis=1
)

# Split into actionable reports and calculate potential savings
no_usage_df = audit_df[audit_df['Status'] == 'NO USAGE']
inactive_df = audit_df[audit_df['Status'] == 'INACTIVE']

no_usage_df.to_csv(reports_dir / 'no_usage_report.csv', index=False)
inactive_df.to_csv(reports_dir / 'inactive_users_report.csv', index=False)

total_savings = no_usage_df['Monthly_Cost'].sum() + inactive_df['Monthly_Cost'].sum()

# Build and send the audit summary email
msg = EmailMessage()
msg['Subject'] = f"Cost Optimization Alert: Vendor Audit {datetime.now().strftime('%Y-%m')}"
msg['From'] = EMAIL_USER
msg['To'] = TARGET_EMAIL

msg.set_content(f"""Hello,

The monthly vendor audit is complete.

Audit Summary:
- Subscriptions with No Usage: {len(no_usage_df)}
- Inactive Subscriptions (>30 Days): {len(inactive_df)}

Total Potential Monthly Savings: ${total_savings:,.2f}

Detailed reports are attached.

Regards,
""")

for report_path in [reports_dir / 'no_usage_report.csv', reports_dir / 'inactive_users_report.csv']:
    with open(report_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename=report_path.name)

if all([EMAIL_USER, EMAIL_PASS, TARGET_EMAIL]):
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
        print(f"Success: Audit report sent to {TARGET_EMAIL}")
    except Exception as e:
        print(f"Email failed: {e}")
else:
    print("Email skipped: Environment variables missing.")