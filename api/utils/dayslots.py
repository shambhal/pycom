from datetime import datetime
from datetime import timedelta
from config.helper import formatPrice
from django.forms import model_to_dict

from taxes.models import TaxHelper 
from service.models import Service,SSpecial,Book
def changeto24hrs(slot):
     slotarr=slot.split(" ")
     ampm=slotarr[1].strip()
     hrmin=slotarr[0].split(':')
     hr=int(hrmin[0])
     if (ampm=='PM' and hr<12): hr=hr+12
     return (hr,hrmin[1])
class ServiceSlotPrice:
    service_id=0
    service_name=''
    slot=''
    dated=''
    dayarr=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    def calculateSchedule(self):
         sparr=[]
         rarr=[]
         barr=[]
         daily={}
         dt =datetime.strptime(str(self.dated),'%Y-%m-%d')
         wd=dt.weekday()
         serv=Service.objects.get(pk=self.service_id)
         if serv!=None:
           s=model_to_dict(serv)
           self.service_name=s['name']
           #print(self.dayarr)
           #print("weekday is ")
           #print(wd)
           routine={'hours':s[self.dayarr[wd]],'off':serv.off}
           daily['hours']=s[self.dayarr[wd]]
           daily['off']=serv.off
           sps=[]  
           spstring=''
           spoff=''
           specialobj=SSpecial.objects.all().filter(service_id=self.service_id,sdate=self.dated) 
           if(specialobj.exists()):
              for rec in specialobj:
                 sps.append(rec.hours)
                 spstring=','.join(sps)
                 spoff=rec.off
    
           bookings=[]
           obj=Book.objects.all().filter(service_id=self.service_id,dated=self.dated)
           if obj.exists():
            for rec in obj:
             bookings.append(rec.slot)
            
             obj2=','.join(bookings)
           else:
             obj2=''
           ds=DaySlots(s['slot'],self.dated)
           ds.makeslots(daily['hours'],'routine')
           ds.makeslots(daily['off'],'off')
           ds.makeslots(obj2,'book')
           ds.makeslots(spstring,'special')
           sched=ds.getSchedule()  
           return sched
