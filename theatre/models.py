from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.conf import settings

from theatre.path_utils import create_custom_path


class Genre(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    photo = models.ImageField(
        upload_to=create_custom_path,
        null=True,
        blank=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["last_name", "first_name"]),
            models.Index(fields=["first_name"], name="first_name_idx"),
            models.Index(fields=["last_name"], name="last_name_idx")
        ]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Play(models.Model):
    title = models.CharField(max_length=63)
    description = models.TextField(null=True, blank=True)
    actors = models.ManyToManyField(Actor, related_name="plays")
    genres = models.ManyToManyField(Genre, related_name="plays")
    poster = models.ImageField(
        upload_to=create_custom_path,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class TheatreHall(models.Model):
    name = models.CharField(max_length=63, unique=True)
    rows = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    seats_in_row = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"Theater: {self.rows} rows, {self.seats_in_row} seats per row"


class Performance(models.Model):
    play = models.ForeignKey(
        Play,
        on_delete=models.CASCADE,
        related_name="performance"
    )
    theatre_hall = models.ForeignKey(
        TheatreHall,
        on_delete=models.CASCADE,
        related_name="performance"
    )
    show_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (
            f"Performance of {self.play.title} at {self.theatre_hall.name}"
            f" on {self.show_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    def __str__(self) -> str:
        user_full_name = (
            f"{self.user.first_name} "
            f"{self.user.last_name}"
        ).strip()
        formatted_created_at = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return f"Reserver {user_full_name} at {formatted_created_at}"


class Ticket(models.Model):
    row = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    seat = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    class Meta:
        unique_together = ["row", "seat", "performance"]

    def __str__(self) -> str:
        return f"Row: {self.row}" f"Seat: {self.seat}"
