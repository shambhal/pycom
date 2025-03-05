from django import http

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.core import serializers
from service.forms import BookForm1
from .models import SSpecial, Service,Book
from django.template.loader import render_to_string
from datetime import datetime
from pycom.settings import CURRENCY_SETTINGS,AADS,MINUTE_GAP
from django.forms import model_to_dict
from django.core import serializers
from django.http import JsonResponse
from fm.models import ImageTool
from datetime import timedelta
from django.views.generic import FormView
from django.shortcuts import redirect
#from django.contrib.auth
from django.contrib.auth.models import User
import json
from cart.cart import Cart
#FormView.get_initial()
dayarr=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']  
def recd(n):
  #print(n)
 
   n1=datetime.now()

   dt1=n1+timedelta(days=n)
  
   return str(dt1).split(' ')[0] 
class Book1View(FormView):
  


  form_class=BookForm1
  template_name="book1_form.html"
  success_url="/"
 

       



  def get_initial(self):
       serv=Service.objects.get(id=1)
       #print(serv)
       dated='2022-01-01'
       slot='09:30'
       initial = super().get_initial()
       initial['dated']=dated
       initial['slot']=slot
       #initial['service']=Service.objects.get(id=1)
       initial['status']='AV'
       return initial
       return {dated:dated,slot:slot}
  def get(self,request,*args,**kwargs)  :
        dated='2022-01-01'
        slot='09:30'
        initial={}
        initial['dated']=dated
        initial['slot']=slot
        initial['service']=Service.objects.get(id=1)
        initial['status']='AV'
        context={

          'form':BookForm1(initial=initial),


        }
        return render(request,self.template_name,context)

  def getD_form(self,form_class=None):
       serv=Service.objects.get(pk=1)
       dated='2022-01-01'
       slot='09:30'
       form_class=BookForm1(initial={dated:dated})
 
         
  def form_valid(self, form) :
       #form['service']=Service.objects.get(id=1)
       #form['status']='AV'
       #console.log(self.request.)
       form.instance.service=Service.objects.get(id=1)
       form.instance.desc="jj"
       form.instance.save()
       return super().form_valid(form)     

# Create your views here.
def check(hrl,minl,hr,min):
     if(hrl<hr):
         return False
     if(hrl==hr and minl<min):
         return False
     return True
def _innerbook(item,user):
         gap=MINUTE_GAP
         date=item['date']
         slot=item['slot']
         n1=datetime.now()+datetime.timedelta(minutes=gap)
         n1=str(n1)
         hr=n1[11:13]
         min=n1[14:16]
         slarr=slot.split(":")
         hrl=slarr[0]
         minl=slarr[1]
         
         if(date<datetime.date.today()):
           return {'type':'error','msg':'old slot'}
         if(date==datetime.date.today() and not check(hrl,minl,hr,min)):
             return {'type':'error','msg':'old slot'}
                   
         status='UN'
         bs= Book()
         bs.dated=date
         bs.slot=slot
         bs.status=status
         bs.service=Service.objects.get(pk=item['service_id'])
         
         
        
         bs.user=user
         try:
          bs.save()
          return {'type':'success','msg':'Saved'}
         except Exception as e:
              return {'type':'error','msg':e.__str__}

def book_slot(request,service_id):
            context={}
            if(not request.POST['slot']):
                HttpResponse("data insufficient")
            if(not request.POST['date']):
                 HttpResponse("data insufficient")
            if(not request.POST['service']):
                 HttpResponse("data insufficient")     
            if(request.user.is_authenticated):
                logged=context['authenticated']=1
                '''ret=_innerbook({'slot':request.POST['slot'],'date':request.POST['date'],'service_id':request.POST['service']},request.user)
                if(ret['type']=='success'):
                  return redirect("customer:mybookings")
                else:
                  return JsonResponse({'error':1,'logged':logged})
                  '''
            else:
                 logged=context['authenticated']=0;    
            cart=Cart(request)
            cart.add(request.POST['date'],request.POST['slot'],service_id)

            return JsonResponse({'success':1,'logged':logged})
def __chunk():
     n1=datetime.now()
     template='chunks/calendar.html'
     n=AADS
     max_date=n1+timedelta(days=n)
     max_date=str(max_date).split(' ')[0]
     min_date=str(n1).split(' ')[0]
     c={'max_date':max_date,'min_date':min_date}
     return render_to_string(template,c)
    
def schedulebasic(request,service_id):
     today=datetime.now()
     arr=[]
     for i in range(0,3):
      arr.append( recd(i))
     context={}
     obj=get_object_or_404(Service,id=service_id)
     context=model_to_dict(obj)
     #print(obj.id)
     context['dates']=','.join(arr)
     context.update(CURRENCY_SETTINGS)
     #context=context.append(CURRENCY_SETTINGS)       
     #serializers.serialize('json'context)
     context['chunk']=__chunk()
     return render (request,'show_options.html',context)
