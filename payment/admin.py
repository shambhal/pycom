from django.contrib import admin
from django.http.request import HttpRequest
from django.template.response import TemplateResponse
from .models import Payment
from django.urls import path,reverse
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from pycom.admin import admin_site 
from pathlib import Path
import importlib
# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
 actions=None
 list_display=['code','status','settings2']
 
 @admin.display(ordering='settings', description='Settings')
 def settings2(self,obj):
      #link='/admin/'+obj.code.lower()+'/'+obj.code.lower()
      #print(link)
      ##it shuld be paypal/paypal/add or paypal/paypal/1/change
      #return 'lupchup'
      param2='payment.gateways.{}.hooks'.format(obj.code.lower())
      module=importlib.import_module(param2)
      link=module.getLink()
      return format_html('<a href="'+link+'">Settings</a>')
 def has_add_permission(self, request):
        return False
 def changelist_view(self, request,extra_context=None) :
     list=self.getList()
     #print(list)
     for pg in list:
        gg= Payment.objects.all().filter(code=pg)
        if(not gg.exists()):
            cr=Payment.objects.create(code=pg,status=0)
           
            #cr.save()
     
     return super().changelist_view(request, extra_context)
 def gateway(self,request):
     list=self.getList()
     context={'gateways':list} 
     return render(request, 'admin/gateways_list.html', context)
 def getList(self):
        path1=Path(settings.BASE_DIR,'payment/gateways')
        #print("in gateways")
        #print(path1)
        k=[x for x in path1.iterdir() if x.is_dir()]
        list=[]
        for module_path in k :
            #print(module_path.name)
            if not module_path.name=='__pycache__':
                list.append(module_path.name)
        return list    
 def get_urls(self):
        urls = super().get_urls()
        urls.remove(urls[1])
        custom_urls = [
            path('list', self.admin_site.admin_view(self.gateway))
        ]
        return urls+ custom_urls
admin.site.register(Payment,PaymentAdmin)
admin_site.register(Payment,PaymentAdmin)