from django.contrib.auth.models import Group
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication
from rest_framework import permissions


from forum_group.models import ForumGroup

from ..models import Post, CommentMapper, Comment
from . import serializers as forum_serializers
from .permissions import IsCreatedUser


class HomePostAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    def get(self, request, *args, **kwargs):
        data = forum_serializers.PostSerializer(Post.objects.feed(request.user), many=True,context={'request': request})
        return Response(data.data, status=status.HTTP_200_OK)


class PostCreateAPIView(APIView):
    queryset = Post.objects.all()
    serializer_class = forum_serializers.PostSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)

    def post(self, request, *args, **kwargs):
        serializer = forum_serializers.PostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        group = generics.get_object_or_404(ForumGroup,pk=serializer.validated_data.get('group_id'))
        if self.request.user == group.admin or self.request.user in group.members.all():
            serializer.save(created_user=self.request.user, group=group)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response('You cannot post a post in non menber group', status=status.HTTP_403_FORBIDDEN)

class PostRetriveUpdateDeleteAPIView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    lookup_field = 'id'
    serializer_class = forum_serializers.PostSerializer
    permission_classes = (permissions.IsAuthenticated,IsCreatedUser)

class CreateCommentAPIView(APIView):
    serializer_class = forum_serializers.CreateCommentSerializer
    
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serialized_data = forum_serializers.CreateCommentSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response(serialized_data.error_messages, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            # create comment object
            if serialized_data.validated_data.get('is_comment'):
                comment = generics.get_object_or_404(Comment, id=serialized_data.validated_data.get('object_id'))
                replied_comment = Comment.objects.create(
                    body=serialized_data.validated_data.get('body'),
                    created_user = self.request.user
                    )
                # map the comment using comment mapper model
                # comment_mapper
                CommentMapper.objects.create(comment=comment, reply_comment=replied_comment)
                serialized_result_data = forum_serializers.CommentSerializer(replied_comment)
                return Response(serialized_result_data.data ,status=status.HTTP_201_CREATED)
            
            else:
                post = generics.get_object_or_404(Post, id=serialized_data.validated_data.get('object_id'))
                replied_comment = Comment.objects.create(
                    body=serialized_data.validated_data.get('body'),
                    created_user = self.request.user
                    )
                # map the comment using comment mapper model
                # comment_mapper
                CommentMapper.objects.create(post=post, reply_comment=replied_comment)
                serialized_result_data = forum_serializers.CommentSerializer(replied_comment)
                return Response(serialized_result_data.data ,status=status.HTTP_201_CREATED)
   
class CommentRetriveUpdateDeleteAPIView(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    lookup_field = 'id'
    serializer_class = forum_serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticated,IsCreatedUser)
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)


class PostUpvoteAPIView(APIView):
    serializer_class = forum_serializers.ActionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)

    def post(self, request, *args, **kwargs):
        serialized_data = forum_serializers.ActionSerializer(data=request.data)
        
        if not serialized_data.is_valid():
            return Response(serialized_data.error_messages, status=status.HTTP_400_BAD_REQUEST)
        
        post = generics.get_object_or_404(Post, id=serialized_data.validated_data.get('object_id'))
        if request.user in post.downvote.all():
            post.downvote.remove(request.user)
            post.downvote_count = post.downvote_count - 1            
        
        if request.user in post.upvote.all():
            post.upvote.remove(request.user)
            post.upvote_count = post.upvote_count - 1
            response = Response(False, status=status.HTTP_204_NO_CONTENT)
        
        else:
            post.upvote.add(request.user)
            post.upvote_count = post.upvote_count + 1
            response = Response(True, status=status.HTTP_201_CREATED)
        
        post.save()
        return response


class PostDownvoteAPIView(APIView):
    serializer_class = forum_serializers.ActionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)

    def post(self, request, *args, **kwargs):
        serialized_data = forum_serializers.ActionSerializer(data=request.data)
        
        if not serialized_data.is_valid():
            return Response(serialized_data.error_messages, status=status.HTTP_400_BAD_REQUEST)
        
        post = generics.get_object_or_404(Post, id=serialized_data.validated_data.get('object_id'))
        if request.user in post.upvote.all():
            post.upvote.remove(request.user)
            post.upvote_count = post.upvote_count - 1  
        
        if request.user in post.downvote.all():
            post.downvote.remove(request.user)
            post.downvote_count = post.downvote_count - 1 
            response = Response(False, status=status.HTTP_204_NO_CONTENT)
        
        else:
            post.downvote.add(request.user)
            post.downvote_count = post.downvote_count + 1
            response = Response(True, status=status.HTTP_201_CREATED)
        
        post.save()
        return response


class CommentUpvoteAPIView(APIView):
    serializer_class = forum_serializers.ActionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)

    def post(self, request, *args, **kwargs):
        serialized_data = forum_serializers.ActionSerializer(data=request.data)
        
        if not serialized_data.is_valid():
            return Response(serialized_data.error_messages, status=status.HTTP_400_BAD_REQUEST)
        
        comment = generics.get_object_or_404(Comment, id=serialized_data.validated_data.get('object_id'))
        if self.user in comment.downvote.all():
            comment.downvote.remove(self.user)
            comment.downvote_count = comment.downvote_count - 1            

        
        if self.user in comment.upvote.all():
            comment.upvote.remove(self.user)
            comment.upvote_count = comment.upvote_count - 1
            response = Response(False, status=status.HTTP_204_NO_CONTENT)
        
        else:
            comment.upvote.add(self.user)
            comment.upvote_count = comment.upvote_count + 1
            response = Response(True, status=status.HTTP_201_CREATED)
        
        comment.save()
        return response


class CommentDownvoteAPIView(APIView):
    serializer_class = forum_serializers.ActionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)

    def post(self, request, *args, **kwargs):
        serialized_data = forum_serializers.ActionSerializer(data=request.data)
        
        if not serialized_data.is_valid():
            return Response(serialized_data.error_messages, status=status.HTTP_400_BAD_REQUEST)
        
        comment = generics.get_object_or_404(Comment, id=serialized_data.validated_data.get('object_id'))
        if self.user in comment.upvote.all():
            comment.upvote.remove(self.user)
        
        if self.user in comment.downvote.all():
            comment.downvote.remove(self.user)
            return Response(False, status=status.HTTP_204_NO_CONTENT)
        
        else:
            comment.downvote.add(self.user)
            return Response(True, status=status.HTTP_201_CREATED)
