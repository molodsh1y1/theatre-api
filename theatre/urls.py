from django.urls import path, include

from rest_framework.routers import DefaultRouter

from theatre.views import (
    GenreViewSet,
    ActorViewSet,
    PlayViewSet,
    TheatreHallViewSet,
    PerformanceViewSet,
    ReservationViewSet,
    TicketViewSet
)

app_name = "theatre"

router = DefaultRouter()
router.register("genres", GenreViewSet, basename="genre")
router.register("actors", ActorViewSet, basename="actor")
router.register("plays", PlayViewSet, basename="play")
router.register("theatre_halls", TheatreHallViewSet, basename="theatre_hall")
router.register("performances", PerformanceViewSet, basename="performance")
router.register("reservations", ReservationViewSet, basename="reservation")
router.register("tickets", TicketViewSet, basename="ticket")


urlpatterns = [
    path("", include(router.urls))
]
