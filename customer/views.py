from warnings import resetwarnings
from warnings import resetwarnings
from django.core.checks import messages
from django.shortcuts import render,redirect
from django.views.generic import CreateView
from customer.forms import CustomerForm,EditCustomerForm, ResetPasswordForm
from .models import Customer
from django.core.paginator import Paginator
from service.models import Book
from django.http import HttpResponse
from django.contrib.auth.models import   User
from django.db import transaction

from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.urls import reverse
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm #add this
# Create your views here.

from django.views import View

class Glogin(View):
     name=''
     email=''
     def _authenticate(self,request,user):
          login(request,user)
          url=request.session.get('redirect',reverse('customer-home'))
          del request.session['redirect']
          return JsonResponse({'type':'redirect','url':url})
     def _decodeCredential(self,request,c):
           if(c!=''):
            
            #sample_string_bytes=base64.b64decode(c)
            data = c.decode("ascii") 
            print(data)
            h=data['header']
            p=data['payload']
            print(p)
            self.email=email=p['email']
            self.name=name=p['name']
            request.session['g_email']=email
            request.session['g_name']=name
            return (name,email)
     @csrf_exempt       
     def post(self,request):
           c=request.POST.get('credential','')
           if(c==''):
            return JsonResponse({'msg':'Invalid Credentials'})
           name,email= self._decodeCredential(request,c)
           record=User.objects.filter(email=email,is_staff=False)
           if(not record.exists()):
              return JsonResponse({'type':'new','name':name,'email':email})
           robj=record.get()
           if(robj.is_active==False):
              return JsonResponse({'type':'ban','name':name,'email':email})
           
           self._authenticate(request,record['user'])
class EditProfile(View):
  def post(self,request):
      cust=Customer.objects.filter(Q(user=request.user))
      if(len(cust)>0):

       edform = EditCustomerForm(request.POST,instance=cust[0])
      else:
       edform = EditCustomerForm(request.POST)
       edform.user=request.user
      if(edform.is_valid()):
        dta=edform.cleaned_data
        name=dta['name']
        namearr=name.split(' ',1)
        surname=''
        if len(namearr) >1 :
          surname= namearr[1]
        edform.save()
        user=request.user
        user.first_name=namearr[0]
        user.last_name=surname
        user.save()
        messages.add_message(request,message="Profile saved ",level=3)
        return redirect(reverse("customer:profile"))
      else:

       return  render(request=request, template_name="customer/edit_profile.html", context={"form":edform,'errors':edform.errors})

  def get(self,request):
    initial={'email':request.user.email,'name':request.user.get_full_name()}
    cust=Customer.objects.filter(Q(user=request.user))
    if(cust):
      cust=cust[0]
      initial['phone']=cust.phone
    password_reset_form = EditCustomerForm(initial=initial)
    return render(request=request, template_name="customer/edit_profile.html", context={"form":password_reset_form})

class Passrr(View):
  def send(self,data):
      associated_users = User.objects.filter(Q(email=data))
      if associated_users.exists():
       for user in associated_users:
           subject = "Password Reset Requested"
           email_template_name = "customer/password_reset_email.txt"
           c = {
                                                    "email":user.email,
                                                    'domain':'127.0.0.1:8000',
                                                    'site_name': 'Website',
                                                     "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                                                     "user": user,
                                                     'token': default_token_generator.make_token(user),
                                                    'protocol': 'http',
                                                    }
           email = render_to_string(email_template_name, c)                                
           try:
             send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
           except BadHeaderError:
             return HttpResponse('Invalid header found.')
           return render(reverse('password_reset_done'))  

  def post(self,request):
      password_reset_form = PasswordResetForm(request.POST)
      if(password_reset_form.is_valid()):
        data = password_reset_form.cleaned_data['email']
        self.send(data)
      return  render(request=request, template_name="customer/password_reset_form.html", context={"password_reset_form":password_reset_form})

  def get(self,request):
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="customer/password_reset_form.html", context={"password_reset_form":password_reset_form})
'''@login_required
class changePassword(LoginRequiredMixin, View):
  login_url=reverse('customer:login')
  def post(self,request):
    form=ResetPasswordForm()
    
    context={}
    context['form']=form
    if form.is_valid():
         return render(request,'customer/change_password.html',context)
    else:
      context['error']=form.errors
      return render(request,'customer/change_password.html',context)  
  def get(self,request):
     form=ResetPasswordForm()
     context={}
     context['form']=form
     return render(request,'customer/change_password.html',context)
'''  
def profile(request):
  return render(request,'customer/profile.html')
def logout_request(request):
     logout(request)
     return render(request,"customer/logged_out.html")
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                if request.session['redirect']:
                  rd=request.session['redirect']
                  del request.session['redirect']  
                  return redirect(rd)  
                return redirect("/")
            else:
                messages.error(request,"Invalid username or password.")
                return redirect(reverse('customer:customer-login'))
        else:
            messages.error(request,"Please write credentials correctly.")
            return redirect(reverse('customer:customer-login'))
    form = AuthenticationForm()
    return render(request, template_name="registration/login.html", context={"login_form":form})

class CustomerLogin(View):

  def get(self,request):
        form = AuthenticationForm()
        
           
        return render(request,'customer/login.html',{'form':form})
  def post(self,request):
       form = AuthenticationForm(request, data=request.POST)
       if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                print(request.session)
                if 'redirect' in request.session:
                  rd=request.session['redirect']
                  del request.session['redirect']  
                  return redirect(rd)  
                return redirect("/")
            else:
                messages.error(request,"Invalid username or password.")
                return redirect(reverse('customer:customer-login'))
       
@login_required
def mybookings(request):
    qs=Book.objects.select_related('user').filter(Q(user=request.user)).order_by("-dated")
    
    paginator = Paginator(qs, 15) # Show 25 contacts per page.

    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    pages={}
   
        
     
    return render(request, 'customer/job_list.html', {'page_obj': page_obj})
  
'''
def glogin(request):
     c=request.POST.get('credential','')
     if(c!=''):
        print(c)
        data=base64.decode(c)
        h=data['header']
        p=data['payload']
        
        email=p['email']
        name=p['name']
        request.session['g_email']=email
        request.session['g_name']=name
        return JsonResponse({'email':email,'name':name})
'''
@login_required
def home(request):
  print(request.user.get_full_name())
  return render(request,'customer/home.html',{'name':request.user.get_full_name()})
@transaction.atomic
def create(request):
    if(request.user.is_authenticated):
       return redirect('customer-home')
    if(request.method=='POST'):

      form=CustomerForm(request.POST)
      context={'form':form}
      if(form.is_valid()):
        '''
   
        save user
        '''
        data=form.cleaned_data
        name=data['name']
        #phone=data['phone']
        namearr=name.split(' ',1)
        surname=''
        if len(namearr) >1 :
          surname= namearr[1]
        try:  
         user = User.objects.create_user(data['email'], data['email'], data['password'])
         user.first_name=namearr[0]
         user.last_name=surname
         user.save()
         
         cust=Customer()
         cust.phone=data['phone']
         cust.user=user
         cust.save()
         login(request,user)
         return redirect('customer-home')
        except Exception as e:
         context['error']=e
         return render(request,'customer/customer_form.html',context) 
      return render(request,'customer/customer_form.html',context)

    else:

      context={'form':CustomerForm()}
      return render(request,'customer/customer_form.html',context)



