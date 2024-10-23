from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComponentViewSet, VehicleViewSet, IssueViewSet, complete_issue, revenue_view, PaymentView

router = DefaultRouter()
router.register('components', ComponentViewSet)
router.register('vehicles', VehicleViewSet)
router.register('issues', IssueViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/revenue/', revenue_view),
    path('api/issues/<int:component_id>/complete/', complete_issue, name='complete_issue'),
    path('api/payments/', PaymentView),
]
