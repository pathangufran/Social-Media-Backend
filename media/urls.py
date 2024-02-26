from django.urls import path
from .views import (
    RegisterAPI, LoginAPI, UserProfileAPI, 
    PostCreateAPIView, PostListAPIView, 
    LikePostAPIView, UnlikePostAPIView, 
    SendConnectionRequestAPIView, IncomingConnectionRequestsAPIView, 
    AcceptConnectionRequestAPIView, DeclineConnectionRequestAPIView, 
    RecommendConnectionsAPIView
)

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('profile/', UserProfileAPI.as_view(), name='profile'),
    path('posts/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('posts/<int:post_id>/like/', LikePostAPIView.as_view(), name='post-like'),
    path('posts/<int:post_id>/unlike/', UnlikePostAPIView.as_view(), name='post-unlike'),
    path('connections/send/<int:to_user_id>/', SendConnectionRequestAPIView.as_view(), name='send-connection-request'),
    path('connections/incoming/', IncomingConnectionRequestsAPIView.as_view(), name='incoming-connection-requests'),
    path('connections/accept/<int:connection_id>/', AcceptConnectionRequestAPIView.as_view(), name='accept-connection-request'),
    path('connections/decline/<int:connection_id>/', DeclineConnectionRequestAPIView.as_view(), name='decline-connection-request'),
    path('connections/recommend/', RecommendConnectionsAPIView.as_view(), name='recommend-connections'),
]
