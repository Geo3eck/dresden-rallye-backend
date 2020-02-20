from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import permissions, generics, status

from .serializers import SignUpUserSerializer

class SignUpAPI(generics.GenericAPIView):
    serializer_class = SignUpUserSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)