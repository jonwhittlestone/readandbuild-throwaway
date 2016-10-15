from django.test import TestCase, RequestFactory
from posts.views import post_list


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view_basic(self):
        """
        Test that index view returns a 200 response and uses
        the correct template
        """
        request = self.factory.get('/')
        with self.assertTemplateUsed('posts/list.html'):
            response = post_list(request)
            self.assertEqual(response.status_code, 200)

