from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import CustomUser

from django.core.cache import caches
from rest_captcha.settings import api_settings
from rest_captcha import utils

class CaptchaTests(APITestCase):
    def test_get_captcha(self):
        url = reverse('rest_captcha')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SignUpTests(APITestCase):
    def test_signup_correct_captcha(self):
        url = reverse('user-signup')
        data = {
            'email': 'example@example.com',
            'password': 'test123pass#@!',
            'captcha_key': 'fe5a64f9-e0c5-4c67-9c1f-ee0a84c88af8',
            'captcha_value': 'TEST0',
        }

        # create the key:value pair in cache for test captcha
        cache = caches[api_settings.CAPTCHA_CACHE]

        cache_key = utils.get_cache_key(data['captcha_key'])
        cache.set(cache_key, data['captcha_value'], api_settings.CAPTCHA_TIMEOUT)

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_wrong_captcha(self):
        url = reverse('user-signup')
        data = {
            'email': 'example@example.com',
            'password': 'test123pass#@!',
            'captcha_key': 'fe5a64f9-e0c5-4c67-9c1f-ee0a84c88af8',
            'captcha_value': 'wrongValue',
        }

        # create the key:value pair in cache for test captcha
        cache = caches[api_settings.CAPTCHA_CACHE]
        cache.set(data['captcha_key'], data['captcha_value'], api_settings.CAPTCHA_TIMEOUT)

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class SignInTests(APITestCase):
    def test_sign_in_correct(self):
        url = reverse('user-signin')
        data = {
            'email': 'example@example.com',
            'password': 'test123pass#@!'
        }

        CustomUser.objects.create_user(
            'example@example.com',
            'test123pass#@!',
        )

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_sign_in_wrong_email(self):
        url = reverse('user-signin')
        data = {
            'email': 'ex@example.com',
            'password': 'test123pass#@!'
        }

        CustomUser.objects.create_user(
            'example@example.com',
            'test123pass#@!',
        )
        
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_in_wrong_password(self):
        url = reverse('user-signin')
        data = {
            'email': 'example@example.com',
            'password': 'test123#@!'
        }
        
        CustomUser.objects.create_user(
            'example@example.com',
            'test123pass#@!',
        )

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
