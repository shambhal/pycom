from django.db import models
from payment.models import Payment
# Create your models here.
class COD(models.Model):
     def __str__(self) -> str:
              #return self.sdate +self.service.name
        return 'COD'
     status=models.BooleanField(default=0)
     sort_order=models.SmallIntegerField(default=10)
     def save(self, *args, **kwargs):
          self.pk = self.id = 1
          Payment.objects.all().filter(code='cod').update(status=self.status,title='Cash on Delivery')
         
          return super().save(*args, **kwargs)