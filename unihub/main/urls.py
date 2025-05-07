from django.urls import path
from .views import (
    # Auth views
    SignupView, LoginView, LogoutView, CurrentUserView,
    
    # Profile views
    UserProfileView, ChangePasswordView, PublicProfileView,
    
    # Community views
    CommunityListView, UserCommunitiesView, CommunityDetailView,
    CommunityJoinView, CommunityLeaveView, CommunityMembersView,
    
    # Event views
    EventListView, EventDetailView, EventJoinView,
    EventLeaveView, EventAttendeesView,
    
    # Post views
    PostListView, PostDetailView, CommunityPostListView,
    
    # Notification views
    NotificationListView, MarkNotificationReadView, MarkAllNotificationsReadView,
    
    # Admin views
    AdminSignupView,
    AdminUserListView, AdminUserDetailView,
    AdminCommunityListView, AdminCommunityDetailView,
    AdminEventListView, AdminEventDetailView,
    AdminPostListView, AdminPostDetailView,
    AdminNotificationListView, AdminNotificationDetailView,
    VirtualSessionDetailView, VirtualSessionListView, AdminVirtualSessionDetailView, AdminVirtualSessionListView, CommunityVirtualSessionListView
)

urlpatterns = [
    # Auth endpoints
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/me/', CurrentUserView.as_view(), name='current-user'),

    # Profile endpoints
    path('users/profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/profile/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('users/<int:id>/profile/', PublicProfileView.as_view(), name='public-profile'),
    
    # Community endpoints
    path('communities/', CommunityListView.as_view(), name='community-list'),
    path('communities/user/', UserCommunitiesView.as_view(), name='user-communities'),
    path('communities/<int:pk>/', CommunityDetailView.as_view(), name='community-detail'),
    path('communities/<int:communityId>/join/', CommunityJoinView.as_view(), name='community-join'),
    path('communities/<int:communityId>/leave/', CommunityLeaveView.as_view(), name='community-leave'),
    path('communities/<int:communityId>/members/', CommunityMembersView.as_view(), name='community-members'),
    
    # Event endpoints
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:eventId>/join/', EventJoinView.as_view(), name='event-join'),
    path('events/<int:eventId>/leave/', EventLeaveView.as_view(), name='event-leave'),
    path('events/<int:eventId>/attendees/', EventAttendeesView.as_view(), name='event-attendees'),
    
    # Post endpoints
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('communities/<int:communityId>/posts/', CommunityPostListView.as_view(), name='community-posts'),
    
    # Notification endpoints
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:notificationId>/mark-read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('notifications/mark-all-read/', MarkAllNotificationsReadView.as_view(), name='mark-all-notifications-read'),

    # Virtual Sessions
#     path('virtual-sessions/', VirtualSessionListView.as_view(), name='virtual-session-list'),
    path('virtual-sessions/<int:pk>/', VirtualSessionDetailView.as_view(), name='virtual-session-detail'),
    path('communities/<int:communityId>/virtual-sessions/', CommunityVirtualSessionListView.as_view(), name='community-virtual-sessions'),
    
    # Admin Virtual Session endpoints
    path('admin/virtual-sessions/', AdminVirtualSessionListView.as_view(), name='admin-virtual-session-list'),
    path('admin/virtual-sessions/<int:pk>/', AdminVirtualSessionDetailView.as_view(), name='admin-virtual-session-detail'),

    # Admin endpoints
    path('admin/signup/', AdminSignupView.as_view(), name='admin-user-list'),
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<int:id>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin/communities/', AdminCommunityListView.as_view(), name='admin-community-list'),
    path('admin/communities/<int:pk>/', AdminCommunityDetailView.as_view(), name='admin-community-detail'),
    path('admin/events/', AdminEventListView.as_view(), name='admin-event-list'),
    path('admin/events/<int:pk>/', AdminEventDetailView.as_view(), name='admin-event-detail'),
    path('admin/posts/', AdminPostListView.as_view(), name='admin-post-list'),
    path('admin/posts/<int:pk>/', AdminPostDetailView.as_view(), name='admin-post-detail'),
    path('admin/notifications/', AdminNotificationListView.as_view(), name='admin-notification-list'),
    path('admin/notifications/<int:pk>/', AdminNotificationDetailView.as_view(), name='admin-notification-detail'),
]



