"""
serializers for recipe api
"""
from rest_framework import serializers
from core.models import (
    Recipe,
    Tag
)

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

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""

    tags= TagSerializer(many=True, required=False)

    class Meta:
        model= Recipe
        fields= ['id','title','time_minutes','price','link','tags']
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

    def create(self, validated_data):
        """Create a recipe with associated tags"""
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Update a recipe and manage tags"""
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        # Use Django's update method for efficiency
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance





class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields=RecipeSerializer.Meta.fields+ ['description']



