#from typing_extensions import Required
from django.db import models
from pycom.admin import admin_site
from django.db.models.enums import Choices
from django.db.models.fields.related import ForeignKey
from django.db.models import UniqueConstraint
from seo.models import SeoModel
from django.contrib.auth.models import User
from django.conf import settings
#from orders.models import Order,OrderItems
from service.constants import SERVICE_STATUS
from django.utils.html import format_html
from django.utils import timezone
from PIL import Image
# Create your models here.
APP_NOT_TYPE=[('BOOK','Book'),('ORD','Order')]
class AppNotification(models.Model):
      ##firebase string
      fbstring=models.CharField( max_length=150,blank=True)
      ######type for order and book
      ntype=models.CharField(max_length=7,choices=APP_NOT_TYPE)
      msg=models.TextField(blank=True)
      created_at = models.DateTimeField(auto_now_add=True)
class Service(SeoModel):
   def __str__(self) -> str:
             return self.seo_title
   sunday=models.TextField(blank=False)
   monday=models.TextField(blank=False)
   tuesday=models.TextField(blank=False)
   wednesday=models.TextField(blank=False)
   thursday=models.TextField(blank=False)
   friday=models.TextField(blank=False)
   saturday=models.TextField(blank=False)
   slot=models.IntegerField(blank=False,default=1800,help_text='Session in seconds')
   name=models.TextField(blank=False)
   off=models.TextField(blank=True)
   img=models.TextField(blank=True,help_text="Cover Image")
class SSpecial(models.Model):
   class Meta:
       verbose_name="Service Special Day"
       verbose_name_plural = "Service Special Days"
   def __str__(self) -> str:
              #return self.sdate +self.service.name
        return self.service.name+' '+str(self.sdate)
   #sdate=models.DateField('Special Date')
   sdate=models.DateField()
   '''sunday=models.TextField(blank=False)
   monday=models.TextField(blank=True)
   tuesday=models.TextField(blank=True)
   wednesday=models.TextField(blank=True)
   thursday=models.TextField(blank=True)
   friday=models.TextField(blank=True)
   saturday=models.TextField(blank=True)
   '''
   hours=models.TextField(blank=False,default="08:00-12:00")
   off=models.TextField(blank=True)
   service=ForeignKey(Service,related_name='service',on_delete=models.CASCADE)  

class Book(models.Model):
   #st=[('UN','UNAVAILABLE'),('AV','AVAILABLE')]
   def __str__(self) -> str:
             return self.name+ '-'+str(self.dated)+'-'+self.slot
   dated=models.DateField(blank=False,max_length=20)
   service=ForeignKey(Service,on_delete=models.CASCADE,default=1)
   slot=models.CharField(blank=False,max_length=20) 
   desc=models.TextField(blank=True,)
   name=models.CharField(blank=False,max_length=60)
   phone=models.CharField(max_length=15)
   order_id=models.IntegerField(blank=True,default=0)
   email=models.CharField(max_length=150,blank=True,default="demo@gmail.com")
   status=models.CharField(choices=SERVICE_STATUS,max_length=15,default='AV')
   device_id=models.CharField(blank=True,max_length=150)
   user_id=models.IntegerField(blank=True,default=0)
   order_item_id=models.IntegerField(blank=True,default=0)
   extra_info=models.TextField(blank=True,default='')
   class Meta:
       constraints = [
              UniqueConstraint(fields=['dated', 'service','slot','status'], name='unique2_booking')
       ] 
class BookHistory(models.Model):
      
    dated=models.DateField(blank=False,max_length=20,default=timezone.now)
    status=models.CharField(max_length=20,blank=False)
    book_id=models.ForeignKey(Book,on_delete=models.CASCADE)
    info=models.TextField(blank=True)
class Simg(models.Model):
    def __str__(self)->str:
       return '<img src="{}">'.format(settings.MEDIA_URL+self.img.name)
    def save3(self,*args, **kwargs):
       #super().save(*args,**kwargs)
       pass
       #img=Image.open(self.img.path)
       #output_size=(300,300)
       #thumb=img.thumbnail(output_size)
       #thumb.save(self.img.path)
    img=models.ImageField(upload_to='uploads/')
    service=models.ForeignKey(Service,on_delete=models.CASCADE,related_name='service_image') 
'''class BookHistory(models.Model):
         book=ForeignKey(Book,on_delete=models.CASCADE,default=1)

    dated=models.DateField(blank=False,max_length=20,default=timezone.now)
    status=models.CharField(max_length=20,blank=False)
    order_id=models.IntegerField(blank=True,default=0)
    order_item_id=models.IntegerField(blank=True,default=0)
'''    
#admin_site.register(Book)
#admin_site.register(Service)