from django.shortcuts import render
from .models import Information
from django.views import View
# Create your views here.
from django.utils.html import format_html
def InformationView(request,slug):
    info=Information.objects.filter(seo_url=slug)
    if(info.exists()):

       return render(request,'information.html',{'content':format_html(info[0].content)})
    else:
     return render(request,'information.html',{'slug':slug})