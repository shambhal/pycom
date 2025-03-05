"""pycom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from mytest import views
app_name="mytest"
urlpatterns = [
   
    path("gp",views.getPrice, name="gp"),
    path("gnq",views.getNameQuote, name="gnq"),
     path("tz",views.tz, name="tz"),
    path("otk",views.otk,name="otk"),
    path("makebookings",views.makebookings,name="mybookings"),
   path("cptest",views.cptest,name="cptest"),
   path("ctest",views.ctest,name="ctest"),
      path("ilinks",views.ilinks,name="ilinks"),
   path("clearcart",views.clearcart,name="clearcart"),
   path("gsignin",views.gsignin,name="gsignin"),
      path("glogin",views.glogin,name="glogin")
   #path("fcmtest",views.fcm ,name="fcmtest")
]
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
