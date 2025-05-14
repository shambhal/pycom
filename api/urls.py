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
from api.vues import ForgotAPIView,VOTPAPIView
#from api.vues import FCMTokenView
from api.views import ServiceAPIView,PaymentMethodsAPIView,PMDetailsAPIView,HomeAPIView,CappRegisterView,TokenInit,CatListView,AListView,ChangePasswordView,RListView,APHistoryView,logouttoken
from api.views import OrderSummary,DeleteCartView,RegenerateKey, AppointView,init2, LoginView,BookView, OrderView,ConfirmView,    RegisterView,ServiceSlotsView,ATCView,CartListView,DetailView,TermsAPIView
from rest_framework_simplejwt import views as jwt_views 
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
urlpatterns = [
   #path('/schedule/<date>/',ServiceAPIView.as_view()),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
   path('token', 
         jwt_views.TokenObtainPairView.as_view(), 
         name ='token_obtain_pair'), 
    path('token/refresh', 
         jwt_views.TokenRefreshView.as_view(), 
         name ='token_refresh'), 
   path("services",ServiceAPIView.as_view()),
   path("appointments/",AListView.as_view()),
   path("ordersummary",OrderSummary.as_view()),
   path("logout",logouttoken),
   path("book",BookView.as_view()),
   path("slots",ServiceSlotsView.as_view()),
   path("regenerate",RegenerateKey.as_view()),
   path("register",CappRegisterView.as_view()),
   path("inn",TokenInit.as_view()),
   #path("init",init),
   path("ini",init2),
   path("cart",CartListView.as_view()),

    path("cart-delete",DeleteCartView.as_view()),
   path("detail",DetailView.as_view()),
   path("register",RegisterView.as_view()),
    path("login",LoginView.as_view()),
    path("confirm",ConfirmView.as_view()),
   path("atc",ATCView.as_view()),
   path("catlist",CatListView.as_view()),
   path("refund",RListView.as_view()),
    path("alist",APHistoryView.as_view()),
   path("homebanners",HomeAPIView.as_view()),
   path("forgot",ForgotAPIView.as_view()),
  # path("ftest",TAPIView.as_view()),
      path("validateotp",VOTPAPIView.as_view()),
    path("terms",TermsAPIView.as_view()),
   path("payment_methods",PaymentMethodsAPIView.as_view()),
   path("payment_method",PMDetailsAPIView.as_view()),
   path("order",OrderView.as_view()),
    path("cp",ChangePasswordView.as_view()),
    # path("fcmtoken",FCMTokenView.as_view()),
]
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
