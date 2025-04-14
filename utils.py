from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from tqdm import tqdm
import requests
import logging
import os
import glob
import uuid

from config import SETTINGS

def setup_logging():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s', 
        filename='logs\\audit.log', 
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)

def delete_old_files(path, number_of_files_to_keep):
    files = glob.glob(path + '\*.zip')
    files.sort(reverse=True)
    if len(files) > number_of_files_to_keep:
        for file in files[number_of_files_to_keep:]:
            os.remove(file)   

def download_backup(wait, element_id, filename, auth):   
    backup_link = find_element(wait, By.ID, element_id).find_element(By.XPATH, ".//a").get_attribute("href")
    logging.info(f"Backup link: {backup_link}")
    response = requests.get(backup_link, auth=auth, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        try:
            with open(filename, 'wb') as f, tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
                for data in response.iter_content(block_size):
                    f.write(data)
                    pbar.update(len(data))
        except Exception as e:
            logging.error(f"Failed to save backup {filename}: {e}")
            raise

def find_element(wait, locator_type, element_id):
    try:
        wait.until(EC.presence_of_element_located((locator_type, element_id)))
        return wait._driver.find_element(locator_type, element_id)
    except:
        logging.warning(f"Element_id: {element_id} was not found")

def enter_text(wait, element_id, text, locator_type=By.ID):
    input_element = find_element(wait, locator_type, element_id)
    input_element.clear()
    input_element.send_keys(text)

def click_element(wait, element_id, locator_type=By.ID):
    element = find_element(wait, locator_type, element_id)
    element.click()

def login(wait, username):
    global is_logged_in
    if not is_logged_in:
        enter_text(wait, "username", username)
        click_element(wait, "login-submit")
        try:
            click_element(wait, f"//small[text()='{username}']", By.XPATH)
        except:
            pass
        is_logged_in = True

def today():
    return datetime.now().strftime('%y%m%d')

def send_slack_message(message):
    response = requests.post(SETTINGS['SLACK_WEBHOOK'], json={'text': message}, verify=False)
    if response.status_code != 200:
        logging.error(f"Failed to send slack message: {response.text}")

def send_opsgenie_hartbeat_ping(heartbeat):
    url = SETTINGS['OPSGENIE_URL'] + "heartbeats/" + heartbeat + "/ping"
    headers = {"Authorization": f"GenieKey {SETTINGS['OPSGENIE_API_KEY']}"}
    response = requests.post(url, headers=headers)
    if response.status_code == 202:
        logging.info(f"OpsGenie heartbeat ping sent successfully")
    else:
        logging.error(f"Failed to send OpsGenie heartbeat ping: {response.text}")
        
        

def create_opsgenie_alarm(message, description):
    url = SETTINGS['OPSGENIE_URL'] + "alerts"
    
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"GenieKey {SETTINGS['OPSGENIE_API_KEY']}"
    }
    
    data = {
        "message": message,
        "alias": "atlassian-backup-" + uuid.uuid4().hex,
        "description": description,
        "responders": [
            {
                "type": "team",
                "name": "fremtind-team-atlassian"
            }
        ],
        "priority": "P2"
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 202:
        logging.info(f"OpsGenie alarm sent successfully: {data}")
    else:
        logging.error(f"Failed to send OpsGenie alarm: {response.text}")
        
    
is_logged_in = False
setup_logging()