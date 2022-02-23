
from urllib import response
from django.http import HttpResponse, request
from django.shortcuts import render,redirect
from django.contrib import auth
from users.models import caertdetails, userdetails,order
from .forms import CouponForm, loginform, orderform, productform,categoryform, sizeform
from .models import  CouponCode,  Category, Variations,product
from django.views.decorators.cache import never_cache
from datetime import date, datetime
from django.db.models import Count,Sum
import xlwt

# Create your views here.
@never_cache
def adminpanel(request):
    if request.session.has_key('admin'):
        admin = request.session['admin']

        orders = order.objects.all()
        products = product.objects.all()
        subcategories = Category.objects.all()
        users = userdetails.objects.all()
        usercount = users.count()
        ordercount = orders.count()
    
        return render(request,'admin2.html',{'admin':admin,'products':products, 'orders':orders,'subcategories':subcategories,'usercount':usercount,'ordercount':ordercount})
    return redirect('admin_login')
    
@never_cache
def adminlogin(request):
    fm = loginform()
    if request.session.has_key('admin'):
        admin = request.session['admin']
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        admin = auth.authenticate(username=username, password=password)

        if admin and admin.is_superuser:
            request.session['admin'] = admin.username
            print(admin)
            return redirect('adminpanel')
        else:

            return render(request, 'adminlogin.html', {'form': fm,'admin':admin})
            
    return render(request, 'adminlogin.html', {'form': fm})
@never_cache
def userview(request):
    if request.session.has_key('admin'):
        admin = request.session['admin']

        users = userdetails.objects.all()

        context = {
            'users':users,
            'admin':admin
        
        }
        return render(request,'user.html',context)
    return render('admin_login')
@never_cache
def blockUser(request, id):
    if request.session.has_key('admin'):
        admin = request.session['admin']

    user = userdetails.objects.get(id=id)
    user.is_active = not(user.is_active)
    user.save()
    return redirect('userview')
@never_cache
def showproducts(request):
    if request.session.has_key('admin'):
        admin = request.session['admin']


        products = product.objects.all()

        return render(request, 'showproduct.html', {'products': products,'admin':admin})
    return redirect('admin_login')


@never_cache
def addproducts(request):
    if request.session.has_key('admin'):
        admin =  request.session['admin']
        pdfm = productform(request.POST or None, request.FILES or None)
        if request.method == 'POST':
        
            if pdfm.is_valid():
                pdfm.save()
                return redirect('showproducts')
            else:
                print(pdfm.errors)
            
                return render(request, 'addproduct.html', {'pdtfm': pdfm,'admin':admin})
        else:
            return render(request, 'addproduct.html', {'pdtfm': pdfm,'admin':admin})
    return redirect('admin_login')


@never_cache
def editproducts(request, id):
    if request.session.has_key('admin'):
        admin = request.session['admin']
        products = product.objects.all()
        if request.method == 'POST':
            pe = product.objects.get(pk=id)
            pdt = productform(request.POST, request.FILES, instance=pe)
            
            if pdt.is_valid():
                pdt.save()
                return redirect('showproducts')
        else:
            pe = product.objects.get(pk=id)
            pdt = productform(instance=pe)
        return render(request, 'updateproduct.html', {'pdf': pdt,'admin':admin,'id':id,'pe':pe})
    return redirect('admin_login')



@never_cache
def deleteproduct(request):
    if request.session.has_key('admin'):
        admin = request.session['admin']
        id = request.GET.get('id')
        product.objects.filter(id=id).delete()
        return redirect('showproducts')
    return redirect('admin_login')




@never_cache
def showcategory(request):
    if request.session.has_key('admin'):
        admin = request.session['admin']
        subcat = Category.objects.all()

        context = {
            'subcategory': subcat,
            'admin':admin
        }
        return render(request, 'subcategory.html', context)
    return redirect('admin_login')


@never_cache
def addcategory(request):
    if request.session.has_key('admin'):
        admin = request.session['admin']
        addfm = categoryform(request.POST or None)
        if request.method == 'POST':
        
            if addfm.is_valid():
                addfm.save()
                return redirect('showsubcategory')

            else:
                print(addfm.errors)
                return render(request, 'addsubcategory.html', {'subform': addfm,'admin':admin})
        else:
            return render(request, 'addsubcategory.html', {'subform': addfm,'admin':admin})
    return redirect('admin_login')

