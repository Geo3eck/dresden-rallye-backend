from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import CustomUserSerializer, SignUpUserSerializer, SignInUserSerializer

class SignUpAPI(generics.GenericAPIView):
    """
    Requires an mail address, a password and a valid captcha value.
    """

    serializer_class = SignUpUserSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)

class SignInAPI(generics.GenericAPIView):
    """
    Requires an email address and a valid password.
    Returns serialized user and a user token
    """

    serializer_class = SignInUserSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data

        try:
            token = Token.objects.get(user=user).key
        except ObjectDoesNotExist:
            token = Token.objects.create(user=user).key

        return Response(
            {
                'user': CustomUserSerializer(user, context=self.get_serializer_context()).data,
                'token': token,
            },
            status=status.HTTP_200_OK,
        )