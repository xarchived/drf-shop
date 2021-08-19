from datetime import timedelta

from django.db.models import Q, F, QuerySet
from django.utils import timezone

from auther.models import User
from purchase.exceptions import EmptyPriceError
from purchase.models import Subscribe, Product, Order, Price


def active_subscribes(user_id: int) -> QuerySet:
    return Subscribe.objects.filter(
        Q(orders__inserted_at__gt=timezone.now() - timedelta(days=1) * F('duration')) &
        Q(orders__payments__ref_id__isnull=False) &
        (
                Q(orders__user_id=user_id) |
                Q(orders__user__children__id=user_id)
        )
    ).distinct()


def active_products(user_id: int) -> QuerySet:
    return Product.objects.filter(
        orders__products__in=active_subscribes(user_id=user_id)
    ).distinct()


def current_product_price(product: Product, user: User) -> Price:
    role = user.roles.order_by('-level').first()
    price = Price.objects.filter(
        Q(product=product) & (
                Q(role=role) |
                Q(role=None)
        )
    ).order_by('-id').first()

    if price is None:
        raise EmptyPriceError(f'No price found for "{role.name}"')

    return price


def calculate_total_amount(order_id: int) -> int:
    order = Order.objects.get(id=order_id)

    total = 0
    for item in order.items.all():
        if not item.price:
            raise EmptyPriceError()

        total += item.price.amount

    return total
