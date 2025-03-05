from django import forms
from django.core.validators import EmailValidator


class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            #visible.field.widget.attrs['placeholder'] = visible.field.label
    
        # new
        self.fields['message'].widget.attrs['rows'] = 5
        #self.fields['price'].widget.attrs['data-discount'] = '10%'
    name = forms.CharField(max_length=100)
    email = forms.CharField(validators=[EmailValidator()])
    phone = forms.CharField(max_length=15)
    #subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)