from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
import random

from .models import User
from .serializers import UserSerializer, RegisterSerializer, ProfileUpdateSerializer


def _normalize_email(email_str: str) -> str:
    """Standardize email formatting."""
    return (email_str or "").strip().lower()


def _normalize_username(username_str: str) -> str:
    """Standardize username formatting."""
    return (username_str or "").strip()


import threading

def _send_otp_email(subject: str, message: str, recipient_email: str):
    """
    Attempts to send an OTP email.
    In DEBUG mode, it sends synchronously to catch errors immediately.
    In production/non-DEBUG, it uses a thread to avoid blocking.
    """
    def send():
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=False,
            )
            return True, None
        except Exception as e:
            print(f"EMAIL ERROR: {str(e)}")
            return False, str(e)

    if settings.DEBUG:
        # Synchronous in debug for immediate feedback
        return send()
    else:
        # Background thread in production
        thread = threading.Thread(target=send)
        thread.start()
        return True, None  # Assume success for UX, or use a proper task queue (Celery)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    payload = request.data.copy()
    payload["email"] = _normalize_email(payload.get("email"))
    payload["username"] = _normalize_username(payload.get("username"))

    serializer = RegisterSerializer(data=payload)

    if serializer.is_valid():
        user = serializer.save()

        # Generate 6-digit OTP
        otp_code = str(random.randint(100000, 999999))
        user.otp = otp_code
        user.otp_expiry = timezone.now() + timezone.timedelta(minutes=10)
        user.save()

        # Dispatch OTP email
        sent, error_msg = _send_otp_email(
            "HireHelper OTP Verification",
            f"Your OTP code is: {otp_code}",
            user.email,
        )

        if sent:
            return Response({"message": "User registered. OTP sent to email."})

        # Fallback for debug mode or email failure
        if settings.DEBUG:
            return Response(
                {
                    "message": "User registered, but email failed. Use the OTP below to verify.",
                    "otp": otp_code,
                    "email_error": error_msg,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": "User registered, but OTP email failed. Please try to resend OTP later."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    email = _normalize_email(request.data.get("email"))
    otp_code = (request.data.get("otp") or "").strip()

    try:
        user = User.objects.get(email__iexact=email)

        if user.otp == otp_code and (not user.otp_expiry or user.otp_expiry > timezone.now()):
            user.is_verified = True
            user.save()
            return Response({"message": "OTP verified successfully"})

        return Response({"error": "Invalid or expired OTP"}, status=400)

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@api_view(['POST'])
@permission_classes([AllowAny])
def resend_otp(request):
    email = _normalize_email(request.data.get("email"))

    if not email:
        return Response({"error": "Email is required"}, status=400)

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    if user.is_verified:
        return Response({"error": "Account is already verified"}, status=400)

    # Generate new OTP
    otp_code = str(random.randint(100000, 999999))
    user.otp = otp_code
    user.otp_expiry = timezone.now() + timezone.timedelta(minutes=10)
    user.save()

    sent, error_msg = _send_otp_email(
        "HireHelper OTP Verification",
        f"Your new OTP code is: {otp_code}",
        user.email,
    )

    if sent:
        return Response({"message": "OTP resent successfully"})

    if settings.DEBUG:
        return Response(
            {
                "message": "Email delivery failed. Use the OTP below.",
                "otp": otp_code,
                "email_error": error_msg,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response({"error": "Failed to send OTP email"}, status= status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = _normalize_email(request.data.get("email"))
    password = (request.data.get("password") or "")

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=400)

    # Simplified login: find user by email or username
    user = User.objects.filter(email__iexact=email).first()
    if not user:
        user = User.objects.filter(username__iexact=email).first()

    if not user or not user.check_password(password):
        return Response({"error": "Invalid credentials"}, status=400)

    if not user.is_verified:
        return Response({"error": "Account not verified"}, status=403)

    refresh = RefreshToken.for_user(user)
    
    # Securely build profile picture URL
    profile_pic = ""
    if user.profile_picture:
        url = user.profile_picture.url
        if url.startswith("http"):
            profile_pic = url
        else:
            profile_pic = request.build_absolute_uri(url)

    return Response({
        'token': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'username': user.username,
            'name': user.first_name or user.username,
            'email': user.email,
            'role': user.role,
            'city': user.city,
            'profile_picture': profile_pic,
            'is_verified': user.is_verified
        }
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = _normalize_email(request.data.get("email"))

    if not email:
        return Response({"error": "Email is required"}, status=400)

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        # Prevent user enumeration
        return Response({"message": "If this email is registered, an OTP has been sent."})

    otp_code = str(random.randint(100000, 999999))
    user.otp = otp_code
    user.otp_expiry = timezone.now() + timezone.timedelta(minutes=10)
    user.save(update_fields=["otp", "otp_expiry"])

    sent, error_msg = _send_otp_email(
        "HireHelper Password Reset OTP",
        f"Your password reset OTP is: {otp_code}",
        user.email,
    )

    if sent:
        return Response({"message": "Password reset OTP sent"})

    if settings.DEBUG:
        return Response(
            {
                "message": "Email delivery failed. Use the OTP below.",
                "otp": otp_code,
                "email_error": error_msg,
            }
        )

    return Response({"message": "If this email is registered, an OTP has been sent."})


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    email = _normalize_email(request.data.get("email"))
    otp_code = (request.data.get("otp") or "").strip()
    new_password = request.data.get("new_password")

    if not email or not otp_code or not new_password:
        return Response({"error": "All fields are required"}, status=400)

    try:
        user = User.objects.get(email__iexact=email, otp=otp_code)
        
        if not user.otp_expiry or user.otp_expiry < timezone.now():
            return Response({"error": "OTP has expired"}, status=400)

        user.set_password(new_password)
        user.otp = ""
        user.otp_expiry = None
        user.save(update_fields=["password", "otp", "otp_expiry"])

        return Response({"message": "Password reset successful"})

    except User.DoesNotExist:
        return Response({"error": "Invalid email or OTP"}, status=400)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method in ['PUT', 'PATCH']:
        serializer = ProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=request.method == 'PATCH'
        )

        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(request.user, context={"request": request}).data)

        return Response(serializer.errors, status=400)

    serializer = UserSerializer(request.user, context={"request": request})
    return Response(serializer.data)