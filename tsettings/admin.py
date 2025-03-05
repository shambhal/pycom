from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.db import models
from django.shortcuts import render
from .forms import SettingsForm
#from ..whrs.models import work
# my dummy model
class DummyModel(models.Model):

    class Meta:
        verbose_name_plural = 'Dummy Model'
        app_label = 'tsettings'

def my_custom_view(request):
   

    form=SettingsForm()
    context = {
        'form': form,
       
    }
    return render(request, 'time/settings.html', context)

class DummyModelAdmin(admin.ModelAdmin):
    model = DummyModel

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('my_admin_path/', my_custom_view, name=view_name),
        ]
admin.site.register(DummyModel, DummyModelAdmin)