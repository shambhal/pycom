from django.http.response import JsonResponse,HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from service.models import Book,Service
from config.helper import formatPrice,addAP,dateformat
from datetime import datetime,timedelta,date as date2
from django.contrib import messages
from django.views import View
from pycom.settings import MINUTE_GAP
from django.db.models import F, Q, When
from cart.cart import Cart
from api.utils.dayslots import Cartitem,DaySlots,CartPrice,ServiceSlotPrice
# Create your views here.
class CartView(View):
       def __getPrice(self,item):
         dated=item.dated
         slot=item.slot
         slot=slot.replace("AM",'')
         slot=slot.replace("A.M",'')
         slot=slot.replace("PM",'')
         slot=slot.replace(":",'')
         service_id=item.service_id
         ssp=ServiceSlotPrice()
         ssp.service_id=service_id
         ssp.dated=dated
         sched=ssp.calculateSchedule()
         for nod in sched:
             #print( nod)
             #return nod
             if(nod['key']==int(slot) and nod['av']==1):
              return nod['wprice']
         return -1   
       def get(self,request):
          cart=Cart(request)
          
          items=cart.getItems() 
          #print(items)
          #return HttpResponse("hello")
          cp=CartPrice()
          arr=[]
          key=0
          for item in items:
          
         
           ci=Cartitem(item['date'],item['slot'],item['price'],item['service_id'])
           #print("calling ci");
           item['price']=cp.getPrice(ci) 
           #print(item)
           if item['price'] ==-1:
               #cart.remove(item['key'])
               pass
           #return HttpResponse("hello")
           price=item['price']
           #return JsonResponse({'PRICE':price})
           if not price:
               continue
           if(price !=-1):
              serv=Service.objects.get(pk=item['service_id'])
               
              obj={'slot':addAP(item['slot']),'dated':dateformat(item['date']),'price':price,'fprice':formatPrice(price),'key':item['key'],'cart_id':item['key'],'name':serv.name,'quantity':1,
                  'options':[{'name':'Date :','value':str(item['date'])},{'name':'Slot','value':item['slot']}]
                  }
                     
              arr.append(obj)
          subtotal=cp.getSubtotal(arr)    
          cp.calculateTotals()
          totals=cp.getTotals()
          #print(totals)
          return render(request,'cartlist.html',{'items':arr,'subtotal':subtotal,'totals':totals})

'''def showCartold(request):   
    cart=Cart(request)
    items=cart.getItems()
    for item in items:
        #print(item.service_id)
        #print("item in item")
        #print(item['service_id'])
        serv=Service.objects.get(pk=item['service_id'])
        item['service']=serv
    context={'items':items,'auth':request.user.is_authenticated}
    #print("printing items")
    #print(items)
    total=cart.getSubtotal()
    context['total']=total
    return render(request,"cartlist.html",context)

'''

def remove(request):
    cart=Cart(request) 
    token=request.POST['key'] 
    cart.remove(token) 
    
    return JsonResponse({'success':1})
def check(hrl,minl,hr,min):
     if(hrl<hr):
         return False
     if(hrl==hr and minl<min):
         return False
     return True
def bookpre(request):
    gap=MINUTE_GAP
    '''if(not request.user.is_authenticated):
         request.session['redirect']=reverse("cart:book-cart")
         return redirect(reverse("customer:customer-login"))
    '''
    cart=Cart(request)
    items=cart.getItems()  
    if(len(items)<1):
         return redirect(reverse('cart:cart'))
    n1=datetime.now()+timedelta(minutes=gap)
    n1=str(n1)
    hr=n1[11:13]
    min=n1[14:16]
    for index,item in enumerate(items):
         date=item['date']
         #print(date)
         slot=item['slot']
         #print(datetime.date.today())
         slarr=slot.split(":")
         hrl=slarr[0]
         minl=slarr[1]
         key=item['key']
         #date2.
         
         if(date2.fromisoformat(date)<date2.today()):
            print(date2.fromisoformat(date))
            print(date2.today())
            print(f"should remove key {index}")
            cart.remove(index)
         if(date==date2.today() and not check(hrl,minl,hr,min)):
             print("removing cart")
             cart.remove(key)

         '''' for going for payment gateway methods'''
    return redirect(reverse('checkout:login'))     
def booknotgood(request):
     #List msgs=[]
     gap=MINUTE_GAP
     '''if(not request.user.is_authenticated):
         request.session['redirect']=reverse("cart:book-cart")
         return redirect(reverse("customer:customer-login"))
     '''
     #if('payment_method' not in request.session   ):
     #    pass
     cart=Cart(request)
     items=cart.getItems()  
     if(len(items)<1):
         return redirect(reverse('cart:cart'))

     n1=datetime.now()+timedelta(minutes=gap)
     n1=str(n1)
     hr=n1[11:13]
     min=n1[14:16]
     for item in items:
         date=item['date']
         print(date)
         slot=item['slot']
         #print(datetime.date.today())
         slarr=slot.split(":")
         hrl=slarr[0]
         minl=slarr[1]
         key=item['key']
         #date2.
         
         if(date2.fromisoformat(date)<date2.today()):
            continue
         if(date==date2.today() and not check(hrl,minl,hr,min)):
             continue
                   
         '''status='UN'
         bs= Book()
         bs.dated=date
         bs.slot=slot
         bs.status=status
         bs.service=Service.objects.get(pk=item['service_id'])
         
         
        
         bs.user=request.user
         try:
          bs.save()
          messages.add_message(request,messages.INFO,'Saved your appointemet {0} {1}'.format(date,slot))
          cart.remove(key)
         except Exception as e:
           #msgs.append('Error in saving %s',date,slot)
           messages.add_message(request,messages.ERROR,'Error in saving {0} {1}'.format(date,slot))
     return render(request,'saved.html')
     '''

          

      