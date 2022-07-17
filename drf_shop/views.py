from rest_framework.viewsets import ModelViewSet

from drf_shop.models import (
    Currency,
    Order,
    OrderProduct,
    Payment,
    Price,
    Product,
    Rate,
    Shop,
)
from drf_shop.serializers import (
    CurrencySerializer,
    OrderProductSerializer,
    OrderSerializer,
    PaymentSerializer,
    PriceSerializer,
    ProductSerializer,
    RateSerializer,
    ShopSerializer,
)


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CurrencyViewSet(ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class RateViewSet(ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class PriceViewSet(ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderProductViewSet(ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
