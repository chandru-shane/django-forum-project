from django.db import models
from rest_framework import serializers
from ..models import ForumGroup

class ForumGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ForumGroup
        fields = "__all__"
        read_only_fields = 'created_user', 'admin'


class JoinMemberSerializer(serializers.Serializer):
    group_id = serializers.IntegerField(required=True)


class MemberUsernameSerializer(serializers.Serializer):
    group_id = serializers.IntegerField(required=True)
    username = serializers.CharField(required=True)

class AcceptOrNotRequestSerializer(serializers.Serializer):
    request_id = serializers.IntegerField(required=True)
    is_added = serializers.BooleanField(required=True)
