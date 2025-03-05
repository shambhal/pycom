from django.db import models
from datetime import datetime
from orders.models import Order
from django.db.models import UniqueConstraint
from customer.models import Customer
# Create your models here.
class CheckoutKey(models.Model):
    '''checkout one time key'''
    device_id=models.CharField(blank=True,)
    customer_id=models.IntegerField(blank=True)
    key=models.CharField(max_length=100)
    created=models.DateTimeField(default=datetime.now, blank=True)
    order=models.ForeignKey(Order,  on_delete=models.CASCADE)
    class Meta:
         constraints = [
              UniqueConstraint(fields=['key'], name='unique_otkey')
       ] 
class Appointee(models.Model):
    
    customer=models.ForeignKey(Customer,  on_delete=models.CASCADE)
    name=models.CharField(max_length=50,blank=False)
    email=models.CharField(max_length=150,blank=False)
    mobile=models.CharField(max_length=12,blank=False)
    address=models.CharField(max_length=120,blank=True)