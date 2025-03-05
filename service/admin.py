
from django.contrib import admin,messages
from django.http import HttpRequest
from pycom.admin import admin_site 
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.http.response import HttpResponse, HttpResponseRedirect
from datetime import date
from django.utils.translation import gettext_lazy as _
#from pycom.settings import get_app_list
from pycom.settings import MEDIA_ROOT, MEDIA_URL, MEDIA_STATIC
from fm.models import ImageTool,FaltuModel as fm2
from .models import Service,SSpecial,Simg,Book,BookHistory
from .forms import SServiceForm, ServiceForm,BookEditForm,RescheduleForm

from django.urls import path,reverse
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, render
from django.conf import settings
import os
from PIL import Image
#from django-thumbnails

def resize(obj,width,height):
    path=obj.img.path
    name, extension = os.path.splitext(obj.img.name)
    basename= os.path.basename(path)
    fname='cache/'+name+'-'+str(width)+'x'+str(height)+extension
    if(os.path.exists(MEDIA_ROOT+fname)):
        return MEDIA_URL+fname
    outputsize=(width,height)
    im=Image.open(path)
    im.thumbnail(outputsize)
    im.save(MEDIA_ROOT+fname)
    return MEDIA_URL+fname

class BookAdmin(admin.ModelAdmin)  :
    #admin.AdminSite.get_app_list
        
    def reschedule(self,request,bookid):
        if(request.method=='POST'):
            bobj=Book.objects.get(pk=bookid)
            if(bobj.status=='CANCELLED'):
                bobj.status='BOOKED'
                form=RescheduleForm(request.POST)
                bobj.dated=form.cleaned_data['dated']
                bobj.slot=form.cleaned_data['slot']
                #bobj.dated=
               
                try:
                 bobj.save()
                 messages.add_message(request, messages.INFO, "Rescheduled Appointment")  
                except:
                    messages.add_message(request, messages.ERROR, "Error in rescheduling Appointment")   
        else:
              bobj=Book.objects.get(pk=bookid)
              form=RescheduleForm(instance=bobj)
              
        #print(request.user)
        app_list = self.admin_site.get_app_list(request)
        context = {
        'form': form,
        'is_popup':0,
         'user':request.user,
         'available_apps':app_list,
        'is_nav_sidebar_enabled':1

        
          }
        return render(request, 'admin/reschedule.html', context)   
    def appointhistory(self,request,bookid):
         records=[]
         if(bookid is not None):
             book=Book.objects.get(pk=bookid)
             if(book):
                flag=BookHistory.objects.all().filter(book_id=book).exists()
                if flag:
                    records=BookHistory.objects.all().filter(book_id=book).order_by('-dated')
                    #app_list = admin.AdminSite.get_app_list(request)
                    context={'records':records,'info':book,'app_list':app_list}
                    return render(request, 'admin/book_history.html', context)   
                else :
                    #app_list = admin.AdminSite.get_app_list(self,request)
                    app_list = self.admin_site.get_app_list(request)
                    app_list_mod=[]
                    remove=['fm','Tsettings','Fm']
                    for app in app_list:
                        if(not app['name'] in remove):
                            app_list_mod.append(app)
                    #print(app_list)
                    #print(app_list)
                    #print (app_list)
                    #context=admin.AdminSite.get_context_data()
                    #context['records']=records
                    context={'records':records,'info':book,'available_apps':app_list_mod}
                    return render(request,'admin/book_history.html', context)
         return render(request,'admin/content.html',{'content':'Record Not Found'})     
     
    def get_urls(self):
        urls = super().get_urls()
        
        urls.remove(urls[1])
       # view_name = 'whrs_add'
        my_urls= [
            path('reschedule/<int:bookid>',self.admin_site.admin_view(self.reschedule),name="reschedule_appointment"),
            path('appointhistory/<int:bookid>',self.admin_site.admin_view(self.appointhistory),name="appointmenthistory"),
        ]
       
        #print(my_urls);
        #return urls
        return urls+my_urls
    def aphistory(self,obj):
       url=reverse('myadmin:appointmenthistory',kwargs={'bookid':obj.id})
      
       #return 'lupchup'
       return format_html("<a href='{}'>History</a>",url)
    #def writereschedu
    def reschedulelink(self,obj):
        if(obj.status=='CANCELLED' or obj.status=='BOOKED'):
          url2=reverse('myadmin:reschedule_appointment',kwargs={'bookid':obj.id})
          return format_html("<a href='{}'>Reschedule</a>",url2)
        else:
            return ''   
        
    list_display=['dated','slot','status','aphistory','reschedulelink']
    change_form_template=  "admin/book_form.html"  

    def change_view(self, request, object_id, form_url='', extra_context=None) :
        
       
        obj=Book.objects.get(pk=object_id)
        if request.method == "POST":
              form=BookEditForm(request.POST)
              if form.is_valid():
                   obj.status=form.cleaned_data['status'] 
                   obj.save()
                   messages.add_message(request, messages.INFO, "Updated.")
                   bhobj=BookHistory()
                   bhobj.dated=date.today()
                   bhobj.book_id=obj
                   bhobj.status=obj.status
                   bhobj.info=form.cleaned_data['extra_info']
                   bhobj.save()
                   messages.add_message(request,message="Updated Record",level=3)
        extra_context={'form':BookEditForm(instance=Book.objects.get(pk=object_id))}
        return super().change_view(request, object_id, form_url, extra_context)
    def get_queryset(self, request):
        oid=request.GET.get('order_id',0)
        
        qs = super().get_queryset(request)
        if(oid==0):
        
            return qs
        return qs.filter(order_id=oid) 
    def changelist_view(self,request,extra_context=None):
        oid=request.GET.get('order_id',0)
        if(oid!=0):
           extra_context={'title':'Appointments for order {}'.format(oid)}
        return super(BookAdmin,self).changelist_view(request,extra_context)
