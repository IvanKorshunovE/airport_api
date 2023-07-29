from rest_framework import serializers

from routes.models import Airport, Route


# class AirportSerializer(serializers.ModelSerializer):
#     destination_names = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Airport
#         fields = (
#             "id",
#             "name",
#             "closest_big_city",
#             "destination_names"
#         )
#
#     def get_destination_names(self, obj):
#         return obj.get_destination_names()


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
