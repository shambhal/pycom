from django.contrib import admin
from .models import Tax
from pycom.admin import admin_site 
# Register your models here.
@admin.register(Tax)
class TaxesAdmin(admin.ModelAdmin)  :
    list_display=['name','type','status','sort_order']
    pass  
admin_site.register(Tax,TaxesAdmin)   