#@admin.register(Simg)
class SimgAdming(admin.ModelAdmin):
    list_display = ['image_tag']
    readonly_fields = ['image_tag']
    def image_tag(self,obj)->str:
       #fetch_thumbnails([obj.img],['small','large'])
       #print(obj.img.name)
       #print("path is ")
       #print(obj.img.path)
       #name, extension = os.path.splitext(obj.img.name)
       #print(name)
       #print(extension)
       #print(obj.id)
       #print(os.path.basename(obj.img.path))
       im=resize(obj,250,250)
       return format_html("<img src='{}'",im)   

class ServiceAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change): 
      
        if(request.method=='POST'):
           if('img' in request.POST):
               #form['img']=request.POST['img']
               obj.img=   request.POST['img']  
               obj.name=request.POST['seo_title'] 
        return super().save_model(request, obj, form, change)
    def change_view(self, request, object_id, form_url='', extra_context={}) :
        
       
        obj=Service.objects.get(pk=object_id)
       

        if request.method == "POST":
              form=ServiceForm(request.POST)
              if form.is_valid():
                   #obj.status=form.cleaned_data['status'] 
                   obj.save()
                   messages.add_message(request, messages.INFO, "Updated.")
        thumb=self.writeThumb(obj)
        extra_context={'thumb':thumb,'image':obj.img,'form':ServiceForm(instance=Service.objects.get(pk=object_id))}
        return super().change_view(request, object_id, form_url, extra_context)
    def save_fform(self, request, form, change):
      
        if(request.method=='POST'):
           if('img' in request.POST):
               form.img=request.POST['img']
         
        return super().save_form(request, form, change)
    change_form_template=add_form_template=  "admin/add_form.html"  
    list_display=['name','writeimage','slot','writeSpecialDaysLink']
    def writeThumb(self,obj):
        ffolder=MEDIA_ROOT
        ffolder.replace("\\",'/')
        if(not obj.img):
         img='placeholder.png'
        
        else:
         img=obj.img 
        
        if(os.path.exists(ffolder+img)) :
           pat= ImageTool.resize(img,100,100)
           return pat# format_html("<img src='{}'/>",pat)
        else:
          return ''
    def writeimage(self,obj):
        ffolder=MEDIA_ROOT
        ffolder.replace("\\",'/')
        if(not obj.img):
         img='placeholder.png'
        
        else:
         img=obj.img 
        
        if(os.path.exists(ffolder+img)) :
           pat= ImageTool.resize(img,100,100)
           return format_html("<img src='{}'/>",pat)
        else:
          return ''
        
        print ("folder is {} and imag is {}", folder,img)
        return ''
    def get_changeform_initial_data(self, request):
         defdata={'slot':'1800',
         'monday':'10:00-18:00#20',
         'tuesday':'10:00-18:00#20',
         'wednesday':'10:00-18:00#20',
         'thursday':'10:00-18:00#20',
          'friday':'10:00-18:00#20',
          'saturday':'10:00-16:00#50',
          'sunday':'00:00-00:00',
          'off':'12:30-13:30',
          'name':'Service 1',
          'seo_title':'Service 1',
          'seo_description':'Service 1'
         }
       
         return defdata
         
    #add_form_template=
    '''def add_view(self,request):
       return HttpResponse("HELLO")
    '''
    def __str__(self) -> str:
       return self.name
    def writeSpecialDaysLink(self,obj):
        
        return format_html("<a href='../sspecial/?service__name={}'>{}</a>",obj.name,obj.name+' Special Days')
    def change_viehw(self, request, object_id, form_url='', extra_context={}) :
       
       #9782432570
        obj=Service.objects.get(pk=object_id)
        print(obj.img+ 'is the image')
       
        #return super().change_view(request, object_id, form_url, extra_context)
    def add_view(self,request,form_url='',extra_content=None):
         thumb=ImageTool.resize('placeholder.png',100,100)
         burl=reverse('admin:commonfilemanager') 
         furl=request.build_absolute_uri(burl)
         #furl='http://localhost:8000/admin/fm/common_filemanager'
         defdata={'slot':'1800',
         'monday':'10:00-18:00#20',
         'tuesday':'10:00-18:00#20',
         'wednesday':'10:00-18:00#20',
         'thursday':'10:00-18:00#20',
          'friday':'10:00-18:00#20',
          'saturday':'10:00-16:00#50',
          'sunday':'00:00-00:00',
          'off':'12:30-13:30',
          'name':'Service 1',
          'seo_title':'Service 1',
          'seo_description':'Service 1'
          
         }
         extra_content={'thumb':thumb,
         'furl':furl,
         'form':ServiceForm(initial=defdata)}
         return super().add_view(request,form_url,extra_content)
        
    '''def get_form(self, request, obj=None, change=False, **kwargs):
             print("in service form")
             if(obj==None):
              initial={'slot':8600,'sunday':'00:00','monday':'10:00-18:00'}
              self.form=ServiceForm
             else:
                 self.form=ServiceForm 
             return super().get_form(request, obj,change,**kwargs)
    '''          

    '''def get_urlss(self):
        urls = super().get_urls()
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        print(view_name)
        urls.remove(urls[1])
       # view_name = 'whrs_add'
        my_urls= [
           path('sadd',self.writeSpecialDays)
        ]
        print(my_urls)
        return my_urls+urls
   '''
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('my_view/<int:size>', self.admin_site.admin_view(self.my_view))
        ]
        
        return custom_urls + urls
       
    def my_view(self,request,size):
        #self.model.objects.all().update(font=size)
        obj= get_object_or_404(Service,
            pk=size
        )
        if(request.method=='POST'):
            form=SServiceForm(request.POST)
            if(form.is_valid()) :
             post = form.save(commit=False)
             #print(post)
             #console.log
             post.service=Service.objects.get(pk=size)
             print("form is valid")
             post.save()
             return HttpResponseRedirect("../service/service")
            else:
               print(form.errors)
            context = {
        'form': form,
         'service_name':obj.name,
         'errors':form.errors
          }
            return render(request, 'admin/sservice.html', context)
        else:    
        #self.message_user(request,'font size set successfully')
        #return HttpResponseRedirect('../')
         form=SServiceForm(initial={'service':Service.objects.get(pk=size)})    
         context = {
        'form': form,
         'service_name':obj.name
          }
        return render(request, 'admin/sservice.html', context)

