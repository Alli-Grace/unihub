from rest_framework import serializers
from .models import (User, Community, CommunityMember, Event, EventAttendee, Post, VirtualSession, Notification)
from rest_framework.validators import ValidationError, UniqueValidator
from django.contrib.auth.password_validation import validate_password


class AdminSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
       }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['role'] = 'admin'  # Force admin role
        validated_data['is_staff'] = True
        
        user = User.objects.create_user(**validated_data)
        return user

# ----------------------------
# User Serializer
# ----------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'password', 'confirm_password', 'role'
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

class LimitedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


# ----------------------------
# User Profile Serializer
# ----------------------------
class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'password', 'confirm_password', 'role',
            'avatar_url', 'major', 'year', 'department', 'position', 'bio',
            'interests', 'social_links', 'privacy_settings', 'notification_preferences',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'email']  # Email usually shouldn't be editable

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    # confirm_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError("Old password is incorrect")
        return value


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

