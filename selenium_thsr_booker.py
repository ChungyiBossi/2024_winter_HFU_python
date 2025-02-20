import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select  # 下拉式選單使用
from selenium.common.exceptions import NoSuchElementException  # Handle exception
from ocr_component import get_captcha_code

options = webdriver.ChromeOptions()  # 創立 driver物件所需的參數物件
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
driver.get("https://irs.thsrc.com.tw/IMINT/")

# Click accept cookie button
accept_cookie_button = driver.find_element(By.ID, "cookieAccpetBtn")
accept_cookie_button.click()

# Choose Booking parameters: startStation, destStation, time
start_station_element = driver.find_element(By.NAME, 'selectStartStation')
Select(start_station_element).select_by_visible_text('台中')

dest_station_element = driver.find_element(By.NAME, 'selectDestinationStation')
Select(dest_station_element).select_by_visible_text('板橋')

start_time_element = driver.find_element(By.NAME, 'toTimeTable')
Select(start_time_element).select_by_visible_text('18:30')

# Choose Booking parameters: date
driver.find_element(
    By.XPATH, "//input[@class='uk-input' and @readonly='readonly']").click()

start_date = '二月 21, 2025'
driver.find_element(
    By.XPATH, f"//span[@class='flatpickr-day' and @aria-label='{start_date}']").click()

while True:
    # captcha
    captcha_img = driver.find_element(
        By.ID, 'BookingS1Form_homeCaptcha_passCode')
    captcha_img.screenshot('captcha.png')
    captcha_code = get_captcha_code()
    captcha_input = driver.find_element(By.ID, 'securityCode')
    captcha_input.send_keys(1234)
    time.sleep(2)

    # submit
    driver.find_element(By.ID, 'SubmitButton').click()
    time.sleep(5)

    # check validation is success or not
    try:
        # driver.find_element(By.CLASS_NAME, 'uk-alert-danger uk-alert')
        driver.find_element(By.ID, 'divErrMSG')
    except NoSuchElementException:
        print("進到第二步驟")
        break


time.sleep(2000)
driver.quit()
