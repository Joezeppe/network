from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView

from users.models import MyUser
from users.serializers import UserRegisterSerializer


# registration API class to register a user

class RegisterUserView(generics.CreateAPIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number", "")
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        if not phone_number and not password and not email:
            return Response(
                data={
                    "message": "phone number, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = MyUser.objects.create_user(
            phone_number=phone_number, password=password, email=email
        )
        return Response(
            data={
                "message": "A new user has been created"
            },
            status=status.HTTP_201_CREATED
        )


class UserDetail(APIView):
    permission_classes = [IsAdminUser, ]

    def get_object(self, pk):
        try:
            return MyUser.objects.get(pk=pk)
        except MyUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        user = self.get_object(pk)
        serializer = UserRegisterSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserRegisterSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


