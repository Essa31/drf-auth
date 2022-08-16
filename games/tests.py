from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Game


# Create your tests here.
class GameTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = get_user_model().objects.create_user(
            username="test_user1", password="pass"
        )
        test_user1.save()

        test_user2 = get_user_model().objects.create_user(
            username="test_user2", password="pass"
        )
        test_user1.save()

        test_game = Game.objects.create(
            name="test_game",
            purchaser=test_user1,
            desc="testing game.",
        )
        test_game.save()

    def setUp(self):
        self.client.login(username='test_user1', password="pass")

    def test_games_model(self):
        game = Game.objects.get(id=1)
        actual_purchaser = str(game.purchaser)
        actual_name = str(game.name)
        actual_description = str(game.desc)
        self.assertEqual(actual_purchaser, "test_user1")
        self.assertEqual(actual_name, "test_game")
        self.assertEqual(
            actual_description, "testing game."
        )

    def test_get_games_list(self):
        url = reverse("games_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        games = response.data
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0]["name"], "test_game")

    def test_auth_required(self):
        self.client.logout()
        url = reverse("games_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_purchaser_can_delete(self):
        self.client.logout()
        self.client.login(username='test_user2', password="pass")
        url = reverse("games_detail", args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)