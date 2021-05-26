from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['eldorado']
db_notes = db.notes

driver = webdriver.Chrome("..\\..\\venv\chromedriver.exe")
driver.get("https://www.eldorado.ru/c/noutbuki")
count = 1
note = dict()
while True:
    while True:
        find = f"//li[contains(@data-product-index, '{count}')]"
        try:
            ell = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, find)))
            item = ell.find_element(By.XPATH, ".//a[contains(@data-dy, 'title')]")
            note["Name"] = item.text
            note["Link"] = item.get_attribute("href")
            if db_notes.count_documents({"Link": {"$eq": note["Link"]}}) == 0:
                db_notes.insert_one(note.copy())
            count += 1
        except Exception as exp:
            print(exp)
            break
    try:
        btn_next = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(@class, 'sk')]")
        ))
        print("Next")
        btn_next.click()
    except Exception:
        break
print(count)
driver.close()
