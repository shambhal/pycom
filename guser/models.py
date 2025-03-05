from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class GUser(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE,default='shambhal')
     refresh=models.CharField(blank=True,max_length=250)
     access=models.CharField(blank=True,max_length=250)
