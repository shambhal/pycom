from payment.models import Payment
from .models import Paypal
from django.shortcuts import  render
from django import template
from django.template import Context
def getQuote(request ):
        
        obj=Paypal.objects.get(pk=1)
        t = template.loader.get_template('test.html')
        #c=Context({'test':'madhuri'})
        return t.render({'test':'jhu'})
        if(not obj):
         return {}
        if(obj.status==0):
          
          return {}
        
        context={'name':'paypal','title':'Paypal','sort_order':obj.sort_order}

def getLink():
    ob= obj=Paypal.objects.get(pk=1)  
    if(ob is None) : 
     return '/myadmin/paypal/paypal/add'
    else:
       return '/myadmin/paypal/paypal/1/change'