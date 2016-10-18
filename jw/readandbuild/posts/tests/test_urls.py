from django.test import TestCase
from django.core.urlresolvers import resolve
from posts.views import post_list

class PostsURLsTestCase(TestCase):
   def test_root_url_uses_detail_view(self):
       """
       Test that the root of the site resolves to the
       correct view function
       """
       root = resolve('/')
       self.assertEqual(root.func, post_list)