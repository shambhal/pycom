from django.db import models
from django.template.defaultfilters import slugify  # new
from ckeditor.fields import RichTextField
# Create your models here.
class Information(models.Model):
     def __str__(self): 
         return self.title
     title=models.CharField( blank=False ,max_length=50)
     seo_url=models.CharField(blank=False,max_length=250,unique=True)
     content=RichTextField(blank=True)
     status=models.BooleanField(default=True)
     sort_order=models.IntegerField(default=10)
     def save(self,*args,**kwargs):
          self.seo_url=slugify(self.seo_url)
          return super().save(*args, **kwargs)