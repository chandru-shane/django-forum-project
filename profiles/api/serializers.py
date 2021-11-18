from django.contrib.auth import get_user_model
from django.conf import settings
from django.core import exceptions
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import get_password_validators

from rest_framework import serializers
from profiles.models import UserProfile, FollowingRelation

class UserProfileSerializer(serializers.ModelSerializer):
    """
    This serialier class serializer user profile image
    and bio.
    """
    image = serializers.ImageField(
                                    max_length=None,
                                    allow_empty_file=False,
                                    allow_null=True,
                                    required=False)
    
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    is_user = serializers.SerializerMethodField()
    follow_status = serializers.SerializerMethodField()
    follows_you = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ('id','image', 'bio', 'display_name', "followers","is_private", "following", "username","is_user", "follow_status","follows_you", "is_verified",)

    def get_follows_you(self, obj):
        request = self.context.get('request')
        if request.user.profile == obj:
            return None
        try:
            FollowingRelation.objects.get(user=request.user, userprofile=obj)
        except exceptions.ObjectDoesNotExist:
            return False
        else:
            return True

    
    
    def get_followers(self, obj):
        """
        returns the followers count

        Args:
            obj ([object]): [userprofile object]

        Returns:
            [int]: [followers count]
        """
        followers = obj.user.followers.all().count()
        return followers
    
    def get_following(self, obj):
        """
        returns the followings count

        Args:
            obj ([object]): [userprofile object]

        Returns:
            [int]: [followings count]
        """
        following = obj.following.all().count()
        return following
    
    def get_username(self, obj):
        username = obj.user.username
        return username
    
    def get_is_user(self, obj):
        request = self.context.get('request')
        return request.user == obj.user 
    
    def get_follow_status(self, obj):
        """
        This will return is user is follows you
        return None when you are the user

        Args:
            obj ([object]): [user profile object]

        Returns:
            None: When user is reqeusting user
            True: When this user object follows you
            False: When this use object not follows you
        """
        request = self.context.get('request')
        if request.user.profile == obj:
            return None
        try:
            FollowingRelation.objects.get(user=obj.user, userprofile=request.user.profile)
        except exceptions.ObjectDoesNotExist:
            return False
        else:
            return True
    
    

class FollowRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ("follows",)

class FollowSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    is_follow = serializers.BooleanField(required=True)

class ProfilePictureSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(allow_empty_file=False,required=True,)

    class Meta:
        model = UserProfile
        fields = ("image",)

class ProfileUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ("display_name", "bio", )

class FollowRelationSerializer(serializers.ModelSerializer):
    
    userprofile = UserProfileSerializer()
    
    class Meta:
        model = FollowingRelation
        fields = ('userprofile',)

class ChangePasswordSerailizer(serializers.Serializer):

    current_password = serializers.CharField()
    change_password = serializers.CharField()
    
    class Meta:
        extra_kwargs = {"current_password": {"write_only": True, "min_length": 8}}
        extra_kwargs = {"change_password": {"write_only": True, "min_length": 8}}
    
    def validate_current_password(self,value):
        request = self.context.get('request')
        is_current_correct = check_password(value,request.user.password)
        if not is_current_correct:
            raise serializers.ValidationError('incorrect password')
        return value

    def validate_change_password(self,value):
        validators = get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
        request = self.context.get('request')
        for validator in validators:
            try:
                validator.validate(value, user=request.user)
            except serializers.ValidationError as e:
                raise e
        return value

