import os
import json
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

#INSERT THE SERVICE ACCOUNT CREDENTIALS (.JSON)
CREDENTIALS_FILE = "PATH_TO_THE_CREDENTIALS"
OUTPUT_LOG_FILE = "/var/ossec/logs/google_workspace/alert_center.log"
ALERT_CACHE_FILE = "/opt/wazuh-gworkspace/alert_cache.json"  
SCOPE = ['https://www.googleapis.com/auth/apps.alerts']
#INSERT THE DELEGATE ACCOUNT FOR THE SERVICE ACCOUNT
DELEGATED_USER = 'DELEGATED_USER'

creds = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE, scopes=SCOPE, subject=DELEGATED_USER
)

creds.refresh(Request())  
print(f"Service account in use: {creds.service_account_email}, delegated account for the service account: {DELEGATED_USER}")

service = build('alertcenter', 'v1beta1', credentials=creds)
alerts_api = service.alerts()

try:
    with open(ALERT_CACHE_FILE, 'r') as f:
        processed_ids = set(json.load(f))
except (FileNotFoundError, json.JSONDecodeError):
    processed_ids = set()

#Enter your Google Workspace customer ID.
results = alerts_api.list(customerId='CUSTOMERID').execute()
new_alerts = results.get('alerts', [])

with open(OUTPUT_LOG_FILE, 'a') as logfile:
    for alert in new_alerts:
        print(alert)
        alert_id = alert.get('alertId')
        if alert_id in processed_ids:
            continue  

        parsed = {
            "alert_id": alert_id,
            "timestamp": alert.get('createTime'),
            "type": alert.get('type'),
            "severity": alert.get('severity'),
            "source": "google_workspace_alert_center",
            "user": alert.get('data', {}).get('affectedUser'),
            "ip": alert.get('data', {}).get('ipAddress'),
            "raw": alert  
        }

        logfile.write(json.dumps(parsed) + '\n')
        processed_ids.add(alert_id)

with open(ALERT_CACHE_FILE, 'w') as f:
    json.dump(list(processed_ids), f)

print(f"Processed alerts = {len(new_alerts)}")

