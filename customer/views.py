from warnings import resetwarnings
from warnings import resetwarnings
#pip install google-auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from google.auth.transport import requests as google_requests
from pycom.settings import GCI
from django.core.checks import messages
from django.shortcuts import render,redirect
from django.views.generic import CreateView
from customer.forms import CustomerForm,EditCustomerForm, ResetPasswordForm
from .models import Customer
from django.core.paginator import Paginator
from service.models import Book
from django.http import HttpResponse
from pycom.settings import GCI
from django.contrib.auth.models import   User
from django.db import transaction
from google.oauth2 import id_token
from google.auth.transport import requests 
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
from pycom.settings import fbl,gl
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm #add this
# Create your views here.

from django.views import View
def social():
     sociala=list()
     if fbl:
       sociala.append('fb')
     if gl:
      
       sociala.append('gl')

     template = "chunk/social.html"
   
     c = {
                                                    
             'sociala':sociala ,
             'gci':GCI

         }
     return render_to_string(template, c)   
def test(request):
    request.session['social_user']={'name':'parsad','email':'parsad@gmail.com'}
    request.session.save()
    messages.Info(request,"You don't have account , but you can create account.")
    return redirect(request.build_absolute_uri(reverse('customer:customer-create')))
def googlestate(request):
      return render(request=request, template_name="customer/callback.html", context={"GCI":GCI,'vgurl':request.build_absolute_uri(reverse('customer:vglogin'))})
class Glogin(View):
     name=''
     email=''
     def get(self,request):
         return render(request=request, template_name="customer/callback.html", context={"GCI":GCI,'url':request.build_absolute_uri(reverse('customer:vglogin'))})
     def gett(self,request):
          atoken=request.GET.get('access_token') 
          print(f'{atoken} is atoken')
          id_info = id_token.verify_oauth2_token(atoken, requests.Request(),GCI)

          user_email = id_info.get('email')
          user_name = id_info.get('name')
          print(user_email)
          print(user_name)
     def post(self,request):
            atoken=request.POST.get('credential','') 
            try :

              id_info = id_token.verify_oauth2_token(atoken,   google_requests.Request(),GCI)
            except Exception as e :  
             print(e)
             return JsonResponse({'error': 'Invalid token', 'details': str(e)}, status=400)
          
            user_email = id_info.get('email')
            user_name = id_info.get('name')

            #return JsonResponse(id_info)
            record=User.objects.filter(email=user_email,is_staff=False) 
            if(record.exists()):
              
               login(request,record[0])
               if 'redirect' in request.session:
                  rd=request.session['redirect']
                  del request.session['redirect']  
               else:
                  rd=reverse('customer:customer-home')   
               return JsonResponse({'code':1,'redirect':rd})
            else:
                request.session['social_user']={'name':user_name,'email':user_email}
                request.session.save()
                messages.Info(request,"You don't have account , but you can create account.")
                return JsonResponse({'code':2,'redirect':request.build_absolute_uri(reverse('customer:customer-create'))})

       
          
        
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
     def postt(self,request):
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
     @csrf_exempt   
     def posttogoogle(self,request):
          atoken=request.GET.get('access_token') 
          id_info = id_token.verify_oauth2_token(atoken, requests.Request())

          user_email = id_info.get('email')
          user_name = id_info.get('name')
         
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
@login_required
def profile(request):
  #print(request.user.)
  #if(request.user.is_authenticated and request.user.is_staff==False)
  if request.customer.is_authenticated :
   return render(request,'customer/profile.html',{'name':request.user.first_name})
  else:
     print(request.customer)
     return HttpResponse("Please login")
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
                messages.Info(request, f"You are now logged in as {username}.")
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
                messages.Info(request, f"You are now logged in as {username}.")
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
    qs=Book.objects.select_related('service').filter(Q(user_id=request.user.id)).order_by("-dated")
    
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
def fblogin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            access_token = data.get('accessToken')
            user_data = data.get('user')

            # Verify token with Facebook
            debug_url = f"https://graph.facebook.com/debug_token"
            params = {
                'input_token': access_token,
                #'access_token': f"{FACEBOOK_APP_ID}|{FACEBOOK_APP_SECRET}"
            }
            fb_res = requests.get(debug_url, params=params).json()

            if fb_res.get('data', {}).get('is_valid'):
                # Simulate saving to DB or creating session
                user = {
                    'facebook_id': user_data.get('id'),
                    'name': user_data.get('name'),
                    'email': user_data.get('email')
                }

                # TODO: Check if user exists, create/update, start session
                return JsonResponse({'success': True, 'user': user})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid token'}, status=401)

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)
def vglogin(request):
          atoken=request.POST.get('access_token') 
          print(f'{atoken} is atoken')
          id_info = id_token.verify_oauth2_token(atoken, requests.Request())

          user_email = id_info.get('email')
          user_name = id_info.get('name')
          print(user_email)
          print(user_name)
          HttpResponse(user_email+ user_name)
@login_required
def home(request):
  print(request.user.get_full_name())
  return render(request,'customer/home.html',{'name':request.user.get_full_name()})
@transaction.atomic
def create(request):
    if(request.user.is_authenticated and request.user.is_staff==False):
       return redirect(reverse('customer:customer-home'))
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
      print("here")
      soc=social() 
      if('social_user' in request.session):
         context={'form':CustomerForm(initial=request.session['social_user'])}
      else: 
       print("here")
       context={'form':CustomerForm(),'social':soc}
      return render(request,'customer/customer_form.html',context)



