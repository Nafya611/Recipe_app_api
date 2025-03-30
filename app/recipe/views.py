from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from recipe.serializers import RecipeSerializer
from core.models import Recipe

@extend_schema(
    methods=['POST'],
    request=RecipeSerializer,  # Explicitly define request body
    responses={201: RecipeSerializer}  # Define response schema
)
@extend_schema(
    methods=['GET'],
    responses={200: RecipeSerializer(many=True)}  # Define response for GET
)
@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def recipe_list(request):
    """
    Handle listing all recipes for the authenticated user or creating a new one.
    """
    if request.method == 'GET':
        recipes = Recipe.objects.filter(user=request.user).order_by('id')
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
