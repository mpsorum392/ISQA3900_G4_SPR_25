
#unit test file to determine if the Mens available items are displayed when user clicks
#the mens link on the home page

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Edge()

    def test_ll(self):

        driver = self.driver
        driver.maximize_window()
        user = "testuser"
        pwd = "test123"
        driver.get("http://127.0.0.1:8000/admin")
        time.sleep(3)
        elem = driver.find_element(By.ID,"id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID,"id_password")
        elem.send_keys(pwd)
        time.sleep(3)
        elem.send_keys(Keys.RETURN)
        driver.get("http://127.0.0.1:8000")
        time.sleep(3)
        # find 'Shop Mens' and click it – note this is all one Python statement
        driver.find_element(By.XPATH, "//a[contains(., 'Shop Mens')]").click()

        time.sleep(5)
        try:
            # verify Mens items exist on screen after clicking 'Mens'
            # note that this test requires at least one mens item in the database
            elem = driver.find_element(By.LINK_TEXT, "Add to Cart")
            self.driver.close()
            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("Men's items do not appear when Shop Mens link is clicked")

        time.sleep(2)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
