from django.shortcuts import render,redirect
from checkout.models import CheckoutKey
from .models import COD
from orders.models import Order
from django.urls import reverse
from django.http import JsonResponse
# Create your views here.
def checkpayment(request):
     ot= request.POST.get('ott','')
     #print(ot)
     #return JsonResponse({'ot':ot})
     qs=CheckoutKey.objects.all().filter(key=ot)
     #print(qs.first())
     #print(qs)
     if(qs.exists()):
          record=qs.first()
          #print(record)
          #return JsonResponse(record)
          order_id=record.order_id
          obj=COD.objects.get(pk=1)
          ord=Order.objects.get(id=order_id)
          ord.status='COMPLETE'
          ord.save()
          obj={'redirect':reverse('checkout:success')}
      
          return JsonResponse(obj)
     obj2={'redirect':reverse('checkout:failure')}
     return JsonResponse(obj2)