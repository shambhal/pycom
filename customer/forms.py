from django import forms
from  django.contrib.auth.models import User
from .models import Customer
class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields = "__all__"
        #fields =['email']
        exclude=['email','user','access','refresh','phone']
    name=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    email=forms.CharField(widget=forms.widgets.EmailInput(attrs={'class':'form-control'})) 
    phone=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    email=forms.CharField(widget=forms.widgets.EmailInput(attrs={'class':'form-control'})) 
    password=forms.CharField( min_length=6,max_length=12,widget=forms.widgets.PasswordInput(attrs={'class':'form-control'})) 
    rpassword=forms.CharField( label="Retype Password", help_text="Retype Password", widget=forms.widgets.PasswordInput(attrs={'class':'form-control'})) 
    fields_order=['name','email','phone','password','rpassword']

    def clean_rpassword(self):

         password = self.cleaned_data['password']
         rpassword=self.cleaned_data['rpassword']
         if (rpassword!=password) :
          raise forms.ValidationError("the two passwords should match")
          return rpassword

class EditCustomerForm(forms.ModelForm):          
    class Meta:
        model=Customer
        fields = "__all__"
        #fields =['email']
        exclude=['user','access','refresh']
    name=forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'form-control'})) 
    email=forms.CharField(widget=forms.widgets.EmailInput(attrs={'class':'form-control', })) 
   
    fields_order=['name','email','phone']

class ResetPasswordForm(forms.ModelForm):
    class Meta:
         model=Customer
         fields = ['password']
    
    password=forms.CharField( widget=forms.widgets.PasswordInput(attrs={'class':'form-control'})) 
    rpassword=forms.CharField( label="Retype Password", help_text="Retype Password", widget=forms.widgets.PasswordInput(attrs={'class':'form-control'})) 
    fields_order=['name','email','password','rpassword']

    def clean_rpassword(self):

         password = self.cleaned_data['password']
         rpassword=self.cleaned_data['rpassword']
         if (rpassword!=password) :
          raise forms.ValidationError("the two passwords should match")
          return rpassword

  