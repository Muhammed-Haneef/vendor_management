from django.db.models import Avg, F, Sum
from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Vendorprofile, Purchaseorder,VendorPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer,VendorPerformanceSerializer

class VendorListCreateApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendors = Vendorprofile.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Vendorprofile.objects.get(pk=pk)
        except Vendorprofile.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vendor = self.get_object(pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseOrderListCreateApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        purchase_orders = Purchaseorder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseOrderDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Purchaseorder.objects.get(pk=pk)
        except Purchaseorder.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        purchase_order = self.get_object(pk)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    def put(self, request, pk):
        purchase_order = self.get_object(pk)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()


            # Calculate and update metrics in VendorPerformance
            vendor = purchase_order.vendor
            vendor_performance = VendorPerformance.objects.get(vendor=vendor)

            # On-Time Delivery Rate
            if purchase_order.status == 'completed':
                completed_orders = purchase_order.objects.filter(vendor=vendor, status='completed')
                on_time_deliveries = completed_orders.filter(delivery_date__lte=purchase_order.delivery_date)
                on_time_delivery_rate = on_time_deliveries.count() / completed_orders.count() if completed_orders.count() > 0 else 0.0
                vendor_performance.on_time_delivery_rate = on_time_delivery_rate

                # Quality Rating Average
            if purchase_order.quality_rating is not None:
                completed_orders = purchase_order.objects.filter(vendor=vendor, quality_rating__isnull=False)
                quality_rating_average = completed_orders.aggregate(Avg('quality_rating'))['quality_rating__avg']
                vendor_performance.quality_rating_average = quality_rating_average if quality_rating_average is not None else 0.0

            # Average Response Time
            if purchase_order.acknowledgment_date is not None:
                response_times = purchase_order.objects.filter(vendor=vendor, acknowledgment_date__isnull=False) \
                    .exclude(acknowledgment_date__gt=timezone.now()) \
                    .annotate(response_time=Sum('acknowledgment_date' - F('issue_date')))
                average_response_time = response_times.aggregate(Avg('response_time'))['response_time__avg']
                vendor_performance.average_response_time = average_response_time if average_response_time is not None else 0.0

            # Fulfilment Rate
            if purchase_order.status == 'completed':
                fulfilled_orders = completed_orders.exclude(fulfilment_status__in=['failure', 'issue'])
                fulfilment_rate = fulfilled_orders.count() / completed_orders.count() if completed_orders.count() > 0 else 0.0
                vendor_performance.fulfilment_rate = fulfilment_rate

            # Save the updated VendorPerformance
            vendor_performance.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        purchase_order = self.get_object(pk)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VendorPerformanceDetailApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

        def get_object(self, pk):
            try:
                return VendorPerformance.objects.get(pk=pk)
            except VendorPerformance.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        def get(self, request, pk):
            vendor_performance = self.get_object(pk)
            serializer = VendorPerformanceSerializer(vendor_performance)
            return Response(serializer.data)

        def put(self, request, pk):
            vendor_performance = self.get_object(pk)
            serializer = VendorPerformanceSerializer(vendor_performance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, pk):
            vendor_performance = self.get_object(pk)
            vendor_performance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

