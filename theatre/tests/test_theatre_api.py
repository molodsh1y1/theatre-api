import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import Actor, Genre, Performance, Play, TheatreHall
from theatre.serializers import (
    ActorSerializer,
    GenreSerializer,
    PlayDetailSerializer,
    PlayListSerializer,
)


GENRE_URL = reverse("theatre:genre-list")
ACTOR_URL = reverse("theatre:actor-list")
PLAY_URL = reverse("theatre:play-list")
THEATRE_HALL_URL = reverse("theatre:theatre_hall-list")
PERFORMANCE_URL = reverse("theatre:performance-list")
RESERVATION_URL = reverse("theatre:reservation-list")
TICKET_URL = reverse("theatre:ticket-list")


def sample_genre(**params):
    defaults = {"name": f"Sample genre_{uuid.uuid4()}"}
    defaults.update(params)
    return Genre.objects.create(**defaults)


def sample_actor(**params):
    defaults = {"first_name": "Sample", "last_name": "Actor"}
    defaults.update(params)
    return Actor.objects.create(**defaults)


def sample_play(**params):
    defaults = {"title": "Sample play", "description": "Sample description"}
    defaults.update(params)
    return Play.objects.create(**defaults)


def sample_theatre_hall(**params):
    defaults = {
        "name": f"Sample hall_{uuid.uuid4()}",
        "rows": 10, "seats_in_row": 10
    }
    defaults.update(params)
    return TheatreHall.objects.create(**defaults)


def sample_performance(**params):
    play = sample_play()
    theatre_hall = sample_theatre_hall()
    defaults = {
        "play": play,
        "theatre_hall": theatre_hall,
        "show_time": "2022-06-02 14:00:00"
    }
    defaults.update(params)
    return Performance.objects.create(**defaults)


def sample_reservation(**params):
    return {
        "tickets": [
            {"row": 1, "seat": 1, "performance": sample_performance().id},
            {"row": 1, "seat": 2, "performance": sample_performance().id},
        ]
    }


class UnauthenticatedApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(GENRE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_list_genres(self):
        sample_genre()
        sample_genre()

        res = self.client.get(GENRE_URL)

        genres = Genre.objects.order_by("name")
        serializer = GenreSerializer(genres, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_list_actors(self):
        sample_actor()
        sample_actor()

        res = self.client.get(ACTOR_URL)

        actors = Actor.objects.order_by("id")
        serializer = ActorSerializer(actors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_list_plays(self):
        sample_play()
        sample_play()

        res = self.client.get(PLAY_URL)

        plays = Play.objects.order_by("title")
        serializer = PlayListSerializer(plays, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)
        self.assertEqual(res.data["count"], plays.count())

    def test_filter_plays_by_genres(self):
        genre1 = sample_genre(name="Genre 1")
        genre2 = sample_genre(name="Genre 2")

        play1 = sample_play(title="Play 1")
        play2 = sample_play(title="Play 2")

        play1.genres.add(genre1)
        play2.genres.add(genre2)

        play3 = sample_play(title="Play without genres")

        res = self.client.get(PLAY_URL, {"genres": [genre1.id, genre2.id]})

        play_data = [
            dict(PlayListSerializer(play1).data),
            dict(PlayListSerializer(play2).data),
            dict(PlayListSerializer(play3).data)
        ]

        res_data = [dict(item) for item in res.data["results"]]

        for data in play_data[:2]:
            self.assertIn(data, res_data)

        self.assertNotIn(play_data[2], res_data)

    def test_filter_plays_by_actors(self):
        actor1 = sample_actor(first_name="Actor 1", last_name="Last 1")
        actor2 = sample_actor(first_name="Actor 2", last_name="Last 2")

        play1 = sample_play(title="Play 1")
        play2 = sample_play(title="Play 2")

        play1.actors.add(actor1)
        play2.actors.add(actor2)

        play3 = sample_play(title="Play without actors")

        res = self.client.get(PLAY_URL, {"actors": [actor1.id, actor2.id]})

        serializer1 = PlayListSerializer(play1)
        serializer2 = PlayListSerializer(play2)
        serializer3 = PlayListSerializer(play3)

        res_data = [
            dict(item)
            for item in res.data["results"]
        ]

        self.assertIn(dict(serializer1.data), res_data)
        self.assertIn(dict(serializer2.data), res_data)
        self.assertNotIn(dict(serializer3.data), res_data)

    def test_retrieve_play_detail(self):
        play = sample_play()
        play.genres.add(sample_genre())
        play.actors.add(sample_actor())

        url = reverse("theatre:play-detail", args=[play.id])
        res = self.client.get(url)

        serializer = PlayDetailSerializer(play)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_reservation_forbidden(self):
        self.client.force_authenticate(user=None)
        payload = sample_reservation()
        res = self.client.post(RESERVATION_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_empty_genres(self):
        res = self.client.get(GENRE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], [])

    def test_empty_actors(self):
        res = self.client.get(ACTOR_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], [])

    def test_empty_plays(self):
        res = self.client.get(PLAY_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], [])

    def test_pagination(self):
        for _ in range(20):
            sample_play()

        res = self.client.get(PLAY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 10)
        self.assertIn("next", res.data)
        self.assertIn("previous", res.data)


class AdminApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="adminpass",
            is_staff=True,
            is_superuser=True
        )
        self.client.force_authenticate(self.admin_user)

    def test_upload_image_for_actor(self):
        actor = sample_actor()
        url = reverse("theatre:actor-upload-image", args=[actor.id])
        with open("theatre/tests/sample.jpg", "rb") as image:
            res = self.client.post(url, {"photo": image}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("photo", res.data)

    def test_upload_image_for_play(self):
        play = sample_play()
        url = reverse("theatre:play-upload-image", args=[play.id])
        with open("theatre/tests/sample.jpg", "rb") as image:
            res = self.client.post(url, {"poster": image}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("poster", res.data)


class ForbiddenApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_genre_forbidden(self):
        res = self.client.post(GENRE_URL, {"name": "Genre name"})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_actor_forbidden(self):
        res = self.client.post(ACTOR_URL, {"first_name": "First", "last_name": "Last"})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_play_forbidden(self):
        res = self.client.post(PLAY_URL, {"title": "Play title"})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_theatre_hall_forbidden(self):
        res = self.client.post(THEATRE_HALL_URL, {"name": "Theatre hall name", "rows": 10, "seats_in_row": 10})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_performance_forbidden(self):
        res = self.client.post(PERFORMANCE_URL, {"play": 1, "theatre_hall": 1, "show_time": "2022-06-02 14:00:00"})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_reservation_forbidden(self):
        res = self.client.post(RESERVATION_URL, {"tickets": [{"row": 1, "seat": 1, "performance": 1}]})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_ticket_forbidden(self):
        res = self.client.post(TICKET_URL, {"row": 1, "seat": 1, "performance": 1, "reservation": 1})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
