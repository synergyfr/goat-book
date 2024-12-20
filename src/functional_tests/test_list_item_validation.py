from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .list_page import ListPage

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def setUp(self):
        self.list_page = ListPage(self)
        super().setUp()

    def get_error_element(self):
        return self.browser.find_element(
                    By.CSS_SELECTOR, '.invalid-feedback')

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.list_page.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load the list page
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid')
        )

        # She starts typing some text for the new item and the error disappears
        self.list_page.get_item_input_box().send_keys('Purchase milk')
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid')
        )

        # And she can submit it successfully
        self.list_page.get_item_input_box().clear()
        self.list_page.add_list_item('Purchase milk')

        # Perversely, she now decides to submit a second blank list item
        self.list_page.get_item_input_box().send_keys(Keys.ENTER)

        # Again, the browser will not comply
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid')
        )

        # And she can make it happy by filling some text in
        self.list_page.get_item_input_box().send_keys('Make tea')
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid')
        )
        self.list_page.get_item_input_box().clear()
        self.list_page.add_list_item('Make tea')

    def test_cannot_add_duplicate_items(self):

        # Edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.list_page.add_list_item('Buy wellies')

        # She accidentally tries to enter a duplicate item
        self.list_page.get_item_input_box().send_keys('Buy wellies')
        self.list_page.get_item_input_box().send_keys(Keys.ENTER)

        # She sees a helpful error message
        self.wait_for(
            lambda: self.assertEqual(
                self.get_error_element().text,
                'You\'ve already got this in your list'
            )
        )

    def test_error_messages_are_cleared_on_input(self):

        # Edith starts a list and causes a validation error:
        self.browser.get(self.live_server_url)
        self.list_page.add_list_item('Banter too thick')
        self.list_page.get_item_input_box().send_keys('Banter too thick')
        self.list_page.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.assertTrue(self.get_error_element().is_displayed())
        )

        # She starts typing in the input box to clear the error
        self.list_page.get_item_input_box().send_keys('a')

        # She is pleased to see that the error message disappears
        self.wait_for(
            lambda: self.assertFalse(self.get_error_element().is_displayed())
        )
