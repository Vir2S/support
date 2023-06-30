from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from users.constants import Role

from tickets.models import Ticket


User = get_user_model()


class RoleIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.ADMIN


class RoleIsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.MANAGER


class RoleIsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.USER


class IsNewManager(BasePermission):
    def has_permission(self, request, view):
        new_manager_id = request.data.get("new_manager_id")
        ticket_id = request.parser_context.get("kwargs").get("pk")

        print(f"{new_manager_id = }")
        print(f"{ticket_id = }")

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
        return True

    def has_object_permission(self, request, view, obj: Ticket):
        return obj.user == request.user
