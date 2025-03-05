from django.dispatch import Signal
from orders.models import Order
from .models import CheckoutKey
from service.helpers import generateKey
create_ott_signal=Signal()
def create_ott(sender,order_id,**kwargs):
    oinfo=Order.objects.get(pk=order_id)
    if(oinfo):
        device_id=oinfo['device_id']
        customer_id=oinfo['customer_id']
        k=generateKey(order_id)
        CheckoutKey.objects.filter(order=oinfo).delete()
        chk=CheckoutKey.objects.create(order=oinfo,key=k,device_id=oinfo.device_id,customer_id=oinfo.customer_id)