from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdmin
from .serializers_users import UsersSerializer, UserProfileSerializer


User = get_user_model()


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = UserProfileSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UsersView(ModelViewSet):
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    http_method_names = (
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    )
    lookup_field = 'username'
    filter_backends = SearchFilter,
    search_fields = 'role', 'username'
    permission_classes = IsAdmin,
    pagination_class = PageNumberPagination
