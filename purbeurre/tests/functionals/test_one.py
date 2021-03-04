from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time

opts = Options()
opts.headless = True
assert opts.headless  # Operating in headless mode

"""a user sign in, search "nutella", add a product in favorites and look aliments page"""
driver = Chrome(options=opts)
driver.get('http://localhost:8000/')
assert "Pur Beurre" in driver.title

#need to have no "user_test" already register
button = driver.find_element_by_css_selector("span")
button.click()
time.sleep(1)
login = driver.find_element_by_css_selector("ul > li:nth-child(2)")
login.click()
time.sleep(1)
register = driver.find_element_by_css_selector(".login > a")
register.click()
time.sleep(1)
title = driver.find_element_by_css_selector(".login > h3")
assert title.text == "Création d'un compte."

fill = driver.find_element_by_css_selector(".login > form > p:nth-child(2) > input")
fill.send_keys("user_test")
fill = driver.find_element_by_css_selector("form > p:nth-child(3) > input")
fill.send_keys("user_test@exemple.com")
fill = driver.find_element_by_css_selector("form > p:nth-child(4) > input")
fill.send_keys("user_test_pass")
fill = driver.find_element_by_css_selector("form > p:nth-child(5) > input")
fill.send_keys("user_test_pass")
button = driver.find_element_by_xpath("/html/body/div/form/input[@type='submit'][@value='Créer']")
button.click()
time.sleep(1)
home = driver.find_element_by_css_selector("h1")
assert home.text == "DU GRAS, OUI MAIS DE QUALITÉ!"

search = driver.find_element_by_css_selector(".input-group > input")
search.send_keys("nutella")
search.send_keys(Keys.RETURN)
#id="crema di nocciole"
save = driver.find_element_by_css_selector(".saving")
save.click()
time.sleep(1)
button = driver.find_element_by_css_selector(".modal-footer > button")
button.click()
time.sleep(1)
button = driver.find_element_by_css_selector("span")
button.click()
time.sleep(1)
link = driver.find_element_by_css_selector("ul > li:nth-child(3)")
link.click()
time.sleep(1)
aliment = driver.find_element_by_css_selector(".bg-light > a")
assert aliment.text == "crema di nocciole"

driver.close()