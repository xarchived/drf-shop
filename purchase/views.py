from rest_framework.viewsets import ModelViewSet

from purchase.models import Product, Order, Payment, Price, Package, Subscribe
from purchase.serializers import (
    ProductSerializer,
    OrderSerializer,
    PaymentSerializer,
    PriceSerializer,
    PackageSerializer,
    SubscribeSerializer, SubscribeOrderSerializer,
)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PriceViewSet(ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class PackageViewSet(ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class SubscribeViewSet(ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class SubscribeOrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = SubscribeOrderSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
