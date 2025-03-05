from django.db import models
from  config.helper import formatPrice
# Create your models here.
choices={
    ('P','Percentage'),
    ('A','Absolute Value')
}
class Tax(models.Model):
    class Meta:
          verbose_name="Tax"
          verbose_name_plural = "Taxes"
    def __str__(self) -> str:
             return self.name
    name=models.CharField(blank=False,max_length=10)
    type=models.CharField(choices=choices,default='P')
    status=models.BooleanField(default=1)
    sort_order=models.IntegerField(editable=True,default=1)
    rate=models.DecimalField(blank=False,max_digits=4,decimal_places=2)
def getTaxes(subtotal):
       taxes=Tax.objects.filter(status=1).order_by('sort_order')
       arr=[]
       for tax in taxes:
              rate=float(tax.rate)
              name=tax.name
              if(tax.type=='P'):
                     total=round(subtotal*float(rate)*0.01,2)
              else:
                     total=rate
              arr.append({'name':name,'total':total,'type':str(tax.type),'rate':rate})      
       return arr
class TaxHelper:
   totals=[]
   gtotal=0
   def getGrandTotal(self):
         return self.gtotal
   def __getTaxes(self,subtotal):
       taxes=Tax.objects.filter(status=1).order_by('sort_order')
       arr=[]
       for tax in taxes:
              rate=float(tax.rate)
              name=tax.name
              if(tax.type=='P'):
                     total=round(subtotal*float(rate)*0.01,2)
                     namesuffix='({} %)'.format(rate)

              else:
                     total=rate
                     namesuffix=''
              self.gtotal=self.gtotal+total
              self.totals.append({'name':name+namesuffix,'text':formatPrice(total),'totals':formatPrice(total),'total':total,'type':str(tax.type),'rate':rate})      
      
   def getTotals(self,subtotal):
         
         self.totals=[]
         self.gtotal=subtotal
         self.totals.append({'name':'Subtotal','total':subtotal,'text':formatPrice(self.gtotal),'totalf':formatPrice(subtotal)})
         self.__getTaxes(subtotal)
         self.totals.append({'name':'Total','total':self.gtotal,'text':formatPrice(self.gtotal),'totalf':formatPrice(self.gtotal)})
         return self.totals
