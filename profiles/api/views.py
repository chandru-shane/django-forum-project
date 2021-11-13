from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.core import exceptions
from django.db import IntegrityError

from rest_framework import (
    generics,
    authentication,
    permissions,
    status,
    filters
)

from rest_framework.views import APIView
from rest_framework.response import Response
from profiles.models import UserProfile, FollowingRelation
from accounts.api.serializers import UserNameProfileSerializer

from .throttle import ChangePasswordThrottle

from .serializers import (
    UserProfileSerializer, 
    FollowRelationSerializer,
    FollowSerializer,
    ProfilePictureSerializer, 
    ProfileUpdateSerializer,
    ChangePasswordSerailizer,
)

from .pagination import (
    UserSearchResultsSetPagination,
    UserProfileListPagination, 
)

from ..signals import follow_notification

User = get_user_model()


class ProfileRetriveAPIView(generics.RetrieveAPIView):
    """
    This ProfileRetriveAPIView class retriew the username
    and profile bio and profile image
    """
    # lookup_field = "username"
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication,
                              authentication.SessionAuthentication]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class ProfileRetirveForOtherAPIView(generics.RetrieveAPIView):
    """
    NOT AUTHENTICATED
    This ProfileRetirveForOtherAPIView class retriew the username
    and profile bio and profile image for others
    """
    lookup_field = "username"
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        user_id = generics.get_object_or_404(User, username=kwargs['username'])
        user_profile = generics.get_object_or_404(UserProfile, user=user_id)
        serializer = UserProfileSerializer(
            user_profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowAPIView(APIView):
    """
    OPTIMIZED VERSION OF
    Follow and Unfollow endpoints
    """

    authentication_classes = (authentication.SessionAuthentication,
                              authentication.TokenAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer

    def post(self, request):
        """
        getting the requested user who wants to follow
        """

        # getting the sender user profie
        user_profile = request.user.profile

        serialized = FollowSerializer(data=request.data)

        if serialized.is_valid():
            # serializer is valid
            # first getting the user object from data base
            # if user not exists return error code

            following_user = generics.get_object_or_404(
                User, username=serialized.data.get('username'))

            # is_follow should be True or False

            if serialized.data.get('is_follow'):
                try:
                    FollowingRelation.objects.create(
                        user=following_user, userprofile=self.request.user.profile)
                except IntegrityError:
                    return Response('Followed', status=status.HTTP_201_CREATED)
                else:
                    # create the notification
                    follow_notification.send(
                        sender=self.__class__, instance=request.user, user=following_user)
                    return Response('Followed', status=status.HTTP_201_CREATED)
            else:
                try:
                    unfollowing_user = FollowingRelation.objects.get(
                        user=following_user, userprofile=self.request.user.profile)
                    unfollowing_user.delete()
                except exceptions.ObjectDoesNotExist:
                    return Response('Unfollowed', status=status.HTTP_200_OK)
                else:
                    return Response('Unfollowed', status=status.HTTP_200_OK)

        else:
            return Response(serialized.data, status=status.HTTP_400_BAD_REQUEST)


class FollowersListAPIView(generics.ListAPIView):
    authentication_classes = (authentication.SessionAuthentication,
                              authentication.TokenAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = UserProfileListPagination
    serializer_class = FollowRelationSerializer

    def get_queryset(self):
        return self.request.user.followers.all()


class FollowingListAPIView(generics.ListAPIView):
    """
    this wil return following users to authenticated user
    """
    authentication_classes = (authentication.SessionAuthentication,
                              authentication.TokenAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = UserProfileListPagination
    serializer_class = UserNameProfileSerializer

    def get_queryset(self):
        return self.request.user.profile.following.all()


class FollowersForOtherUserListAPIView(generics.ListAPIView):
    """
    List Api View of Followers user for other users getting by 
    useraname
    """
    authentication_classes = (authentication.SessionAuthentication,
                              authentication.TokenAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = UserProfileListPagination
    serializer_class = FollowRelationSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(get_user_model(), username=username)
        return user.followers.all()


class FollowingsForOtherUserListAPIView(generics.ListAPIView):
    """
    List Api View of Following users for other users getting by 
    useraname
    """
    authentication_classes = (authentication.SessionAuthentication,
                              authentication.TokenAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = UserProfileListPagination
    serializer_class = UserNameProfileSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(get_user_model(), username=username)
        return user.profile.following.all()


class IsAuth(APIView):
    """
    This class tells the user is authenticated or not, when
    they make get request.
    if authentication -> response status code is 200
    else -> response status code is 401
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, reqeust, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


class UpdateProfilePictureAPIView(APIView):
    authentication_classes = (authentication.TokenAuthentication,
                              authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfilePictureSerializer

    def post(self, request, *args, **kwargs):

        serialized = ProfilePictureSerializer(
            self.request.user.profile, data=request.data)

        if serialized.is_valid():
            previous_image = self.request.user.profile.image
            check_value = 'profile_pics/default.png'
            #checking the do we deleting the default image
            # if not delete the image 
            if not previous_image.url[len(previous_image.url)-len(check_value):] == check_value:
                previous_image.delete()
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)

        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfileAPIView(APIView):
    """
    This class update the profile data except profile picture
    that will handled by the other class 
    """
    authentication_classes = (authentication.TokenAuthentication,
                              authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileUpdateSerializer

    def post(self, request, *args, **kwargs):
        serialized = ProfileUpdateSerializer(
            self.request.user.profile, data=request.data)
        
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)
        
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

# SEARCH AREA VIEW


class UserApiListSearchView(generics.ListAPIView):
    search_fields = ['username']
    filter_backends = (filters.SearchFilter,)
    queryset = User.objects.all()
    serializer_class = UserNameProfileSerializer
    pagination_class = UserSearchResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,
                              authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if request.query_params.get('search') != None and len(request.query_params.get('search')):
            return super().get(request, *args, **kwargs)
        else:
            return Response('no queries', status=status.HTTP_200_OK)





class ChangePasswordAPIView(APIView):
    """
    This class take care of user to change their password.
    """
    serializer_class = ChangePasswordSerailizer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (authentication.TokenAuthentication,
                              authentication.SessionAuthentication)
    throttle_classes = [ChangePasswordThrottle]

    def post(self, request, *args, **kwargs):
        serialized = ChangePasswordSerailizer(
            data=request.data, context={'request': request})
        if serialized.is_valid():
            current_password = serialized.validated_data.get(
                'current_password')
            is_current_correct = check_password(
                current_password, request.user.password)
            if is_current_correct:
                user = authenticate(
                    username=request.user.username, password=current_password)
                if user != None:
                    change_password = serialized.validated_data.get(
                        'change_password')
                    user.set_password(change_password)
                    user.save()
                    return Response('Changed', status=status.HTTP_200_OK)
                else:
                    return Response('Something went worng', status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response('Worng Password', status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
