from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer
from core.models import Recipe
from django.shortcuts import get_object_or_404

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

@extend_schema(
    methods=['PUT'],
    description="Update an existing recipe by providing all required fields.",
    request=RecipeDetailSerializer,
    responses={
        200: RecipeDetailSerializer,
        400: OpenApiResponse(description="Bad request")
    },
)
@api_view(['PUT','GET','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def recipe_detail(request,pk):
    """handle detail of recipe in id"""
    try:
        recipe = Recipe.objects.get(pk=pk, user=request.user)
    except Recipe.DoesNotExist:
        return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer =  RecipeDetailSerializer(recipe)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer =RecipeDetailSerializer(recipe,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        recipe.delete()
        return Response({"message":"Recipe deleted successfully."},status=status.HTTP_204_NO_CONTENT)
