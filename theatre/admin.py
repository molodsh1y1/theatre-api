from django.contrib import admin

from theatre.models import (
    Actor,
    Genre,
    Performance,
    Play,
    Reservation,
    TheatreHall,
    Ticket,
)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    list_filter = ("last_name",)


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "get_actors", "get_genres")
    list_filter = ("title", "actors", "genres")

    def get_actors(self, obj) -> str:
        return ", ".join([actor.__str__() for actor in obj.actors.all()[:3]])
    get_actors.short_description = "Actors"

    def get_genres(self, obj) -> str:
        return ", ".join([genre.name for genre in obj.genres.all()[:3]])
    get_genres.short_description = "Genres"


@admin.register(TheatreHall)
class TheatreHallAdmin(admin.ModelAdmin):
    list_display = ("name", "rows", "seats_in_row")
    list_filter = ("name",)


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ("play", "theatre_hall", "show_time")
    list_filter = ("show_time", "theatre_hall")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    list_filter = ("user", "created_at")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("row", "seat", "performance", "reservation")
    list_filter = ("performance", "reservation")