class DaySlots:
  def replaceampm(self,string):
     string=string.replace("AM",'')
     string=string.replace("PM",'')
     string=string.replace("A.M",'')
     return string
  def __init__(self,interval,dated):
      self.slots={}
      self.off={}
      self.booked={}
      self.special={}
      self.sinterval=interval
      self.dated=dated
  def getSchedule(self):
       self.slots.update(self.special)
       self.slots.update(self.off)
       self.slots.update(self.booked)
       keys=list(self.slots.keys())
       keys.sort()
       arr=[]
       for key in keys:
          arr.append(self.slots[key])
       return arr
  def makeslots(self,slotinterval1,type):
      if(slotinterval1=='' or slotinterval1=='00:00-00:00'):
       return
      temp=slotinterval1.split(',')
      #print(temp)
      #return
      for slotinterval in temp:
          #print(slotinterval)
          
          if(type=='off'):
            self.off=self.__makeslots(slotinterval,type)
          elif(type=='book'):
            self.booked=self.__makeslots(slotinterval,type)
          elif(type=='special'):
              self.special=self.__makeslots(slotinterval,type)
          else:  
            self.slots=self.__makeslots(slotinterval,type)
            
  def __makeslots(self,slotinterval,type):
    '''slotinterval like 10:00-18:30#10'''
    '''type=off or booked'''
    av=1
    if(type=='off'): av=0
    if(type=='book'): av=0
    
    tarr1=slotinterval.split("#")
    if(len(tarr1)<2):
      price=10
    else:
      price=tarr1[1]
    hrmin=tarr1[0]  
    tarr2=hrmin.split('-')
    hrmin1=tarr2[0].split(':')
    hr1=hrmin1[0]
    min1=self.replaceampm(hrmin[1])

    if(len(tarr2)<2):
       d1 = datetime(2022,5,9,int(hr1),int(min1),00)
       d2=d1+timedelta(seconds=self.sinterval)
       hr2=d2.hour
       min2=d2.minute
       hr2=str(hr2)
       min2=str(min2)
    else:   
     hrmin2=tarr2[1].split(':')
     hr2=hrmin2[0]
    
   
     min2=hrmin2[1]
    hr1=int(hr1)
    hr2=int(hr2)
    hr22=hr2
    min1=int(min1)
    min2=int(min2)
    if(hr1==hr2):
      hr22=hr1+1
    arr=range(hr1,hr22)
    
    
    slots={}
    if(hr1==0 and hr2==0):
      return  
    mins=''
    if(min1<10): mins='0'
    key1=str(hr1)+''+str(min1)+mins
    key1=int(key1)
    hrstring=str(hr1)
    minstring=str(min1)
    ## user riendly slot with am/pm
    suffix='PM'
   
    if(hr1<12):suffix='AM' 

    if(hr1>12) :hrstring=str(hr1-12)

    ######################
    #price=formatPrice(price)
    slots[key1]={'slot':hrstring+':'+minstring+mins+ ' '+suffix,'date':self.dated,'min':min1,'type':type,'wprice':price,'key':key1,'price':formatPrice(price),'av':av}
    for hr in arr:
        d1 = datetime(2022,5,9,hr,min1,00)
        d2=d1+timedelta(seconds=1800)
        thr=d2.hour
        tmin=d2.minute
        mins=''
        if(tmin<10): mins='0'
        key1=str(thr)+''+str(tmin)+mins
        key1=int(key1)

        hrstring=str(thr)
        minstring=str(tmin)
        ## user riendly slot with am/pm
        suffix='PM'
        mins=''
        if(thr<hr2):
         if(thr<12):suffix='AM' 

         
         if(thr>12) :hrstring=str(thr-12)
         slotstring=hrstring+':'+minstring+mins+' '+suffix
        
         slots[key1]={'slot':slotstring,'key':key1,'date':self.dated,'min':tmin,'type':type,'wprice':price,'price':formatPrice(price),'av':av}
        if(thr==hr2 and tmin<=min2) :
         if(thr<12):suffix='AM' 

         if(tmin<10): mins='0'
         if(thr>12) :hrstring=str(thr-12)
         slotstring=hrstring+':'+minstring+mins+' '+suffix
         #slots.append({'hr':thr,'min':tmin,'type':type,'price':price,'av':av})
        
        slots[key1]={'slot':slotstring,'key':key1,'date':self.dated,'min':tmin,'type':type,'wprice':price,'price':formatPrice(price),'av':av}
    return slots
class Cartitem:
     
     def __init__(self,dated,slot,price,service_id):
         self.dated=dated
         self.slot=slot
         self.price=price
         self.service_id=service_id
class CartPrice:
     subtotal=0
     grandtotal=0
     totals=[]
     def getPrice(self,item):
         #print(item.dated)
         #print(item.slot)
         dated=item.dated 
         slot=item.slot
        
         #return item
         if 'PM' in item.slot or 'AM' in item.slot :
          kslot=changeto24hrs(item.slot)
         else:
            kslot=item.slot.split(":")
        
         kslot=str(kslot[0])+''+str(kslot[1])
         slot=slot.replace("AM",'')
         slot=slot.replace("A.M",'')
         slot=slot.replace("PM",'')
         slot=slot.replace(":",'')
         service_id=item.service_id
         ssp=ServiceSlotPrice()
         ssp.service_id=service_id
         ssp.dated=dated
         sched=ssp.calculateSchedule()
         
         #print(slot)
        # return sched
         for nod in sched:
             #print( nod)
             #return nod
             if(nod['key']==int(kslot) and nod['av']==1):
              return nod['wprice']
         return -1  
     def getTotals(self):
        return self.totals
     def calculateTotals(self):
         
         th=TaxHelper()
         self.totals=th.getTotals(self.subtotal)
         self.grandtotal=th.getGrandTotal()
     def getSubtotal(self,items):
         total=0
         for item in items  :
             #pass
             total=total+float(item['price'])
         self.subtotal=total   
         return [{'title':'Sub Total','total':total,'text':(formatPrice(total))}]      
         return [{'title':'Sub Total','total':total,'text':str(formatPrice(total))}]      