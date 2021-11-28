from django.contrib.auth import get_user_model
from django.db.models.fields import json
from rest_framework import generics, permissions, status, authentication
from rest_framework.views import APIView 
from rest_framework.response import Response

from .serializers import (
    ForumGroupSerializer, 
    JoinMemberSerializer,
    MemberUsernameSerializer,
    AcceptOrNotRequestSerializer
)

from ..models import ForumGroup, JoinRequest
from .permissions import IsGroupAdminUser

User = get_user_model()

class FourmGroupCreateAPIView(generics.CreateAPIView):
    queryset = ForumGroup.objects.all()
    serializer_class = ForumGroupSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)

    def perform_create(self, serializer):
        serializer.save(created_user=self.request.user,admin=self.request.user)


class FroumGroupUpdateRetriveUpdateDestoryAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ForumGroup.objects.all()
    lookup_field = 'id'
    serializer_class = ForumGroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsGroupAdminUser)
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)


class JoinMemberAPIView(APIView):
    serializer_class = JoinMemberSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)

    def post(self, request, *args, **kwargs):
        serialized_data = JoinMemberSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        forum_group = generics.get_object_or_404(ForumGroup,id=serialized_data.validated_data.get('group_id'))
        if forum_group.is_private:

            JoinRequest.objects.create(group=forum_group, user=self.request.user) 
            return Response({'request':True,  'joined':True}, status=status.HTTP_200_OK)
        else:
            forum_group.members.add(self.request.user)
            return Response({'request':False, 'joined':True}, status=status.HTTP_200_OK)
            


class AcceptOrNotMemberAPIView(APIView):
    serializer_class = AcceptOrNotRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    
    def post(self, request, *args, **kwargs):
        serialized_data = AcceptOrNotMemberAPIView(data=request.data)
        if not serialized_data.is_valid():
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        join_request = generics.get_object_or_404(JoinRequest, id=serialized_data.validated_data.get('request_id'))
        if join_request.admin == request.user:
            join_request.group.members.add(join_request.user)
            join_request.delete()
            return Response('Done', status=status.HTTP_200_OK)
        else:
            return Response('Admin only can accpet the request', status=status.HTTP_403_FORBIDDEN)
        

class RemoveMemberAPIView(APIView):
    serializer_class = MemberUsernameSerializer
    permission_classes = (permissions.IsAuthenticated,IsGroupAdminUser)
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)

    def post(self, request, *args, **kwargs):
        serialized_data = MemberUsernameSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        forum_group = generics.get_object_or_404(ForumGroup,id=serialized_data.validated_data.get('group_id'))
        # this is not gonna run permissions will handle this function
        if self.request.user != forum_group.admin:
            message = 'Admin user only remove the members of this groups'
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            remove_user = generics.get_object_or_404(User,username=serialized_data.validated_data.get('username'))
            forum_group.members.remove(remove_user)
            return Response(True, status=status.HTTP_200_OK)


class RemoveFromGroupAPIView(APIView):
    serializer_class = JoinMemberSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)

    def post(self, request, *args, **kwargs):
        serialized_data = JoinMemberSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        
        forum_group = generics.get_object_or_404(ForumGroup,id=serialized_data.validated_data.get('group_id'))
        if request.user in forum_group.members.all():
            forum_group.members.remove(request.user)
            return Response('removed', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Cannot do that',status=status.HTTP_403_FORBIDDEN)


class GroupListAPIView(APIView):
    # serializer_class = 
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)

    def get(self, request, *args, **kwargs):
        admin_groups= request.user.admin_groups.all()
        member_groups = request.user.group_members.all()
        groups = [*admin_groups, *member_groups]
        serialized = ForumGroupSerializer(groups, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)