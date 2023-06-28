from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tickets.models import Ticket
from tickets.permissions import IsOwner, RoleIsAdmin, RoleIsManager, RoleIsUser
from tickets.serializers import TicketAssignSerializer, TicketSerializer
from users.constants import Role

User = get_user_model()


class TicketAPIViewSet(ModelViewSet):
    serializer_class = TicketSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == Role.ADMIN:
            return Ticket.objects.all()

        if user.role == Role.MANAGER:
            Ticket.objects.filter(Q(manager=user) | Q(manager=None))

        return Ticket.objects.filter(user=user)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions
        that this view requires.
        """
        match self.action:
            case "list":
                permission_classes = [RoleIsAdmin | RoleIsManager | RoleIsUser]
            case "create":
                permission_classes = [RoleIsUser]
            case "retrieve":
                permission_classes = [IsOwner | RoleIsAdmin | RoleIsManager]
            case "update":
                permission_classes = [RoleIsAdmin | RoleIsManager]
            case "destroy":
                permission_classes = [RoleIsAdmin | RoleIsManager]
            case "take":
                permission_classes = [RoleIsManager]
            case "reassign":
                permission_classes = [RoleIsAdmin]
            case _:
                permission_classes = []

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["put"])
    def take(self, request, pk):
        ticket = self.get_object()

        if ticket.manager and ticket.manager_id != request.user.id:
            raise PermissionError("This ticket is already taken")

        serializer = TicketAssignSerializer(data={"manager_id": request.user.id})
        serializer.is_valid()
        ticket = serializer.assign(ticket)

        return Response(TicketSerializer(ticket).data)

    @action(detail=True, methods=["put"])
    def reassign(self, request, pk):
        if request.user.role != Role.ADMIN:
            raise PermissionDenied(
                "You don't have permission to reassign the ticket.", 403
            )

        ticket = self.get_object()

        manager_id = request.data.get("manager_id")
        if manager_id is None:
            return Response({"error": "You have to add manager_id in request"}, 400)

        if manager_id and User.objects.filter(id=manager_id).role == Role.MANAGER:
            serializer = TicketAssignSerializer(data={"manager_id": manager_id})
            serializer.is_valid()
            ticket = serializer.assign(ticket)

            return Response(TicketSerializer(ticket).data)

        return Response({"error": "Bad request"}, 400)


class MessageListCreateAPIView(ListCreateAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        # TODO: Start from here
        raise NotImplementedError
