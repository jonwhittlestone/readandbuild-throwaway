from django.test import LiveServerTestCase
from selenium import webdriver
import logging

logger = logging.getLogger(__name__)

class PostTestCase(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def test_i_see_posts(self):
        home_page = self.browser.get(self.live_server_url + '/posts/')

        header = self.browser.find_element_by_css_selector('h1')
        self.assertEqual('Welcome', header.text)

        #logger.error('')
        #logger.error(">> " + self.live_server_url + '/posts')

        #self.fail('Incomplete Test')