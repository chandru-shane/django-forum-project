from django.urls import path
from . import views


app_name = "api_forum_group"


urlpatterns = [
    path('create/', views.FourmGroupCreateAPIView.as_view(), name='group-create'),
    path('<int:id>/', views.FroumGroupUpdateRetriveUpdateDestoryAPIView.as_view(),name='group-r-u-d'),
    path('join/',views.JoinMemberAPIView.as_view(),name='join-member'),
    path('response/',views.AcceptOrNotMemberAPIView.as_view(),name='response' ),
    path('remove/', views.RemoveMemberAPIView.as_view(), name='remove'),
    path('removefromgroup/', views.RemoveFromGroupAPIView.as_view(), name='remove-from-group'),
]
