# Wazuh GWorkspace Alerts Integration

This repository contains a Python script that integrates **Google Workspace Alert Center** with **Wazuh**, extracting security-related events via Google’s official API and formatting them into structured JSON logs under `/var/ossec/logs/google_workspace/`.

> 🔐 This project enables visibility into Google Workspace security alerts from within Wazuh or any SIEM platform.

---

## 🧠 What does this script do?

- Authenticates using a **delegated service account** to access the Google Workspace Alert Center.
- Fetches newly generated alerts (avoids duplicates).
- Outputs logs in JSON format, easy to parse and visualize with Wazuh.
- Uses a local cache file (`alert_cache.json`) to track already-processed alerts.

---

## 🚀 How to set it up?

All configuration and setup steps — including Google Cloud service account creation, domain-wide delegation, API scopes, and Wazuh integration — are explained in my LinkedIn post:

🔗 **[See full guide in my LinkedIn post](https://www.linkedin.com/pulse/exporting-google-workspace-alert-center-logs-siem-emir-ataide-codof)**

---

## 📁 Key Files

- `fetch_alerts.py`: Main script to query and process alerts.
- `alert_cache.json`: Local cache to avoid reprocessing.
- `alert_center.log`: Log file with structured JSON alerts.

---

## ⚙️ Requirements

- Python 3.7+
- Google Cloud SDK (`gcloud`) for initial authentication
- Service Account with **domain-wide delegation** enabled
- Scope: `https://www.googleapis.com/auth/apps.alerts`
- Workspace domain with **Alert Center enabled**
- The customerId of your Google Workspace domain
- Wazuh agent/server access to `/var/ossec/logs/`

Note: The Google Cloud SDK (gcloud) is optional and primarily useful for initial setup and testing. The integration works standalone using only Python and the Google API libraries.

---

## 🙌 Contributing

Contributions are welcome to improve or expand this script — e.g., adding support for other Google Workspace APIs (Admin SDK, Gmail API, etc.). If your organization uses Google Workspace, this integration may greatly improve your visibility in centralized SIEM dashboards.

---

## 📄 License

MIT License — free to use, modify, and share.

