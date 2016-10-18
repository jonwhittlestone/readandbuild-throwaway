from django.test import TestCase, RequestFactory
from posts.views import post_list, post_create


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

class CreateViewTestCase(TestCase):
        """
        Test the create view returns a 200, uses the correct template
        and has context
        """

        def setUp(self):
            self.factory = RequestFactory()

        def test_create_view(self):
            request = self.factory.get('posts/create')

            with self.assertTemplateUsed('posts/create.html'):
                response = post_create(request)
                self.assertEqual(response.status_code,200)