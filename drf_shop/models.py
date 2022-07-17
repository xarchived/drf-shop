from uuid import uuid4

from django.contrib.auth.models import User
from django.db.models import (
    RESTRICT,
    CheckConstraint,
    DateTimeField,
    DecimalField,
    F,
    FloatField,
    ForeignKey,
    IntegerChoices,
    ManyToManyField,
    Model,
    Q,
    SmallIntegerField,
    TextField,
    UUIDField,
)
from drf_manipulation.models import ManipulationAbstractModel

from drf_shop.settings import (
    ORDER_SHOP_NULL,
    PRICE_DECIMAL_PLACES,
    PRICE_MAX_DIGITS,
    PRODUCT_SHOP_NULL,
)

# region Abstract Models


class BaseAbstractModel(ManipulationAbstractModel):
    id: UUIDField = UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        db_index=True,
    )

    class Meta:
        abstract = True


# endregion


# region Core Models


class Shop(BaseAbstractModel):
    name: TextField = TextField()
    owner: ForeignKey = ForeignKey(
        to=User,
        on_delete=RESTRICT,
        related_name="shops",
        db_index=True,
    )

    def __str__(self):
        return self.name


class Product(BaseAbstractModel):
    name: TextField = TextField()
    shop: ForeignKey = ForeignKey(
        to="Shop",
        on_delete=RESTRICT,
        related_name="products",
        null=PRODUCT_SHOP_NULL,
        db_index=True,
    )

    def __str__(self):
        return self.name


class Currency(BaseAbstractModel):
    name: TextField = TextField()
    code: TextField = TextField()
    fluctuates: FloatField = FloatField()

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name_plural = "currencies"


class Rate(BaseAbstractModel):
    base: ForeignKey = ForeignKey(
        to="Currency",
        on_delete=RESTRICT,
        related_name="based_rates",
        db_index=True,
    )
    quote: ForeignKey = ForeignKey(
        to="Currency",
        on_delete=RESTRICT,
        related_name="quoted_rates",
        db_index=True,
    )
    rate: FloatField = FloatField()

    class Meta:
        unique_together = ["base", "quote"]
        constraints = [
            CheckConstraint(
                check=~Q(base=F("quote")),
                name="same_base_quote",
            ),
        ]

    def __str__(self):
        return f"{self.base.name} => {self.quote.name}"


class Price(BaseAbstractModel):
    amount: DecimalField = DecimalField(
        max_digits=PRICE_MAX_DIGITS, decimal_places=PRICE_DECIMAL_PLACES
    )
    currency: ForeignKey = ForeignKey(
        to="Currency",
        on_delete=RESTRICT,
        related_name="prices",
        db_index=True,
    )
    product: ForeignKey = ForeignKey(
        to="Product",
        on_delete=RESTRICT,
        related_name="prices",
        db_index=True,
    )
    constraints = [
        CheckConstraint(
            check=Q(amount__gte=0),
            name="positive_amount",
        ),
    ]

    def __str__(self):
        return f"{self.product.name}: {self.amount} {self.currency.name}"


class Order(BaseAbstractModel):
    buyer: ForeignKey = ForeignKey(
        to=User,
        on_delete=RESTRICT,
        related_name="orders",
        db_index=True,
    )
    products: ManyToManyField = ManyToManyField(
        to="Product",
        through="OrderProduct",
        related_name="orders",
    )


class OrderProduct(Model):
    order: ForeignKey = ForeignKey(
        to="Order",
        on_delete=RESTRICT,
        related_name="items",
        db_index=True,
    )
    shop: ForeignKey = ForeignKey(
        to="Shop",
        on_delete=RESTRICT,
        related_name="items",
        null=ORDER_SHOP_NULL,
        db_index=True,
    )
    product: ForeignKey = ForeignKey(
        to="Product",
        on_delete=RESTRICT,
        related_name="items",
        db_index=True,
    )
    price: ForeignKey = ForeignKey(
        to="Price",
        on_delete=RESTRICT,
        related_name="items",
        db_index=True,
    )

    class Meta:
        unique_together = ["order", "product"]


class Payment(BaseAbstractModel):
    class Method(IntegerChoices):
        ONLINE: int = 1
        MANUAL: int = 2
        REMISSION: int = 3

    order: ForeignKey = ForeignKey(
        to="Order",
        on_delete=RESTRICT,
        related_name="payments",
        db_index=True,
    )
    currency: ForeignKey = ForeignKey(
        to="Currency",
        on_delete=RESTRICT,
        related_name="payments",
        db_index=True,
    )
    received_amount: DecimalField = DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        null=True,
    )
    method: SmallIntegerField = SmallIntegerField(
        choices=Method.choices,
    )
    reference_code: TextField = TextField(null=True)
    verifier: ForeignKey = ForeignKey(
        to=User,
        on_delete=RESTRICT,
        related_name="verified_payments",
        null=True,
        db_index=True,
    )
    verified_at: DateTimeField = DateTimeField(null=True)
    rejected_at: DateTimeField = DateTimeField(null=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(received_amount__gte=0),
                name="positive_amount",
            ),
        ]


# endregion
