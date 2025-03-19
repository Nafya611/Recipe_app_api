"""serializes for user api view"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
    )
from django.utils.translation import gettext as _
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """serializer for user object"""


    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self,validated_data):
        """Create and return  a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

class AuthTokenSerializer(serializers.Serializer):
    """serializer for the user auth token """

    email = serializers.EmailField()
    password= serializers.CharField(
        style= {'input_type': 'password'},
        trim_whitespace = False,
    )