admin.site.register(Service,ServiceAdmin)
admin_site.register(Service,ServiceAdmin)     
admin_site.register(Book,BookAdmin)   

class SSpecialAdmin (admin.ModelAdmin):
    
   list_filter=['service__name','service__id']
   add_form_template='admin/sservice.html'
   def getBlocks():
       blocks=[{'name':'Home','url':'..'},
               {'name':'Service','url':'../service/service'}
               ]
   def add_view(self, request, form_url='', extra_context=None) :
        sid=request.GET.get('sid',0)
        if(not request.method =='POST'):
         initial={}
         if(not sid ==0)  :
             initial['service']=Service.objects.get(pk=sid)
         form=SServiceForm(initial=initial)
        else:
          form=SServiceForm(request.POST)   
        extra_context = extra_context or {}
        extra_context = {
         'form': form,
        
        
          }
        ret=super().add_view(request, form_url, extra_context) 
       
        return super().add_view(request, form_url, extra_context)    
   '''def adds_view(self,request,form_url='', extra_context=None):
         cfl=request.GET.get('_changelist_filters','')
         print(cfl)
         
         if(cfl !='' and request.method!='POST'):
                form=SServiceForm()
                context = {
         'form': form,
         'service':Service.objects.get(pk=1),
        
          }
         return render(request, 'admin/sservice.html', context)

         service=Service.objects.get(pk=1)
         extra_context={'service':service}
         return super(SSpecialAdmin, self).add_view(request, form_url, extra_context)
         '''
   def edit_view(self,request,sid):
        #self.model.objects.all().update(font=size)
        print("edit view called")
        obj= get_object_or_404(SSpecial,
            pk=sid
        )
        #print("sid is "+str(sid))
        #print(obj)
       # return HttpResponse("HELO")
        if(request.method=='POST'):
            form=SServiceForm(request.POST,instance=obj)
            if(form.is_valid()) :
             post = form.save(commit=False)
             #print(post)
             #console.log
             #print(obj.service_id)
             #post.service=Service.objects.get(obj.service_id)
             #print("form is valid")
             post.save()
             #return HttpResponseRedirect("../service/service")
            else:
               print(form.errors)
            context = {
         'form': form,
         'service_name':obj.service.name,
         'errors':form.errors
          }
            return render(request, 'admin/sservice.html', context)
        else:    
        #self.message_user(request,'font size set successfully')
        #return HttpResponseRedirect('../')
        
        # return HttpResponse("hello")
         form=SServiceForm(instance=obj)    
         context = {
        'form': form,
         'service_name':obj.service.name
          }
        return render(request, 'admin/sservice.html', context)
  
       
   list_display=['date_cat','edit']
   @admin.display(description="Category-date")
   def date_cat(self,obj):
    return obj.service.name+'- '+str(obj.sdate)
   def edit(self,obj):
       #return format_html("<a href='"+service_sspecial_change
       #print(reverse('myadmin:service_sspecial_change',args={obj.id}))
       url1=reverse('myadmin:service_sspecial_change',args={obj.id})
       #print((reverse("admin:{}_{}_change".format(obj._meta.app_label, obj._meta.model_name))))
       return format_html("<a href='{}'><i class='fa fa-edit'></i></a>".format(url1))
       return format_html("<a href='../sspecial/edit_view/{}'>Edit</a>",obj.id)
   list_display_links=None
   def get_urls(self):
        urls = super().get_urls()
        #print(urls)
        #urls.remove(urls[1])
        custom_urls = [
            path('edit_view/<int:sid>', self.admin_site.admin_view(self.edit_view))
        ]
        #print("urls are")
        #print(urls)
        return urls
        return urls +custom_urls
    
admin.site.register(SSpecial,SSpecialAdmin)
admin_site.register(SSpecial,SSpecialAdmin)