from datetime import timedelta

from django.db.models import F, Q
from django.utils import timezone

from fancy.decorators import queryset_credential_handler
from fancy.viewsets import FancySelfViewSet, FancyViewSet
from purchase.models import Order, Payment, Subscribe
from purchase.serializers import (
    OrderSerializer,
    PaymentSerializer,
    SubscribeSerializer,
)


class SelfOrderViewSet(FancySelfViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    self_field = 'user_id'


class SelfPaymentViewSet(FancySelfViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    self_field = 'user_id'


class SelfPurchasedSubscribe(FancyViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

    @queryset_credential_handler
    def get_queryset(self):
        return super().get_queryset().filter(
            Q(inserted_at__gt=timezone.now() - timedelta(days=1) * F('duration')) &
            Q(orders__payments__ref_id__isnull=False) &
            (
                    Q(orders__user_id=self.credential['id']) |
                    Q(orders__user__children__id=self.credential['id'])
            )
        )
