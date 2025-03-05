from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from .forms import ContactForm
from django.conf import settings
def terms(request):
    return render(request, 'terms.html')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']


            EmailMessage(
               'Contact Form Submission from {}'.format(name),
               message,
               'info@appoint.shambhalnetworks.in', # Send from (your website)
               ['siddharthsingh.chauhan@gmail.com'], # Send to (your admin email)
               [],

               reply_to=[email] # Email from the form to get back to
           ).send()
        apimode=request.GET.get('apimode',0)
        if apimode==0:
            base='catalog/base.html'
            suffix=''
        else:
            base='content/base.html'  
            suffix='?apimode=1' 

        return redirect('success',{'base':base})
    else:
        form = ContactForm()
        apimode=request.GET.get('apimode',0)
        if apimode==0:
            base='catalog/base.html'
            suffix=''
        else:
            base='content/base.html'  
            suffix='?apimode=1'  
    return render(request, 'contact.html', {'form': form,'apimode':apimode,'suffix':suffix,'base':base})