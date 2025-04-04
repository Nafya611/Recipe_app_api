"""views for user API - function-based version"""

from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
        methods=['POST'],
        request=UserSerializer,
        responses=UserSerializer
)
@api_view(['POST'])
def create_user(request):
    """Create a new user in the system"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
        methods=['POST'],
        request=AuthTokenSerializer,
        responses=AuthTokenSerializer
)
@api_view(['POST'])
@renderer_classes(api_settings.DEFAULT_RENDERER_CLASSES)
def create_token(request):
    """Create a new auth token for the user"""
    serializer = AuthTokenSerializer(data=request.data,
                                     context={'request': request})
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
        methods=['PUT'],
        request=UserSerializer,
        responses=UserSerializer
)
@api_view(['GET', 'PUT'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def manage_user(request):
    """Retrieve or update the authenticated user"""
    user = request.user

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
