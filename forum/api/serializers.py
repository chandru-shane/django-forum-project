
from django.db.models import fields
from rest_framework import serializers
from accounts.api.serializers import UserNameProfileSerializer


from ..models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    group_id = serializers.IntegerField(write_only=True)
    created_user = UserNameProfileSerializer(read_only=True)
    is_you_upvoted = serializers.SerializerMethodField()
    is_you_downvoted = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        exclude = ('upvote','downvote','group',)
        read_only_fields = 'created_user','upvote_count', 'downvote_count'
    
    def get_username(self, instance):
        return instance.created_user.username
    
    def get_is_you_upvoted(self, instance):
        request = self.context.get('request')
        return request.user in instance.upvote.all()

    def get_is_you_downvoted(self, instance):
        request = self.context.get('request')
        return request.user in instance.downvote.all()
    
    def get_comment_count(self, intance):
        return 10

class CreateCommentSerializer(serializers.ModelSerializer):
    object_id = serializers.CharField(required=True)
    is_comment = serializers.BooleanField(required=True)
    
    
    class Meta:
        model = Comment
        exclude = ('upvote','downvote')
        read_only_fields = 'created_user','upvote_count', 'downvote_count'

    

class CommentSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        exclude = ('upvote','downvote', 'created_user')
        read_only_fields = 'upvote_count', 'downvote_count'
    
    def get_created_by(self, instance):
        return instance.created_user.username


class ActionSerializer(serializers.Serializer):
    object_id = serializers.IntegerField(required=True)
