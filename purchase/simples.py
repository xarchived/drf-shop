from fancy.serializers import CommonFieldsSerializer
from purchase.models import Product, Order, Payment, Price


class SimpleProductSerializer(CommonFieldsSerializer):
    class Meta:
        model = Product
        fields = [
            *CommonFieldsSerializer.Meta.fields,
            'name',
        ]


class SimplePriceSerializer(CommonFieldsSerializer):
    class Meta:
        model = Price
        fields = [
            *CommonFieldsSerializer.Meta.fields,
            'product_id',
            'amount',
        ]


class SimpleOrderSerializer(CommonFieldsSerializer):
    class Meta:
        model = Order
        fields = [
            *CommonFieldsSerializer.Meta.fields,
            'user_id',
            'duration',
        ]


class SimplePaymentSerializer(CommonFieldsSerializer):
    class Meta:
        model = Payment
        fields = [
            *CommonFieldsSerializer.Meta.fields,
            'order_id',
        ]
