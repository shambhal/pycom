from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from information import views
app_name="information"
urlpatterns = [
   
    path("<slug:slug>",views.InformationView ,name="view"),
   
]