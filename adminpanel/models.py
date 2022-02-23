

from django.conf import settings
from django.db import models
from django import forms
settings.AUTH_USER_MODEL
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.

class loginform(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)




class Category(models.Model):
  
    name = models.CharField(max_length=20,blank=True)
  
    discount = models.FloatField(blank=True,default=0)
    def __str__(self):
        return self.name





    
MinValueValidator
COLOR_CHOICES = (
    ('Black','Black'),
    ('Red','Red'),
    ('Pink','Pink'),
    ('Green','Green'),
    ('Purple','Purple'),
    ('Yellow','Yellow'),
    ('Violet','Violet'),
    ('White','White'),
    ('Orange','Orange'),
    ('Blue','Blue'),
)
   
   

class product(models.Model):
   
    Name = models.CharField(max_length=20,blank=True)
    description = models.TextField(max_length=120,blank=True)
  
    category= models.ForeignKey(Category,on_delete=models.CASCADE,default=True)
    discount=models.FloatField(null=True,blank=True,default=0)
    price = models.FloatField(max_length=20,blank=True,null=True)
  
    
    color = models.CharField(choices=COLOR_CHOICES,max_length=200,blank=True)
    
    stock = models.IntegerField(default=1,null=True,blank=True)
    images = models.ImageField(upload_to='medias',null=True,blank=True, verbose_name='')
    images2 = models.ImageField(upload_to='medias',null=True,blank=True, verbose_name='')
    images3 = models.ImageField(upload_to='medias',null=True,blank=True, verbose_name='')
    
    total_price = models.FloatField(max_length=20,blank=True,null=True)

    def __str__(self):
        return self.Name

    # def save(self, *args, **kwargs):
    #     self.total_price = round(self.total_price, 2)
    #     super(product, self).save(*args, **kwargs)


class CouponCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    code = models.CharField(max_length=10,blank=True,unique=True)
    valid_from = models.DateField(blank=True)
    valid_to = models.DateField(blank=True)
    discount = models.FloatField(max_length=10,null=True,blank=True,validators=[MinValueValidator(0),
                                                                                 MaxValueValidator(90)])
    used = models.IntegerField(default=0,null=True)
    active = models.BooleanField()

    def __str__(self):
        return self.code                                                                                

    

class productimg(models.Model):
    
    image =  models.ImageField(upload_to='medias',null=True,blank=True, verbose_name='')
    product = models.ForeignKey(product,on_delete=models.CASCADE)


# class VariationsManager(models.Manager):
#     def size(self):
#         return super(VariationsManager,self).filter(product='')

variation_category_choices = (

    ('Size','Size'),
  
)
class Variations(models.Model):
    product = models.ForeignKey(product,on_delete=models.SET_NULL,null=True)
    variation_category = models.CharField(choices=variation_category_choices,max_length=100)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.product

   




        