from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tickets.models import Ticket
from tickets.permissions import IsOwner, RoleIsAdmin, RoleIsManager, RoleIsUser
from tickets.serializers import TicketAssignSerializer, TicketSerializer


class TicketAPIViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

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
            case _:
                permission_classes = []

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"])
    def take(self, request, pk):
        ticket = self.get_object()

        if ticket.manager and ticket.manager_id != request.user.id:
            raise PermissionError("This ticket is already taken")

        serializer = TicketAssignSerializer(
            data={"manager_id": request.user.id}
        )
        serializer.is_valid()
        ticket = serializer.assign(ticket)

        return Response(TicketSerializer(ticket).data)
