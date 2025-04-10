from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,parser_classes
)
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response
from rest_framework import status,serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse,OpenApiParameter
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer,TagSerializer,IngredientSerializer
from core.models import Recipe,Tag,Ingredient
from django.shortcuts import get_object_or_404


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='tags',
            type={'type': 'array', 'items': {'type': 'string'}},
            location=OpenApiParameter.QUERY,
            description='Comma-separated list of tag names (e.g., ?tags=vegan,quick)',
            explode=False,
            required=False,
        ),
        OpenApiParameter(
            name='ingredients',
            type={'type': 'array', 'items': {'type': 'string'}},
            location=OpenApiParameter.QUERY,
            description='Comma-separated list of ingredient names (e.g., ?ingredients=onion,tomato)',
            explode=False,
            required=False,
        ),
    ]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def filter_recipes(request):
    """
    Filter recipes by a list of tags and/or ingredients.
    Example:
    /api/recipes/filter/?tags=vegan,quick&ingredients=tomato,onion
    """
    tags_param = request.GET.get('tags')
    ingredients_param = request.GET.get('ingredients')
    recipes = Recipe.objects.filter(user=request.user)

    if tags_param:
        tag_names = tags_param.split(',')
        tags = Tag.objects.filter(name__in=tag_names)
        recipes = recipes.filter(tags__in=tags)

    if ingredients_param:
        ingredient_names = ingredients_param.split(',')
        ingredients = Ingredient.objects.filter(name__in=ingredient_names)
        recipes = recipes.filter(ingredients__in=ingredients)

    recipes = recipes.distinct()
    serializer = RecipeDetailSerializer(recipes, many=True)
    return Response(serializer.data)

@extend_schema(
    methods=['POST'],
    request=RecipeSerializer,
    responses={201: RecipeSerializer}
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_recipe(request):
    """
    Handle listing all recipes for the authenticated user or creating a new one.
    """


    if request.method == 'POST':
        serializer = RecipeSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    methods=['PATCH'],
    request=RecipeDetailSerializer,
    responses={
        200: RecipeDetailSerializer,
        400: OpenApiResponse(description="Bad request")
    },
)
@api_view(['PATCH'])
@parser_classes([MultiPartParser, FormParser])
def upload_recipe_photos_view(request, recipe_id):
    """
    Endpoint for uploading photos to specific image fields in the Recipe model.
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    serializer = RecipeSerializer(recipe, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
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
        serializer =RecipeDetailSerializer(recipe,data=request.data,context= {'request':request })
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
@extend_schema(
    methods=['PATCH'],
    request=TagSerializer,
    responses={
            200:TagSerializer,
            400:OpenApiResponse({'message':'bad request'})
        }



)
@api_view(['GET','PUT','PATCH','DELETE'])
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
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer= TagSerializer(tag,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tag.delete()
        return Response({"message": "Tag deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

@extend_schema(
        methods=['POST'],
        request=IngredientSerializer,
        responses=IngredientSerializer
)
@api_view(['POST','GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ingredient_list(request):
    """"""

    if request.method == 'GET':
        ingredient=Ingredient.objects.filter(user=request.user).order_by('name')
        serializer=IngredientSerializer(ingredient,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer= IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
        methods=['PUT','PATCH'],
        request=IngredientSerializer,
        responses=IngredientSerializer
)
@api_view(['GET','PUT','PATCH','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ingredient_detail(request,name):
    try:
        ingredient= Ingredient.objects.get(user=request.user,name=name)
    except Ingredient.DoesNotExist:
        Response({'error':'ingredient is not found'},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer= IngredientSerializer(ingredient)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer= IngredientSerializer(ingredient,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer= IngredientSerializer(ingredient,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ingredient.delete()
        return Response({'message':'ingredient deleted succesfully'},status=status.HTTP_204_NO_CONTENT)

