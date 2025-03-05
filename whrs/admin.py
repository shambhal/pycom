from django.contrib import admin
from .models import work,Special
from django.urls import path
from django.shortcuts import render

from . import views
# Register your models here.
from  whrs.forms import SettingsForm

class SpecialAdmin(admin.ModelAdmin):
    list_display = ('sdate', 'sunday')
admin.site.register(Special,SpecialAdmin)
@admin.register(work)
class WorkAdmin(admin.ModelAdmin):
    #add_form_template="time/settings.html"
    
        
    def get_urls(self):
        urls = super().get_urls()
        
        urls.remove(urls[1])
       # view_name = 'whrs_add'
        my_urls= [
            path('add',self.my_custom_view,name="whrs_work_add"),
        ]
        #print(my_urls);
        return my_urls
    def my_custom_view(request,id):
        #print("in my_custom_view")
        if(request.method=='POST'):
         form=SettingsForm(request.POST)
         if(form.is_valid):
             # work_instance=work(request.POST);
             # print(request.POST)
              #print(work_instance);
            
              #work_instance.sunday="12-11";
              form.save()
              context = {
        'form': form,
         'saved':1
          }
              return render(request, 'time/settings.html', context)
            
        else :
         work_i=work.objects.get(id=1)
         
         if(work_i):
          initial={'sunday':'10:00-16:00#5',
                  'monday':'10:00-12:00#5',
                  'tuesday':'10:00-12:00#5',
                  'wednesday':'10:00-12:00#5',
                  'thursday':'10:00-12:00#5',
                  'friday':'10:00-12:00#5',
                  'saturday':'10:00-12:00#5',
                  }
          
          form=SettingsForm(initial=initial)
         else :
          form=SettingsForm(work_i)    
         context = {
        'form': form,
       
          }
         return render(request, 'time/settings.html', context)
   
