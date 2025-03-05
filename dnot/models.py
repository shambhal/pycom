from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
class NotificationHistory(models.Model):

    dated=models.DateField(blank=False,max_length=20,default=timezone.now)
    status=models.CharField(max_length=20,blank=False)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)


# Create your models here.
