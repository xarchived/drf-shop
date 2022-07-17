from django.conf import settings

if not hasattr(settings, "SHOP"):
    settings.SHOP = dict()

DEBUG = settings.DEBUG
PRODUCT_SHOP_NULL = settings.SHOP.get("PRODUCT_SHOP_NULL", True)
ORDER_SHOP_NULL = settings.SHOP.get("ORDER_SHOP_NULL", True)
PRICE_MAX_DIGITS = settings.SHOP.get("PRICE_MAX_DIGITS", 30)
PRICE_DECIMAL_PLACES = settings.SHOP.get("PRICE_DECIMAL_PLACES", 0)
