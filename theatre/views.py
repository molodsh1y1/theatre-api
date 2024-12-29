from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from theatre.models import (
    Genre,
    Actor,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket
)

from theatre.serializers import (
    GenreSerializer,
    ActorImageSerializer,
    ActorSerializer,
    PlaySerializer,
    PlayImageSerializer,
    PlayListSerializer,
    PlayDetailSerializer,
    TheatreHallSerializer,
    TheatreHallListSerializer,
    TheatreHallDetailSerializer,
    PerformanceSerializer,
    PerformanceListSerializer,
    PerformanceDetailSerializer,
    ReservationSerializer,
    ReservationListSerializer,
    ReservationDetailSerializer,
    TicketSerializer,
    TicketListSerializer,
    TicketDetailSerializer
)

from theatre.permissions import IsAdminOrIfAuthenticatedReadOnly
from theatre.pagination import CustomPagination


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.order_by("name")
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    pagination_class = CustomPagination


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.order_by("last_name")
    serializer_class = ActorSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "upload_image":
            return ActorImageSerializer
        return ActorSerializer

    @action(detail=True, methods=["POST"], url_path="upload-image")
    def upload_image(self, request, pk=None):
        actor = self.get_object()
        serializer = self.get_serializer(actor, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.prefetch_related("actors", "genres")
    serializer_class = PlaySerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    pagination_class = CustomPagination
    filterset_fields = ("actors", "genres")

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        if self.action == "retrieve":
            return PlayDetailSerializer
        if self.action == "upload_image":
            return PlayImageSerializer
        return PlaySerializer

    @action(detail=True, methods=["POST"], url_path="upload-image")
    def upload_image(self, request, pk=None):
        play = self.get_object()
        serializer = self.get_serializer(play, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    pagination_class = CustomPagination
    filterset_fields = ("name",)

    def get_serializer_class(self):
        if self.action == "list":
            return TheatreHallListSerializer
        if self.action == "retrieve":
            return TheatreHallDetailSerializer
        return TheatreHallSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("play", "theatre_hall")
    serializer_class = PerformanceSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    pagination_class = CustomPagination
    filterset_fields = ("play", "theatre_hall", "show_time")

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        return PerformanceSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.select_related("user")

        if self.action == "list":
            return queryset.prefetch_related("tickets")

        if self.action == "retrieve":
            return queryset.prefetch_related(
                "tickets__performance__play__actors",
                "tickets__performance__play__genres",
                "tickets__performance__theatre_hall"
            )

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        if self.action == "retrieve":
            return ReservationDetailSerializer
        return ReservationSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            "performance__play",
            "performance__theatre_hall",
            "reservation",
        )

        return queryset.filter(reservation__user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        if self.action == "retrieve":
            return TicketDetailSerializer
        return TicketSerializer
