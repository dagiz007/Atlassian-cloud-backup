from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.webdriver import WebDriver as Edge
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from utils import *

def main_backup(SETTINGS):
    auth = (SETTINGS['USERNAME'], SETTINGS['TOKEN'])
    backup_path = SETTINGS['BACKUP_PATH']
    
    try:
        options = EdgeOptions()
        options.use_chromium = True
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = Edge(service=service, options=options)
        wait = WebDriverWait(driver, 10)
    except Exception as e:
        create_opsgenie_alarm("Failed to start WebDriver", e)
        return

    def process_sites(sites, url_suffix, element_id, product):
        for site in sites:
            try:
                driver.get(f"https://{site}.atlassian.net/{url_suffix}")
                login(wait, SETTINGS['USERNAME'])
                filename = f"{backup_path}\{today()}_{site}_{product}.zip"
            
                delete_old_files(backup_path, SETTINGS['NUMBER_OF_FILES_TO_KEEP'])
                download_backup(wait, element_id, filename, auth)
                send_opsgenie_hartbeat_ping(SETTINGS['HEARTBEAT'])
            except Exception as e:
                create_opsgenie_alarm(f"Failed to download backup {product} - {site}", e)
                
    process_sites(SETTINGS['CONFLUENCE_SITES'], "wiki/plugins/servlet/ondemandbackupmanager/admin", "backupLocation", "confluence")
    process_sites(SETTINGS['JIRA_SITES'], "secure/admin/CloudExport.jspa", "cloudBackupLocation", "jira")

    driver.quit()

if __name__ == "__main__":
    import config
    main_backup(config.SETTINGS)