from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import BaseRouter

from drf_shop.settings import DEBUG
from drf_shop.views import (
    CurrencyViewSet,
    OrderProductViewSet,
    OrderViewSet,
    PaymentViewSet,
    PriceViewSet,
    ProductViewSet,
    RateViewSet,
    ShopViewSet,
)

router: BaseRouter
if DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(r"_shops", ShopViewSet)
router.register(r"_products", ProductViewSet)
router.register(r"_currencies", CurrencyViewSet)
router.register(r"_rates", RateViewSet)
router.register(r"_prices", PriceViewSet)
router.register(r"_orders", OrderViewSet)
router.register(r"_order_products", OrderProductViewSet)
router.register(r"_payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
