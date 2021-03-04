from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time

opts = Options()
opts.headless = True
assert opts.headless  # Operating in headless mode

"""user_test log in and look his home page"""
driver = Chrome()
driver.get('http://localhost:8000/')
assert "Pur Beurre" in driver.title

#need to have  "user_test" already register
button = driver.find_element_by_css_selector("span")
button.click()
time.sleep(1)
login = driver.find_element_by_css_selector("ul > li:nth-child(2)")
login.click()
time.sleep(1)
login = driver.find_element_by_name("username")
login.send_keys("user_test")
login = driver.find_element_by_name("password")
login.send_keys("user_test_pass")
login = driver.find_element_by_xpath("//input[@type='submit'][@value='Login']")
login.click()
time.sleep(1)
button = driver.find_element_by_css_selector("span")
button.click()
time.sleep(1)
login = driver.find_element_by_css_selector("ul > li:nth-child(2)")
login.click()
time.sleep(1)
mail = driver.find_element_by_css_selector(".profil > div > span")
assert mail.text == "user_test@exemple.com"

button = driver.find_element_by_css_selector("span")
button.click()
time.sleep(1)
login = driver.find_element_by_css_selector("ul > li:nth-child(3)")
login.click()
time.sleep(1)
link = driver.find_element_by_css_selector(".third-screen > div > a")
link.click()
time.sleep(1)


driver.close()