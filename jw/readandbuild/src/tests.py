from django.test import LiveServerTestCase
from selenium import webdriver
from django.contrib.auth import get_user_model

import logging
import pdb

from datetime import date

logger = logging.getLogger(__name__)

class PostTestCase(LiveServerTestCase):

    """
        Testing posts:
            - A home page with blog listing and pagination
                - test url for homepage
                - I can see more than one blog entry on the home page
            - Staff can create add post content
            - A post can have an image associated with it
            - The create blog post page is behind auth
            - A functional test for creating with publish date
            - A functional test for post_detail with slug (model test)
            - A functional test for draft state
            - content and title search
            - Pagination
    """
    admin_username = 'admin'
    admin_email = 'dev@howapped.com'
    admin_password = 'password'

    post1 = dict(title='First Post', content='This is the content for my first post')
    post2 = dict(title='Second Post', content='This is more post fun in my follow-up!')


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
        admin_root = self.browser.get(
            self.live_server_url + '/admin/')
        login_form = self.browser.find_element_by_id(
            'login-form')
        login_form.find_element_by_name('username'). \
            send_keys(self.admin_username)
        login_form.find_element_by_name('password'). \
            send_keys(self.admin_password)
        login_form.find_element_by_css_selector(
            '.submit-row input').click()

    def test_i_see_welcome_on_home_page(self):
        """
        test url for homepage
        :return:
        """

        home_page = self.browser.get(self.live_server_url + '/')

        header = self.browser.find_element_by_css_selector('h1')
        self.assertEqual('Welcome', header.text,
                         'I could not see Welcome on the homepage')

    def test_staff_user_can_login(self):

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

        self.staff_create_post(self.post1)


        # pdb.set_trace()
        #logger.error('')

    def staff_create_post(self, post):
        # go to posts create page
        self.browser.get(
            self.live_server_url + '/admin/posts/post/add')
        self.staff_submit_create_form(post)

    def staff_submit_create_form(self, post):

        today = date.today()

        post_form = self.browser.find_element_by_xpath('//*[@id="post_form"]')
        post_form.find_element_by_name('title').send_keys(post['title'])
        post_form.find_element_by_name('content').send_keys(post['content'])

        post_form.find_element_by_name('publish').send_keys(str(today))

        post_form.find_element_by_css_selector(
            '.submit-row input').click()


    def test_i_can_see_a_list_of_post_entries_on_the_home_page_in_desc_order(self):

        self.staff_login()
        self.staff_create_post(self.post1)
        self.staff_create_post(self.post2)

        home_page = self.browser.get(self.live_server_url + '/')

        # get posts to see if they are listed descending order
        post_title_links = self.browser.find_elements_by_css_selector('div.title a')

        self.assertEqual(post_title_links[0].text,self.post2['title'])

        self.assertEqual(post_title_links[1].text.strip(),self.post1['title'])