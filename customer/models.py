from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
class Customer(models.Model):
    def __str__(self): 
         return self.user.first_name +' '+self.user.last_name
    user = models.OneToOneField(User, on_delete=models.CASCADE,default='shambhal')
    phone = models.CharField(null=True, blank=True ,max_length=20)
    access=models.CharField(null=True,max_length=150)
    refresh=models.CharField(null=True,max_length=150)
    
class CustomerOTP(models.Model):
    
    otp = models.CharField(null=True, blank=True ,max_length=8)
    email=models.CharField(null=True,max_length=150)
    created_at = models.DateTimeField(default=timezone.now)
