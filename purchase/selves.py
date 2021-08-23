from django.db.models import QuerySet

from fancy.viewsets import ReadOnlySelfModelViewSet, SelfModelViewSet
from purchase.models import Order, Payment, Subscribe, Product
from purchase.serializers import (
    OrderSerializer,
    PaymentSerializer,
    SubscribeSerializer,
    ProductSerializer,
)
from purchase.utils import active_subscribes, active_products


class SelfOrderViewSet(SelfModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    self_field = 'user_id'


class SelfPaymentViewSet(ReadOnlySelfModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    self_field = 'user_id'


class SelfActiveSubscribe(ReadOnlySelfModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

    def self_func(self, queryset: QuerySet, credential_id: int) -> QuerySet:
        return active_subscribes(user_id=credential_id)


class SelfActiveProduct(ReadOnlySelfModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def self_func(self, queryset: QuerySet, credential_id: int) -> QuerySet:
        return active_products(user_id=credential_id)
