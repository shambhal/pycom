from django.contrib import admin
from django.urls import path,include
from django.views.generic.edit import CreateView
from .views import APView
from checkout import views
from checkout.views import CheckoutCartView,PaymentView,CheckoutLogin
app_name="checkout"
urlpatterns = [
path('payment',views.payment_view,name="pview"),
path("success",views.success,name="success"),
path("fail",views.fail,name="fail"),
path("appointee",APView.as_view(),name="appointee"),
path("checkout",views.CheckoutView.as_view(),name="checkout"),
path("login",views.CheckoutLogin.as_view(),name="login"),
path("apdetails",views.apdetails,name="apdetails"),
path("pms",views.pms,name="pms"),
path("wpayment",views.PaymentView.as_view(),name="wpayment"),
path("cartdetails",views.CheckoutCartView.as_view(),name="cartdetails")
]