from fancy.decorators import queryset_credential_handler
from fancy.viewsets import FancySelfViewSet, FancyViewSet
from purchase.models import Order, Payment, Subscribe
from purchase.serializers import (
    OrderSerializer,
    PaymentSerializer,
    SubscribeSerializer,
)
from purchase.utils import get_active_subscribes


class SelfOrderViewSet(FancySelfViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    self_field = 'user_id'


class SelfPaymentViewSet(FancySelfViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    self_field = 'user_id'


class SelfActiveSubscribe(FancyViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

    @queryset_credential_handler
    def get_queryset(self):
        return get_active_subscribes(user_id=self.credential['id'])
