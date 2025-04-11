from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.webdriver import WebDriver as Edge
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from utils import *

def main_start(settings):         
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
            driver.get(f"https://{site}.atlassian.net/{url_suffix}")
            login(wait, SETTINGS['USERNAME'])
            try:
                click_element(wait, element_id)
                send_opsgenie_hartbeat_ping(SETTINGS['HEARTBEAT'])
            except Exception as e: 
                create_opsgenie_alarm(f"Failed to start backup {product} - {site}", e)
                    
    process_sites(SETTINGS['CONFLUENCE_SITES'], "wiki/plugins/servlet/ondemandbackupmanager/admin", "submit", "confluence")
    process_sites(SETTINGS['JIRA_SITES'], "secure/admin/CloudExport.jspa", "submit-cloud-new", "jira")
    
    driver.quit()

if __name__ == "__main__": 
    import config
    main_start(config.SETTINGS)