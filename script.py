from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import datetime



LOGIN_URL = os.environ["URL_LOGIN"]
BOOKING_URL = os.environ["URL_PRENOTAZIONE"]

USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]

PATH_AULA = "/html/body/div/div/main/div/div/div[2]/div[5]/div[2]/div/button[7]"

# ===== HEADLESS OBBLIGATORIO =====
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

wait = WebDriverWait(driver, 20)


def wait_until_after_midnight():
    while True:
        now = datetime.utcnow()
        if now.hour == 13 and now.minute == 43 and now.second >= 1:
            break
        time.sleep(1)
        
def login():
    driver.get(LOGIN_URL)

    username_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div/div[2]/div[2]/form/div[1]/div/input")
        )
    )
    password_input = driver.find_element(
        By.XPATH, "/html/body/div/div/div[2]/div[2]/form/div[2]/div/div/input")
    
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)

    driver.find_element(
        By.XPATH, "/html/body/div/div/div[2]/div[2]/form/button"
    ).click()

    wait.until(EC.url_to_be("https://collegio-booking-bue9.vercel.app/"))
    print("Login done at:", datetime.utcnow())
    
def prenota_aula():
    
    driver.get(BOOKING_URL)
    print("Entered booking page at:", datetime.utcnow())

    aula = wait.until(EC.presence_of_element_located((By.XPATH, PATH_AULA)))
    aula.click()

    conferma = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div/main/div/div/div[3]/div[2]/div[2]/div[2]/button[2]")
        )
    )
    conferma.click()
    print("Booked at:", datetime.utcnow())

    time.sleep(2)
    

try:
    login()
    wait_until_after_midnight()
    prenota_aula()
finally:
    driver.quit()
