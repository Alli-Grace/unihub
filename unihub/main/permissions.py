from rest_framework.permissions import BasePermission
from .models import User
from rest_framework import permissions
# importing modules
from django.contrib.auth.models import Group, User, Permission
# from django.contrib.contenttypes import 
from django.shortcuts import get_object_or_404

class IsAdmin(BasePermission):
    # Allow access to admin user only
    message = "You are not authorized to perform this action"

    def has_permission(self, request, view): 
        if request.user.is_authenticated and request.user.is_admin:
            return True
        return False
    