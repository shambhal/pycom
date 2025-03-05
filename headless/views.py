from django.shortcuts import render,HttpResponse
from information.models import Information
from headless.serializers import InformationSerializer
from rest_framework.response import Response
from pycom.settings import SITE_URL
from django.http import JsonResponse
# Create your views here.
def infolinks(request):
     
     #infos=  Information.objects.all().filter(status=True).values_list("title","seo_url").order_by("sort_order")
     infos=  Information.objects.all().filter(status=True).order_by("sort_order")
     serializer_context = {
            'request': request,
        }
     serializer = InformationSerializer(infos,many=True,context=serializer_context)
     #print(serializer.data)
     #return Response(serializer.data)   
     return JsonResponse({'links':serializer.data,'site_url':SITE_URL})