from django.urls import path
from . import views

app_name = "api_forum"

urlpatterns = [
    path('home/', views.HomePostAPIView.as_view(), name='home' ),
    path('post/create/', views.PostCreateAPIView.as_view(), name='create-post'),
    path('comment/create/', views.CreateCommentAPIView.as_view(),name='create-comment'),
    path('post/<int:id>/', views.PostRetriveUpdateDeleteAPIView.as_view(),name='post-update-delete'),
    path('comment/<int:id>/', views.CommentRetriveUpdateDeleteAPIView.as_view(),name='comment-update-delete'),
    path('post/upvote/',views.PostUpvoteAPIView.as_view(),name='post-upvote'),
    path('post/downvote/',views.PostDownvoteAPIView.as_view(),name='post-downvote'),
    path('comment/upvote/',views.CommentUpvoteAPIView.as_view(),name='comment-upvote'),
    path('comment/downvote/',views.CommentDownvoteAPIView.as_view(),name='comment-downvote'),
]
