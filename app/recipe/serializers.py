"""
serializers for recipe api
"""
from rest_framework import serializers
from core.models import (
    Recipe,
    Tag,
    Ingredient
)

import os
import uuid
from django.core.files.storage import default_storage
from django.conf import settings

class TagSerializer(serializers.ModelSerializer):
    """serializer for Tag model"""

    class Meta:
        model= Tag
        fields=['id','name']
        read_only_fileds= ['id']

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.partial:
                for field in self.fields.values():
                    field.required = False



class IngredientSerializer(serializers.ModelSerializer):
    """serializer for Ingeredients"""
    class Meta:
        model= Ingredient
        fields=['id','name']
        read_only_fields= ['id']



class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""

    tags= TagSerializer(many=True, required=False)
    ingredients= IngredientSerializer(many=True,required=False)

    class Meta:
        model= Recipe
        fields= ['id','title','time_minutes','price','link','tags','ingredients','image1',]
        read_only_fields= ['id']



    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.partial:
                for field in self.fields.values():
                    field.required = False




    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags"""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, _ = Tag.objects.get_or_create(user=auth_user, **tag)
            recipe.tags.add(tag_obj)


    def _get_or_create_ingredients(self, ingredients, recipe):
        """Handle getting or creating ingredients"""
        if not ingredients:
            return
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, _=Ingredient.objects.get_or_create(user=auth_user, **ingredient)
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        """Create a recipe with associated tags"""
        tags = validated_data.pop('tags', [])
        ingredients=validated_data.pop('ingredient',[])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags,recipe)
        self._get_or_create_ingredients(ingredients,recipe)
        return recipe

    def update(self, instance, validated_data):
        """Update a recipe and manage tags"""
        tags = validated_data.pop('tags', None)
        ingredients=validated_data.pop('ingredients',None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        if Ingredient is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients,instance)

        # Use Django's update method for efficiency
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance





class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields=RecipeSerializer.Meta.fields+ ['description']

