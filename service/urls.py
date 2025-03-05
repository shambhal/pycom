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
from service import views
app_name="service"
urlpatterns = [
   
    path("list",views.list, name="list"),
    path("<int:service_id>",views.detail, name="servicedetail"),
    path('ondate/<date>',views.ondate, name='ondate'),
    path('schedule/<int:service_id>/',views.schedule,name="schedule"),
    path('look/<int:service_id>/',views.schedulebasic,name="schedulebasic"),
    path('book/<int:service_id>/',views.book_slot,name="book_now")
]
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
