from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from knox.models import AuthToken
from .models import UserProfile, Post, Like, Connection
from .serializers import UserProfileSerializer, PostSerializer, LikeSerializer, ConnectionSerializer, UserSerializer
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

class RegisterAPI(APIView):
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            _, token = AuthToken.objects.create(user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPI(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            _, token = AuthToken.objects.create(user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Check if UserProfile exists for the authenticated user
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            # Create UserProfile if it doesn't exist
            user_profile = UserProfile.objects.create(user=request.user)
        
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request, format=None):
        # Check if UserProfile exists for the authenticated user
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            # Create UserProfile if it doesn't exist
            user_profile = UserProfile.objects.create(user=request.user)

        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class LikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, format=None):
        try:
            post = Post.objects.get(pk=post_id)
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            if created:
                return Response({'message': 'Post liked successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

class UnlikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id, format=None):
        try:
            like = Like.objects.get(user=request.user, post__id=post_id)
            like.delete()
            return Response({'message': 'Post unliked successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({'message': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)

class SendConnectionRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, to_user_id, format=None):
        try:
            to_user = User.objects.get(pk=to_user_id)
            if request.user == to_user:
                return Response({'message': 'You cannot send a connection request to yourself'}, status=status.HTTP_400_BAD_REQUEST)
            connection, created = Connection.objects.get_or_create(from_user=request.user, to_user=to_user)
            if created:
                return Response({'message': 'Connection request sent successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Connection request already sent'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class IncomingConnectionRequestsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        incoming_requests = Connection.objects.filter(to_user=request.user, status='pending')
        serializer = ConnectionSerializer(incoming_requests, many=True)
        return Response(serializer.data)

class AcceptConnectionRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, connection_id, format=None):
        try:
            connection = Connection.objects.get(pk=connection_id, to_user=request.user, status='pending')
            connection.status = 'accepted'
            connection.save()
            return Response({'message': 'Connection request accepted successfully'}, status=status.HTTP_200_OK)
        except Connection.DoesNotExist:
            return Response({'message': 'Connection request not found'}, status=status.HTTP_404_NOT_FOUND)

class DeclineConnectionRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, connection_id, format=None):
        try:
            connection = Connection.objects.get(pk=connection_id, to_user=request.user, status='pending')
            connection.status = 'declined'
            connection.save()
            return Response({'message': 'Connection request declined successfully'}, status=status.HTTP_200_OK)
        except Connection.DoesNotExist:
            return Response({'message': 'Connection request not found'}, status=status.HTTP_404_NOT_FOUND)

class RecommendConnectionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Get current user's connections
        user_connections = Connection.objects.filter(from_user=request.user, status='accepted').values_list('to_user', flat=True)
        user_connections_ids = list(user_connections)

        # Get users who are not already connected with the current user
        suggested_users = User.objects.exclude(id__in=user_connections_ids).exclude(id=request.user.id)

        suggested_users = self.get_users_based_on_mutual_connections(suggested_users, request.user)

        serializer = UserSerializer(suggested_users, many=True)
        return Response(serializer.data)

    def get_users_based_on_mutual_connections(self, suggested_users, user):
        mutual_connections_users = []

        # Get current user's connections
        user_connections = Connection.objects.filter(from_user=user, status='accepted').values_list('to_user', flat=True)
        user_connections_ids = list(user_connections)

        # Iterate through suggested users
        for suggested_user in suggested_users:
            # Check if the suggested user has any connections with the current user's connections
            mutual_connections = Connection.objects.filter(from_user=suggested_user, to_user__in=user_connections_ids, status='accepted').count()
            if mutual_connections > 0:
                mutual_connections_users.append(suggested_user)

        return mutual_connections_users
