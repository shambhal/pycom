from django.contrib import admin
from django.urls import path,include
from django.views.generic.edit import CreateView
from contact import views
from django.contrib.auth import views as auth_views #import this

app_name="contact"
urlpatterns = [
   
    path("",views.contact,name="contact"),
    path("terms",views.terms,name='terms')
]
  