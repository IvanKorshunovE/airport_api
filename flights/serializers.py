from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from flights.models import (
    Flight, Airplane, Crew, AirplaneType
)
from orders.models import Ticket
from routes.serializers import RouteReadSerializer


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = "__all__"


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = "__all__"


class DefaultFlightSerializer(serializers.ModelSerializer):
    route = RouteReadSerializer()

    class Meta:
        model = Flight
        fields = "__all__"


class FlightReadSerializer(serializers.ModelSerializer):
    route = RouteReadSerializer()
    tickets_available = serializers.IntegerField()

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "tickets_available"
        )


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")

    def validate(self, attrs):
        data = super().validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            ValidationError
        )
        return data


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class FlightDetailSerializer(DefaultFlightSerializer):
    route = RouteReadSerializer(many=False, read_only=True)
    airplane = AirplaneSerializer(many=False, read_only=True)
    taken_places = TicketSeatsSerializer(
        source="tickets", many=True, read_only=True
    )

    class Meta:
        model = Flight
        fields = (
            "id",
            "departure_time",
            "arrival_time",
            "route",
            "airplane",
            "taken_places"
        )


class FlightCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
        )
