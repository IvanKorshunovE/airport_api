from rest_framework import serializers

from flights.models import Flight
from routes.serializers import RouteReadSerializer


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
