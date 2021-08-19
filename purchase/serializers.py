from typing import Any

from rest_framework.fields import CharField, IntegerField, ChoiceField
from rest_framework.relations import PrimaryKeyRelatedField

from auther.models import User, Role
from auther.simples import SimpleUserSerializer, SimpleRoleSerializer
from fancy.serializers import CommonFieldsSerializer, NestedModelSerializer
from purchase.exceptions import LimitExceededError
from purchase.models import Product, Order, Payment, Package, Price, Item, Subscribe
from purchase.simples import (
    SimpleProductSerializer,
    SimpleOrderSerializer,
    SimplePriceSerializer,
)
from purchase.utils import current_product_price


class ProductSerializer(CommonFieldsSerializer, NestedModelSerializer):
    name = CharField(max_length=128)
    order_limit = IntegerField(required=False, allow_null=True, min_value=1, max_value=999)
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
            'order_limit',
            'prices',
            'prices_ids',
        ]


class PriceSerializer(CommonFieldsSerializer):
    product = SimpleProductSerializer(read_only=True)
    product_id = PrimaryKeyRelatedField(
        source='product',
        queryset=Product.objects.all(),
    )
    role = SimpleRoleSerializer(read_only=True)
    role_id = PrimaryKeyRelatedField(
        source='role',
        queryset=Role.objects.all(),
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
            'role',
            'role_id',
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


class SubscribeSerializer(ProductSerializer):
    duration = IntegerField(
        required=False,
        min_value=0,
        max_value=999999999,
    )

    class Meta:
        model = Subscribe
        fields = [
            *ProductSerializer.Meta.fields,
            'duration',
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
        def check_order_limitation(_validated_data: dict) -> None:
            for product in _validated_data['products']:
                count = Item.objects.filter(product=product, order__user=_validated_data['user']).count()
                if product.order_limit and count > product.order_limit:
                    raise LimitExceededError()

        def update_item_prices(_order: Order, user: User) -> None:
            items = Item.objects.filter(order=_order)
            for item in items:
                item.price = current_product_price(item.product, user)
                item.save()

        check_order_limitation(validated_data)
        order = super().create(validated_data)
        update_item_prices(order, validated_data['user'])
        return order

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
    type = CharField(source='get_type_id_display', read_only=True)
    type_id = ChoiceField(
        choices=Payment.Type.choices,
        allow_null=True,
        required=False,
    )
    identity_token = CharField(min_length=5, max_length=150, required=False)
    ref_id = CharField(min_length=5, max_length=150, required=False)

    class Meta:
        model = Payment
        fields = [
            *CommonFieldsSerializer.Meta.fields,
            'order',
            'order_id',
            'type',
            'type_id',
            'identity_token',
            'ref_id',
        ]
