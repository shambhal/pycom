from django import forms
from .models import work
# creating a form
class SettingsForm(forms.ModelForm):
  class Meta:
        model = work
        fields = "__all__"