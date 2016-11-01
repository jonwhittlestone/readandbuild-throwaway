from django.test import LiveServerTestCase
from selenium import webdriver
from django.contrib.auth import get_user_model
from django.conf import settings
from posts.models import Post

import logging
import pdb

from datetime import date

logger = logging.getLogger(__name__)


class BaseTestCase(LiveServerTestCase):
    """
        Testing posts:
            - A home page with blog listing and pagination
                - test url for homepage
                - I can see more than one blog entry on the home page
            - Staff can create add post content
            - A post can have an image associated with it
            - A functional test for post_detail with slug (model test)
            - A functional test for edit button so an auth user to edit post
            - A functional test for draft state
    """

    # pdb.set_trace()
    # logger.error('')

    admin_username = 'admin'
    admin_email = 'dev@howapped.com'
    admin_password = 'password'

    post1 = dict(title='First Post', content='This is the content for my first post')
    post2 = dict(title='Second Post', content='This is more post fun in my follow-up!')

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(2)
        self.admin_user = get_user_model().objects.create_superuser(
            username=self.admin_username,
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

    def staff_create_post(self, post):
        # go to posts create page
        self.browser.get(
            self.live_server_url + '/admin/posts/post/add')
        self.staff_submit_create_form(post)

    def staff_submit_create_form(self, post):
        file_to_upload = settings.STATIC_ROOT + '/w1408.jpeg'

        today = date.today()

        post_form = self.browser.find_element_by_xpath('//*[@id="post_form"]')
        post_form.find_element_by_name('title').send_keys(post['title'])
        post_form.find_element_by_name('content').send_keys(post['content'])

        post_form.find_element_by_name('publish').send_keys(str(today))

        # logger.error(os.path.isfile(file_to_upload))

        post_form.find_element_by_id('id_image').send_keys(file_to_upload)
        post_form.find_element_by_css_selector(
            '.submit-row input').click()

    def user_view_post_detail(self, post):

        slug = self.get_recent_post_slug()

        self.browser.get(self.live_server_url + '/posts/' + slug)
        #pdb.set_trace()
        # can i see heading
        heading = self.browser.find_element_by_css_selector('h1')
        self.assertEqual(post['title'], heading.text,
                         'I could not see the post title on the detail page')
        # can i see the content
        content = self.browser.find_element_by_css_selector('div.content')
        self.assertEqual(post['content'], content.text,
                         'I could not see the post content on the detail page')
        # can i see the image?
        image_tag = self.browser.find_element_by_css_selector('img.img-responsive')
        logger.error(image_tag.get_attribute('src'))
        #self.assertEqual(post['content'], content.text,
                         #'I could not see the post content on the detail page')
        self.assertIn('/media/w1408', image_tag.get_attribute('src'),
                      'I could not see w1408 in the image src attribute')


    def get_recent_post_slug(self):
        """
        gets most recent post slug
        :return:
        """
        return 'first-post'
        return Post.objects.order_by('-id')[0]


class UserTestCase(BaseTestCase):

    def test_i_see_welcome_on_home_page(self):
        """
        test url for homepage
        :return:
        """

        home_page = self.browser.get(self.live_server_url + '/')

        header = self.browser.find_element_by_css_selector('h1')
        self.assertEqual('Welcome', header.text,
                         'I could not see Welcome on the homepage')

    def test_user_can_see_list_of_post_entries_on_the_home_page_in_desc_order(self):
        self.staff_login()
        self.staff_create_post(self.post1)
        self.staff_create_post(self.post2)

        home_page = self.browser.get(self.live_server_url + '/')

        # get posts to see if they are listed descending order
        post_title_links = self.browser.find_elements_by_css_selector('div.title a')

        self.assertEqual(post_title_links[0].text, self.post2['title'])

        self.assertEqual(post_title_links[1].text.strip(), self.post1['title'])


    # Todo. Test: Authenticated user to edit post
    def test_authenticated_user_can_see_click_edit_button_to_edit_post(self):
        pass

    # Todo. Unauthenticted user cannot edit post
    def test_unauthenticated_user_cannot_edit_post(self):
        pass

    # Todo. Unauthenticated user cannot see post in draft state
    def test_unauthenticated_user_cannot_view_post_in_draft_state(self):
        pass

class StaffTestCase(BaseTestCase):
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

    def test_staff_can_create_post_with_an_image(self):
        """
            Tests that a 'staff' user can access the admin and
                   add Posts
        """
        admin_root = self.browser.get(
            self.live_server_url + '/admin/')
        self.assertEqual(self.browser.title,
                         'Log in | Django site admin')

        self.staff_login()

        self.create_post_with_image(self.post1)
        # assert when post is visited i see the image

        self.user_view_post_detail(self.post1)

        # assert image has been moved to media_root in dynamic url by trying to visit it



        # home_page = self.browser.get(self.live_server_url + '/')
        # post_img_links = self.browser.find_elements_by_css_selector('div.post img.img-responsive')

        # src = post_img_links[0].get_attribute("src")
        # logger.error(src)
        # self.assertEqual(post_img_links[0].text, self.post2['title'])

    def create_post_with_image(self, post):
        # go to posts create page
        self.browser.get(
            self.live_server_url + '/admin/posts/post/add')

        self.staff_submit_create_form(post)

