from payment.models import Payment
from .models import COD
from django.shortcuts import render
from django.urls import reverse
def getQuote():
        
        obj=COD.objects.get(pk=1)
        if(not obj):
         return {}
        if(obj.status==0):
          
          return {}
        
        context={'name':'cod','title':'Cash on Visit','sort_order':obj.sort_order}
        return context
def getLink():
    ob= obj=COD.objects.get(pk=1)  
    if(ob is None) : 
     return '/myadmin/cod/cod/add'
    else:
       return '/myadmin/cod/cod/1/change'
    
def paymentForm(request,extra):
          action='payment/checkout/success'
          action=reverse('payment:checkpay')
          if 'web' in extra:
            return render(request,'front/webpayment.html',{'ott':extra['key'],'action':action})
          else:    

           return render(request,'front/payment.html',{'ott':extra['key'],'action':action})