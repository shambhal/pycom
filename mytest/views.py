from django.shortcuts import render
from django.views import View
import zoneinfo
from pycom.settings import GCI
from django.http import JsonResponse
from django.http.response import HttpResponse
from datetime import datetime,timedelta,date
from service.models import Service,SSpecial
from django.contrib.auth.models import User
from django.conf import settings
from config.helper import formatPrice
from customer.models import Customer
from information.models import Information
import importlib
import os.path
from datetime import date
from cart.models import AppCart
import service.helpers 
from django.shortcuts import reverse
from taxes.models import getTaxes,TaxHelper
from django.db.models.query_utils import Q
import babel.numbers
from orders.models import Order,OrderItems,OrderHistory
from service.models import Book
import base64
from django.views.decorators.csrf import csrf_exempt
'''from firebase_admin.messaging import Message
from fcm_django.models import FCMDevice
from firebase_admin import initialize_app
FIREBASE_APP = initialize_app()
def fcmtest(request):
     msg=Message(
     data={
        "Nick" : "Mario",
        "body" : "great match!",
        "Room" : "PortugalVSDenmark"
        },
     topic="Optional topic parameter: Whatever you want",)
     device = FCMDevice.objects.all().first()
     device.send_message(msg)
''' 
def glogin(request):
    c=request.POST.get('credential','')
    if(c!=''):
        print(c)
        data=base64.decode(c)
        h=data['header']
        p=data['payload']
        print(p)
        email=p['email']
        name=p['name']
        return JsonResponse({'email':email,'name':name})
def ctest(request):
    record=User.objects.filter(email='dem@gmail.com',is_staff=False)
    if(record.exists()):
        print(record.get().is_active)
        print( "yes")
        return HttpResponse("yes")
    else:
        print("no")
        return HttpResponse("No")
def gsignin(request):
    context={}
    context['gci']=GCI
    return render(request, 'front/gsignin.html', context)
def ilinks(request):
       infos=  Information.objects.filter(status=True).values_list("title","seo_url").order_by("sort_order")
       print(infos)
       return render(request, 'front/confirmpre.html', {'11':'11'})
def cptest(request):
     url=reverse('payment:payment-showpay')
     content={'order_id':'54','ott':'LIM9WYSB','action':url}
  
     return render(request, 'front/confirmpre.html', content)
def tz(request):
     url=reverse('payment:payment-showpay')
     content={'tz':zoneinfo}
     print(zoneinfo)
     return render(request, 'front/confirmpre.html', content)
def clearcart(request):
    user_id=43
    content={'order_id':'54','ott':'LIM9WYSB','action':''}
    objs=AppCart.objects.filter(user_id=user_id)
    for obj in objs:
       print('Date={} and slot={}'.format(obj.dated,obj.slot))
    return render(request, 'front/confirmpre.html', content)   
def makebookings(request):
   order_id=request.GET.get('order_id',0)
   
   oinfo=Order.objects.get(pk=order_id)
   
      

   
   oitems= OrderItems.objects.all().filter(order_id=order_id)
   print(oitems)
   flag=True
   for oitem in oitems:
    try:
      bo=Book()
      bo.dated=oitem.dated
      bo.slot=oitem.slot
      bo.status='BOOKED'
      bo.user_id=90
      bo.order_item_id=oitem.id
      bo.order_id=order_id
      bo.service_id=oitem.service_id
      bo.email=oinfo.email
      bo.desc=oitem.name
      bo.name=oinfo.name
      bo.phone=oinfo.phone
      bo.save()
    except Exception as e: 
       flag=False  
   oh= OrderHistory()
   oh.dated=date.today()
   oh.order_id=order_id
   oh.status='COMPLETED' if flag==True    else 'Partially Completed'
   oh.save()
      
def otk(request):
    k1=service.helpers.generateKey(5)
    print(k1)
def getNameQuote(request):
    '''param='paypal'
    param2='payment.gateways.{}.hooks'.format(param)
    module=importlib.import_module(param2)
    print(module.getLink())
    return JsonResponse({'hh':module.getLink()})
    '''
    '''currency_in_number = 3212834.2
    price=babel.numbers.format_currency(currency_in_number, 'INR', locale="en_IN")
    '''

    price=formatPrice('2500.89',None)
    taxes=getTaxes(300)
    taxh=TaxHelper()
    t=taxh.getTotals(300)
    print(taxes)
    return JsonResponse({'price':price,'taxes':t})
def calculateSlotPrice():
     pass
def getPrice(request):
    #monday is zero based
    date1="2023-10-18"
    service_id=request.GET.get('service_id')
    print("Service id="+service_id)
    #request.GET.get('date')
    serviceobj=Service.objects.get(pk=service_id)
    wkarr=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    #sspobj= SSpecial.objects.filter(service=serviceobj).filter(sdate=)
    # sspobj= SSpecial.objects.filter(service=serviceobj).get()
    dateobj=datetime.fromisoformat(date1)
    sspobj= SSpecial.objects.filter(service=serviceobj).filter(sdate=dateobj)
    if(sspobj.exists()):
       obj=sspobj.get()
       slotexpr=obj.hours
    else:
        wd=dateobj.weekday()
        slotexpr=getattr(serviceobj,wkarr[wd])
        #param=wkarr[wd]
        #slotexpr=serviceobj.param
    print(slotexpr)   
    #print( "hello")
    #return HttpResponse("hello")
    print(dateobj.weekday())
    #dt1=datetime.datetime()
    # sspobj=SSpecial.objects.select_related('service').filter(Q(service=serviceobj)).filter(sdate=date1).get()
    print(sspobj)
    wd=dateobj.weekday()
   
    varr=_slothours(slotexpr)
    price=_decodePrice({'varr':varr,'date':'2023-10-11','interval':1800,'selt':'10:30'})
    return JsonResponse({'success':1,'wd':wkarr[wd],'price':price})
def _decodePrice(obj):
   varr=obj['varr']
   date1=obj['date']
   selt=obj['selt']
   
   interval=obj['interval']
   datestring=date1+' '+"00:00:00"
   dtobj=datetime.strptime(datestring,'%Y-%m-%d %H:%M:%S')
   dtobj2=dtobj+timedelta(seconds=interval)
   print(dtobj2)
   selarr=selt.split(':')
   selh=selarr[0]
   selm=selarr[1]
   for node in varr:
      h1=node['h1']
      min1=node['min1']
      h2=node['h2']
      min2=node['min2']
      if h1==selh  and min1==selm:
         return node['price']
      if(selh>=h1 and selh<h2):
         return node['price']
      if(selh==h2 and (selm==min2 or selm<min2 )):
         return node['price']
   return -1
def _slothours(val):
   '''val=10:00-12:00#90,12:01-16:00#20'''
   strdate="2023-10-11"
   varr=[]
   #print(dt1)
   arr=val.split(',')
   for slot in arr:
    #print(slot)
    sarr=slot.split('#')
    price=sarr[1]
    slots=sarr[0]
    dslots=slots.split('-')
    h1a=dslots[0].split(':')
    h1=h1a[0]
    min1=h1a[1]
    
    h2a=dslots[1].split(':')
    h2=h2a[0]
    min2=h2a[1]
    varr.append({'price':price,'h1':h1,'min1':min1,'h2':h2,'min2':min2})
    #print(h1+' '+min1 +' '+h2 +' '+min2)
   #print(varr)
   return varr