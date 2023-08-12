from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from user.serializers import (
    RegisterSerializer,
    UserProfile,
    LoginSerializer,
    OnboardingSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    UserUpdate,
    VerifyEmailSerializer,
    SendEmailVerificationSerializer
)
from user.models import User
from goals.models import Friend
from rest_framework import permissions
from user.utils import Util
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
                        
    
class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
    http_method_names = [
        "post", "get", "put", "patch", "delete"
    ]
    lookup_field = "id"

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=RegisterSerializer,
        url_path="register",
    )
    def create_user_account(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                referred_by = request.data.get('referred_by', None)
                is_verified = request.data.get('is_verified', False)
                serializer.save(email=serializer.validated_data['email'].lower())
                user = User.objects.get(email=serializer.validated_data['email'].lower())
                user.referral_link = Util.generate_referral_link()
                if is_verified:
                    user.is_verified = is_verified
                user.save()
                
                if referred_by is not None:
                    user.referred_by = referred_by
                    referral = User.objects.filter(referral_link=referred_by)
                    if referral.exists():
                        referral = referral.first()
                        new_friend = Friend.objects.create(user=referral, friend=user)
                    else:
                        pass
                return Response(
                    {
                        "Success": True,
                        "message": "Your account has been created successfully.",
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"success": False, "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as err:
            return Response(
                {"success": False, "message": str(err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
    @action(methods=['POST'], detail=False, serializer_class=SendEmailVerificationSerializer, url_path='send-otp')
    def send_registration_otp(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.filter(email=serializer.data['email']).first()
                if user:
                    otp = Util.generate_otp()
                    user.otp = otp
                    user.save()
                    # Util.send_registration_email(user.email, otp)
                    return Response({'success': True, 'message': f'OTP sent successfully {otp}'}, status=status.HTTP_200_OK)
                return Response({'success': False, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            except Exception as err:
                return Response({'success': False, 'message': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["GET"], detail=False, serializer_class=UserProfile, url_path="users"
    )
    def get_all_users(self, request):
        try:
            users = User.objects.all()
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response(
                {"success": False, "message": str(err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        methods=["GET"],
        detail=False,
        serializer_class=UserProfile,
        url_path="users/(?P<id>[^/.]+)",
    )
    def get_user(self, request, *args, **kwargs):
        try:
            user = User.objects.filter(id=kwargs["id"])
            if not user.exists():
                return Response(
                {"success": False, "message": "User not found."},
                status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(user.first())
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response(
                {"success": False, "message": str(err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        methods=["DELETE"],
        detail=False
    )
    def delete_user(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.GET.get('id'))
            user.delete()
            return Response(
                {"success": True, "message": "User deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as err:
            return Response(
                {"success": False, "message": str(err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
    @action(
        methods=["PATCH"],
        detail=False,
        serializer_class=UserUpdate
    )
    def update_user(self, request, *args, **kwargs):
        try:
            user = User.objects.filter(id= request.GET.get('id')).first()
            if user:
                serializer = self.get_serializer(
                    user, data=request.data, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(
                    {"success": False, "message": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"success": False, "message": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as err:
            return Response(
                {"success": False, "message": str(err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
    @action(
        methods=["PATCH"],
        detail=False,
        serializer_class=OnboardingSerializer
    )
    def onboard_user(self, request, *args, **kwargs):
        try:
            user = User.objects.filter(id=request.GET.get('id')).first()
            serializer = self.get_serializer(user, data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"success": False, "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as err:
            return Response(
                {"success": False, "message": str(err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AuthenticationViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
    http_method_names = [
        "post",
    ]

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=LoginSerializer,
        url_path="login",
    )
    def login_user(self, request):
        try:
            email = request.data["email"].lower()
            password = request.data["password"]
            fcm_token = request.data.get("device_token")
            if email is None or password is None:
                return Response(
                    data={
                        "invalid_credentials": "Please provide both email and password"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = authenticate(username=email, password=password)
            if not user:
                return Response(
                    data={"invalid_credentials": "Invalid credentials"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if user.is_verified is False:
                return Response(
                    data={"invalid_credentials": "Please verify your email address"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            token, _ = Token.objects.get_or_create(user=user)
            if fcm_token is not None:
                user.fcm_token = fcm_token
                user.save()
            return Response(
                data={"token": token.key, "message": "Login successful"},
                status=status.HTTP_200_OK,
            )
        except Exception as err:
            return Response(
                {"success": False, "message": str(err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
    @action(methods=["POST"], detail=False, serializer_class=VerifyEmailSerializer, url_path="verify-email")
    def verify_email(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]
            otp = serializer.validated_data["otp"]
            if not email or not otp:
                return Response({"message":"Please provide both email and otp"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.get(email=email)
                if user.otp == otp:
                    user.is_verified = True
                    user.save()
                    return Response({"message":"Email verified successfully"}, status=status.HTTP_200_OK)
                return Response({"message":"Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            
            except ObjectDoesNotExist:
                return Response({"message":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    
class ForgotPasswordViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = ForgotPasswordSerializer

    @action(
        methods=["POST"],
        detail=False,
        url_path="forgot-password",
    )
    def forgot_password(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
            
            except ObjectDoesNotExist:
                return Response({"message":"User does not exist"}, status=404)
            encoded_pk = urlsafe_base64_encode(force_bytes(user.id))
            
            if user.is_verified is True:
                token = PasswordResetTokenGenerator().make_token(user)

                reset_url = f"/api/forgot/reset-password/?encoded_pk={encoded_pk}&token={token}/"
                reset_password_link = f"localhost:8000{reset_url}"

                # Util.send_forgot_password_email(email, reset_password_link)

                return Response(
                    {
                        "success": True,
                        "message": f"Your reset password link: {reset_password_link}",
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"success": False, "message": "Please verify your email address"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(
            {"success": False, "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
    @action(
        methods=["PATCH"],
        detail=False,
        serializer_class=ResetPasswordSerializer,
        permission_classes=[permissions.AllowAny],
    )
    def reset_password(self, request):
        get_token = request.GET.get("token", None)
        get_encoded_pk = request.GET.get("encoded_pk", None)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if (
                serializer.validated_data["password"]
                != serializer.validated_data["confirm_password"]
            ):
                return Response(
                {"success": False, "message": "Passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            if get_token is None or get_encoded_pk is None:
                return Response(
                    {"success": False, "message": "Invalid token or user"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
 
            tk = urlsafe_base64_decode(get_encoded_pk).decode()
            print(tk)
            try:
                user = User.objects.get(id=tk)
            except ObjectDoesNotExist:
                return Response(
                    {"success": False, "message": "Invalid user"}, status=status.HTTP_404_NOT_FOUND)
            if not PasswordResetTokenGenerator().check_token(user, get_token):
                return Response(
                    {"success": False, "message": "Invalid token for password reset"})

            user.set_password(serializer.validated_data["password"])
            user.save()
            
            return Response(
                {"success": True, "message": "Password reset successful"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    
