from django.db import transaction
from rest_framework import serializers

from flights.serializers import FlightReadSerializer
from orders.models import Order, Ticket


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class TicketListSerializer(TicketSerializer):
    flight = FlightReadSerializer(many=False, read_only=True)


# class TicketSeatsSerializer(TicketSerializer):
#     class Meta:
#         model = Ticket
#         fields = ("row", "seat")


class OrderCreateSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = (
            "id",
            "tickets",
            "created_at",
        )

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderCreateSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
