from fancy.viewsets import FancySelfViewSet

from purchase.models import Order, Payment
from purchase.serializers import (
    OrderSerializer,
    PaymentSerializer,
)


class SelfOrderViewSet(FancySelfViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    self_field = 'user_id'


class SelfPaymentViewSet(FancySelfViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    self_field = 'user_id'
