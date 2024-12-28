from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.forms import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .constants import MESSAGE, SUBJECT
from .serializers import (
    UserSignupSerializer, UserConfirmationSerializer
)


User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_or_update(request):
    serializer = UserSignupSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    # Генерируем код подтверждения и создаем для него токен
    confirmation_code = default_token_generator.make_token(data['user'])

    # Отправляем код подтверждения по электронной почте
    send_mail(
        subject=SUBJECT,
        message=MESSAGE.format(confirmation_code),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[data['email']]
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def confirmation(request):
    serializer = UserConfirmationSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    return Response(
        {'token': str(AccessToken.for_user(
            serializer.validated_data['user']
        ))}, status=status.HTTP_200_OK
    )
