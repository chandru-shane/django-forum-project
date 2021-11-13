import re

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from profiles.api.serializers import UserProfileSerializer

User = get_user_model()

regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"


def is_email(email):
    """This function returns True if given argument is email
    else returns False"""

    if re.search(regex, email):
        return True
    else:
        return False


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        """Create new user with encrypted password and return it"""
        User = get_user_model()
        created_user = User.objects.create_user(**validated_data)
        return created_user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    username_or_email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        username = attrs.get("username_or_email")
        password = attrs.get("password")

        if is_email(username):
            User = get_user_model()
            username = User.objects.get(email=username).username

        user = authenticate(
            request=self.context.get("request"), username=username, password=password
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class UserNameProfileSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("profile",)
