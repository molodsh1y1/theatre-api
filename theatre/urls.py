from django.urls import include, path
from rest_framework.routers import DefaultRouter

from theatre.views import (
    ActorViewSet,
    GenreViewSet,
    PerformanceViewSet,
    PlayViewSet,
    ReservationViewSet,
    TheatreHallViewSet,
    TicketViewSet,
)


app_name = "theatre"

router = DefaultRouter()
router.register("genres", GenreViewSet, basename="genre")
router.register("actors", ActorViewSet, basename="actor")
router.register("plays", PlayViewSet, basename="play")
router.register("theatre-halls", TheatreHallViewSet, basename="theatre_hall")
router.register("performances", PerformanceViewSet, basename="performance")
router.register("reservations", ReservationViewSet, basename="reservation")
router.register("tickets", TicketViewSet, basename="ticket")


urlpatterns = router.urls
