from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path('username/', views.ProfileRetriveAPIView.as_view(), name='username'),
    path('username/<str:username>/', views.ProfileRetirveForOtherAPIView.as_view(), name='username-other'),
    path("follow/", views.FollowAPIView.as_view(), name='follow'),
    path('followers/', views.FollowersListAPIView.as_view(), name='followers'),
    path('following/', views.FollowingListAPIView.as_view(), name='following'),
    path('followers/<str:username>/', views.FollowersForOtherUserListAPIView.as_view(), name='followers-username'),
    path('following/<str:username>/', views.FollowingsForOtherUserListAPIView.as_view(), name='following-username'),
    path('isauth/', views.IsAuth.as_view(), name='is-auth'),
    path('updateprofilepicture/', views.UpdateProfilePictureAPIView.as_view(), name='update-profile-picture'),
    path('updateprofile/', views.UpdateProfileAPIView.as_view(), name='update-profile'),
    path('search/', views.UserApiListSearchView.as_view(),name='userprofile-search'),
    path('changepassword/', views.ChangePasswordAPIView.as_view(),name='change-password'),
]