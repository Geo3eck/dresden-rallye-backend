from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate

from django.core.cache import caches
from rest_captcha.settings import api_settings
from rest_captcha import utils


class SignUpUserSerializer(serializers.Serializer):
    captcha_key = serializers.CharField(max_length=64)
    captcha_value = serializers.CharField(max_length=8, trim_whitespace=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
        
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        captcha_key = data.get('captcha_key')
        captcha_value = data.get('captcha_value')

        cache = caches[api_settings.CAPTCHA_CACHE]
        cache_key = utils.get_cache_key(captcha_key)

        if captcha_key in api_settings.MASTER_CAPTCHA:
            real_value = api_settings.MASTER_CAPTCHA[captcha_key]
        else:
            real_value = cache.get(cache_key)

        if real_value is None:
            raise serializers.ValidationError('Invalid or expired captcha key')

        cache.delete(cache_key)
        if captcha_value.upper() != real_value:
            raise serializers.ValidationError('Invalid captcha value')

        email_query = CustomUser.objects.filter(email=email)
        if email_query.exists():
            raise serializers.ValidationError('Account with this email already exists.')

        return data

    def create(self, validated_data):
        CustomUser.objects.create_user(
            validated_data['email'],
            validated_data['password'],
        )

        return validated_data
