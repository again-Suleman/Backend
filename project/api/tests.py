from django.test import TestCase
from django.urls import reverse
from api.models import Order, User
from rest_framework import status


# Create your tests here.
class UserOrderTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="user1", email="test1@gmail.com")
        user2 = User.objects.create(username="user2", email="test2@gmail.com")
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)

    def test_user_order_endpoint_only_returns_authenticated_user_orders(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)
        response = self.client.get(reverse("user-orders"))

        assert response.status_code == 200

        user_orders = response.json()
        print(response.json())
        self.assertTrue(
            all(orders["user"] == user.id for orders in user_orders)
        )

    def test_user_order_endpoint_fail_for_unauthenticated_user(self):
        response = self.client.get(reverse("user-orders"))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_wrong_authenticated_user_orders(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)
        response = self.client.get(reverse("user-orders"))

        assert response.status_code == 200

        user_orders = response.json()
        # print(response.json())
        self.assertFalse(
            all(orders["user"] == user.id for orders in user_orders)
        )
