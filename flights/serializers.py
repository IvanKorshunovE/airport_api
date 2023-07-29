from rest_framework import serializers

from flights.models import Flight
from routes.serializers import RouteReadSerializer


class FlightReadSerializer(serializers.ModelSerializer):
    route = RouteReadSerializer()

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
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
