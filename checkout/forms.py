from django import forms
from .models import Appointee
from django.utils.translation import gettext_lazy as _
class AppointeeForm(forms.ModelForm):
    class Meta:
        model=Appointee
        fields = "__all__"
        exclude=["customer"]
       