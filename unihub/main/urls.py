from django.urls import path
from .views import (
    # Auth views
    SignupView, LoginView, LogoutView,
    PasswordResetView, SetNewPasswordView, CurrentUserView,
    
    # Profile views
    UserProfileView, PublicProfileView, ChangePasswordView,
    
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
    AdminUserListView, AdminUserDetailView,
    AdminCommunityListView, AdminCommunityDetailView,
    AdminEventListView, AdminEventDetailView,
    AdminPostListView, AdminPostDetailView,
    AdminNotificationListView, AdminNotificationDetailView
)

urlpatterns = [
    # Auth endpoints
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    # path('auth/reset-password/', PasswordResetView.as_view(), name='password-reset'),
    # path('auth/set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
    path('auth/me/', CurrentUserView.as_view(), name='current-user'),

    # Profile endpoints
    path('users/profile/', UserProfileView.as_view(), name='user-profile'),
    # path('users/profile/change-password/', ChangePasswordView.as_view(), name='change-password'),
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
    
    # Admin endpoints
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

# urlpatterns = [
#     # Authentication
#     path('signup/', views.RegisterView.as_view(), name='signup'),
#     path('login/', views.LoginView.as_view(), name='login'),
#     path('admin/signup/', views.AdminRegisterView.as_view(), name='admin-signup'),

#     # Profiles
#     path('profile/view/<int:pk>/', views.ProfileRetrieveView.as_view(), name='profile-view'),
#     path('profile/update/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile-update'),

#     # Categories
#     path('categories/', views.CategoryListView.as_view(), name='category-list'),
#     path('category/<int:pk>/', views.CategoryRetrieveView.as_view(), name='category-view'),
#     path('admin/category/create/', views.CategoryCreateView.as_view(), name='admin-category-create'),
#     path('admin/category/<int:pk>/', views.AdminCategoryRetrieveUpdateDestroyView.as_view(), name='admin-category-rud'),

#     # Communities
#     path('communities/', views.CommunityListView.as_view(), name='community-list'),
#     path('community/<int:pk>/', views.CommunityRetrieveView.as_view(), name='community-view'),
#     path('admin/community/create/', views.CommunityCreateView.as_view(), name='admin-community-create'),
#     path('admin/community/<int:pk>/', views.AdminCommunityRetrieveUpdateDestroyView.as_view(), name='admin-community-rud'),
#     path('communities/<int:community_pk>/members/', views.CommunityMemberListCreateView.as_view(), name='community-members-list-create'),
#     path('communities/<int:community_pk>/members/<int:pk>/', views.CommunityMemberDetailView.as_view(), name='community-members-detail'),

#     # Posts
#     path('posts/', views.PostListView.as_view(), name='post-list'),
#     path('posts/create/', views.PostCreateView.as_view(), name='post-create'),
#     path('post/<int:pk>/', views.PostRetrieveView.as_view(), name='post-view'),
#     path('admin/post/<int:pk>/', views.AdminPostRetrieveUpdateDestroyView.as_view(), name='admin-post-rud'),

#     # Events
#     path('events/', views.EventListView.as_view(), name='event-list'),
#     path('event/<int:pk>/', views.EventRetrieveView.as_view(), name='event-view'),
#     path('admin/event/create/', views.EventCreateView.as_view(), name='admin-event-create'),
#     path('admin/event/<int:pk>/', views.AdminEventRetrieveUpdateDestroyView.as_view(), name='admin-event-rud'),
#     path('events/<int:event_pk>/attendees/', views.EventAttendeeListCreateView.as_view(), name='event-attendees-list-create'),
#     path('events/<int:event_pk>/attendees/<int:pk>/', views.EventAttendeeDetailView.as_view(), name='event-attendees-detail'),

#     # Notifications
#     path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
#     path('notification/<int:pk>/', views.NotificationRetrieveView.as_view(), name='notification-view'),
#     path('admin/notification/create/', views.NotificationCreateView.as_view(), name='admin-notification-create'),
#     path('admin/notification/<int:pk>/', views.AdminNotificationRetrieveUpdateDestroyView.as_view(), name='admin-notification-rud'),

#     # Virtual Sessions
#     path('virtual-sessions/', views.VirtualSessionListView.as_view(), name='virtual-session-list'),
#     path('virtual-sessions/create/', views.VirtualSessionCreateView.as_view(), name='virtual-session-create'),
#     path('virtual-sessions/<int:pk>/', views.VirtualSessionRetrieveUpdateDestroyView.as_view(), name='virtual-session-rud'),
# ]


# # from . import views
# # from django.urls import path

# # urlpatterns = [
# #     # Student(Memeber)
# #     path('signup/', views.RegisterView.as_view(), name='signup'),
# #     path('login/', views.LoginView.as_view(), name='login'),
# #     path('profile/view/<int:pk>/', views.ProfileRetrieveView.as_view(), name='profile-view'),
# #     path('profile/update/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile-update'),
# #     path('categories/', views.CategoryListView.as_view(), name='category-list'),
# #     path('category/<int:pk>/', views.CategoryRetrieveView.as_view(), name='category-view'),
# #     path('communities/', views.CommunityListView.as_view(), name='community-list'),
# #     path('community/<int:pk>/', views.CommunityRetrieveView.as_view(), name='community-view'),
# #     path('events/', views.EventListView.as_view(), name='event-list'),
# #     path('event/<int:pk>/', views.EventRetrieveView.as_view(), name='event-view'),
# #     path('post/create', views.PostCreateView.as_view(), name='post-create'),
# #     path('posts/', views.PostListView.as_view(), name='post-list'),
# #     path('post/<int:pk>/', views.PostRetrieveView.as_view(), name='post-view'),
    


# # # Admin
# #     path('admin/signup/', views.AdminRegisterView.as_view(), name='admin-signup'),
# #     path('admin/profile/<int:k>/', views.ProfileUpdateView.as_view(), name='login'),
# #     path('admin/category/create/', views.CategoryCreateView.as_view(), name='login'),
# #     path('admin/category/<int:k>/', views.AdminCategoryRetrieveUpdateDestroyView.as_view(), name='login'),
# #     path('admin/community/<int:k>/', views.AdminCommunityRetrieveUpdateDestroyView.as_view(), name='login'),
# #     path('admin/community/create/', views.CommunityCreateView.as_view(), name='login'),
# #     path('admin/event/create/', views.EventCreateView.as_view(), name='login'),
# #     path('admin/event/<int:k>/', views.AdminEventRetrieveUpdateDestroyView.as_view(), name='login'),

# #     path('admin/event/create/', views.LoginView.as_view(), name='login'),
# #     path('login/', views.LoginView.as_view(), name='login'),
# #     path('login/', views.LoginView.as_view(), name='login'),
# # ]

