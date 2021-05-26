import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['mail_ru']
db_emails = db.emails

driver = webdriver.Chrome("..\\..\\venv\chromedriver.exe")
driver.get("https://www.mail.ru")
elem = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                   "//input[contains(@class, 'email-input')]")))
elem.send_keys("study.ai_172")
elem.send_keys(Keys.ENTER)
elem = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                   "//input[contains(@class, 'password-input')]")))
elem.send_keys("NextPassword172!")
elem.send_keys(Keys.ENTER)
elem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'llc')]")))
elem.send_keys(Keys.ENTER)
emails = list()
email = dict()
curr_email = None
prev_email = None
count = 0
while True:
    curr_email = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'thread__letter')]"))
    ).get_attribute("data-id")
    sender_el = driver.find_element(By.XPATH, "//span[contains(@class, 'letter-contact')]")
    if curr_email == prev_email:
        break
    email["Email"] = sender_el.get_attribute("title")
    email["Sender"] = sender_el.text
    email["Subject"] = driver.find_element(By.XPATH, "//h2[contains(@class, 'thread__subject')]").text
    id_body = f"//div[contains(@id,'style_{curr_email}_BODY')]"
    email["Body"] = driver.find_element(By.XPATH, id_body).text
    email["Date"] = driver.find_element(By.XPATH, "//div[contains(@class, 'letter__date')]").text
    prev_email = curr_email
    emails.append(email.copy())
    if db_emails.count_documents(email) == 0:
        db_emails.insert_one(email.copy())
    else:
        break
    elem = driver.find_element(By.TAG_NAME, "body")
    elem.send_keys(Keys.LEFT_CONTROL + Keys.ARROW_DOWN)
    count += 1
    time.sleep(3)
    # break
print(count)
for el in emails:
    print(el)

