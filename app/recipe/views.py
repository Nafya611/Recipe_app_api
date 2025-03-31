from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer,TagSerializer
from core.models import Recipe,Tag
from django.shortcuts import get_object_or_404

@extend_schema(
    methods=['POST'],
    request=RecipeSerializer,
    responses={201: RecipeSerializer}
)
@extend_schema(
    methods=['GET'],
    responses={200: RecipeSerializer(many=True)}

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



@extend_schema(
    methods=['POST'],
    request=TagSerializer,
    responses={
        200: TagSerializer,
        400: OpenApiResponse(
            response={"message": "bad request"},
            description="Invalid request data"
        ),
    },
)
@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tag_list(request):

    if request.method == 'GET':
        tag= Tag.objects.filter(user=request.user).order_by('name')
        serializer= TagSerializer(tag, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer= TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
        methods=['PUT'],
        request=TagSerializer,
        responses={
            200:TagSerializer,
            400:OpenApiResponse({'message':'bad request'})
        }
)
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])

def tag_detail(request,name):
    try:
        tag = Tag.objects.get(name=name, user=request.user)
    except Tag.DoesNotExist:
        return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = TagSerializer(tag, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tag.delete()
        return Response({"message": "Tag deleted successfully."}, status=status.HTTP_204_NO_CONTENT)







