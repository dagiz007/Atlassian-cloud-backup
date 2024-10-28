from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.webdriver import WebDriver as Edge
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from utils import login, download_backup, delete_old_files, today, send_slack_message

def main_start(settings):         
    try: 
        options = EdgeOptions()
        options.use_chromium = True
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = Edge(service=service, options=options)
        wait = WebDriverWait(driver, 10)
    except Exception as e: 
        print(f"Failed to start WebDriver. Error: {e}")
        send_slack_message("Failed to start WebDriver.", settings['slack_webhook'])
        return

    def process_sites(sites, url_suffix, element_id, product):
        for site in sites:
            driver.get(f"https://{site}.atlassian.net/{url_suffix}")
            login(wait, settings['username'])
            try:
                click_element(wait, element_id)
                send_slack_message(f"Backup for {product} - {site} started", settings['slack_webhook'])
            except:
                send_slack_message(f"Failed to start backup for {product} - {site}", settings['slack_webhook'])
    
    process_sites(settings['confluence_sites'], "wiki/plugins/servlet/ondemandbackupmanager/admin", "submit", "confluence")
    process_sites(settings['jira_sites'], "secure/admin/CloudExport.jspa", "submit-cloud-new", "jira")
    
    driver.quit()

if __name__ == "__main__": 
    import config
    main_start(config.SETTINGS)