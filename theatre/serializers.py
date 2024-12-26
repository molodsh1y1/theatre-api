from rest_framework import serializers

from theatre.models import (
    Genre,
    Actor,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket
)

from accounts.serializers import UserSerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title", "description", "actors", "genres")


class PlayListSerializer(PlaySerializer):
    genres = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    actors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )

    class Meta:
        model = Play
        fields = ("id", "title", "actors", "genres")
        read_only_fields = fields


class PlayDetailSerializer(PlaySerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = ("id", "title", "description", "actors", "genres")
        read_only_fields = fields


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row")


class TheatreHallListSerializer(TheatreHallSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name")
        read_only_fields = fields


class TheatreHallDetailSerializer(TheatreHallSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row")
        read_only_fields = fields


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")


class PerformanceListSerializer(PerformanceSerializer):
    play_title = serializers.SlugRelatedField(
        slug_field="title", read_only=True, source="play"
    )
    theatre_hall_name = serializers.SlugRelatedField(
        slug_field="name", read_only=True, source="theatre_hall"
    )

    class Meta:
        model = Performance
        fields = ("id", "play_title", "theatre_hall_name", "show_time")
        read_only_fields = fields


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlaySerializer(read_only=True)
    theatre_hall = TheatreHallSerializer(read_only=True)

    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")
        read_only_fields = fields


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")


class ReservationListSerializer(ReservationSerializer):
    user_email = serializers.SlugRelatedField(
        slug_field="email", read_only=True, source="user"
    )

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user_email")
        read_only_fields = fields


class ReservationDetailSerializer(ReservationSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")
        read_only_fields = fields


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance", "reservation")


class TicketListSerializer(TicketSerializer):
    performance = PerformanceListSerializer(read_only=True)
    reservation = ReservationListSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance", "reservation")
        read_only_fields = fields


class TicketDetailSerializer(TicketSerializer):
    performance = PerformanceSerializer(read_only=True)
    reservation = ReservationSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance", "reservation")
        read_only_fields = fields
