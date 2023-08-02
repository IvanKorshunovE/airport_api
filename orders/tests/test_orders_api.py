from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from flights.models import Crew, Airplane, AirplaneType, Flight
from orders.models import Order, Ticket
from routes.models import Airport, Route

ORDER_URL = reverse("orders:order-list")


def sample_airport(**params):
    defaults = {
        "name": "Boryspil",
        "closest_big_city": "Kyiv",
    }
    defaults.update(params)

    return Airport.objects.create(**defaults)


def sample_route(**params):
    airport_boryspil = sample_airport()
    airport_modlin = sample_airport(
        name="Modlin",
        closest_big_city="Warsaw",
    )

    defaults = {
        "source": airport_boryspil,
        "destination": airport_modlin,
        "distance": 1200,
    }
    defaults.update(params)

    return Route.objects.create(**defaults)


def sample_crew_member(**params):
    defaults = {
        "first_name": "John",
        "last_name": "Smith",
    }
    defaults.update(params)

    return Crew.objects.create(**defaults)


def sample_airplane_type(**params):
    defaults = {
        "name": "Airliner",
    }
    defaults.update(params)

    return AirplaneType.objects.create(**defaults)


def sample_airplane(**params):
    airliner = sample_airplane_type()
    defaults = {
        "name": "Boeing 747",
        "rows": 10,
        "seats_in_row": 4,
        "airplane_type": airliner
    }
    defaults.update(params)

    return Airplane.objects.create(**defaults)


def sample_flight(**params):
    route = sample_route()
    airplane = sample_airplane()
    departure_time = datetime.now()
    arrival_time = departure_time + timedelta(hours=2)
    defaults = {
        "route": route,
        "airplane": airplane,
        "departure_time": departure_time,
        "arrival_time": arrival_time
    }
    defaults.update(params)

    return Flight.objects.create(**defaults)


class UnauthenticatedOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ORDER_URL)
        self.assertEqual(
            res.status_code, status.HTTP_403_FORBIDDEN
        )


class AuthenticatedOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com",
            "admin",
        )
        self.client.force_authenticate(self.user)

    def test_list_orders(self):
        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        flight = sample_flight()
        payload = {
            "tickets": [
                {
                    "row": 1,
                    "seat": 1,
                    "flight": flight.pk
                }
            ]
        }
        res = self.client.post(
            ORDER_URL,
            payload,
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        order_id = res.data.get("id")
        self.assertIsNotNone(order_id)
        order = Order.objects.get(id=order_id)
        ticket = Ticket.objects.filter(order=order).first()
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.row, payload["tickets"][0]["row"])
        self.assertEqual(ticket.seat, payload["tickets"][0]["seat"])
        self.assertEqual(ticket.flight.pk, payload["tickets"][0]["flight"])

    def test_create_duplicate_ticket_order_not_allowed(self):
        """
        This test case is designed to verify that the system correctly handles
        the scenario when a user attempts to create an order with duplicate
        tickets, which should not be allowed. Duplicate tickets in an order
        mean that two or more tickets have the same combination of
        row, seat, and flight.
        """
        flight = sample_flight()
        payload = {
            "tickets": [
                {
                    "row": 1,
                    "seat": 1,
                    "flight": flight.pk
                },
                {
                    "row": 1,
                    "seat": 1,
                    "flight": flight.pk
                }
            ]
        }
        with self.assertRaises(DjangoValidationError) as e:
            self.client.post(
                ORDER_URL,
                payload,
                format="json"
            )

        actual_error = e.exception
        expected_error = {
            "__all__": [
                "Ticket with this Flight, Row and Seat already exists."
            ]
        }
        self.assertEqual(actual_error.message_dict, expected_error)

    def test_create_ticket_invalid_row_or_seat_not_allowed(self):
        """
        This test case aims to confirm that the system appropriately handles
        a scenario in which neither the order nor any tickets are created
        when attempting to create a ticket with invalid (999) values
        for the row or seat.
        """
        flight = sample_flight()
        payload = {
            "tickets": [
                {
                    "row": 999,
                    "seat": 999,
                    "flight": flight.pk
                }
            ]
        }
        initial_order_count = Order.objects.count()
        initial_ticket_count = Ticket.objects.count()
        res = self.client.post(
            ORDER_URL,
            payload,
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), initial_order_count)
        self.assertEqual(Ticket.objects.count(), initial_ticket_count)
