from django.shortcuts import render,HttpResponse
from pycom.settings import CURRENCY_SETTINGS
import babel.numbers
# Create your views here.
def index(request):
  return render(request,'catalog/index.html')
def test(request):
   lapp=  babel.numbers.format_currency(90,CURRENCY_SETTINGS['currency_code'],locale=CURRENCY_SETTINGS['locale'])
   return render(request,'catalog/test.html',{
      'param':lapp
   })
