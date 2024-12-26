from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .constants import INVALID_CONFIRM_CODE, MESSAGE, SUBJECT, USER_NOT_FOUND
from .serializers_users import (
    UserCreateSerializer, UserSignupSerializer, UserConfirmationSerializer
)


User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_or_update(request):
    # Сериализуем и валидируем полученные данные
    # без проверки уникальности полей
    serializer = UserSignupSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    # Ищем пользователя в БД
    try:
        user = User.objects.get(**data)
    except User.DoesNotExist:
        # Если пользователь не найден, помещаем данные в сериализатор
        # и проверяем на соответствие полям модели
        serializer = UserCreateSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        user = serializer.save()

    # Генерируем код подтверждения и создаем для него токен
    confirmation_code = default_token_generator.make_token(user)

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
    if serializer.is_valid():
        data = serializer.validated_data
        try:
            user = User.objects.get(
                username=data['username']
            )
        except User.DoesNotExist:
            return Response(
                {'username': USER_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )

        if not default_token_generator.check_token(
            user, request.data['confirmation_code']
        ):
            return Response(
                {'confirmation_code': INVALID_CONFIRM_CODE},
                status=status.HTTP_400_BAD_REQUEST
            )

        token = AccessToken.for_user(user)

        return Response(
            {'token': str(token)}, status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
