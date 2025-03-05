from django.apps import AppConfig
import importlib
from django.utils.module_loading import import_string
class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'
    
    def ready(self) :
      
       return super().ready() 