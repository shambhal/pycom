from django import forms
from .models import Information
from ckeditor.widgets import CKEditorWidget
class InformationForm(forms.ModelForm):
    class Meta:
        model=Information
        fields = "__all__"
    content = forms.CharField(widget=CKEditorWidget())    