from django.shortcuts import render
from  .models import Payment
from pathlib import Path
from django.conf import settings
from django.http.response import HttpResponse,JsonResponse
from service.helpers import generateKey,simplegeneratekey
from orders.models import Order
from checkout.models import CheckoutKey
from payment.gateways import cod
import importlib
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def pmethods(request):
    pobjects=Payment.objects.all().filter(status=1).order_by('name')
    path1=Path(settings.BASE_DIR,'payment/gateways/')
    str='cod'
    package=Path(path1,str)
    #print(package.__fspath__)
    #print("pack down")
    #print(package.name)
    #mod=importlib.import_module('.cod.hooks', 'payment.gateways')
    #mod.getQuote()
    quotes=_getModifiedList(pobjects)

    #print(moda)
    context={'pm':pobjects}
    return render(request,"pmlist.html",context) 
@csrf_exempt
def webshowpay(request):
     oid=request.session.get('orderid',0)
     oinfo=Order.objects.get(pk=oid)
     #print(oinfo)
    
     
     if(not oinfo is None):
         ''' createkey '''
         print(oinfo)
         k=simplegeneratekey()
         pm=oinfo.payment_method
         chk=CheckoutKey.objects.create(order=oinfo,key=k,device_id=oinfo.device_id,customer_id=oinfo.user_id) 
         param="."+pm+'.hooks'
         #print(param)
         mod=importlib.import_module(param, 'payment.gateways')
         extra_content={'key':k,'web':1}
         #return HttpResponse("jello")
         return mod.paymentForm(request,extra_content)
@csrf_exempt
def showpay(request):
     #print(request)    
     oid=request.POST.get('order_id',0)
     #print(oid)
     oinfo=Order.objects.get(pk=oid)
     #print(oinfo)
     if(not oinfo is None):
         ''' createkey '''
         k=simplegeneratekey()
         pm=oinfo.payment_method
         chk=CheckoutKey.objects.create(order=oinfo,key=k,device_id=oinfo.device_id,customer_id=oinfo.user_id) 
         param="."+pm+'.hooks'
         print(param)
         mod=importlib.import_module(param, 'payment.gateways')
         extra_content={'key':k}
         return mod.paymentForm(request,extra_content)
@csrf_exempt
def cpayment(request):
      mod=request.POST.get('gateway')
      param2='payment.gateways.{}.views'.format(mod)
      module=importlib.import_module(param2)
      return module.checkpayment(request)         
def sort_order(tuple):
    return tuple['sort_order']
def _getModifiedList(pobjects):
    '''get modified list'''
    quotes=[]
    for pg in pobjects:
        param="."+pg.name+'.hooks'
        mod=importlib.import_module(param, 'payment.gateways')
        quotes.append(mod.getQuote())
        return quotes.sort(key=sort_order)
