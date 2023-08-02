from datetime import datetime
from unittest import TestCase

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from flights.models import Flight, Airplane
from flights.serializers import FlightReadSerializer
from orders.tests.test_orders_api import (
    sample_flight,
    sample_airport
)
from routes.models import Route

FLIGHT_URL = reverse("flights:flight-list")


class UnauthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(FLIGHT_URL)
        self.assertEqual(
            res.status_code, status.HTTP_403_FORBIDDEN
        )


@pytest.mark.django_db
class AuthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com",
            "admin",
        )
        self.superuser = get_user_model().objects.create_superuser(
            "superadmin@admin.com",
            "super_admin",
        )
        self.client.force_authenticate(self.user)
        self.date_1 = datetime(2023, 8, 1, 12, 0, 0)
        self.date_2 = datetime(2023, 8, 2, 12, 0, 0)
        self.flight_1 = sample_flight(
            departure_time=self.date_1
        )
        self.flight_1.tickets_available = 40

    def test_list_flights(self):
        res = self.client.get(FLIGHT_URL)
        self.assertEqual(
            res.status_code, status.HTTP_200_OK
        )

    def test_filter_flights_by_date(self):
        flight_2 = Flight.objects.create(
            route=Route.objects.first(),
            airplane=Airplane.objects.first(),
            departure_time=self.date_2,
            arrival_time=self.date_2
        )
        flight_2.tickets_available = 40

        date_param = "2023-08-01"
        response = self.client.get(
            FLIGHT_URL, {"date": date_param}
        )
        serializer_flight_1 = FlightReadSerializer(
            self.flight_1
        )
        serializer_flight_2 = FlightReadSerializer(
            flight_2
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertIn(
            serializer_flight_1.data, response.data
        )
        self.assertNotIn(
            serializer_flight_2.data, response.data
        )

    def test_filter_flights_by_route_id(self):
        airport_fiumicino = sample_airport(
            name="Fiumicino",
            closest_big_city="Rome",
        )
        airport_brandenburg = sample_airport(
            name="Brandenburg",
            closest_big_city="Berlin",
        )
        route_two = Route.objects.create(
            source=airport_fiumicino,
            destination=airport_brandenburg,
            distance=2200
        )
        flight_2 = Flight.objects.create(
            route=route_two,
            airplane=Airplane.objects.first(),
            departure_time=self.date_2,
            arrival_time=self.date_2
        )
        flight_2.tickets_available = 40

        route_id_str = route_two.id
        response = self.client.get(
            FLIGHT_URL, {"route": route_id_str}
        )
        serializer_flight_1 = FlightReadSerializer(
            self.flight_1
        )
        serializer_flight_2 = FlightReadSerializer(
            flight_2
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertIn(
            serializer_flight_2.data, response.data
        )
        self.assertNotIn(
            serializer_flight_1.data, response.data
        )

    def test_create_flight_for_simple_user_forbidden(self):
        route = Route.objects.first()
        airplane = Airplane.objects.first()
        payload = {
            "route_id": route.id,
            "airplane_id": airplane.id,
            "departure_time": "2023-08-01T16:47:46Z",
            "arrival_time": "2023-08-01T17:47:46Z",
        }

        res = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_flight_for_superuser_user_allowed(self):
        self.client.force_authenticate(self.superuser)
        route = Route.objects.first()
        airplane = Airplane.objects.first()
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": "2023-08-01T16:47:46Z",
            "arrival_time": "2023-08-01T17:47:46Z",
        }

        res = self.client.post(FLIGHT_URL, payload)

        flight = Flight.objects.filter(
            departure_time="2023-08-01T16:47:46Z"
        )
        self.assertEqual(
            res.status_code, status.HTTP_201_CREATED
        )
        self.assertTrue(
            flight.exists()
        )
