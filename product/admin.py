from django.contrib import admin
from django.http.response import HttpResponse
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
# Register your models here.


from .models import Category, Category_SEO,Language,SeoModel
from django_summernote.admin import SummernoteModelAdmin

class CategoryAdmin(admin.ModelAdmin) :
    exclude=['date_modified']
    
    list_display=('name','status','links_seo')
    def get_form(self, request, obj=None, change=False, **kwargs):
       
        # print(request)
        #print(kwargs)
        #print(change)
        #print(obj)
        if(obj!=None) :
           objstr= str(obj)
           objstr= objstr.replace("Category","")
           print(objstr)
           form=super().get_form(request, obj,change,  **kwargs)
           #print(form.base_fields['parent'])
        return super().get_form(request, obj,change,  **kwargs)
     
    def get_changelist_form(self, request, **kwargs):
        #print("in getcheangelist_form")
        #print(self);
        return super().get_changelist_form(request, **kwargs)
    def links_seo(self,obj):
        obj2= Category_SEO.objects.filter(category_id=obj.pk)
        print(obj2)
        if(obj2):
         return format_html("<a href='../category_seo/{pk}/change'>seo</a>",pk=obj.pk )
        else:
         return format_html("<a href='../category_seo/{pk}/add'>seo</a>",pk=obj.pk)   
    links_seo.allow_tags=True
admin.site.register(Category,CategoryAdmin)
admin.site.register(Language)
class Category_SEO_ADMIN(SummernoteModelAdmin) :
     summernote_fields = ('seo_description',)
     readonly_fields=['category']
     def get_urlsf(self):
         urls=super().get_urls()
         urls.remove(urls[1])
         myurls=[path("addd",self.add_seo,name='product_category_seo_add')]
         return urls+myurls
     def add(request):  
         print(request)
         context={}
         return render(request, 'time/settings.html', context)     
     def add_seo(self,request):
         print(request)
         context={}
         return render(request, 'time/settings.html', context)        
admin.site.register(Category_SEO,Category_SEO_ADMIN)