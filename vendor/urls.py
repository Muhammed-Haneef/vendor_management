# vendor/urls.py

from django.urls import path
from .views import (
    VendorListCreateApiView,
    VendorDetailApiView,
    PurchaseOrderListCreateApiView,
    PurchaseOrderDetailApiView,
    VendorPerformanceDetailApiView,
)

urlpatterns = [
    path('api/vendors/', VendorListCreateApiView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:pk>/', VendorDetailApiView.as_view(), name='vendor-detail'),
    path('api/purchase-orders/', PurchaseOrderListCreateApiView.as_view(), name='purchase-order-list-create'),
    path('api/purchase-orders/<int:pk>/', PurchaseOrderDetailApiView.as_view(), name='purchase-order-detail'),
    path('api/vendor-performance/<int:pk>/', VendorPerformanceDetailApiView.as_view(), name='vendor-performance-detail'),

]
