from django.db import models
from pycom.admin import admin_site
from django.utils.translation import gettext_lazy as _
from payment.models import Payment
# Create your models here.
class Paypal(models.Model):
    def __str__(self) -> str:
              #return self.sdate +self.service.name
        return 'Paypal '
    class TranStatus(models.TextChoices):
       AUTH ='Auth', _('Authorization')
       SALE = 'Sale', _('Sale')

    email=models.CharField(blank=False,max_length=100)
    status=models.BooleanField(default=0)
    sandbox=models.BooleanField(default=1)
    transaction=models.CharField(choices=TranStatus.choices)
    sort_order=models.IntegerField(blank=False,default=10)
    def save(self, *args, **kwargs):
          self.pk = self.id = 1
          Payment.objects.all().filter(code='paypal').update(status=self.status)
         
          return super().save(*args, **kwargs)
   
admin_site.register(Paypal)       