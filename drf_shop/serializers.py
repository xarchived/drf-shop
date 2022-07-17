from drf_manipulation.serializers import ManipulationSerializerMixin
from rest_framework.serializers import ModelSerializer

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


class BaseSerializer(ModelSerializer, ManipulationSerializerMixin):
    class Meta:
        fields = [
            *ManipulationSerializerMixin.Meta.fields,
            "id",
        ]


class ShopSerializer(BaseSerializer):
    class Meta:
        model = Shop
        fields = [
            *BaseSerializer.Meta.fields,
            "name",
            "owner",
        ]


class ProductSerializer(BaseSerializer):
    class Meta:
        model = Product
        fields = [
            *BaseSerializer.Meta.fields,
            "name",
        ]


class CurrencySerializer(BaseSerializer):
    class Meta:
        model = Currency
        fields = [
            *BaseSerializer.Meta.fields,
            "name",
        ]


class RateSerializer(BaseSerializer):
    class Meta:
        model = Rate
        fields = [
            *BaseSerializer.Meta.fields,
            "base",
            "quote",
            "rate",
        ]


class PriceSerializer(BaseSerializer):
    class Meta:
        model = Price
        fields = [
            *BaseSerializer.Meta.fields,
            "amount",
            "currency",
            "product",
        ]


class OrderSerializer(BaseSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            *BaseSerializer.Meta.fields,
            "buyer",
            "products",
        ]


class OrderProductSerializer(ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = [
            "id",
            "order",
            "shop",
            "product",
            "price",
        ]


class PaymentSerializer(BaseSerializer):
    class Meta:
        model = Payment
        fields = [
            *BaseSerializer.Meta.fields,
            "order",
            "currency",
            "received_amount",
            "method",
            "reference_code",
            "verifier",
            "verified_at",
            "rejected_at",
        ]
