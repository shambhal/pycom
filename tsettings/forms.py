from django import forms
 
# creating a form
class SettingsForm(forms.Form):
   Sunday = forms.CharField()
   
   Monday = forms.CharField(help_text='Monday Opening Hours')
   Tuesday = forms.CharField()
   Wednesday = forms.CharField()
  
   Thursday = forms.CharField()
   Friday =Saturday= forms.CharField()
   #Saturday= forms.CharField()