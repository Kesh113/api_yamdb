from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .constants import INVALID_CONFIRM_CODE, MESSAGE, SUBJECT, USER_NOT_FOUND
from .serializers_users import (
    UserConfirmationSerializer, UserCreateSerializer, UserUpdateSerializer
)


User = get_user_model()


@api_view(['POST'])
def signup_or_update(request):
    # Сериализуем и валидируем полученные данные
    # без проверки уникальности полей
    serializer = UserUpdateSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Генерируем код подтверждения
    confirmation_code = get_random_string(length=30)

    # Ищем пользователя в БД
    try:
        user = User.objects.get(**data)
        # Если пользователь найден, обновляем код подтверждения
        user.confirmation_code = confirmation_code
        user.is_active = False
        user.save()
    except User.DoesNotExist:
        # Если пользователь не найден, помещаем данные в сериализатор
        # и проверяем на соответствие полям модели
        serializer = UserCreateSerializer(data=data)

        if serializer.is_valid():
            serializer.save(
                confirmation_code=confirmation_code, is_active=False
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    # Отправляем код подтверждения по электронной почте
    send_mail(
        subject=SUBJECT,
        message=MESSAGE.format(confirmation_code),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[data['email']]
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
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
        if user.confirmation_code != data['confirmation_code']:
            return Response(
                {'confirmation_code': INVALID_CONFIRM_CODE},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Меняем статус на активный (почта подтверждена)
        user.is_active = True
        user.save()

        access_token = AccessToken.for_user(user)

        return Response(
            {'token': str(access_token)}, status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
