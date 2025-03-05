
from pycom.admin import admin_site

from django.contrib import admin,messages
from .forms import CatModuleForm
from .models import CatModule
from fm.models import ImageTool,FaltuModel as fm2
from django.urls import path,reverse
# Register your models here.
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from pycom.settings import MEDIA_ROOT, MEDIA_URL, MEDIA_STATIC
import os
from PIL import Image
class CatModuleAdmin(admin.ModelAdmin) :
    
       
    list_display=['getServiceName','sort_order','writeimage']
    @admin.display(description='Service')
    def getServiceName(self,obj):
       return obj.service.name
    def writeThumb(self,obj):
        ffolder=MEDIA_ROOT
        ffolder.replace("\\",'/')
        if(not obj.image):
         img='placeholder.png'
        
        else:
         img=obj.image 
        
        if(os.path.exists(ffolder+img)) :
           pat= ImageTool.resize(img,100,100)
           return pat# format_html("<img src='{}'/>",pat)
        else:
          return ''
    @admin.display(description='')    
    def writeimage(self,obj):
        ffolder=MEDIA_ROOT
        ffolder.replace("\\",'/')
        if(not obj.image):
         img='placeholder.png'
        
        else:
         img=obj.image 
        
        if(os.path.exists(ffolder+img)) :
           pat= ImageTool.resize(img,100,100)
           return format_html("<img src='{}'/>",pat)
        else:
          return ''
        
        print ("folder is {} and imag is {}", folder,img)
        return ''
    change_form_template=add_form_template=  "admin/catmodule.html"  
    def add_view(self,request,form_url='',extra_content=None):
         thumb=ImageTool.resize('placeholder.png',100,100)
         burl=reverse('myadmin:commonfilemanager') 
         furl=request.build_absolute_uri(burl)
         #furl='http://localhost:8000/admin/fm/common_filemanager'
         defdata={
          
         }
         extra_content={'thumb':thumb,
         'furl':furl,
         'form':CatModuleForm(initial=defdata)}
         return super().add_view(request,form_url,extra_content)
    def change_view(self, request, object_id, form_url='', extra_context={}) :
        
       
        obj=CatModule.objects.get(pk=object_id)
       

        if request.method == "POST":
              form=CatModuleForm(request.POST)
              if form.is_valid():
                   #obj.status=form.cleaned_data['status'] 
                   obj.save()
                   messages.add_message(request, messages.INFO, "Updated.")
        thumb=self.writeThumb(obj)
        extra_context={'thumb':thumb,'image':obj.image,'form':CatModuleForm(instance=CatModule.objects.get(pk=object_id))}
        return super().change_view(request, object_id, form_url, extra_context)
admin_site.register(CatModule,CatModuleAdmin)