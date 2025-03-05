from django.contrib import admin
from .models import Information
from pycom.admin import admin_site 
from .forms import InformationForm
# Register your models here.
@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
   list_display=['title','seo_url','status','sort_order']
   prepopulated_fields = {'seo_url': ('title', )}

   #add_form_template='admin/add_information.html'

   '''def add_vixew(self,request,form_url='',extra_content=None):
        
       
        
         extra_content={
         
         'form':InformationForm()}
         return super().add_view(request,form_url,extra_content)

'''         
admin_site.register(Information,InformationAdmin)   