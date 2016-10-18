from django.test import TestCase
from django.core.urlresolvers import resolve
from .posts import views


class PostsURLsTestCase(TestCase):
    def test_root_url_uses_list_view(self):
        """
        Test that the root of the site resolves to the
        correct view function
        """
        root = resolve('/')
        self.assertEqual(root.func, post_list)