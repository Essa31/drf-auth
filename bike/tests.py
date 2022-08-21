from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Bike


# Create your tests here.
class BikeTest(APITestCase):
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

        test_game = Bike.objects.create(
            name="test_bike",
            purchaser=test_user1,
            desc="testing bike.",
        )
        test_game.save()

    def setUp(self):
        self.client.login(username='test_user1', password="pass")

    def test_bike_model(self):
        bike = Bike.objects.get(id=1)
        actual_purchaser = str(bike.purchaser)
        actual_name = str(bike.name)
        actual_description = str(bike.desc)
        self.assertEqual(actual_purchaser, "test_user1")
        self.assertEqual(actual_name, "test_bike")
        self.assertEqual(
            actual_description, "testing bike."
        )

    def test_get_bike_list(self):
        url = reverse("bike_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        bike = response.data
        self.assertEqual(len(bike), 1)
        self.assertEqual(bike[0]["name"], "test_bike")

    def test_auth_required(self):
        self.client.logout()
        url = reverse("bike_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_only_purchaser_can_delete(self):
        self.client.logout()
        self.client.login(username='test_user2', password="pass")
        url = reverse("bike_detail", args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)