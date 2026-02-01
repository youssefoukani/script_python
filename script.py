from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

LOGIN_URL = "https://collegio-booking-bue9.vercel.app/login"
BOOKING_URL = "https://collegio-booking-bue9.vercel.app/aule-studio"

USERNAME = ""
PASSWORD = ""

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
    print("Login successful")

def prenota_aula():
    driver.get(BOOKING_URL)

    aula = wait.until(EC.presence_of_element_located((By.XPATH, PATH_AULA)))
    aula.click()

    conferma = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div/main/div/div/div[3]/div[2]/div[2]/div[2]/button[2]")
        )
    )
    conferma.click()

    time.sleep(3)
    print("Prenotazione successful")

try:
    login()
    prenota_aula()
finally:
    driver.quit()
