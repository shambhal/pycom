from django.db.models.signals import post_save
from django.dispatch import receiver
from  orders.models import Order,OrderItems,OrderHistory,OS_CHOICES
from service.models import Book
from cart.models import AppCart
from datetime import date
import logging
from pycom.settings import EMAIL_ADMIN
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
logger = logging.getLogger(__name__)
@receiver(post_save, sender=Order)
def order_updated(sender, instance, created, **kwargs):
     #print("signal processed")
     #print(created)
     logger.warning(instance.status)
     logger.warning(kwargs)
     order_id=instance.id
     order=Order.objects.get(pk=order_id)
     if(order):
          items=OrderItems.objects.filter(order_id=order)
          #bh=BookHistory.objects.all.filter(order_id=order_id,status=instance.status).get()
          for item in items:
           
         
           '''''''''adding booking'''
           bo=Book.objects.all().filter(order_item_id=item.id)
           if(not bo.exists() and (order.status=='PROCESSING' )):
            bo2=Book(slot=item.slot,dated=item.dated,service=item.service)
            bo2.order_item_id=item.id
            bo2.desc=item.name
            bo2.order_id=instance.id
            bo2.name=order.name
            bo2.phone=order.phone
            bo2.email=order.email
            bo2.device_id=order.device_id
            bo2.status=instance.status
            bo2.save()
     oh=OrderHistory.objects.filter(order=order).last() 
     if oh is None:
        oh=OrderHistory(order=order,status=instance.status)   
        oh.save()
     else:
        if oh.status  != instance.status :  
           oh=OrderHistory(order=order,status=instance.status)   
           oh.save() 
@receiver(post_save, sender=Book) 
def sendmail(sender,instance,created,**kwargs) :
   book_id=instance.id
   binfo=Book.objects.get(pk=book_id)
   #if not binfo.ex
   #   return 
   if(binfo):
    message = get_template("mail/book.html").render(Context({
        'order': binfo
    }))
    mail = EmailMessage(
        subject='Appointment confirmation',
        body=message,
        from_email=EMAIL_ADMIN,
        to=[binfo.email],
        reply_to=[EMAIL_ADMIN],
    )
    mail.content_subtype = "html"
    return mail.send()             
@receiver(post_save, sender=Book) 
def clear_cart(sender,instance,created,**kwargs) :
   book_id=instance.id
   binfo=Book.objects.get(pk=book_id)
   #if not binfo.ex
   #   return 
   if(binfo):
    ap=AppCart.objects.filter(user_id=binfo.user_id,dated=binfo.dated,slot=binfo.slot,service=binfo.service).delete()
              
@receiver(post_save, sender=Order)
def order_success(sender, instance, created, **kwargs):
   order_id=instance.id
   #print("in order success")
   oinfo=Order.objects.get(pk=order_id)
   
   if not instance.status=='COMPLETE':
       return   
  
   
   oitems= OrderItems.objects.all().filter(order_id=order_id)
   #print(oitems)
   flag=True
   for oitem in oitems:
    try:
      bo=Book.objects.all().filter(order_item_id=oitem.id)
      if(not bo.exists()):
         bo=Book()
         bo.dated=oitem.dated
         bo.slot=oitem.slot
         bo.status='BOOKED'
         bo.user_id=oinfo.user_id
         bo.order_item_id=oitem.id
         bo.order_id=order_id
         bo.service_id=oitem.service_id
         bo.email=oinfo.email
         bo.desc=oitem.name
         bo.name=oinfo.name
         bo.phone=oinfo.phone
         bo.save()
      else:
         bo.status='BOOKED'
         bo.save()   
    except Exception as e: 
       flag=False  
   oh= OrderHistory()
   oh.dated=date.today()
   oh.order_id=order_id
   oh.status='COMPLETED' if flag==True    else 'Partially Completed'
   oh.save()