
from django.contrib.auth.forms import UserCreationForm

from adminpanel.models import CouponCode


from . models import customer
from django import forms
from django.forms import ModelForm

class otpform(forms.Form):
    otp = forms.CharField(max_length=6)

class phoneform(forms.Form):
    phone = forms.CharField(max_length=10)
    def clean(self):
        cleaned_data = super(phoneform,self).clean()
        phone=cleaned_data.get('phone')

        if phone == '':
            self.add_error('phone','phone field cannot be empty')


class customerprofileform(forms.ModelForm):
    class Meta:
        model = customer
        fields = ['name','phone','email','address','locality','city','zipcode','state']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.NumberInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),

        }
    def clean(self):
        cleaned_data = super(customerprofileform,self).clean()
        name=cleaned_data.get('name')
        locality = cleaned_data.get('locality')
        city = cleaned_data.get('city')
        state = cleaned_data.get('state')
        zipcode = cleaned_data.get('zipcode')
        print(name)

        if name == '':
            self.add_error('name','Name field cannot be empty')
            

        if len(locality) == '':
            self.add_error('locality','please select your locality')
            

        if zipcode == '':
            self.add_error('zipcode','zipcode cannot be null')

class addressform(forms.ModelForm):
    class Meta:
        model = customer
        fields = ['name','phone','address','locality','city','zipcode','state']
        widgets = {
            
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.NumberInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),

        }
    def clean(self):
        cleaned_data = super(addressform,self).clean()
        name=cleaned_data.get('name')
        locality = cleaned_data.get('locality')
        address = cleaned_data.get('address')
        state = cleaned_data.get('state')
        zipcode = cleaned_data.get('zipcode')
        print(name)

        if name == '':
            self.add_error('name','Name field cannot be empty')
            

        if len(locality) == '':
            self.add_error('locality','please select your locality')
            

        if zipcode == '':
            self.add_error('zipcode','zipcode cannot be null')

        if address == '':
            self.add_error('address','address cannot be null')
