from django.db import models
from django.db.models.fields.related import ForeignKey
from django.db.models import UniqueConstraint
from service.models import Service
from customer.models import Customer
# Create your models here.
class AppCart(models.Model):

     service=models.ForeignKey(Service,on_delete=models.CASCADE,) 
     dated=models.DateField(blank=False,max_length=20)
     price=models.DecimalField(max_digits=6,decimal_places=2),
     slot=models.CharField(blank=False,max_length=20)
     device_id=models.CharField(blank=True,max_length=50)
     user_id=models.IntegerField(blank=True,default=0)
     '''class Meta:
          constraints = [
              UniqueConstraint(fields=['dated', 'service','slot','device_id','user_id'], name='unique2_cart')
       ] 
     '''  
     #user=ForeignKey(Customer,  on_delete=models.CASCADE,blank=True)
    