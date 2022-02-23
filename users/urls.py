from os import name
from django.urls import path
from . import views


urlpatterns = [ 
    path('',views.home,name='home'),
    path('signin',views.signin,name='signin'),
    path('signup',views.signup,name='signup'),
    # path('cart',views.cart,name='cart'),
    path('phone',views.phone,name='phone'),
    path('otpverify',views.otpverify,name='otpverify'),
    path('signout',views.signout,name='signout'),
    path('singleproduct/<int:id>/',views.sigleproduct,name='singleproduct'),

    
    path('cartadd/',views.addtocart,name='cartadd'),
    path('showcart',views.showcart,name='showcart'),
    path('pluscart/',views.plus_cart,name='pluscart'),
    path('minuscart/',views.minus_cart,name='minuscart'),
    path('removecart/',views.remove_cart,name='removecart'),
 

    path('wishlist',views.wishlist,name='wishlist'),
    path('showWishlist',views.showWishlist,name='showWishlist'),
    path('removewishlist',views.removewishlist,name='removewishlist'),

    path('products',views.allproduct,name='products'),
    path('profile',views.profile,name='profile'),
 

  
    path('orders',views.orders,name='orders'),
    path('checkout',views.checkout,name='checkout'),
    path('invoice',views.invoice,name='invoice'),
  
  
    path('paymentdone/<int:pid>/',views.paymentdone,name='paymentdone'), 
    path('ordercancel/<int:id>/',views.ordercancel,name='ordercancel'),
    path('returnorder/<int:id>/',views.returnorder,name='returnorder'),  

    path('address',views.address,name='address'),

    path('add_address',views.add_address,name='add_address'),
    path('edit_address/<int:id>/',views.edit_address,name='edit_address'),
    path('delete_address',views.delete_address,name='delete_address'),

    path('resend',views.resend,name='resend'),
    path('search',views.search,name='search'),

    path('filter',views.filter,name='filter'),
    
 
]