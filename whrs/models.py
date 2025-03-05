from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH

# Create your models here.
class work(models.Model):
   class Meta:
        verbose_name_plural = 'work'
      
   sunday=models.TextField(blank=False)
   monday=models.TextField(blank=False)
   tuesday=models.TextField(blank=False)
   wednesday=models.TextField(blank=False)
   thursday=models.TextField(blank=False)
   friday=models.TextField(blank=False)
   saturday=models.TextField(blank=False)
   slot=models.IntegerField(blank=False,default=1800,help_text='Session in seconds')
   def save(self, *args, **kwargs):
        self.pk = self.id = 1
        return super().save(*args, **kwargs)

class Special(models.Model):
   sdate=models.DateField('Special Date')
   sunday=models.TextField(blank=False)
   monday=models.TextField(blank=True)
   tuesday=models.TextField(blank=True)
   wednesday=models.TextField(blank=True)
   thursday=models.TextField(blank=True)
   friday=models.TextField(blank=True)
   saturday=models.TextField(blank=True)