from datetime import timedelta

from django.db.models import Q, F, QuerySet
from django.utils import timezone

from purchase.models import Subscribe, Product, Order


def get_active_subscribes(user_id: int) -> QuerySet:
    return Subscribe.objects.filter(
        Q(orders__inserted_at__gt=timezone.now() - timedelta(days=1) * F('duration')) &
        Q(orders__payments__ref_id__isnull=False) &
        (
                Q(orders__user_id=user_id) |
                Q(orders__user__children__id=user_id)
        )
    ).distinct()


def get_active_products(user_id: int) -> QuerySet:
    return Product.objects.filter(
        orders__products__in=get_active_subscribes(user_id=user_id)
    ).distinct()


def calculate_total_amount(order_id: int) -> int:
    order = Order.objects.get(pk=order_id)

    return sum([item.price.amount for item in order.items.all()])
