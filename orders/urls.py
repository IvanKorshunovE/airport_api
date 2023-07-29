from rest_framework import routers

from orders.views import OrderViewSet

router = routers.DefaultRouter()

router.register("orders", OrderViewSet)

urlpatterns = router.urls

app_name = "orders"
