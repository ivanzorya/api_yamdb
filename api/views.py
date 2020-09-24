from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import User
from api.permissions import IsAdmin, IsOwner
from api.serializers import UserSerializer, \
    TokenObtainPairWithoutPasswordSerializer, UserAllSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAllSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_field = 'username'


class APIUserDetail(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request):
        serializer = UserAllSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserAllSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(User, email=request.data.get('email'))
        subject = 'Thank you for registering to YaMDB'
        message = f'Your confirmation code is {user.confirmation_key}.' \
                  f' Use code for token taking.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [f'{user.email}', ]
        send_mail(subject, message, email_from, recipient_list)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairWithoutPasswordSerializer

