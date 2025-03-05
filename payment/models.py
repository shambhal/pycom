from django.db import models
from pycom.admin import admin_site
# Create your models here.
class Payment(models.Model):
     def __str__(self) -> str:
              #return self.sdate +self.service.name
        return self.title
     code=models.CharField(blank=False,max_length=10,default='')
     title=models.CharField(max_length=20,default='Payment Title')
     status=models.BooleanField(default=0)
     #settings=models.TextField()

     '''def save(self ,args, **kwargs):
          #print(args)
        
          return super().save(*args, **kwargs)
     '''
#admin_site.register(Payment)     