from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from utils import login, click_element, send_slack_message

def main_start(settings):         
    try: 
        driver = webdriver.Edge(service=Service(settings['webdriver_path'] + '\msedgedriver.exe'))
        wait = WebDriverWait(driver, 10)
    except Exception as e: 
        send_slack_message(f"Failed to start WebDriver. {e}", settings['slack_webhook'])

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