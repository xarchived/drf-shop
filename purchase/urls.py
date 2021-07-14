from rest_framework.routers import SimpleRouter

from purchase.views import ProductViewSet, OrderViewSet, PaymentViewSet, PriceViewSet, PackageViewSet

router = SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'prices', PriceViewSet)
router.register(r'packages', PackageViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = router.urls
