from rest_framework.routers import SimpleRouter

from purchase.selves import SelfPaymentViewSet, SelfOrderViewSet
from purchase.views import ProductViewSet, OrderViewSet, PaymentViewSet, PriceViewSet, PackageViewSet, SubscribeViewSet

router = SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'prices', PriceViewSet)
router.register(r'packages', PackageViewSet)
router.register(r'subscribes', SubscribeViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'self_payments', SelfPaymentViewSet)
router.register(r'self_orders', SelfOrderViewSet)

urlpatterns = router.urls
