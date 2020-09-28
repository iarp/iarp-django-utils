from django.contrib.auth import get_user_model
from django.test import TestCase


class BaseTestClassMethods(TestCase):

    def setUp(self):
        self.created_documents = []
        self.user = self.setup_test_user()
        super(BaseTestClassMethods, self).setUp()

    def tearDown(self):
        for doc in self.created_documents:
            doc.delete()
        super(BaseTestClassMethods, self).tearDown()

    def setup_test_user(self, username='test', password='12345',
                        first_name='John', last_name='Doe',
                        email='john.doe@example.com'):
        return get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
