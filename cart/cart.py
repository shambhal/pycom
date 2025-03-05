from django.conf import settings
from datetime import datetime,timedelta,date
from service.models import Service,SSpecial
from django.db.models.query_utils import Q
import datetime
class Cart(object):
    items=[]
    def removeold(self,arr,dts):
        #dts =currentday
     arr2=[]   
     for x in arr:
        dt =datetime.datetime.strptime(arr[x]['date'],'%Y-%m-%d')
        timediff=dt-dts
        if(timediff.days<0):
         del self.cart[x]
           
     self.save() 
    def __slothours(self,val):
        '''val=10:00-12:00#90,12:01-16:00#20'''
        strdate="2023-10-11"
        varr=[]
        #print(dt1)
        arr=val.split(',')
        for slot in arr:
            #print(slot)
            sarr=slot.split('#')
            price=sarr[1]
            slots=sarr[0]
            dslots=slots.split('-')
            h1a=dslots[0].split(':')
            h1=h1a[0]
            min1=h1a[1]
            
            h2a=dslots[1].split(':')
            h2=h2a[0]
            min2=h2a[1]
            varr.append({'price':price,'h1':h1,'min1':min1,'h2':h2,'min2':min2})
            #print(h1+' '+min1 +' '+h2 +' '+min2)
    
        return varr
    def __decodePrice(self,obj):
        varr=obj['varr']
        date1=obj['date']
        selt=obj['selt']
        
        interval=obj['interval']
        datestring=date1+' '+"00:00:00"
        dtobj=datetime.datetime.strptime(datestring,'%Y-%m-%d %H:%M:%S')
        dtobj2=dtobj+timedelta(seconds=interval)
        #print(dtobj2)
        selarr=selt.split(':')
        selh=selarr[0]
        selm=selarr[1]
        for node in varr:
            h1=node['h1']
            min1=node['min1']
            h2=node['h2']
            min2=node['min2']
            if h1==selh  and min1==selm:
                return node['price']
            if(selh>=h1 and selh<h2):
                return node['price']
            if(selh==h2 and (selm==min2 or selm<min2 )):
                return node['price']
        return -1
    def _getPrice(self,service_id,date1,selt):
       serviceobj=Service.objects.get(pk=service_id)
       interval=serviceobj.slot
       
      
       wkarr=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
       dateobj=date.fromisoformat(date1)
       sspobj= SSpecial.objects.filter(service=serviceobj).filter(sdate=dateobj)
       if(sspobj.exists()):
          obj=sspobj.get()
          slotexpr=obj.hours
       else:
        wd=dateobj.weekday()
        slotexpr=getattr(serviceobj,wkarr[wd])
        varr=self.__slothours(slotexpr)
        price=self.__decodePrice({'varr':varr,'date':str(date1),'interval':interval,'selt':selt})
        return price
    def __getItems(self):
       self.items=[]
       for i, item in enumerate(self.cart) :
           #print(item)
           val=self.cart[i]
          
           #print(val.service_id)
           service_id=val['service_id']
           slot=val['slot']
           price=self._getPrice(service_id,str(val['date']),slot)
           if(price==-1):
             continue
           val['price']=price
           self.items.append(val)
       #print(self.items)
    def getSubtotal(self):
        total=0
        if(self.items.count==0):
           self.__getItems()
        for item in self.items:
           total=float(item['price'])+total
        return total
    def getCount(self):
        return len(self.items)
    def __init__(self, request):
      
        
        self.session = request.session
        
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart=self.session[settings.CART_SESSION_ID]=[]
        self.cart=cart;   
    
    def getItems(self):
        self.__getItems()
        return self.items;          
    def remove(self,key):
        #print(f"delete index {key}")
        #print(self.cart)
        del(self.cart[key])
        self.save()
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        # Указываем, что сессия изменена
        self.session.modified = True 
        self.__getItems()   
    def add(self,date,slot,service_id):
         ''' date and slot is
         nothing but date and slot
         ''' 
         dateslot=str(service_id)+'_'+str(date)+'_'+slot
         #print(dateslot)
         if not dateslot in self.cart :
           self.cart.append({'dated':date,'date':date,'slot':slot,'service_id':service_id,'key':dateslot})
           self.save()