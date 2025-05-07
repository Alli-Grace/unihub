from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, LimitedUserSerializer, PostSerializer, ChangePasswordSerializer, EventSerializer, CommunitySerializer, NotificationSerializer, EventAttendeeSerializer, VirtualSessionSerializer, AdminSignupSerializer, CommunityMemberSerializer
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Community, CommunityMember, Post, Event, EventAttendee, VirtualSession, Notification
from .serializers import UserSerializer
from rest_framework.views import APIView




class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

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
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
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

# PROFILE
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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

# VIRTUALSESSIONS
class VirtualSessionListView(generics.ListCreateAPIView):
    queryset = VirtualSession.objects.all()
    serializer_class = VirtualSessionSerializer
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['community', 'platform', 'organizer']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        now = timezone.now()
        
        # Filter by upcoming/past sessions if requested
        status_filter = self.request.query_params.get('status', None)
        if status_filter == 'upcoming':
            queryset = queryset.filter(start_datetime__gte=now)
        elif status_filter == 'past':
            queryset = queryset.filter(start_datetime__lt=now)
            
        return queryset.order_by('start_datetime')

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class VirtualSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VirtualSession.objects.all()
    serializer_class = VirtualSessionSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsSessionOrganizer]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommunityVirtualSessionListView(generics.ListAPIView):
    serializer_class = VirtualSessionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        community_id = self.kwargs['communityId']
        return VirtualSession.objects.filter(
            community_id=community_id
        ).order_by('start_datetime')



# ADMIN
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class AdminSignupView(generics.CreateAPIView):
    serializer_class = AdminSignupSerializer
    permission_classes = [permissions.IsAdminUser]  # Only existing admins can create new admins

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role
            }
        }, status=status.HTTP_201_CREATED)

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

# Admin Views
class AdminVirtualSessionListView(generics.ListCreateAPIView):
    queryset = VirtualSession.objects.all()
    serializer_class = VirtualSessionSerializer
    permission_classes = [IsAdmin]
    
class AdminVirtualSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VirtualSession.objects.all()
    serializer_class = VirtualSessionSerializer
    permission_classes = [IsAdmin]