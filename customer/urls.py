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
from django.views.generic.edit import CreateView
from customer import views
from django.contrib.auth import views as auth_views #import this
from customer.views import CustomerLogin,Passrr,EditProfile,Glogin
app_name="customer"
urlpatterns = [
   
    path("register/",views.create,name="customer-create"),
    path("profile/",views.profile,name="profile"),
    path("bookings/",views.mybookings,name= 'mybookings'),
    path("edit-profile/",EditProfile.as_view(),name="edit-profile"),
    path("login/",CustomerLogin.as_view(),name="customer-login"),
    path("change-password/", auth_views.PasswordChangeView.as_view(
            template_name='customer/password_change_form.html',
            success_url = '/'
        ),name="change-password"),
    path("resetpassword/",Passrr.as_view() ,name="password-reset"),
    path("glogin/",Glogin.as_view(),name="customer-glogin"),
    path("logout/",views.logout_request,name='logout'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='customer/registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="customer/registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='customer/registration/password_reset_complete.html'), name='password_reset_complete'),   
    path("myaccount",views.home,name='customer-home'),
   
]
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
