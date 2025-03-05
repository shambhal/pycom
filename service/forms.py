from django import forms
from .models import Book, SSpecial,Service
from django.utils.translation import gettext_lazy as _
class SServiceForm(forms.ModelForm):
    class Meta:
        model=SSpecial
        fields = "__all__"
       
        #exclude=["service"]
    #sunday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'hello'})) 
    #monday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    #tuesday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    #wednesday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    #thursday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    sdate=forms.DateField(label=_("sdate"),widget=forms.widgets.TextInput(attrs={'id':'sdate','class':'date'})  )  
    #friday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    #saturday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))  
    off=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    hours=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    #service=forms.IntegerField(widget=forms.HiddenInput)
   
class ServiceForm(forms.ModelForm):
    class Meta:
        model=Service
        #fields = "__all__"
        exclude=('specialdate','img')
    sunday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'00:00-00:00'})) 
    monday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    tuesday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    wednesday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    thursday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
      
    friday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    saturday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))  
    slot=forms.IntegerField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    seo_title=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    seo_description=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    name=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'hello'}))  
    off=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))  
class BookForm1(forms.ModelForm):
    class Meta:
        model=Book
        fields = "__all__"
        exclude=['service','desc','status']
    dated=forms.CharField(widget=forms.widgets.HiddenInput,max_length=20,required=True) 
    desc=forms.CharField(widget=forms.widgets.HiddenInput,required=False)
    #service=forms.BoundField(field=Service,widget=forms.HiddenInput,required=False)
    slot=forms.CharField(widget=forms.widgets.HiddenInput,max_length=20)  
    status=forms.CharField(widget=forms.widgets.HiddenInput,max_length=20)  
    name=forms.CharField(required=True,max_length=20,widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'nAME'}))    
    email=forms.CharField(required=True,max_length=100,widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    phone=forms.CharField(required=True,max_length=15,widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'Phone'}))    

class BookEditForm(forms.ModelForm):
   class Meta: 
    model=Book
    #fields = "__all__"
    fields=["phone","name","status","dated","slot","email","extra_info"]
    exclude=['order_id','order_item_id','device_id']
    widgets={ 'dated': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control'}
            )
     }
class RescheduleForm(forms.ModelForm):
   class Meta: 
     model=Book
     fields=["dated","slot","email"]
     widgets={ 'dated': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control date'}
            )}
    
     