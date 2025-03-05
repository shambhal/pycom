from django.contrib import admin,messages
from django.http import HttpRequest
from django.http.response import HttpResponse
from .models import Order,OrderItems,OrderTotals
from config.helper import formatPrice
from .forms import OrderForm
from pycom.admin import admin_site
from django.template.loader import render_to_string
from config.helper import formatPrice
from django.db.models.query_utils import Q
class OrderAdmin(admin.ModelAdmin) :
 change_form_template=  "order_form.html"  
 def _getOrderSummaryChunk(self,order_id):
      user=Order.objects.get(pk=order_id)
      oi=OrderItems.objects.all().filter(order_id=user)
      ot=OrderTotals.objects.all().filter(order_id=user)
      '''items=[]
      for item in oi:
          print(item)
          items.append(item)
      '''
      template = "chunks/order_summary.html"
      c = {
                                                    "email":user.email,
                                                    'phone':user.phone,
                                                     'name':user.name,
                                                     'comment':user.comment,
                                                     'ot':ot,
                                                     'total':formatPrice(user.total),
                                                    
                                                     'items':oi
 
                                                    }
      return render_to_string(template, c)                                
 def change_view(self, request, object_id, form_url='', extra_context=None):
    
    #return HttpResponse("HELLO")
    obj=Order.objects.get(pk=object_id)
    if(request.method=='POST'):
       form=OrderForm(request.POST)
       if form.is_valid():
                   obj.status=form.cleaned_data['status'] 
                   obj.save()
                   messages.add_message(request, messages.INFO, "Updated.")
                   
    chunk= self._getOrderSummaryChunk(object_id)            
    extra_context={'chunk':chunk,'form':OrderForm(instance=Order.objects.get(pk=object_id))}
    return super().change_view(request, object_id, form_url, extra_context) 
 def get_queryset(self,request):
      queryset = super().get_queryset(request) 
      #print(queryset)
      queryset=queryset.filter( ~Q(status ='CREATED'))  
      return queryset
 list_display=['id','Total','Customer','Status']
 def Total(self,obj):
    return formatPrice(obj.total)
 def Customer(self,obj):
    return obj.name +' - '+obj.phone
 def Status(self,obj):
   return obj.status
 def od(sel,obj):
   ####order details
   pass
admin.site.register(Order,OrderAdmin)

admin_site.register(Order,OrderAdmin)
