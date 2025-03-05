from django.db import models
from service.models import Service
from pycom.admin import admin_site
from django.db.models.fields.related import ForeignKey
# Create your models here.
class CatModule(models.Model):
     class Meta:
      verbose_name='Category Banner'
     def __str__(self):
          return self.service.name+' '+'banner'
     service=models.ForeignKey(Service,on_delete=models.CASCADE,) 
     image=models.TextField(max_length=100)
     sort_order=models.IntegerField()
     status=models.IntegerField(default=1)