def schedule(request,service_id):
     #print(service_id)
     sparr=[]
     rarr=[]
     barr=[]
     if('dated' in request.GET):
          dat=request.GET['dated']
     else:
         dat=str(datetime.today()).split(" ")[0]
     #serv=Service.objects.get(pk=service_id)
     ''' for daywise
     dt =datetime.strptime(date,'%Y-%m-%d')
     '''
     dt =datetime.strptime(dat,'%Y-%m-%d')
     n1=datetime.now()
   
     n=AADS
     max_date=n1+timedelta(days=n)
     max_date=str(max_date).split(' ')[0]
     min_date=str(n1).split(' ')[0]
     max_datef=datetime.strptime(max_date,'%Y-%m-%d')
     min_datef=datetime.strptime(min_date,'%Y-%m-%d')
     if dt >max_datef or dt <min_datef:
         
          routine={'hours':"00:00-00:00"}
          return JsonResponse({'routine':routine,'book':'','spoff':'','sp':''})
          #return JsonResponse({'routine': "hours": "00:00-00:00",,'book':obj2,'spoff':spoff,'sp':spstring})
    



    
     #dt.weekday
     wd=dt.weekday()
     #wd=wd-1
     #print(wd)
     #print(dat)
     #print(wd)
     #print(dayarr[wd])
     serv=Service.objects.get(pk=service_id)
     if serv!=None:
       s=model_to_dict(serv)
       #print(s)
       routine={'hours':s[dayarr[wd]],'off':serv.off}
     sps=[]  
     spstring=''
     spoff=''
     specialobj=SSpecial.objects.all().filter(service_id=service_id,sdate=dat)
     if(specialobj.exists()):
        for rec in specialobj:
           sps.append(rec.hours)
        spstring=','.join(sps)
        spoff=rec.off
     else:
       spstring=''
       
     bookings=[]
     obj=Book.objects.all().filter(service_id=service_id,dated=dat)
     if obj.exists():
          for rec in obj:
           bookings.append(rec.slot)
          
          obj2=','.join(bookings)
     else:
          obj2=''
    


     return JsonResponse({'routine':routine,'book':obj2,'spoff':spoff,'sp':spstring})
def _getTimed(vd):
    '''get time details
    '''
    vv=str(vd).split(" ")
    year=vv[0][0:4]
    month=vv[0][5:7]
    date=vv[0][8:10]
    '''print(year)
    print(month)
    print(date)
   '''
    hr=vv[1][0:2]
    mm=vv[1][3:5]
    return [year,month,date,hr,mm]



def ondate(req):
     pass

def _getDaydd(service_id,date1):
     obj2=get_object_or_404(Service,pk=service_id)
     

def detail(request,service_id):
     obj2=get_object_or_404(Service,pk=service_id)
     dt=datetime.now()
     
     days=[]
     dts=[]
     #print(dt.weekday())
     tempd=dt.strftime("%Y-%M-%d")
     days.append(dt.strftime("%a"))
     dts.append({'key':tempd,'val':dt.strftime('%b %d')})
     for i in range(1,5):
        dt2=dt+datetime.timedelta(days=i) 
        #print(dt2.date)
        tempd=dt2.strftime("%Y-%M-%d")
        days.append(str(dt2.strftime("%a")))
        dts.append({'key':tempd,'val':dt2.strftime('%b %d')})

    
     #print(days)
     #print(dts)
 
     return  HttpResponse(f'{dt}_{dt2}')
def detail2(request,service_id):

    obj2=get_object_or_404(Service,pk=service_id)
    ''' 
     get current date and then seek if it is special day or not
    '''
    dt=datetime.now()

    l=_getTimed(dt)
    gd=l[0]+'-'+l[1]+'-'+l[2]
    spobj=SSpecial.objects.filter(sdate=gd,service_id=service_id)
    #spobj=spobj.filter(service_id=service_id,sdate=gd)
    
    #print(obj2.sunday)
    if(spobj.exists()):
         
         #print(spobj[0].sunday)
         obj=spobj.first()
         return HttpResponse(serializers.serialize('json',spobj))
    else:
     obj=Service.objects.get(pk=service_id)
    #return HttpResponse(str(service_id))
    #print(obj)
    #print(obj)
    format={'sunday':obj.sunday,'off':obj.off,'slot':obj.slot,'monday':obj.monday,'tuesday':
    obj.tuesday,
    'wednesday':obj.wednesday,
    'thursday':obj.thursday,
    'friday':obj.friday,
    'saturday':obj.saturday

    }
    return JsonResponse(format)

def list(request):
    qs=Service.objects.all().order_by("seo_title")
    paginator = Paginator(qs, 5) # Show 25 contacts per page.

    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    pages={}
    for page in page_obj:
         #print(page.img)
         if(not page.img == None and not page.img==''):
                page.imurl=ImageTool.resize(page.img,220,220) 
         else:
           page.imurl=ImageTool.resize('placeholder.png',180,180) 
     
    return render(request, 'service_list.html', {'page_obj': page_obj})
