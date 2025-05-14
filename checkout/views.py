from django.shortcuts import render,redirect
from orders.models import Order
from config.helper import formatPrice,dateformat,addAP
from orders.models import Order,OrderItems,OrderTotals
from django.template.loader import render_to_string
from pycom.settings import fbl,gl
from django.core.checks import messages
from pycom.settings import GCI
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
#from service.helpers import generateKey
from time import time  
from django.urls import reverse
from pycom.settings import SITE_URL
from django.middleware.csrf import get_token
from checkout.signals import create_ott_signal
import importlib 
from cart.cart import Cart
from api.utils.dayslots import Cartitem,DaySlots,CartPrice,ServiceSlotPrice
from service.models import Book,Service
import json
from .forms import  AppointeeForm
from django.views.generic import FormView
from django.http.response import HttpResponse,JsonResponse
from django.views import View
from payment.models import Payment
from payment.views import webshowpay 
# Create your views here.
def pms(request):
    #
    obs=Payment.objects.all().filter(status=1)
    pms=[]
    if(obs.exists()):
      pms=list(obs)
   
    '''for pm in pms:
        print(pm.code)
    '''    
    return render(request,'chunks/pmlist.html',{'pms':pms})  
def createOTT(request):
    
    order_id=request.POST['order_id']
    '''oinfo=Order.objects.get(pk=order_id)
    if(oinfo):
        device_id=oinfo['device_id']
        customer_id=oinfo['customer_id']
        k=generateKey(order_id)
   '''
    create_ott_signal.send(None,order_id=order_id)
def payment_view(request):
    #key=request.POST['order_id']
    param2='payment.gateways.{}.hooks'.format('cod')
    module=importlib.import_module(param2)
    return module.paymentForm(request)
def success(request):
      return render(request,'result.html',{'result':'success'})
def fail(request):
   return render(request,'result.html',{'result':'fail'})
def apdetails(request):
     ap= request.session.get('appointee','') 
     return render(request,'chunks/apdetails.html',{'ap':ap})
class CheckoutCartView(View):
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
           item['price']=cp.getPrice(ci) 
           #print(item)
           if item['price'] ==-1:
               cart.remove(item['key'])
           #return HttpResponse("hello")
           price=item['price']
             #return JsonResponse({'PRICE':price})
            
           if(price !=-1):
              serv=Service.objects.get(pk=item['service_id'])
              #print("serv object down")
              #print(serv.name)
              obj={'slot':addAP(item['slot']),'dated':dateformat(item['date']),'price':price,'fprice':formatPrice(price),'cart_id':item['key'],'name':serv.name,'quantity':1,
                  'options':[{'name':'Date :','value':str(item['date'])},{'name':'Slot','value':item['slot']}]
                  }
                     
              arr.append(obj)
          subtotal=cp.getSubtotal(arr)    
          cp.calculateTotals()
          totals=cp.getTotals()
          #print(totals)
          return render(request,'chunks/cartdetails.html',{'items':arr,'subtotal':subtotal,'totals':totals})

'''def cartdetails(request):
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
        return render(request,'chunks/cartdetails.html',context)

'''        
class APView(View):
    def get(self,request):
        ap= request.session.get('appointee','')  
        if ap=='':
            form=AppointeeForm()
        else:
            apdata=ap
            form=AppointeeForm(apdata)
        context={'form':form}    
        return render(request,'apform.html',context) 
    def post(self,request):
         form=AppointeeForm(request.POST)
         if(form.is_valid()):
            request.session['appointee']=request.POST
            return redirect(reverse('checkout:checkout'))
         
                
         return render(request,'apform.html',{'form':form})       

def getAP(request):
    pass

def postAp(request):
     form=AppointeeForm(request.POST)
     if(form.is_valid()):
            request.session['appointee']=request.POST
            return JsonResponse({'success':1})
     
     else:
         
         return JsonResponse({'errors':form.errors})
def showPayments(request) :
    pass    
def social(request):
     sociala=list()
     if fbl:
       sociala.append('fb')
     if gl:
      
       sociala.append('gl')

     template = "chunk/social.html"
   
     c = {
                                                    
             'sociala':sociala ,
             'gci':GCI,
            'glogin_uri':request.build_absolute_uri(reverse('customer:customer-gloginval')),
             'csrf_token': get_token(request),

         }
     return render_to_string(template, c)  
