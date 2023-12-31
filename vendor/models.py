from django.db import models

# Create your models here.
class Vendorprofile(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    contact_details=models.TextField(max_length=500)
    address=models.CharField(max_length=200,null=True,blank=True)
    vendorcode=models.CharField(max_length=200,unique=True)
    # on_time_delivery_percentage=models.FloatField()
    # quality_rating=models.FloatField()
    # fulfilment_rate=models.FloatField()

class Purchaseorder(models.Model):
    vendor=models.ForeignKey(Vendorprofile,on_delete=models.CASCADE)
    order_number=models.CharField(max_length=50,unique=True)
    order_date=models.DateField()
    delivery_date=models.DateTimeField()
    items=models.CharField(max_length=200)
    quantity=models.IntegerField()
    status=models.CharField(max_length=100)
    quality_rating=models.FloatField()
    issue_date=models.FloatField()
    acknowledgment_date=models.DateTimeField()


class VendorPerformance(models.Model):
    vendor=models.ForeignKey(Vendorprofile,on_delete=models.CASCADE)
    quality_rating=models.FloatField()
    on_time_delivery_percentage=models.FloatField()
    average_response_time=models.FloatField()
    fulfilment_rate=models.FloatField()







