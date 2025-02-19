import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Step 1, 2:
driver = webdriver.Chrome()
# driver = webdriver.Firefox()
# driver = webdriver.Edge()
# driver = webdriver.Safari()
driver.get("https://www.selenium.dev/selenium/web/web-form.html")

# Step 4:
driver.implicitly_wait(2)
print("driver already wait 2 secs")

# Step 5:
# text_box = soup.find(name='my-text') # bs4的寫法
text_box = driver.find_element(by=By.NAME, value="my-text")
# submit_button = soup.find('button') # bs4的寫法
submit_button = driver.find_element(by=By.TAG_NAME, value="button")
# submit_button = soup.css.select('button') # bs4的寫法
submit_button = driver.find_element(By.CSS_SELECTOR, "button")

# Step 5.1: 找到其他的textbox
password_text_box = driver.find_element(By.NAME, "my-password")
textarea = driver.find_element(By.TAG_NAME, 'textarea')

# Step 6:
text_box.send_keys("xxxxxxxxxxxxx")
password_text_box.send_keys("P@55w0rd")
textarea.send_keys("An apple a day, keeps doctor away.")
time.sleep(5)
submit_button.click()

time.sleep(10)
driver.quit()
