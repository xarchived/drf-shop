from typing import Any

from rest_framework.exceptions import APIException
from rest_framework.fields import CharField, IntegerField
from rest_framework.relations import PrimaryKeyRelatedField

from auther.models import User
from auther.simples import SimpleUserSerializer
from fancy.serializers import CommonFieldsSerializer, NestedModelSerializer
from purchase.models import Product, Order, Payment, Package, Price, Item
from purchase.simples import SimpleProductSerializer, SimpleOrderSerializer, SimplePriceSerializer


class ProductSerializer(CommonFieldsSerializer, NestedModelSerializer):
    name = CharField(max_length=128)
    prices = SimplePriceSerializer(many=True)
    prices_ids = PrimaryKeyRelatedField(
        source='prices',
        many=True,
        queryset=Price.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Product
        fields = [
            *CommonFieldsSerializer.Meta.fields,
            'name',
            'prices',
            'prices_ids',
        ]


class PriceSerializer(CommonFieldsSerializer):
    product = SimpleProductSerializer(read_only=True)
    product_id = PrimaryKeyRelatedField(
        source='product',
        queryset=Product.objects.all(),
    )
    amount = IntegerField(
        required=True,
        min_value=0,
        max_value=999999999999999999,
    )

    class Meta:
        model = Price
        fields = [
            *CommonFieldsSerializer.Meta.fields,
            'product',
            'product_id',
            'amount',
        ]


class PackageSerializer(ProductSerializer):
    products = SimpleProductSerializer(many=True, read_only=True)
    products_ids = PrimaryKeyRelatedField(
        source='products',
        many=True,
        queryset=Product.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Package
        fields = [
            *ProductSerializer.Meta.fields,
            'products',
            'products_ids',
        ]


class OrderSerializer(CommonFieldsSerializer, NestedModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.all(),
    )
    products = SimpleProductSerializer(many=True, read_only=True)
    products_ids = PrimaryKeyRelatedField(
        source='products',
        many=True,
        queryset=Product.objects.all(),
        required=False,
        allow_null=True,
    )

    def create(self, validated_data: dict) -> Any:
        a = super().create(validated_data)
        items = Item.objects.filter(order_id=a.pk)
        for item in items:
            price = Price.objects.filter(product_id=item.product.pk).last()
            if price is None:
                raise APIException("Price Not Found")
            item.price = price
            item.save()

        return a

    class Meta:
        model = Order
        fields = [
            *CommonFieldsSerializer.Meta.fields,
            'user',
            'user_id',
            'products',
            'products_ids',
        ]


class PaymentSerializer(CommonFieldsSerializer):
    order = SimpleOrderSerializer(read_only=True)
    order_id = PrimaryKeyRelatedField(
        source='order',
        queryset=Order.objects.all(),
    )

    class Meta:
        model = Payment
        fields = [
            *CommonFieldsSerializer.Meta.fields,
            'order',
            'order_id',
        ]
