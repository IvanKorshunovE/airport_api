from django.contrib import admin

from flights.models import (
    Crew,
    AirplaneType,
    Airplane,
    Flight
)

admin.site.register(Crew)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Flight)
