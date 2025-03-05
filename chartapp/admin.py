
from django.contrib import admin,messages
from django.http import HttpRequest
from datetime import datetime,timedelta
from service.models import Book
from django.db.models import Count
# Register your models here.
def dashindex(request):
    cdate=datetime.now
    date1=request.GET.get('date1',cdate[0:10])
    cdate2=cdate+timedelta(days=-30)
    cdate=cdate2[0:10]
    date2=request.GET.get('date2',date2)
    fdiff=(date2-date1).days
    if(date2>date1):
       temp1=date1
       temp2=date2
    else:
        temp1=date2
        temp2=date1
    res=Book.objects.annotate(num_appointments=Count('dated')).filter(status='BOOKED').filter(dated__range=[date2,date1])
    while temp1<=temp2:
        #//operation
        temp1=temp1+timedelta(days=1)

                 

