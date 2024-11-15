import time
import os
from datetime import datetime
from pathlib import Path

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from .management.commands.create_session import create_pre_authenticated_session
from .server_tools import create_session_on_server


from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .server_tools import reset_database

MAX_WAIT = 20

SCREEN_DUMP_LOCATION = Path(__file__).absolute().parent / 'screendumps'

User = get_user_model()

def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        # staging_server
        self.browser = webdriver.Firefox()
        self.test_server = os.environ.get('TEST_SERVER')
        if self.test_server:
            self.live_server_url = "http://" + self.test_server
            reset_database(self.test_server)

    def tearDown(self):
        if self._test_has_failed():
            if not SCREEN_DUMP_LOCATION.exists():
                SCREEN_DUMP_LOCATION.mkdir(parents=True)
            self.take_screenshot()
            self.dump_html()
        self.browser.quit()
        super().tearDown()

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def wait_to_be_logged_in(self, email):

        self.browser.find_element(By.CSS_SELECTOR, '#id_logout')
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):

        self.browser.find_element(By.CSS_SELECTOR, 'input[name=email]')
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertNotIn(email, navbar.text)

    def _test_has_failed(self):
        # slightly obscure but couldn't find a better way!
        return self._outcome.result.failures or self._outcome.result.errors

    def take_screenshot(self):
        path = SCREEN_DUMP_LOCATION / self._get_filename('png')
        print('screenshotting to', path)
        self.browser.get_screenshot_as_file(str(path))

    def dump_html(self):
        path = SCREEN_DUMP_LOCATION / self._get_filename('html')
        print('dumping page HTML to', path)
        path.write_text(self.browser.page_source)

    def _get_filename(self, extension):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return (
            f'{self.__class__.__name__}.{self._testMethodName}-{timestamp}.{extension}'
        )

    def create_pre_authenticated_session(self, email):

        if self.test_server:
            session_key = create_session_on_server(self.test_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session_key,
                path='/',
            )
        )
