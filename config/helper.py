from .models import ConfigModel
from pycom.settings import CURRENCY_SETTINGS
import datetime
import babel.numbers
'''
class Currency:
     code='INR'
    
     locale='en_IN'
     round=2
     def __init__(self,code,locale,digits):
          self.code=code
          self.locale=locale
          self.round=digits
          
     def format(self,val) : 
         val=round(val) 
        
         return babel.numbers.format_currency(val,self.code,locale=self.locale)
'''
def formatPrice(val,obj=None):
     '''if(obj is None):
          object=ConfigModel.objects.get(cname='rounded_digits')
          digits=int(object.cvalue)
          object=ConfigModel.objects.get(cname='currency_code')
          code=object.cvalue
          object=ConfigModel.objects.get(cname='locale')
          locale=object.cvalue
          obj=Currency(code=code,locale=locale,digits=digits)
      '''    
     return babel.numbers.format_currency(val,CURRENCY_SETTINGS['currency_code'],locale=CURRENCY_SETTINGS['locale'])
'''def getCurrencyObject():
          object=ConfigModel.objects.get(cname='rounded_digits')
          digits=int(object.cvalue)
          object=ConfigModel.objects.get(cname='currency_code')
          code=object.cvalue
          object=ConfigModel.objects.get(cname='locale')
          locale=object.cvalue
          obj=Currency(code=code,locale=locale,digits=digits)
          return obj
'''          
def addAP(param):
     #param has to be in 12:30 or 13:40 format
     hour=param[0:2]
     if(int(hour)<12):
       return param+' AM'
     return param+' PM'
def dateformat(param):
    return datetime.datetime.strptime(param, '%Y-%m-%d').strftime('%b-%d-%y %a')