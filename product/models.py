from django.db import models
from datetime import date
from django.db.models.fields.files import ImageField
from django.utils import timezone
#from versatileimagefield.fields import PPOIField, VersatileImageField
# Create your models here.
from django.utils.translation import gettext_lazy as _

from seo.models import SeoModel, SeoModelTranslation
from django_measurement.models import MeasurementField

    
class ProductType(SeoModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    has_variants = models.BooleanField(default=True)
    is_shipping_required = models.BooleanField(default=True)
    is_digital = models.BooleanField(default=False)
    

    

class Language(models.Model):
    name=models.CharField(blank=False,max_length=10)
    flag=models.CharField(blank=False,max_length=10)
    code=models.CharField(max_length=5)
    def __str__(self) -> str:
        return self.name
class SeoModel(models.Model):
    seo_title = models.CharField(
        max_length=70, blank=True, null=True
    )
    seo_description = models.CharField(
        max_length=300, blank=True, null=True
    )

    class Meta:
        abstract = True  
        
class Category(SeoModel) :
    class Status(models.TextChoices):
        DISABLED = 0, _('Disabled')
        ENABLED = 1, _('Enabled')
       
    status=models.CharField(max_length=2,choices=Status.choices,)
    #image=ImageField(upload_to="category",)
    name=models.CharField(blank=False,max_length=20,default='Category')
    date_modified=models.DateField(default=date.today)
    parent=models.ManyToManyField("self",blank=True,related_name="children")
    def __str__(self) -> str:
        return self.name
    class Meta:
        verbose_name_plural = "categories"

    

class Category_SEO(SeoModel):
    category=models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    language = models.ForeignKey(Language,on_delete=models.CASCADE,default=1)