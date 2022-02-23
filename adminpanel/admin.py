
from django.contrib import admin

from adminpanel.models import *

class productimgTublerinline(admin.TabularInline):
    model = productimg

class productAdmin(admin.ModelAdmin):
    inlines = [productimgTublerinline]

# Register your models here.

admin.site.register(Category)
admin.site.register(product,productAdmin)
admin.site.register(Variations)

admin.site.register(CouponCode)

admin.site.register(productimg)






