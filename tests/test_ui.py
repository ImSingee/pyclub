
import time
import unittest
from selenium import webdriver


class TestURLs(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()

    def test_add_new_post(self):
        """ Tests if the new post page saves a Post object to the
            database

            1. Log the user in
            2. Go to the new_post page
            3. Fill out the fields and submit the form
            4. Go to the home page and verify that the post is
               on the page
        """
        # login
        self.driver.get("http://localhost:2333/main/login")
        time.sleep(2)

        username_field = self.driver.find_element_by_name("username")
        username_field.send_keys("admin")

        password_field = self.driver.find_element_by_name("password")
        password_field.send_keys("password")

        login_button = self.driver.find_element_by_id("login")
        login_button.click()

        # fill out the form
        self.driver.get("http://localhost:2333/Tiezi/new")

        title_field = self.driver.find_element_by_name("title")
        title_field.send_keys("Test Title")

        # find the editor in the iframe
        #等待js加载
        time.sleep(3)
        self.driver.switch_to.frame(
            self.driver.find_element_by_tag_name("iframe")
        )
        post_field = self.driver.find_element_by_class_name(
            "cke_editable"
        )
        post_field.send_keys("Test content")
        self.driver.switch_to.parent_frame()

        post_button = self.driver.find_element_by_class_name("btn-primary")
        post_button.click()

        # verify the post was created
        self.driver.get("http://localhost:2333/Tiezi/")
        self.assertIn("Test Title", self.driver.page_source)
        self.assertIn("Test content", self.driver.page_source)


if __name__ == "__main__":
    unittest.main()