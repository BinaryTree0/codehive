from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import CustomUser, UserActivationToken, UserResetToken
from .permissions import IsCreationOrIsAuthenticated
from .serilaziers import (ChangePasswordSerializer, EmailSerializer,
                          PasswordResetSerializer, TokenSerializer,
                          UserSerializer)
from .tokens import account_activation_token, password_reset_token
from .utils import send_activation_mail, send_reset_mail


class UserViewSet(ModelViewSet):
    """
    This endpoint contains all basic functionalities regarding the user model.
    """
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsCreationOrIsAuthenticated, ]


class ActivateView(CreateAPIView):
    """
    This endpoint is used to request a new user activation email.
    """
    serializer_class = EmailSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(email=serializer.data["email"])
            send_activation_mail(user)

        return Response(status=status.HTTP_202_ACCEPTED)


class ActivateConfirmView(CreateAPIView):
    """
    This endpoint is used to activate the users account.
    """
    serializer_class = TokenSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = activation_token = serializer.data["token"]
            user = UserActivationToken.objects.get(activation_token=token).user

            if user is not None and account_activation_token.check_token(user, token):
                if not user.is_confirmed:
                    user.is_confirmed = True
                    user.save()
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ResetView(CreateAPIView):
    """
    This endpoint is used to request a password reset.
    """
    serializer_class = EmailSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(email=serializer.data["email"])

            send_reset_mail(user)

        return Response(status=status.HTTP_202_ACCEPTED)


class ResetConfirmView(CreateAPIView):
    """
    This endpoint is used to reset the users password.
    """
    serializer_class = PasswordResetSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = serializer.data["token"]
            try:
                user = UserResetToken.objects.get(reset_token=token).user
            except:
                user = None

            if user is not None and password_reset_token.check_token(user, token):
                user.set_password(serializer.data["password"])
                user.save()
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    """
    This endpoint is used to change the user password.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def put(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=kwargs["uid"])
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            # Check old password
            old_password = serializer.data["old_password"]
            if not user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data["new_password"])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