class CheckoutLogin(View):
    def post(self,request):

        

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user.email)
            if user is not None:
                login(request, user)
                messages.Info(request, f"You are now logged in as {username}.")
                if request.session['redirect']:
                  rd=request.session['redirect']
                  del request.session['redirect']  
                  return redirect(rd)  
                return redirect("/")
            else:
                messages.error(request,"Invalid username or password.")
                return redirect(reverse('checkout:login'))
        else:
            messages.error(request,"Please write credentials correctly.")
            return redirect(reverse('checkout:login'))
    def get(self,request):
       soc=social(request)
       if(request.customer.is_authenticated):
         redirect(reverse('checkout:checkout')) 
       rd=request.session.get('redirect','')
       if  rd=='':
           request.session['redirect']=reverse('checkout:checkout')
           
       context={'csrf_token': get_token(request),
                 'form': AuthenticationForm(),
                 'gci':GCI,
                 'social':soc,
                 'glogin_uri':request.build_absolute_uri(reverse('customer:customer-gloginval')),
              
                 }


       
       return render(request,'checkoutpre.html',context) 
  
class CheckoutView(View):
    


    def get(self,request):
        if(not request.customer.is_authenticated):
           return redirect('checkout:login')
        ap=request.session.get("appointee",'')
        if ap == '' :
            return redirect('checkout:appointee')
        csrf_token = get_token(request)
        return render(request,'checkout.html',{'csrf_token':csrf_token})
class PaymentView(View):
        def __saveTotals(self,order_id,arr):
           #arr=json.loads(arrstring)
           order=Order.objects.get(pk=order_id)
           OrderTotals.objects.filter(order_id=order).delete()
           for node in arr :
               oi=OrderTotals.objects.create(title=node['name'],order_id=order,total=node['total'])
        def __saveitems(self,order_id,arr):
           #arr=json.loads(arrstring)
           #print(arr)
           order=Order.objects.get(pk=order_id)
           OrderItems.objects.filter(order_id=order).delete()
           for node in arr:
               #node.order=order_id
               oi=OrderItems()
               oi.order_id=order
               oi.name=node['name']
               oi.slot=node['slot']
               oi.price=node['price']
               oi.dated=node['dated']
               oi.service=node['service']
               oi.save()
        def _createOrder(self,request):
         print("in create order")
         cart=Cart(request)
         items=cart.getItems()
         cp=CartPrice()
         arr=[]
         gtotal=0
         for item in items:
             ci=Cartitem(item['date'],item['slot'],item['price'],item['service_id'])
             item['price']=cp.getPrice(ci) 
             #print(item)
             if item['price'] ==-1:
               cart.remove(item['key'])
             price=ci.price
             if(price !=-1):
                serv=Service.objects.get(pk=item['service_id'])
               
                obj={'slot':item['slot'],'dated':item['date'],'price':price,'fprice':formatPrice(price),'cart_id':item['key'],'name':serv.name,'quantity':1,'service':serv,
                  'options':[{'name':'Date :','value':str(item['date'])},{'name':'Slot','value':item['slot']}]
                  }
                     
                arr.append(obj) 
                subtotal=cp.getSubtotal(arr)    
                cp.calculateTotals()
                totals=cp.getTotals()
                gtotal=cp.grandtotal
         ap=request.session['appointee']
         comment=request.POST.get('comment','')
         tarr={
             
         'phone':ap['mobile'],
         'device_id':'web',
         'email':ap['mobile'],
         'name':ap['name'],
          'user_id':0,
         'total':gtotal,
         'payment_method':request.POST['payment'],
         'email':ap['email'],
         'status':'CREATED',
         'comment':comment

         }
         #print(tarr)
         ord=Order.objects.create(**tarr)
         orderid=ord.id
         request.session['orderid']=orderid
         self.__saveitems(orderid,arr)
         self.__saveTotals(orderid,cp.getTotals())
        def post(self,request):

            if(not 'payment' in request.POST):
                return JsonResponse({'error':'Please select payment Method'})
                
                #return self.get(request)
            self._createOrder(request)
            pm=request.POST['payment']
            return webshowpay(request)