@never_cache
def editcategory(request, id):
    if request.session.has_key('admin'):
        admin = request.session['admin']
        if request.method == 'POST':
            ed = Category.objects.get(pk=id)
            sub = categoryform(request.POST, instance=ed)
            if sub.is_valid():
                sub.save()
                return redirect('showsubcategory')
        else:
            ed = Category.objects.get(pk=id)
            sub = categoryform(instance=ed)
        return render(request, 'editsubcategory.html', {'editform': sub,'admin':admin})
    return redirect('admin_login')



@never_cache
def deletecategory(request):
    if request.session.has_key('admin'):
        admin = request.session['admin']
        id = request.GET.get('id')
        Category.objects.filter(id=id).delete()
    return redirect('showsubcategory')
  
@never_cache
def variation(request):
    if request.session.has_key('admin'):
        admin = request.session['admin']

        variation = Variations.objects.all()
    

        context = { 
            'variation':variation,
            'admin':admin
        }
        return render (request,'app/variation.html',context)
    return redirect('admin_login')
            
  
@never_cache  
def addvariation(request):
    if request.session.has_key('admin'):
        admin = request.session['admin']

        pdfm = sizeform(request.POST or None)
        if request.method == 'POST':

            if pdfm.is_valid():
                pdfm.save()
                return redirect('variation')
            else:
                return render(request, 'variationform.html', {'fm': pdfm,'admin':admin})
        else:
            return render(request,'variationform.html', {'fm': pdfm,'admin':admin})

    else:
        return redirect('admin_login')


@never_cache
def showorders(request):
    if request.session.has_key('admin'):
        admin = request.session['admin']

        orders = order.objects.all().order_by('-ordered_date')
        
    

        context = { 
            'orders':orders,
            'admin':admin
        }
        return render (request,'adminorder.html',context)
    return redirect('admin_login')

@never_cache
def editorder(request,id):
    if request.session.has_key('admin'):
        admin = request.session['admin']
        od = order.objects.get(id=id)
        form = orderform()
        if request.method == 'POST':
            form = orderform(request.POST,instance=od)
            if form.is_valid():
                form.save()
                if od.ordered == 'Delivered':
                    order.objects.filter(id = id).update(delivered_date = datetime.now())
                return redirect('adorders')
        else:
            od = order.objects.get(pk=id)
            form = orderform(instance=od)
        return render(request,'orderedit.html',{'form':form,'admin':admin})
    return redirect('admin_login')

@never_cache
def export_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attatchments;filename=SalesReport'+\
        str(datetime.now())+'.xls'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('SalesReport')
    row_num = 0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True
    columns = ['ordered_date','customers','product','quantity','total']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style=xlwt.XFStyle()
    rows = order.objects.all().values_list('ordered_date','customers','product','quantity','total')
    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
    wb.save(response)

    return response
@never_cache
def offertable(request):
    if request.session.has_key('admin'):
        admin =  request.session['admin']
        products = product.objects.all()

        return render(request,'offertable.html',{'admin':admin,'products':products})
    return redirect('admin_login')
@never_cache
def offerview(request):
    if request.session.has_key('admin'):
        admin =  request.session['admin']

        products = product.objects.all()

        return render(request,'productoffer.html',{'admin':admin,'products':products})
    return redirect('admin_login')
@never_cache
def productoffer(request,id):

    if request.session.has_key('admin'):
        admin =  request.session['admin']
        
           
        if request.method == 'POST':

          
            discount = request.POST['discount']
            data = product.objects.get(id=id)
            
            data.discount = discount
            data.save()
            data.total_price = (int(data.price)-(int(data.price)*int(data.discount)/100))
            
            data.save()

            print(discount)
            print(data.total_price)
           
            return redirect('offertable')

        return redirect('admin_login')
@never_cache       
def catoffertable(request):
    if request.session.has_key('admin'):
        admin =  request.session['admin']
        categories = Category.objects.all()

        return render(request,'catoffertable.html',{'admin':admin,'categories':categories})
    return redirect('admin_login')
