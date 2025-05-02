from typing import Any
from django.contrib import admin
from django.contrib.auth.models import User,Group
from django.db.models.query import QuerySet
from django.http import HttpRequest
from customer.models import Customer
#from appmodules.models import CatModule
from django.utils.translation import gettext_lazy as _
from django.core.handlers.wsgi import WSGIRequest 
class MyAdminSite(admin.AdminSite): 
    site_header = "Appointment administration"
    def get_app_list(self, request: WSGIRequest) :
        app_list= super().get_app_list(request)
        models=[]
        flist=[]
        gateways=[]
        l=['auth','payment','service']
        ignore=['faltumodel']
        licons={'auth':'fa-cog',
                'order':'fa-file-invoice',
                'information':'fa-bell',
                'catmodule':'fa-puzzle-piece',
                'group':'fa-user-group',
                'tax':'fa-list-ul',
                'payment':'fa-wallet','service':'fa-tags','user':'fa-user',
                  'service':'fa-handshake','book':'fa-calendar-days',
                  'customer':'fa-person'}
        index=-1
        pindex=0
        for app in app_list:
            index=index+1
            #print(app['models'])
            #print("----")
            # print(app)
            for mode in app['models']:
             #print(mode)
             #print('--')
             name=mode['object_name'].lower()
             #print(name)
             modelclass=str(mode['model'])
             if('gateways' in modelclass):
                 gateways.append(mode)
                 continue
             if(name in ignore):
                continue
             param='menu_'+name
             mode['icon']=licons[name] if name in licons else 'fa-eject'
             mode['name']=_(param) if _(param)  else name
             # mode['name']=_('Enabled')
             models.append(mode)
            #print(app['models'][0]['model'])
            label=app['app_label']
            if  label in  l:
                app['icon']=licons[label]
                #print (app['icon'])
                #print(app)
                flist.append(app)
        #print("models down")
        #print(models)
        #models[pindex]['child']=gateways
        #print(models)
        return models
        return super().get_app_list(request)
    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        l=['auth','payment','service']
        app_list=extra_context["app_list"] = admin.AdminSite.get_app_list(self,request)
        '''for app in app_list:
            #print (app)
            #print(app['models'][0]['model'])
            label=app['app_label']
            #print(app['app_label'])
        #print(extra_context)
        '''
        return super(MyAdminSite, self).index(request)
admin_site = MyAdminSite(name="myadmin")   
#admin_site.register(User)

class UserLastNameListFilter(admin.SimpleListFilter):
    title = 'last name'
    parameter_name = 'last_name'

    def lookups(self, request, model_admin):
        return (
            ('last_name', 'Last name'),
        )

    def queryset(self, request, queryset):
        if self.value is not None:
            queryset = queryset.filter(last_name=self.value)
        return queryset

class UserAdmin(admin.ModelAdmin):
    list_filter = ("is_active",)
    list_display=('username','email','is_active')
    def queryset(self,request,queryset):
          queryset = queryset.filter(is_staff=False)
          return queryset
   
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        return qs.filter(is_staff=True)
class CustomerAdmin(admin.ModelAdmin):
  list_display=['name','phone']
  ordering=["-id"]
  #list_filter=["user__first_name"]
  search_fields=["user__first_name"]
  @admin.display(description="Name")
  def name(self,obj):
      return obj.user.first_name
  '''def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
    qs = super().get_queryset(request)
    return qs.filter(=False)

    '''
class GroupAdmin(admin.ModelAdmin):
     pass    

class CatModuleAdmin(admin.ModelAdmin):
    pass
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(Customer, CustomerAdmin)
#admin_site.register(Customer, CustomerAdmin)
#admin_site.register(CatModule, CatModuleAdmin)