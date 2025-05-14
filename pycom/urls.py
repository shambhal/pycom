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
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from .admin import admin_site
#from customer
#from api.views import ServiceAPIView

#from rest_framework import routers
#from api.views import ServiceViewSet
#router = routers.DefaultRouter()
#router.register(r'api/services',ServiceViewSet )
urlpatterns = [
    path('myadmin/', admin_site.urls),
     path('admin/', admin.site.urls),
    #path('summernote/', include('django_summernote.urls')),
    
    #path("api/services/",ServiceAPIView.as_view()),
    #path("api/",include("api.urls")),
    path("headless/",include('headless.urls')),
    path("checkout/",include("checkout.urls",namespace="checkout")),
    #path("api/schedule/<int:service_id>/<string:date>/",include()),
    path("service/",include("service.urls",namespace="service")),
     path("contact/",include("contact.urls",namespace="contact")),
    #path("mytest/",include("mytest.urls",namespace="mytest")),
    path("cart/",include("cart.urls",namespace="cart")),
     path("payment/",include("payment.urls",namespace="payment")),
    path("customer/",include("customer.urls",namespace="customer")),
    
     #path('vapi/schema/', SpectacularAPIView.as_view(), name='schema'),
    #path('vapi/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", include("catalog.urls")),
    path("",include("information.urls")),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
