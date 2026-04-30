from django.contrib.auth import get_user, get_user_model
from django.test import TestCase
from django.urls import reverse

CustomUser = get_user_model()


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
        user = CustomUser.objects.get(username='testuser')
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
        self.assertEqual(CustomUser.objects.count(), 0)
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
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertFormError(response.context['form'], 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        CustomUser.objects.create_user(
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
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertFormError(response.context['form'], 'username', 'A user with that username already exists.')


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username="Naruto", first_name="Uzumaki")
        self.db_user.set_password("somepass")
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "Naruto",
                "password": "somepass"
            },
            follow=True
        )
        user = get_user((self.client))
        print(user.is_authenticated)
        self.assertTrue(user.is_authenticated)

    def test_wrong_password(self):
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

    def test_logout(self):
        self.client.login(username="Naruto", password="somepass")

        self.client.get(reverse("users:logout"))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=" + reverse("users:profile"))

    def test_profile_details(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            first_name='testname',
            last_name='testlastname',
            email='testemail@gmail.com',
            password='testpassword'
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)
