from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HospitalViewSet, TreatmentPriceViewSet, compare_prices, monitor_prices

router = DefaultRouter()
router.register('hospitals', HospitalViewSet)
router.register('prices', TreatmentPriceViewSet)

urlpatterns = [
    path('compare/', compare_prices),
    path('monitor/', monitor_prices),
    path('', include(router.urls)),
]
