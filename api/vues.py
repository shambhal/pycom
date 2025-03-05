from django.http.response import HttpResponse

from rest_framework.views import APIView

from customer.models import Customer,CustomerOTP
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import AccessToken
from service.helpers import generateOTP
from .views import isGOC
from cart.models import AppCart
from  service.models import Service

from orders.models import Order
#from fcm_django.models import FCMDevice
'''
class FCMTokenView(APIView):
     def post(self,request,*args,**kwargs):
          device_id=request.data['device_id'] if request.data['device_id'] else ''
          arr={
               'registration_id':request.data['token_id'],
               'active':1,
                'device_id':device_id,
                'user_id':request.data['user_id'],
                'name':'',

             }
          
          device=FCMDevice()
          device.registration_id=arr['registration_id']
          device.active=1
          device.user=User.objects.get(pk=arr['user_id'])
          device.name=''
          device.device_id=arr['device_id']
          device.save()
          return JsonResponse({'success':1})
         
def schedule(request,*args,**kwargs) :
         
          print(request)
          return HttpResponse.write("HELLO")
          d1 = datetime(2022,5,9,15,20,15)
'''          
class ForgotAPIView(APIView):          
     def post(self,request,*args,**kwargs):
         email=request.data['email']
         rs=User.objects.filter(email=email,is_staff=False,is_active=True)
         if(not rs.exists()):
               return JsonResponse({'error':'No user with this email'})
         record=rs[0]
         now = datetime.now()
         new_time = now + timedelta(minutes=-30)
         #CustomerOTP.objects.filter()
         CustomerOTP.objects.filter(created_at__lt=new_time).delete()
         ke=generateOTP(5)
         cs=CustomerOTP()
         cs.email=email
         cs.otp=ke
         cs.save()
         return JsonResponse({'success':1,'otp':ke})
         
class VOTPAPIView(APIView):   
    
     def post(self,request,*args,**kwargs):
         email=request.data['email']
         otp=request.data['otp']
         '''rs=User.objects.filter(email=email)
         if(not rs.exists()):
               return JsonResponse({'error':'OTP and email do not match'})
         record=rs[0]
         now = datetime.now()
         new_time = now + timedelta(minutes=-30)
         '''
         #CustomerOTP.objects.filter()
         rec=CustomerOTP.objects.filter(email=email,otp=otp).first()
         if(not rec):
            return JsonResponse({'error':'OTP is incorrect'})
         #check if user is not suspended
         rs=User.objects.filter(email=email,is_staff=False,is_active=True)
         if(not rs.exists()):
               return JsonResponse({'error':'No user with this email'})
         rec=rs[0]
         if(not rec.is_active):
              return JsonResponse({'error':'{} is suspended'.format(email)})
         user=request.user
         if(isGOC(user)=='guest'):
              AppCart.objects.filter(user_id=user.id).update(user_id=rec.id)
              Order.objects.filter(user_id=user.id).update(user_id=rec.id)
         refresh=RefreshToken.for_user(rec)     
         
         return JsonResponse({'success':1,'access':str(refresh.access_token),'refresh':str(refresh),
                              'info':{'email': rec.email,
                        'first_name':rec.first_name,
                        'last_name':rec.last_name,
                        'type':'customer',
                        #'phone':user.phone,
                        'name':rec.first_name +' '+rec.last_name,
                'customer_id':rec.id}
                              
                              
                              
                              })  
'''
class TAPIView(APIView): 
         
 def post(self,request,*args,**kwargs):
         email=request.data['email']
         rs=User.objects.filter(email=email)
         if(not rs.exists()):
               return JsonResponse({'error':'No user with this email'})
         rec=rs[0]
         if(not rec.is_active):
              return JsonResponse({'error':'{} is suspended'.format(email)})
         user=request.user
         if(user!=None and user.id!=None and  isGOC(user)=='guest'):
              AppCart.objects.filter(user_id=user.id).update(user_id=rec.id)
              Order.objects.filter(user_id=user.id).update(user_id=rec.id)
         refresh=RefreshToken.for_user(rec)     
         
         return JsonResponse({'success':1,'access':str(refresh.access_token),'refresh':str(refresh)})  
'''         