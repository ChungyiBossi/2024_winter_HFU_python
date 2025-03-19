
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint

options = webdriver.ChromeOptions()  # 創立 driver物件所需的參數物件
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
driver.get("https://www.akc.org/dog-breeds/shiba-inu/")


accept_cookie = driver.find_element(By.ID, "onetrust-accept-btn-handler")
accept_cookie.click()
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 　Use JavaScript
# elements_texts = driver.execute_script(
#     "return Array.from(document.querySelectorAll('p.breed-table__accordion-padding__p')).map(el => el.innerText);"
# )

# find preloaded JSON-Like Data
element = driver.find_element(
    By.XPATH, "//div[@data-js-component='breedPage']")
data = element.get_attribute("data-js-props")

data = json.loads(data)

with open("breed_data.json", 'w') as output:
    json.dump(data, output, indent=4)


time.sleep(2000)
driver.quit()
