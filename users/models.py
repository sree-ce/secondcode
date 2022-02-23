

from math import prod
from os import name
from pickle import TRUE


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.forms import BooleanField, CharField

from adminpanel.models import CouponCode, Variations, product




class userdetails(AbstractUser):
    
    phone_no = models.CharField(max_length=10,blank=True,unique=True,null=True)
    password2=models.CharField(max_length=10)

class Cart(models.Model):
 
    cart_id = models.CharField(max_length=250,blank=True,null=True)
    

    def __str__(self):
        return self.cart_id
    
   
class caertdetails(models.Model):
    user = models.ForeignKey(userdetails,on_delete=models.CASCADE,null=True)
    cart = models.ForeignKey(Cart,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(product,on_delete=models.CASCADE,default=True)
    quantity = models.PositiveIntegerField(default=1)
    variation = models.ForeignKey(Variations,on_delete=models.SET_NULL,null=True,blank=True)

    @property
    def total_cost(self):
        return self.quantity * self.product.total_price

MinValueValidator
STATE_CHOICES = (
    ('Kerala','Kerala'),
    ('Karnataka','Karnataka'),
    ('Tamil Nadu','Tamil Nadu'),
    
)
MinValueValidator
STATUS_CHOICES = (
    ('Placed','Placed'),
    ('Packed','Packed'),
    ('Shipped','Shipped'),
    ('Delivered','Delivered'),
  
)

class customer(models.Model):
    user = models.ForeignKey(userdetails,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=True)
    phone = models.CharField(max_length=10,null=True,blank=True,unique=True)
    email = models.EmailField(max_length=250,null=True,blank=True)
    address=models.CharField(max_length=500,null=True,blank=True)
    locality = models.CharField(max_length=200,blank=True)
    city = models.CharField(max_length=50,blank=True)
    zipcode = models.IntegerField(blank=True,null=True)
    state = models.CharField(choices=STATE_CHOICES,max_length=50,blank=True)

    def __str__(self):
        return self.name



class order(models.Model):
    user = models.ForeignKey(userdetails,on_delete=models.CASCADE)
    customers = models.ForeignKey(customer,on_delete=models.CASCADE,default=True)
    coupon = models.ForeignKey(CouponCode,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(product,on_delete=models.CASCADE,default=True)
    delivered_date = models.DateField(blank=True,null=True)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)
    ordered = models.CharField(choices=STATUS_CHOICES,max_length=50,blank=True)
    quantity = models.IntegerField(default=1)
    total = models.FloatField(default=0)
    variation = models.ForeignKey(Variations,on_delete=models.SET_NULL,null=True,blank=True)
    
 

    def __str__(self):
        return self.user.username
    
    @property
    def total_cost(self):
        shipping_amount = 40
        return self.quantity * self.product.total_price + shipping_amount
    


class orderplaced(models.Model):
    user = models.ForeignKey(userdetails,on_delete=models.CASCADE)
    customer = models.ForeignKey(customer,on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='pending')


class Customers(models.Model):
    user = models.OneToOneField(userdetails,on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    device = models.CharField(max_length=20,null=True,blank=True)


    def __str__(self):
        if self.name:
            name = self.name

        else:
            name = self.device
        return str(name)

class WishList(models.Model):
    product = models.ForeignKey(product,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(userdetails,on_delete=models.SET_NULL,null=True)
    variation = models.ForeignKey(Variations,on_delete=models.SET_NULL,null=True)
    def __unicode__(self):
        return self.product


   