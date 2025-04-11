# Atlassian Cloud Backup

Two Python scripts for managing backups for Jira and Confluence.

`start_backup.py` logs into all defined Jira and Confluence sites to initiate the backup.

`start_download.py` can be scheduled after the backup is finished (for example, the day after, depending on how large your sites are). It logs into all Jira and Confluence sites and downloads the backup files to the defined location.

The scripts will send Heartbeats and Alerts to Opsgenie

## Installation

Create `config.py`:

```python
SETTINGS = {
    'USERNAME': '',
    'TOKEN': '',
    'CONFLUENCE_SITES': ['xxx'],
    'JIRA_SITES': ['xxx'],
    'BACKUP_PATH': r'', 
    'NUMBER_OF_FILES_TO_KEEP': 14, 
    'SLACK_WEBHOOK': '', 
    'HEARTBEAT': '',
    'OPSGENIE_URL': 'https://api.eu.opsgenie.com/v2/', 
    'OPSGENIE_API_KEY': ''
    }

```

## Required libarys

pip install selenium 
pip install tqdm 
pip install requests 
pip install msedge-selenium-tools 
pip install webdriver-manager 