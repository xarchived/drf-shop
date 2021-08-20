from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from fancy.decorators import queryset_credential_handler
from fancy.views import SelfAPIView, CredentialAPIView
from purchase.models import Order, Payment, Subscribe, Product
from purchase.serializers import (
    OrderSerializer,
    PaymentSerializer,
    SubscribeSerializer,
    ProductSerializer,
)
from purchase.utils import active_subscribes, active_products


class SelfOrderViewSet(ReadOnlyModelViewSet, SelfAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    self_field = 'user_id'


class SelfPaymentViewSet(ReadOnlyModelViewSet, SelfAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    self_field = 'user_id'


class SelfActiveSubscribe(ReadOnlyModelViewSet, CredentialAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

    @queryset_credential_handler
    def get_queryset(self):
        return active_subscribes(user_id=self.credential['id'])


class SelfActiveProduct(ReadOnlyModelViewSet, CredentialAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @queryset_credential_handler
    def get_queryset(self):
        return active_products(user_id=self.credential['id'])
