from django import forms
from django.contrib import messages
from django.db import models
from django.db.models import fields
from django.forms import CharField, PasswordInput, ValidationError, widgets
from django.http import request
from adminpanel.models import CouponCode, Variations, product, Category
from users.models import order


class loginform(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(widget=PasswordInput)
 

class productform(forms.ModelForm):
    images = forms.ImageField(widget=forms.FileInput)
    images2 = forms.ImageField(widget=forms.FileInput)
    images3 = forms.ImageField(widget=forms.FileInput)
    class Meta:
        model = product
        fields = ['Name','description','category','price','color','stock','images','images2','images3']
       



    def clean(self):
        cleaned_data = super(productform,self).clean()
        Name=cleaned_data.get('Name')
        description = cleaned_data.get('description')
        price = cleaned_data.get('price')
        stock = cleaned_data.get('stock')
        print(Name)

 

        if Name == '':
            self.add_error('Name','Name field cannot be empty')

        if len(description)<5:
            self.add_error('description','description not be short')
        if price == '':
            self.add_error('price','price cannot be empty')
          
        if price < 0 :
            self.add_error('price','price cannot be negative ')
        if price == 0:
            self.add_error('price','price cannot be Zero')
      
        if stock == '':
            self.add_error('stock','stock field cannot be empty')
        
     
         



class categoryform(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
      

    def clean(self):
        cleaned_data = super(categoryform,self).clean()
        name=cleaned_data.get('name')
      
       
        if name == '':
            self.add_error('name','Name field cannot be empty')
        
     




class sizeform(forms.ModelForm):
    class Meta:
        model = Variations
        fields = ['product','variation_category','variation_value','is_active']
      
    

class orderform(forms.ModelForm):
    class Meta:
        model = order
        fields = ['ordered']
 

class CouponForm(forms.ModelForm):
    class Meta:
        model = CouponCode
        fields = ['code','valid_from','valid_to','discount','active']  

        
    def clean(self):
        cleaned_data = super(CouponForm,self).clean()
        
        code=cleaned_data.get('code')
        valid_from=cleaned_data.get('valid_from')
        valid_to=cleaned_data.get('valid_to')
        discount=cleaned_data.get('discount')

        

        if code == '':
            self.add_error('code','Please Enter the coupon code')

        if valid_from == '':
            self.add_error('valid_from','Please enter the valid from date')

        if valid_to == '':
            self.add_error('valid_to','Please enter the valid to date')

        if discount < 0:
            self.add_error('discount','Discount cannot be negative')



    