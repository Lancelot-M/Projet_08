from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

"""user search "POUIC" and get a empty page"""
opts = Options()
opts.headless = True
assert opts.headless  # Operating in headless mode

driver = Chrome(options=opts)
driver.get('http://localhost:8000/home/')
assert "Pur Beurre" in driver.title

search_form = driver.find_element_by_id('main-search-bar')
search_form.send_keys("POUIC")
search_form.send_keys(Keys.RETURN)
result = driver.find_element_by_class_name('bubble')
assert result.text == "pouic"

driver.close()