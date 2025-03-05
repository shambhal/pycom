from django.db import models
from service.models import Service
from django.utils import timezone
OS_CHOICES=[
('PENDING','Pending'),
('CREATED','Created'),
('PROCESSING','Processing'),
('COMPLETED','Completed'),
('CANCELLED','Cancelled'),
('REFUNDED','Refunded')
]
# Create your models here.
class Order(models.Model):
    def __str__(self) -> str:
             return str(self.id)+' '+self.name +' '+str(self.total)
    name=models.CharField( blank=False ,max_length=50)
    email=models.CharField(blank=False,max_length=200)
    phone=models.CharField(blank=False ,max_length=20)
    device_id=models.CharField(blank=True ,max_length=120)
    payment_method=models.CharField(blank=False ,max_length=20)
    user_agent=models.CharField(blank=True, max_length=300)
    total=models.DecimalField( max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    comment=models.CharField(blank=True ,max_length=200)
    currency_code=models.CharField(max_length=4,blank=True)
    user_id=models.IntegerField(blank=True,default=0)
    status=models.CharField(choices=OS_CHOICES, blank=False, max_length=10,default='PENDING')
class OrderItems(models.Model) :
    quantity=  models.IntegerField( blank=False ,default=1) 
    name=models.CharField( max_length=50)
    dated=models.DateField(blank=False)
    service=models.ForeignKey(Service,on_delete=models.DO_NOTHING,default=1)
    slot=models.CharField( blank=False ,max_length=50)
    price=models.DecimalField( max_digits=7, decimal_places=2)
    order_id=models.ForeignKey(Order,on_delete=models.DO_NOTHING,null=True,default=0)
class OrderHistory(models.Model):
    
    dated=models.DateField(blank=False,max_length=20,default=timezone.now)
    status=models.CharField(max_length=20,blank=False)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
   
class OrderTotals(models.Model):
      title=models.CharField( max_length=50)  
      order_id=models.ForeignKey(Order,on_delete=models.CASCADE)
      total=models.DecimalField( max_digits=7, decimal_places=2)