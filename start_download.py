from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.webdriver import WebDriver as Edge
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from utils import login, download_backup, delete_old_files, today, send_slack_message

def main_backup(settings):
    auth = (settings['username'], settings['token'])
    backup_path = settings['backup_path']
    
    try:
        options = EdgeOptions()
        options.use_chromium = True
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = Edge(service=service, options=options)
        wait = WebDriverWait(driver, 10)
    except Exception as e:
        handle_error("Failed to start WebDriver", e, settings['slack_webhook'])
        return

    def handle_error(message, error, webhook):
        print(f"{message}. Error: {error}")
        send_slack_message(message, webhook)

    def process_sites(sites, url_suffix, element_id, product):
        for site in sites:
            driver.get(f"https://{site}.atlassian.net/{url_suffix}")
            login(wait, settings['username'])
            filename = f"{backup_path}\{today()}_{site}_{product}.zip"
            try:
                delete_old_files(backup_path, settings['number_of_files_to_keep'])
                download_backup(wait, element_id, filename, auth)
                send_slack_message(f"Backup for {product} - {site} is downloaded completely", settings['slack_webhook'])
            except Exception as e:
                handle_error(f"Failed to download backup {product} - {site}", e, settings['slack_webhook'])

    process_sites(settings['confluence_sites'], "wiki/plugins/servlet/ondemandbackupmanager/admin", "backupLocation", "confluence")
    process_sites(settings['jira_sites'], "secure/admin/CloudExport.jspa", "cloudBackupLocation", "jira")

    driver.quit()

if __name__ == "__main__":
    import config
    main_backup(config.SETTINGS)