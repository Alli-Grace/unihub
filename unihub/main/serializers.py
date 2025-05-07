from rest_framework import serializers
from .models import (
    User, Community, CommunityMember, Event, EventAttendee,
    Post, VirtualSession, Notification
)
from django.contrib.auth.password_validation import validate_password


# ----------------------------
# User Serializer
# ----------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'password', 'confirm_password', 'role',
            'avatar_url', 'major', 'year', 'department', 'position', 'bio',
            'interests', 'social_links', 'privacy_settings', 'notification_preferences',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


# ----------------------------
# Community Serializer
# ----------------------------
class CommunitySerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Community
        fields = [
            'id', 'name', 'description', 'category', 'creator',
            'is_private', 'cover_image_url', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ----------------------------
# Community Member Serializer
# ----------------------------
class CommunityMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CommunityMember
        fields = ['id', 'community', 'user', 'role', 'joined_at']
        read_only_fields = ['joined_at']


# ----------------------------
# Event Serializer
# ----------------------------
class EventSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    community = CommunitySerializer(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'date_time', 'location',
            'type', 'creator', 'community', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ----------------------------
# Event Attendee Serializer
# ----------------------------
class EventAttendeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EventAttendee
        fields = ['id', 'event', 'user', 'attended_at']


# ----------------------------
# Post Serializer
# ----------------------------
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    community = CommunitySerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 'community',
            'post_type', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ----------------------------
# Virtual Session Serializer
# ----------------------------
class VirtualSessionSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    community = CommunitySerializer(read_only=True)

    class Meta:
        model = VirtualSession
        fields = [
            'id', 'title', 'description', 'organizer', 'community',
            'start_datetime', 'end_datetime', 'meeting_link', 'platform',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ----------------------------
# Notification Serializer
# ----------------------------
class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'type', 'message', 'link',
            'is_read', 'created_at'
        ]
        read_only_fields = ['created_at']

