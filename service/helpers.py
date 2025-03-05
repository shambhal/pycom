import datetime
from django.forms import model_to_dict
from api.utils.dayslots import DaySlots
import random
import string
from time import time  
import hashlib 
from service.models import Service,SSpecial,Book
def changeto24hrs(slot):
     slotarr=slot.split(" ")
     ampm=slotarr[1].strip()
     hrmin=slotarr[0].split(':')
     hr=int(hrmin[0])
     if (ampm=='PM' and hr<12): hr=hr+12
     return (hr,hrmin[1])
def generateOTP(maxd):
        '''if(order_id>0):
         md5oid=hashlib.md5(str(order_id).encode("utf-8")).hexdigest()
       # md5oid=md5oid.digest()
        else:
        '''
        md5oid=''
        maxdigits=maxd
        #tstr=str(time())
        #tstr=tstr.replace('.','_')
        res = ''.join(random.choices('234518967', k=5))
        return res
def generateKey(order_id):
        '''if(order_id>0):
         md5oid=hashlib.md5(str(order_id).encode("utf-8")).hexdigest()
       # md5oid=md5oid.digest()
        else:
        '''
        md5oid=''
        maxdigits=8
        tstr=str(time())
        tstr=tstr.replace('.','_')
        res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=maxdigits))
        return (str(res)+md5oid+tstr,str(res))
def simplegeneratekey():
        '''if(order_id>0):
         md5oid=hashlib.md5(str(order_id).encode("utf-8")).hexdigest()
       # md5oid=md5oid.digest()
        else:
        '''
        md5oid=''
        maxdigits=8
       
        res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=maxdigits))
        return str(res)