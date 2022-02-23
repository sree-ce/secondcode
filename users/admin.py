from django.contrib import admin

from users.models import *


# Register your models here.
admin.site.register(userdetails)
admin.site.register(caertdetails)
admin.site.register(customer)
admin.site.register(Cart)
admin.site.register(order)
admin.site.register(WishList)



