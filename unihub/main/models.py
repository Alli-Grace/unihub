from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.utils.translation import gettext_lazy as _
# from django.contrib.postgres.fields import ArrayField, JSONField  # If you want to use these
from django.db.models import JSONField 
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator
# from django.contrib.postgres.fields import ArrayField, JSONField  # For PostgreSQL
from django.db.models import JSONField
# ----------------------------
# User Manager
# ----------------------------
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# ----------------------------
# User Model
# ----------------------------
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('student', 'Student'),
        # ('staff', 'Staff'),
        ('admin', 'Admin'),
    )


    first_name = models.CharField(max_length=255, default='Text')
    last_name = models.CharField(max_length=255, default='Text')
    email = models.EmailField(unique=True)
    #validators=[RegexValidator(regex=EDU_EMAIL_REGEX, message="Must use a .edu email")])
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    avatar_url = models.URLField(blank=True, null=True)
    major = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True)  # e.g., Freshman
    department = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    interests = models.CharField(models.CharField(max_length=100), blank=True, null=True)
    social_links = JSONField(blank=True, default=dict)
    privacy_settings = JSONField(blank=True, default=dict)
    notification_preferences = JSONField(blank=True, default=dict)

    groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

# ----------------------------
# Community
# ----------------------------
class Community(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('hobbies', 'Hobbies'),
    ]
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_communities')
    is_private = models.BooleanField(default=False)
    cover_image_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

# ----------------------------
# Community Member
# ----------------------------
class CommunityMember(models.Model):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
    )
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('community', 'user')

# ----------------------------
# Event
# ----------------------------
class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('workshop', 'Workshop'),
        ('social', 'Social'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

# ----------------------------
# Event Attendee
# ----------------------------
class EventAttendee(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('event', 'user')

# ----------------------------
# Post
# ----------------------------
class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('announcement', 'Announcement'),
        ('general', 'General'),
        ('discussion', 'Discussion'),
    ]

    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, blank=True)
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='general')

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

# ----------------------------
# Virtual Session
# ----------------------------
class VirtualSession(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    meeting_link = models.URLField()
    platform = models.CharField(max_length=100)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

# ----------------------------
# Notification
# ----------------------------
class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('event_reminder', 'Event Reminder'),
        ('new_community_post', 'New Community Post'),
        ('event_invitation', 'Event Invitation'),
        ('community_join_request', 'Community Join Request'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

