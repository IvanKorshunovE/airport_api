from rest_framework import serializers

from routes.models import Airport, Route


class AirportRouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = (
            "id",
            "name",
            "closest_big_city",
        )


class RouteReadSerializer(serializers.ModelSerializer):
    source = AirportRouteSerializer()
    destination = AirportRouteSerializer()

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class AirportImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = ("id", "image")
