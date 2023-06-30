from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tickets.models import Message, Ticket
from tickets.permissions import (
    IsOwner,
    RoleIsAdmin,
    RoleIsManager,
    RoleIsUser,
    IsNewManager,
)
from tickets.serializers import (
    MessageSerializer,
    TicketAssignSerializer,
    TicketSerializer,
)
from users.constants import Role


User = get_user_model()


class TicketAPIViewSet(ModelViewSet):
    serializer_class = TicketSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == Role.ADMIN:
            return Ticket.objects.all()

        if user.role == Role.MANAGER:
            return Ticket.objects.filter(Q(manager_id=user.id) | Q(manager_id=None))

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
                permission_classes = [RoleIsAdmin, IsNewManager]
            case _:
                permission_classes = []

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["put"])
    def take(self, request, pk):
        ticket = self.get_object()

        if ticket.manager_id and ticket.manager_id == request.user.id:
            raise PermissionDenied("This ticket is already taken", 403)

        serializer = TicketAssignSerializer(data={"manager_id": request.user.id})
        serializer.is_valid()
        ticket = serializer.assign(ticket)

        return Response(TicketSerializer(ticket).data)

    @action(detail=True, methods=["put"])
    def reassign(self, request, pk):
        ticket = self.get_object()
        new_manager_id = request.data.get("new_manager_id")

        serializer = TicketAssignSerializer(data={"manager_id": new_manager_id})
        serializer.is_valid()
        ticket = serializer.assign(ticket)

        return Response(TicketSerializer(ticket).data)


class MessageListCreateAPIView(ListCreateAPIView):
    serializer_class = MessageSerializer
    lookup_field = "ticket_id"

    def get_queryset(self):
        messages = Message.objects.filter(
            Q(ticket__user=self.request.user) | Q(ticket__manager=self.request.user),
            ticket_id=self.kwargs[self.lookup_field],
        )

        if not messages:
            raise Http404

        return messages

    @staticmethod
    def get_ticket(user: User, ticket_id: int) -> Ticket:
        """Get tickets for current user."""

        tickets = Ticket.objects.filter(Q(user=user) | Q(manager=user))
        return get_object_or_404(tickets, id=ticket_id)

    def post(self, request, ticket_id: int):
        ticket = self.get_ticket(request.user, ticket_id)
        payload = {
            "text": request.data["text"],
            "ticket": ticket_id,
        }
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=201, headers=headers)
