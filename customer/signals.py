from django.db.models.signals import post_save
from django.dispatch import receiver
from  customer.models import CustomerOTP,Customer
from django.core.mail import EmailMessage
from pycom.settings import EMAIL_ADMIN,SITE_URL
from datetime import date
import logging
from django.template import Context
from django.template.loader import get_template
logger = logging.getLogger(__name__)
@receiver(post_save, sender=Customer)

def sendregmail(sender,instance,created,**kwargs):
    customer_id=instance.id
    customer_info=Customer.objects.get(pk=customer_id)
    if (customer_info):
         message = get_template("mail/register.html").render({
        'info': customer_info,
        'site_url':SITE_URL

    })
    mail = EmailMessage(
        subject='Thanks for registering with us',
        body=message,
        from_email=EMAIL_ADMIN,
        to=[customer_info.email],
        reply_to=[EMAIL_ADMIN],
    )
    mail.content_subtype = "html"
    return mail.send()              
@receiver(post_save, sender=CustomerOTP)

 
def sendmail(sender,instance,created,**kwargs) :
   book_id=instance.id
   binfo=CustomerOTP.objects.get(pk=book_id)
   #if not binfo.ex
   #   return 
   if(binfo):
    message = get_template("mail/otp.html").render({
        'otpinfo': binfo
    })
    mail = EmailMessage(
        subject='OTP',
        body=message,
        from_email=EMAIL_ADMIN,
        to=[binfo.email],
        reply_to=[EMAIL_ADMIN],
    )
    mail.content_subtype = "html"
    return mail.send()             
