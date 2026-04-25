from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'testuser',
                'first_name': 'testname',
                'last_name': 'testlastname',
                'email': 'testemail@gmail.com',
                'password': 'testpassword'
            }
        )

        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='testuser')
        self.assertEqual(user.first_name, 'testname')
        self.assertEqual(user.last_name, 'testlastname')
        self.assertEqual(user.email, 'testemail@gmail.com')
        self.assertTrue(user.check_password('testpassword'))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'first_name': 'testname',
                'email': 'testemail@gmail.com'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(response.context['form'], 'username', 'This field is required.')
        self.assertFormError(response.context['form'], 'password', 'This field is required.')

    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'testuser',
                'first_name': 'testname',
                'last_name': 'testlastname',
                'email': 'invalid-email',
                'password': 'testpassword'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(response.context['form'], 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        User.objects.create_user(
            username='testuser',
            first_name='testname',
            last_name='testlastname',
            email='testemail@gmail.com',
            password='testpassword'
        )
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'testuser',
                'first_name': 'testname2',
                'last_name': 'testlastname2',
                'email': 'testemail2@gmail.com',
                'password': 'testpassword2'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertFormError(response.context['form'], 'username', 'A user with that username already exists.')


class LoginTestCase(TestCase):
    def test_successful_login(self):
        db_user = User.objects.create_user(
            username='testuser',
            first_name='testname',
            last_name='testlastname',
            email='testemail@gmail.com',
            password='testpassword'
        )
        db_user.set_password("somepass")
        db_user.save()
        self.client.post(
            reverse("users:login"),
            data={
                "username": "testuser",
                "password": "somepass"
            }
        )
        user = get_user((self.client))
        self.assertTrue(user.is_authenticated)

    def test_wrong_password(self):
        db_user = User.objects.create_user(
            username='testuser',
            first_name='testname'
        )
        db_user.set_password('somepass')
        db_user.save()
        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong-username",
                "password": "somepass"
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.client.post(
            reverse("users:login"),
            data={
                "username": "username",
                "password": "wrong-somepass"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
