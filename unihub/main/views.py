from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, PostSerializer, EventSerializer, CommunitySerializer, NotificationSerializer, EventAttendeeSerializer, VirtualSessionSerializer, CommunityMemberSerializer
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Community, CommunityMember, Post, Event, EventAttendee, VirtualSession, Notification
from .serializers import UserSerializer

class LimitedUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']

class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        user_data = LimitedUserSerializer(user).data
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_data
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(email=email, password=password)
        
        if not user:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        user_data = LimitedUserSerializer(user).data
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_data
        })


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out'})
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

# class PasswordResetView(generics.GenericAPIView):
#     serializer_class = PasswordResetSerializer

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         email = serializer.validated_data['email']
#         try:
#             user = User.objects.get(email=email)
#             # Generate reset token and send email
#             # Implementation depends on your email service
#             return Response({'message': 'Password reset link sent'})
#         except User.DoesNotExist:
#             return Response(
#                 {'error': 'User with this email does not exist'},
#                 status=status.HTTP_404_NOT_FOUND
#             )

# class SetNewPasswordView(generics.GenericAPIView):
#     serializer_class = SetNewPasswordSerializer

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         # Validate reset token and update password
#         # Implementation depends on your token validation logic
#         return Response({'message': 'Password updated successfully'})

class CurrentUserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user



# PROFILE
class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class PublicProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['public_view'] = True
        return context

# class ChangePasswordView(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = ChangePasswordSerializer

#     def put(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         user = request.user
#         if not user.check_password(serializer.validated_data['current_password']):
#             return Response(
#                 {'current_password': 'Wrong password'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         user.set_password(serializer.validated_data['new_password'])
#         user.save()
#         return Response({'message': 'Password updated successfully'})
    
# COMMUNITY
class CommunityListView(generics.ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['category', 'is_private']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        community = serializer.save(creator=self.request.user)
        CommunityMember.objects.create(
            community=community,
            user=self.request.user,
            role='admin'
        )

class UserCommunitiesView(generics.ListAPIView):
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Community.objects.filter(
            members__user=self.request.user
        )

class CommunityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
            # return [permissions.IsAuthenticated(), IsCommunityAdmin()]
        return [permissions.IsAuthenticated()]

class CommunityJoinView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, communityId):
        community = Community.objects.get(pk=communityId)
        if community.is_private:
            # Handle join request for private communities
            return Response(
                {'message': 'Join request sent for approval'},
                status=status.HTTP_202_ACCEPTED
            )
        
        CommunityMember.objects.get_or_create(
            community=community,
            user=request.user,
            defaults={'role': 'member'}
        )
        return Response({'message': 'Successfully joined community'})

class CommunityLeaveView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, communityId):
        CommunityMember.objects.filter(
            community_id=communityId,
            user=request.user
        ).delete()
        return Response({'message': 'Successfully left community'})

class CommunityMembersView(generics.ListAPIView):
    serializer_class = CommunityMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        community_id = self.kwargs['communityId']
        return CommunityMember.objects.filter(community_id=community_id)
    
# EVENTS

class EventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['type', 'community', 'date_time']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
            # return [permissions.IsAuthenticated(), IsEventOrganizer()]
        return [permissions.AllowAny()]

class EventJoinView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, eventId):
        EventAttendee.objects.get_or_create(
            event_id=eventId,
            user=request.user
        )
        return Response({'message': 'Successfully joined event'})

class EventLeaveView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, eventId):
        EventAttendee.objects.filter(
            event_id=eventId,
            user=request.user
        ).delete()
        return Response({'message': 'Successfully left event'})

class EventAttendeesView(generics.ListAPIView):
    serializer_class = EventAttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['eventId']
        return EventAttendee.objects.filter(event_id=event_id)

# POSTS

class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['post_type', 'community', 'author']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            # return [permissions.IsAuthenticated(), IsPostAuthorOrModerator()]
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

class CommunityPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        community_id = self.kwargs['communityId']
        return Post.objects.filter(community_id=community_id)
    

# NOTIFICATION

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['is_read', 'type']

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class MarkNotificationReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, notificationId):
        notification = Notification.objects.get(
            pk=notificationId,
            user=request.user
        )
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'})

class MarkAllNotificationsReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)
        return Response({'message': 'All notifications marked as read'})


# ADMIN
from rest_framework import generics, permissions
from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Community, Event, Post, Notification
from .serializers import (
    UserSerializer, 
    CommunitySerializer,
    EventSerializer,
    PostSerializer,
    NotificationSerializer
)

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

# User Admin Views
class AdminUserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['role', 'department', 'year']

class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'id'

# Community Admin Views
class AdminCommunityListView(generics.ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAdmin]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['category', 'is_private']

class AdminCommunityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAdmin]

# Event Admin Views
class AdminEventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdmin]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['type', 'community', 'creator']

class AdminEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdmin]

# Post Admin Views
class AdminPostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdmin]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['post_type', 'community', 'author']

class AdminPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdmin]

# Notification Admin Views
class AdminNotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdmin]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['type', 'is_read', 'user']

class AdminNotificationDetailView(generics.RetrieveDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdmin]