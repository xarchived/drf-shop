from rest_framework.fields import CharField, IntegerField
from rest_framework.relations import PrimaryKeyRelatedField

from auther.models import User
from auther.simples import SimpleUserSerializer
from fancy.serializers import CommonFieldsSerializer
from purchase.models import Product, Order, Payment, Package, Price
from purchase.simples import SimpleProductSerializer, SimpleOrderSerializer, SimplePriceSerializer


class ProductSerializer(CommonFieldsSerializer):
    name = CharField(max_length=128)
    prices = SimplePriceSerializer(many=True, read_only=True)
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


class OrderSerializer(CommonFieldsSerializer):
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
            'order_id',
        ]
