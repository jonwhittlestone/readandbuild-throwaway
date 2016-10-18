from django.test import LiveServerTestCase
from selenium import webdriver
from django.contrib.auth import get_user_model

import logging
import pdb

logger = logging.getLogger(__name__)

class PostTestCase(LiveServerTestCase):
    """
        Testing posts:
            - A home page with blog listing and pagination
                - test url for homepage
                - I can see more than one blog entry on the home page
            - Staff can create add post content
            - A create blog post page with input elements
            - The create blog post page is behind auth
            - A functional test for creating with publish date
            - A functional test for draft state
            - Author search
            - Pagination
    """
    admin_username = 'admin'
    admin_email = 'dev@howapped.com'
    admin_password = 'password'

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(2)
        self.admin_user = get_user_model().objects.create_superuser(
            username = self.admin_username,
            email=self.admin_email,
            password=self.admin_password
        )

    def tearDown(self):
        self.browser.quit()

    def staff_login(self):
        login_form = self.browser.find_element_by_id(
            'login-form')
        login_form.find_element_by_name('username'). \
            send_keys(self.admin_username)
        login_form.find_element_by_name('password'). \
            send_keys(self.admin_password)
        login_form.find_element_by_css_selector(
            '.submit-row input').click()

    def test_i_see_posts_on_home_page(self):
        """
        test url for homepage
        :return:
        """

        home_page = self.browser.get(self.live_server_url + '/')

        header = self.browser.find_element_by_css_selector('h1')
        self.assertEqual('Welcome', header.text,
                         'I could not see Welcome on the homepage')


        #logger.error('')
        #logger.error(">> " + self.live_server_url + '/posts')

        #self.fail('Incomplete Test')

    def test_staff_user_can_login(self):
        admin_root = self.browser.get(
            self.live_server_url + '/admin/')
        self.staff_login()


    def test_staff_can_add_content(self):
        """
            Tests that a 'staff' user can access the admin and
                   add Posts
        """

        admin_root = self.browser.get(
            self.live_server_url + '/admin/')

        self.assertEqual(self.browser.title,
                         'Log in | Django site admin')

        self.staff_login()

        post_links = self.browser. \
            find_elements_by_link_text('Posts')
        self.assertEqual(
            post_links[0].get_attribute('href'),
            self.live_server_url + '/admin/posts/post/')

        post_links[0].click()
        #add_post_link = self.browser.find_elements_by_link_text('Add post')
        add_post_link = self.browser.find_elements_by_xpath('//*[@id="content-main"]/ul/li/a')
        add_post_link[0].click()
        #pdb.set_trace()

        post_form = self.browser.find_element_by_xpath('//*[@id="post_form"]')
        post_form.find_element_by_name('title').send_keys('this is my first post')
        post_form.find_element_by_name('content').send_keys('this is the content of my first post')

        post_form.find_element_by_css_selector(
            '.submit-row input').click()

        #pdb.set_trace()

        post_rows = self.browser.find_elements_by_xpath('//*[@id="result_list"]/tbody/tr[1]/th/a')

        #logger.error('')
        #logger.error(post_rows[0].text)

        self.assertEqual(post_rows[0].text.strip(),'this is my first post')
