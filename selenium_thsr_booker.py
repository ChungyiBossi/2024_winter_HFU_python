import pprint
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

#
# 第一個頁面
#

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
    captcha_input.send_keys(captcha_code)
    time.sleep(2)

    # submit
    driver.find_element(By.ID, 'SubmitButton').click()

    # check validation is success or not
    try:
        time.sleep(5)
        driver.find_element(By.ID, 'BookingS2Form_TrainQueryDataViewPanel')
        print("驗證碼正確, 進到第二步驟")
        break
    except NoSuchElementException:
        print("驗證碼錯誤，重新驗證")


#
# 第二個頁面
#

trains_info = list()
trains = driver.find_element(
    By.CLASS_NAME, 'result-listing').find_elements(By.TAG_NAME, 'label')
for train in trains:
    # depart_time = train.find_element(By.ID, 'QueryDeparture').text
    # arrival_time = train.find_element(By.ID, 'QueryArrival').text
    # duration = train.find_element(
    #     By.CLASS_NAME, 'duration').find_elements(By.TAG_NAME, 'span')[1].text
    # train_code = train.find_element(By.ID, 'QueryCode').text
    # radio_box = train.find_element(By.CLASS_NAME, 'uk-radio')
    info = train.find_element(By.CLASS_NAME, 'uk-radio')
    trains_info.append(
        {
            # info.get('屬性名稱')
            'depart_time': info.get_attribute('querydeparture'),
            'arrival_time': info.get_attribute('queryarrival'),
            'duration': info.get_attribute('queryestimatedtime'),
            'train_code': info.get_attribute('querycode'),
            'radio_box': info,
        }
    )

pprint.pprint(trains_info)
# Choose train
for idx, train in enumerate(trains_info):
    print(
        f"({idx}) - {train['train_code']}, 行駛時間={train['duration']} | {train['depart_time']} -> {train['arrival_time']}")

which_train = int(input("Choose your train. Enter from 0~9:\n"))
trains_info[which_train]['radio_box'].click()


# Submit booking requests
driver.find_element(By.NAME, 'SubmitButton').click()


time.sleep(2000)
driver.quit()
