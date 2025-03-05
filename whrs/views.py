from django.shortcuts import render

# Register your models here.
from  .forms import SettingsForm
# Create your views here.
def workadds(request):
      form=SettingsForm()
      context = {
        'form': form,
       
           }
      return render(request, 'time/settings.html', context)
    