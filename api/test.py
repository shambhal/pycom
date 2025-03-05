from datetime import datetime
from datetime import timedelta

def makeslots(slotinterval,type):
    '''slotinterval like 10:00-18:30#10'''
    '''type=off or booked'''
    if(type=='off'): av=0
    if(type=='book'): av=0
    
    tarr1=slotinterval.split("#")
    if(tarr1[1]==None):
      price=10
    else:
      price=tarr1[1]
    hrmin=tarr1[0]  
    tarr2=hrmin.split('-')
    hrmin1=tarr2[0].split(':')
    hr1=hrmin1[0]
    min1=hrmin1[1]
    hrmin2=tarr2[1].split(':')
    hr2=hrmin2[0]
    hr22=hr2
    if(hr1==hr2):
      hr22=hr+1
    min2=hrmin2[1]
    hr1=int(hr1)
    hr2=int(hr2)
    min1=int(min1)
    min2=int(min2)
    arr=range(hr1,hr22)
    
    
    slots=[]
    if(hr1==0 and hr2==0):
      return []
    slots.append({'hr':arr[0],'min':min1,'type':type,'price':price})
    for hr in arr:
        d1 = datetime(2022,5,9,hr,min1,00)
        d2=d1+timedelta(seconds=1800)
        thr=d2.hour
        tmin=d2.minute
        if(thr<hr2):
         slots.append({'hr':thr,'min':tmin,'type':type,'price':price,'av':av})
        if(thr==hr2 and tmin<=min2) :
         slots.append({'hr':thr,'min':tmin,'type':type,'price':price,'av':av})
    
    return slots
expr="10:00-12:00#10,12:00-18:00#12"
fslots=[]
t=expr.split(',')
for s in t:
  fslots.extend(makeslots(s,'normal'))
off="11:30-12:00#0"
