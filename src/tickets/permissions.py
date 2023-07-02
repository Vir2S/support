from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from users.constants import Role

from tickets.models import Ticket


User = get_user_model()


def user_is_anonymous(user):
    if isinstance(user, AnonymousUser):
        raise PermissionDenied("Forbidden")


class RoleIsAdmin(BasePermission):
    def has_permission(self, request, view):
        user_is_anonymous(user=request.user)
        return request.user.role == Role.ADMIN


class RoleIsManager(BasePermission):
    def has_permission(self, request, view):
        user_is_anonymous(user=request.user)
        return request.user.role == Role.MANAGER


class RoleIsUser(BasePermission):
    def has_permission(self, request, view):
        user_is_anonymous(user=request.user)
        return request.user.role == Role.USER


class IsNewManager(BasePermission):
    def has_permission(self, request, view):
        user_is_anonymous(user=request.user)
        new_manager_id = request.data.get("new_manager_id")
        ticket_id = request.parser_context.get("kwargs").get("pk")

        try:
            ticket = Ticket.objects.get(id=ticket_id)
            user = User.objects.get(id=new_manager_id)
        except (Ticket.DoesNotExist, User.DoesNotExist):
            raise PermissionDenied("Invalid ticket or user.")

        if user.role != Role.MANAGER:
            raise PermissionDenied("User is not a manager.")

        if ticket.manager_id == new_manager_id:
            raise PermissionDenied("Cannot assign current manager as the new manager.")

        return True


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        user_is_anonymous(user=request.user)
        return True

    def has_object_permission(self, request, view, obj: Ticket):
        return obj.user == request.user
