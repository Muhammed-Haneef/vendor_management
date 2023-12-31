from rest_framework import serializers
from .models import Vendorprofile,Purchaseorder,VendorPerformance


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendorprofile
        fields='__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Purchaseorder
        fields='__all__'

class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorPerformance
        fields='__all__'
