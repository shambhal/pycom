from rest_framework import serializers
from service.models import Service,Book,BookHistory
from payment.models import Payment
from cart.models import AppCart
from customer.models import Customer
from django.contrib.auth.models import User
from orders.models import Order
# for delete cart serializer
class DCSerializer(serializers.Serializer):
    cart_id=serializers.IntegerField()

class ServiceSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Service
        fields = ["name","id","sunday","monday","tuesday","thursday","friday","saturday","off",'slot']
class PaymentMethodSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Payment
        fields = ["title","status",'code']   
class CartSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = AppCart
        fields = ["slot",'dated','id']   
class RegisterSerializer(serializers.Serializer):  
       name=serializers.CharField(required=True) 
     
       email=serializers.CharField(required=True)
       phone=serializers.CharField(required=True,max_length=10) 
      
       def save(self):
           password = self.validated_data['password']
           data=self.validated_data
           password2 = self.validated_data['password2']
           if password != password2:
             raise serializers.ValidationError({'error': 'Passwords must match.'})
           us=User.objects.filter(email=self.validated_data['email'])
           if us.exists():
               raise serializers.ValidationError({'error':'User exists with such email'})
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
           except Exception as e:
               raise serializers.ValidationError({'email':e})
class LoginSerializer(serializers.Serializer):  
       password=serializers.CharField(required=True) 
       email=serializers.CharField(required=True)
class OrderSerializer(serializers.Serializer)  :
       
    class Meta:
        model = Order
        fields='__all__'
class BookHistorySerializer(serializers.ModelSerializer)  : 
     class Meta:
        model = BookHistory
        #ordering=['-id']
        fields='__all__'
        #fields=['id','dated']             
class ChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(required=True)
    retype=serializers.CharField(required=True)
    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['password'] != data['retype']:
            raise serializers.ValidationError({'retype':"passwords should match "})
        return data
    def update(self,instance,validated_data):

           user=instance
           password=validated_data['password']
           user.set_password=password
           user.save()

class ASerializer(serializers.ModelSerializer)  :
       
    class Meta:
        model = Book
        #ordering=['-id']
        fields='__all__'
        #fields=['id','dated']         
class CustomerRegistrationSerializer(serializers.ModelSerializer)  :
       
    
       name=serializers.CharField(required=True) 
       password = serializers.CharField(required=True)
       password2 = serializers.CharField(required=True)
       email=serializers.CharField(required=True)
       phone=serializers.CharField(required=True,max_length=10) 