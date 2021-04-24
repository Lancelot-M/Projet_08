import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

"""
a user sign in, search "nutella", add a product in favorites and
look aliments page
"""


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ["dump.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.headless = True
        cls.selenium = Chrome(options=opts)
        cls.selenium.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        button = self.selenium.find_element_by_css_selector("span")
        button.click()
        time.sleep(1)
        login = self.selenium.find_element_by_css_selector("ul > "
                                                           "li:nth-child(2)")
        login.click()
        time.sleep(1)
        register = self.selenium.find_element_by_css_selector(".login > a")
        register.click()
        time.sleep(1)
        title = self.selenium.find_element_by_css_selector(".login > h3")
        assert title.text == "Création d'un compte."
        fill = self.selenium.find_element_by_css_selector(".login > form >"
                                                          " p:nth-child(2) >"
                                                          " input")
        fill.send_keys("user_test")
        fill = self.selenium.find_element_by_css_selector(".login > form >"
                                                          " p:nth-child(3) >"
                                                          " input")
        fill.send_keys("user_test@exemple.com")
        fill = self.selenium.find_element_by_name("password1")
        fill.send_keys("OIEJ?DZZpass99999")
        fill = self.selenium.find_element_by_name("password2")
        fill.send_keys("OIEJ?DZZpass99999")
        time.sleep(1)
        button = self.selenium.find_element_by_xpath("/html/body/div/form/"
                                                     "input[@type='submit']")
        button.click()
        time.sleep(1)
        home = self.selenium.find_element_by_css_selector("h1")
        assert home.text == "DU GRAS, OUI MAIS DE QUALITÉ!"
        search = self.selenium.find_element_by_css_selector(".input-group >"
                                                            " input")
        search.send_keys("nutella")
        search.send_keys(Keys.RETURN)
        time.sleep(1)
        save = self.selenium.find_element_by_css_selector(".saving")
        save.click()
        time.sleep(1)
        button = self.selenium.find_element_by_css_selector(".modal-footer >"
                                                            " button")
        button.click()
        time.sleep(1)
        button = self.selenium.find_element_by_css_selector("span")
        button.click()
        time.sleep(1)
        link = self.selenium.find_element_by_css_selector("ul > "
                                                          "li:nth-child(3)")
        link.click()
        time.sleep(1)
        aliment = self.selenium.find_element_by_css_selector(".bg-light > a")
        assert aliment.text == "pâte à tartiner cacao"

    def test_show_info(self):
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        button = self.selenium.find_element_by_css_selector("span")
        button.click()
        time.sleep(1)
        login = self.selenium.find_element_by_css_selector("ul > li:nth"
                                                           "-child(2)")
        login.click()
        time.sleep(1)
        login = self.selenium.find_element_by_name("username")
        login.send_keys("purbeurre")
        login = self.selenium.find_element_by_name("password")
        login.send_keys("purbeurre")
        login = self.selenium.find_element_by_xpath("//input[@type='submit'"
                                                    "][@value='Login']")
        login.click()
        time.sleep(1)
        button = self.selenium.find_element_by_css_selector("span")
        button.click()
        time.sleep(1)
        login = self.selenium.find_element_by_css_selector("ul > li:nth-"
                                                           "child(2)")
        login.click()
        time.sleep(1)
        button = self.selenium.find_element_by_css_selector("span")
        button.click()
        time.sleep(1)
        login = self.selenium.find_element_by_css_selector("ul > li:nth-"
                                                           "child(3)")
        login.click()
        time.sleep(1)
        link = self.selenium.find_element_by_css_selector(".third-screen > "
                                                          "div > a")
        link.click()
        time.sleep(1)
