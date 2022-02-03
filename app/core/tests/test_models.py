from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_seccessful(self):
        """
        Test creating a new user with an email is seccessful
        """
        email = 'test@londonappdev.com'
        password = 'Testpass123'
        user = get_user_model().object.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized
        """
        email = 'test@LONDONAPPDEV.com'
        user = get_user_model().object.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        Testing creating user with no emial raises error
        """
        with self.assertRaises(ValueError):
            get_user_model().object.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """
        Test creating a new superuser
        """
        user = get_user_model().object.create_superuser(
            'test@london.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
