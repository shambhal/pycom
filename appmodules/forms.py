from django import forms
from .models import CatModule
from django.utils.translation import gettext_lazy as _
class CatModuleForm(forms.ModelForm):
    class Meta:
        model=CatModule
        fields = "__all__"
        exclude=["image"]
        #exclude=["service"]
    #sunday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'hello'})) 
    #monday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    #tuesday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    #wednesday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    #thursday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
  
    #friday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))
    #saturday=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'}))  
    #sort_order=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    
    #service=forms.IntegerField(widget=forms.HiddenInput)
   