@never_cache
def subofferview(request):
    if request.session.has_key('admin'):
        admin = request.session['admin']

        subcategories = Category.objects.all()
        return render(request,'suboffer.html',{'admin':admin,'subcategories':subcategories})

    return redirect('admin_login')
@never_cache
def suboffer(request,id):
    if request.session.has_key('admin'):
        admin = request.session['admin']

        if request.method == 'POST':

            discount = int(request.POST['discount'])

            data = Category.objects.get(id=id)

            data.discount = discount
            data.save()
            product_list = product.objects.filter(category=data)
            for products in product_list:
                if data.discount >= products.discount:
                    products.total_price = (int(products.price)-(int(products.price)*int(data.discount)/100))
                else:
                    products.total_price = (int(products.price)-(int(products.price)*int(products.discount)/100))
                products.save()

            return redirect('catoffertable')
    return redirect('admin_login')

@never_cache
def showcoupon(request):
    if request.session.has_key('admin'):
        admin = request.session['admin']

        coupons = CouponCode.objects.all()

        return render(request,'coupontable.html',{'coupons':coupons,'admin':admin})
    return redirect('admin_login')

@never_cache
def couponoffer(request):
    if request.session.has_key('admin'):
        admin = request.session['admin']

        cform = CouponForm(request.POST or None)
        if request.method == 'POST':

            if cform.is_valid():
                cform.save()   
                return redirect('showcoupon')
            else:
                return render(request,'coupon.html',{'form':cform,'admin':admin})     

        return render(request,'coupon.html',{'form':cform,'admin':admin})
    return redirect('admin_login')

@never_cache
def deletecoupon(request):
    if request.session.has_key('admin'):
        admin = request.session['admin']

        id = request.GET.get('id')
        CouponCode.objects.filter(id=id).delete()
        return redirect('showcoupon')
    return redirect('admin_login')

    

@never_cache
def logout(request):

    del request.session['admin']

    return redirect('admin_login')

@never_cache
def daily_report(request):
    if request.session.has_key('admin'):
        if request.method == 'POST':
            print('-------------------------------------------')
            fromdate = request.POST['from']
            to = request.POST['to']
            if to != '':
                setto = to.split('-')
                if (int(setto[2])+1) < 10:
                    setto[2] = '0'+str(int(setto[2])+1)
                else:
                    setto[2] = str(int(setto[2])+1)
                todate = '-'.join(setto)
            else:
                todate = ''
            request.session['fromdate'] = fromdate
            request.session['todate'] = todate
            if fromdate == '' and todate == '':
                report = order.objects.all().order_by('-ordered_date')
            elif fromdate == '':
                report = order.objects.filter(orderdate__lt=todate).order_by('-ordered_date')
            elif todate == '':
                report = order.objects.filter(
                    ordered_date__gte=fromdate).order_by('-ordered_date')
            else:
                report = order.objects.filter(
                    ordered_date__range=[fromdate, todate]).order_by('-ordered_date')
            return render(request, 'salesreport.html', {'report': report})
   

    else:
        return redirect('admin_login')

def year_report(request):
    if request.session.has_key('admin'):
        if request.method == "POST":
            year = int(request.POST['year'])
            if year!='':
                report =order.objects.filter(ordered_date__year = year).order_by('-ordered_date')
            else:
                report = order.objects.all().order_by('-ordered_date')


            return render(request, 'salesreport.html',{'report':report})
      
    else:
        return redirect('admin_login')

def month_report(request):
    if request.session.has_key('admin'):
        if request.method == "POST":
            month_report = request.POST['month']
            print(month_report)
            if month_report!='':
                month = month_report.split('-')
                report = order.objects.filter(ordered_date__month = month[1],ordered_date__year = month[0]).order_by('-ordered_date')
            else:
                report = order.objects.all().order_by('-ordered_date')
            return render(request, 'salesreport.html',{'report':report})
        
    else:
        return redirect('admin_login')
    
def salesreport(request):
    if request.session.has_key('admin'):
        report = order.objects.filter(ordered = 'Delivered')
     
        return render(request,'salesreport.html',{'report':report})
       
         