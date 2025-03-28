"""
serializers for recipe api
"""
from rest_framework import serializers
from core.models import Recipe

class RecipeSerialzer(serializers.ModelSerializer):
    """Serializer for recipes"""

    class Meta:
        model= Recipe
        fields= ['id','title','time_minutes','price','Link']
        read_only_fields= ['id']
