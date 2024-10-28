# Atlassian Cloud Backup

Two Python scripts for managing backups for Jira and Confluence.

`start_backup.py` logs into all defined Jira and Confluence sites to initiate the backup.

`start_download.py` can be scheduled after the backup is finished (for example, the day after, depending on how large your sites are). It logs into all Jira and Confluence sites and downloads the backup files to the defined location.

The scripts will send a message to a defined Slack channel when finish. 

## Installation

Create `config.py`:

```python
SETTINGS = {
    'username': '',
    'token': '',
    'confluence_sites': ['xxx', 'yyy'],
    'jira_sites': ['xxx', 'yyy'],
    'backup_path': r'c:\temp', 
    'slack_webhook': '',
    'number_of_files_to_keep': 10
}
```

## Required libarys

pip install selenium 
pip install tqdm 
pip install requests 
pip install msedge-selenium-tools 
pip install webdriver-manager 