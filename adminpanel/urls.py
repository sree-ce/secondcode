from django import views
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('adminpanel',views.adminpanel,name='adminpanel'),
    path('admin_login',views.adminlogin,name='admin_login'),
    path('userview',views.userview,name='userview'),
    path('blockuser/<int:id>',views.blockUser,name='blockuser'),

    path('variation',views.variation,name='variation'),
    path('addvariation',views.addvariation,name='addvariation'),

    path('offertable',views.offertable,name='offertable'),
    path('offerview',views.offerview,name='offerview'),
    path('productoffer/<int:id>/',views.productoffer,name='productoffer'),

    path('subofferview',views.subofferview,name='subofferview'),
    path('catoffertable',views.catoffertable,name='catoffertable'),
    path('suboffer/<int:id>/',views.suboffer,name='suboffer'),

    path('showcoupon',views.showcoupon,name='showcoupon'),
    path('couponoffer',views.couponoffer,name='couponoffer'),
    path('deletecoupon',views.deletecoupon,name='deletecoupon'),

    path('export_excel',views.export_excel,name='export_excel'),

    path('adorders',views.showorders,name='adorders'),
    path('editorder/<int:id>/',views.editorder,name='editorder'),
   

    path('showproducts',views.showproducts,name='showproducts'),
    path('addproduct',views.addproducts,name='addproduct'),
    path('editpdt/<int:id>/',views.editproducts,name='editpdt'),
    path('deletepdt',views.deleteproduct,name='deletepdt'),


    path('showsubcategory',views.showcategory,name='showsubcategory'),
    path('addsubcategory',views.addcategory,name='addsubcategory'),
    path('editsubcategory/<int:id>/',views.editcategory,name='editsubcategory'),
    path('deletesubcategory',views.deletecategory,name='deletesubcategory'),

    path('logout',views.logout,name='logout'),

    path('salesreport',views.salesreport,name='salesreport'),
    path('daily_report',views.daily_report,name='daily_report'),
    path('year_report',views.year_report,name='year_report'),
    path('month_report',views.month_report,name='month_report'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)