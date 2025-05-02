from django.db import models

# Create your models here.
class ConfigModel(models.Model):
    cname=models.CharField( blank=False ,max_length=20)
    cvalue=models.CharField(blank=False,max_length=20)
    cgroup=models.CharField(blank=False,max_length=20)