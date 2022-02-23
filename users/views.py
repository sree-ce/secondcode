
from calendar import c
from datetime import date

import numbers
from unicodedata import category

from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.template import context
import razorpay
from twilio.rest import Client
from django.views import View
import os
from twilio.rest import Client
from adminpanel.models import CouponCode, product, Category, Variations
from adminpanel.views import variation
from onlineshop.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY, ACCOUNT_SID, AUTH_TOKEN, SERVICES
from users.forms import addressform, customerprofileform, otpform, phoneform
from adminpanel.forms import CouponForm
from users.models import WishList, caertdetails, customer, order, userdetails, Cart
from twilio.rest import Client
from django.views.decorators.cache import never_cache
from django.db.models import Q, Sum
from django.http import HttpResponse, JsonResponse, request
num = ''
no = ''
client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))

# Create your views here.


@never_cache
def home(request):

    total_item = 0
    products = product.objects.all()
    variation = Variations.objects.all()
    categories = Category.objects.all()

    if request.session.has_key('user'):
        user = request.session['user']

        print(user)
        # del request.session['user']
        # return redirect('/')
        try:
            newuser = userdetails.objects.get(username=user)
            wishlist = [
                i.product for i in WishList.objects.filter(user=newuser)]
        except userdetails.DoesNotExist:
            newuser = None
            wishlist = None

        amount = 0.0
        shipping_amount = 40.0
        total_amount = 0.0
        cart_product = [p for p in caertdetails.objects.all()
                        if p.user == newuser]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                # dis_perc = (p.product.price - p.product.total_price)/p.product.price*100
                # tempamount =( p.product.total_price)-p.product.total_price*dis_perc/100
                tempamount = (p.quantity*p.product.total_price)
                amount += tempamount
                total_amount = amount + shipping_amount

        newuser = userdetails.objects.get(username=user)
        total_item = caertdetails.objects.filter(user=newuser).count()
        return render(request, 'app/home.html', {'products': products, 'user': newuser, 'categories': categories, 'total_item': total_item, 'variation': variation, 'wishlist': wishlist, 'total_amount': total_amount, 'amount': amount, 'shipping_amount': shipping_amount})
    else:
        try:

            cart = Cart.objects.get(cart_id=shahin(request))
        except:
            pass

        return render(request, 'app/home.html', {'products': products, 'categories': categories, 'total_item': total_item, 'user': None, 'variation': variation})


@never_cache
def signin(request):

    if request.session.has_key('user'):
        user = request.session['user']
        try:
            newuser = userdetails.objects.get(username=user)
        except userdetails.DoesNotExist:
            newuser = None

        return redirect('/')

    elif request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        print(user)
        if user and (not user.is_superuser):
            request.session['user'] = user.username
            u = userdetails.objects.get(username=request.session['user'])
            try:
                print('user is not')

                cart = Cart.objects.get(cart_id=shahin(request))
                gcart = caertdetails.objects.filter(cart=cart)

                for item in gcart:

                    if caertdetails.objects.filter(product=item.product, user=u).exists():

                        cart_item = caertdetails.objects.get(
                            product=item.product, user=u)
                        cart_item.quantity += item.quantity
                        cart_item.save()
                        item.delete()

                gcart.update(user=u)
                cart.delete()

            except:
                print('dfghjk')

            return redirect('/')

        else:
            if userdetails.objects.filter(username=username).exists():
                try:
                    user = userdetails.objects.get(username=username)
                except userdetails.DoesNotExist:
                    newuser = None
                if not user.is_active:

                    return redirect('signin')
                else:

                    messages.info(request, 'Invalid credentials')
                    return redirect('signin')
    else:

        return render(request, 'app/login.html', {'user': None})


def phone(request):
    global num

    fm = phoneform(request.POST or None)

    if request.method == 'POST':

        if fm.is_valid():

            getNum = request.POST['phone']
            if not userdetails.objects.filter(phone_no=getNum).exists():
                return redirect('phone')

            num = getNum
            sendotp(num)

            request.session['usr'] = getNum
            return redirect('otpverify')

    return render(request, 'app/phonenumber.html', {'forms': fm, 'user': None})


@never_cache
def signup(request):
    global num
    if request.session.has_key('user'):
        user = request.session['user']
        return redirect('/')

    elif request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_no = request.POST['phone_no']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if userdetails.objects.filter(username=username).exists():
                messages.info(request, 'username already exists')
                return redirect('signup')
            elif len(username) > 10:
                messages.info(request, 'username should be short')
                return redirect('signup')
            if username == '':
                messages.info(request, 'username cannot bet empty')
                return redirect('signup')
            elif userdetails.objects.filter(email=email).exists():
                messages.info(request, 'email alredy exists')
                return redirect('signup')
            else:

                user = userdetails.objects.create_user(
                    username=username, password=password, email=email, first_name=first_name, last_name=last_name, phone_no=phone_no)

                request.session['usr'] = user.phone_no
                num = request.POST['phone_no']

                if user and (user.phone_no == num):
                    # num ="+91"+ user.phone_no

                    sendotp(num)
                    print(num)
                    return redirect('otpverify')
        else:
            messages.info(request, 'password did not match')
            return redirect('signup')

    else:

        return render(request, 'app/customerregistration.html', {'user': None})


def sendotp(num):
    global no
    no = '+91'+num
    print(no)
    try:
        account_sid = ACCOUNT_SID
        auth_token = AUTH_TOKEN
        client = Client(account_sid, auth_token)

        verification = client.verify \
            .services(SERVICES) \
            .verifications \
            .create(to=no, channel='sms')

        print(verification.status)
    except:
        print('otp error')


def verify(otp):
    global no
    try:
        account_sid = ACCOUNT_SID
        auth_token = AUTH_TOKEN
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
            .services(SERVICES) \
            .verification_checks \
            .create(to=no, code=otp)

        print(verification_check.status)
        return (verification_check.status)
    except:
        print('error')


def resend(request):

    print(request.session['usr'])
    sendotp(request.session['usr'])
    # return render(request,'app/otp.html')
    return redirect('otpverify')


def otpverify(request):

    if request.session.has_key('usr'):
        user = request.session['usr']

        if request.method == 'POST':

            ofm = otpform(request.POST)
            if ofm.is_valid():

                otp = request.POST['otp']

                print(otp)
                if verify(otp) == 'approved':

                    newuser = userdetails.objects.get(phone_no=user)
                    request.session['user'] = newuser.username

                    if user:

                        u = userdetails.objects.get(
                            username=request.session['user'])
                        try:
                            print('user is not')

                            cart = Cart.objects.get(cart_id=shahin(request))
                            gcart = caertdetails.objects.filter(cart=cart)

                            for item in gcart:

                                if caertdetails.objects.filter(product=item.product, user=u).exists():

                                    cart_item = caertdetails.objects.get(
                                        product=item.product, user=u)
                                    cart_item.quantity += item.quantity
                                    cart_item.save()
                                    item.delete()

                            gcart.update(user=u)
                            cart.delete()

                        except:
                            print('dfghjk')

                        return redirect('/')

                    return redirect('/')
                else:
                    return render(request, 'app/otp.html', {'forms': ofm, 'user': None})
        else:
            ofm = otpform()
            return render(request, 'app/otp.html', {'forms': ofm, 'user': None})


@never_cache
def cart(request):

    return render(request, 'app/addtocart.html')


@never_cache
def sigleproduct(request, id):
    total_item = 0
    products = product.objects.get(id=id)
    variation = Variations.objects.filter(product=products)

    if request.session.has_key('user'):
        user = request.session['user']
        try:
            newuser = userdetails.objects.get(username=user)
            wishlist = [
                i.product for i in WishList.objects.filter(user=newuser)]
        except userdetails.DoesNotExist:
            newuser = None
            wishlist = None

        item_exist = False
        item_exist = caertdetails.objects.filter(
            Q(product=products.id) & Q(user=newuser)).exists()
        newuser = userdetails.objects.get(username=user)
        total_item = caertdetails.objects.filter(user=newuser).count()

        return render(request, 'app/productdetail.html', {'products': products, 'user': newuser, 'item_exist': item_exist, 'total_item': total_item, 'variation': variation, 'wishlist': wishlist})

    else:

        try:

            a = shahin(request)
            print(a)

            cart = Cart.objects.get(cart_id=a)
        except:

            cart = Cart.objects.create(cart_id=shahin(request))

        total_item = caertdetails.objects.filter(cart=cart).count()
        return render(request, 'app/productdetail.html', {'products': products, 'user': None, 'total_item': total_item, 'variation': variation})


@never_cache
def signout(request):

    del request.session['user']

    return redirect('/')


def profile(request):
    total_item = 0
    form = customerprofileform(request.POST or None)

    if request.session.has_key('user'):
        user = request.session['user']
        try:
            newuser = userdetails.objects.get(username=user)

        except userdetails.DoesNotExist:
            newuser = None
        if user:
            total_item = len(caertdetails.objects.filter(user=newuser))

            return render(request, 'profile.html', {'user': newuser, 'form': form, 'active': 'btn-primary', 'total_item': total_item})
    return redirect('signin')


def address(request):

    if request.session.has_key('user'):
        user = request.session['user']

        try:
            newuser = userdetails.objects.get(username=user)
        except userdetails.DoesNotExist:
            newuser = None

        add = customer.objects.filter(user=newuser)
        newuser = userdetails.objects.get(username=user)
        total_item = caertdetails.objects.filter(user=newuser).count()

        return render(request, 'app/address.html', {'add': add, 'user': user, 'total_item': total_item})
    else:
        user = None
        return render(request, 'app/address.html', {'user': user})


def orders(request):

    if request.session.has_key('user'):
        user = request.session['user']
        print(id)
        newuser = userdetails.objects.get(username=user)
        op = order.objects.filter(user=newuser).order_by('-ordered_date')

        order_list = []

        for i in op:

            deli = i.delivered_date
            ord = i.ordered_date
            print(ord)
            if deli:

                today = date.today()
                print(today)
                diff = today-deli
                print(diff)
                if diff.days >= 2:

                    order_list.append(i)

        newuser = userdetails.objects.get(username=user)
        total_item = caertdetails.objects.filter(user=newuser).count()

        return render(request, 'app/orders.html', {'order_placed': op, 'user': newuser, 'total_item': total_item, 'order_list': order_list})

    return render(request, 'app/orders.html')


def checkout(request):

    if request.session.has_key('user'):
        user = request.session['user']
        newuser = userdetails.objects.get(username=user)
        add = customer.objects.filter(user=newuser).order_by('id')

        couponcode = request.GET.get('couponcode')
        coupon_message = None
        coupon = None
        amount = 0.0

        shipping_amount = 40.0
        try:
            buy = int(request.session['buynow'])

            products = product.objects.get(id=buy)
            amount = products.total_price

            total_amount = products.total_price + shipping_amount

            cart_items = None
        except:

            products = None
            total_amount = 0.0
            shipping_amount = 40.0
            cart_items = caertdetails.objects.filter(user=newuser)
            cart_product = [
                p for p in caertdetails.objects.all() if p.user == newuser]

            if cart_product:

                for p in cart_product:
                    tempamount = (p.quantity*p.product.total_price)
                    amount += tempamount
            total_amount = amount + shipping_amount

            total_amount = round(total_amount, 2)

        print(amount)
        DATA = {
            "amount": int(total_amount)*100,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "key1": "value3",
                "key2": "value2"
            }
        }
        client.order.create(data=DATA)

        newuser = userdetails.objects.get(username=user)
        total_item = caertdetails.objects.filter(user=newuser).count()

        if couponcode:

            if CouponCode.objects.filter(code=couponcode).exists():
                code = CouponCode.objects.get(code=couponcode)
                newuser = userdetails.objects.get(username=user)

                if code.active == True:

                    days = code.valid_to-date.today()
                    if days.days > 0:
                        if order.objects.filter(coupon=code, user=newuser).exists():
                            messages.info(request, 'Coupon Already Used')
                            return redirect('checkout')
                        else:
                            coupon = CouponCode.objects.get(code=couponcode)
                            request.session['coupon'] = coupon.code

                        total_amount = (
                            int(amount)-(int(amount)*int(coupon.discount)/100))+shipping_amount
                    else:
                        code.active = False
                        code.save()
                else:
                    messages.info(request, 'Coupon is not Active')
                    return redirect('checkout')
            else:
                coupon_message = 'INVALID COUPON CODE'
                print('couponcode invalid')

        context = {
            'add': add,
            'user': newuser,
            'total_amount': total_amount,
            'cart_items': cart_items,
            'shipping_amount': shipping_amount,
            'amount': int(total_amount)*100,
            'total_item': total_item,
            'coupon_message': coupon_message,
            'coupon': coupon,
            'product': products
        }
        print(total_amount)

        return render(request, 'app/checkout.html', context)
    return redirect('signin')


@never_cache
def cart_id(request):

    if not request.session.session_key:
        request.session.create()

    return request.session.session_key


def shahin(request):

    if not request.session.session_key:
        request.session.create()

    return request.session.session_key


@never_cache
def addtocart(request):

    if request.session.has_key('user'):
        user = request.session['user']
        size = request.GET.get('get_size')

        print(size)
        if int(request.GET.get('mode')) == 1:
            request.session['buynow'] = int(request.GET.get('proid'))
            return redirect('checkout')
        else:
            product_id = int(request.GET.get('proid'))
            if request.method == 'GET':

                products = product.objects.get(id=product_id)
                variation = Variations.objects.get(
                    variation_value=size, product=products)

            try:
                newuser = userdetails.objects.get(username=user)
            except userdetails.DoesNotExist:
                newuser = None
            wish = WishList.objects.filter(user=newuser)
            wish.delete()

            if caertdetails.objects.filter(user=newuser, product_id=product_id, variation=variation).exists():
                cart_items = caertdetails.objects.get(
                    user=newuser, product_id=product_id, variation=variation)
                cart_items.quantity += 1
                cart_items.save()

            else:
                caertdetails.objects.create(
                    user=newuser, product_id=product_id, variation=variation).save()

            return redirect('showcart')
    else:
        if request.method == 'GET':
            size = request.GET['get_size']
            print(size)
            product_id = int(request.GET.get('proid'))

            products = product.objects.get(id=product_id)
            variation = Variations.objects.get(
                variation_value=size, product=products)

        try:
            

            a = shahin(request)

            print(a)

            # get the cart using cart_id present in the cart session
            cart = Cart.objects.get(cart_id=a)

        except:
            cart = Cart.objects.create(
                cart_id=shahin(request)
            )
        cart.save()
        try:
            cart_items = caertdetails.objects.get(
                product_id=product_id, cart=cart, variation=variation)
            cart_items.quantity += 1
            cart_items.save()
        except caertdetails.DoesNotExist:
            cart_items = caertdetails.objects.create(
                product_id=product_id,
                quantity=1,
                cart=cart,
                variation=variation,

            )
        cart_items.save()
    return redirect('showcart')


@never_cache
def showcart(request):

    if request.session.has_key('user'):
        user = request.session['user']
        try:
            newuser = userdetails.objects.get(username=user)
        except userdetails.DoesNotExist:
            newuser = None
        cart = caertdetails.objects.filter(user=newuser)

        print(cart)
        amount = 0.0
        shipping_amount = 40.0
        total_amount = 0.0
        cart_product = [p for p in caertdetails.objects.all()
                        if p.user == newuser]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                # dis_perc = (p.product.price - p.product.total_price)/p.product.price*100
                # tempamount =( p.product.total_price)-p.product.total_price*dis_perc/100
                tempamount = (p.quantity*p.product.total_price)
                amount += tempamount
                total_amount = amount + shipping_amount

            newuser = userdetails.objects.get(username=user)
            total_item = caertdetails.objects.filter(user=newuser).count()
            return render(request, 'app/addtocart.html', {'user': newuser, 'cart': cart, 'total_amount': total_amount, 'tempamount': tempamount, 'amount': amount, 'shipping_amount': shipping_amount, 'total_item': total_item})
        else:
            return render(request, 'app/emptycart.html', {'user': user})
    else:
        try:

            cart = Cart.objects.get(cart_id=shahin(request))
        except:

            cart = Cart.objects.create(cart_id=shahin(request))

        amount = 0.0
        shipping_amount = 40.0
        total_amount = 0.0
        cart_product = [p for p in caertdetails.objects.all()
                        if p.cart == cart]
        print(cart_product)
        if cart_product:
            for p in cart_product:

                tempamount = (p.quantity*p.product.total_price)
                amount += tempamount
                total_amount = amount + shipping_amount

            total_item = caertdetails.objects.filter(cart=cart).count()

            return render(request, 'app/addtocart.html', {'cart': cart_product, 'user': None, 'total_item': total_item, 'total_amount': total_amount, 'tempamount': tempamount, 'amount': amount, 'shipping_amount': shipping_amount})
        else:
            return render(request, 'app/emptycart.html', {'user': None})


def plus_cart(request):
    if request.session.has_key('user'):
        user = request.session['user']
        if request.method == 'GET':

            prod_id = request.GET['prod_id']
            print(prod_id)
            newuser = userdetails.objects.get(username=user)
            c = caertdetails.objects.get(
                Q(variation=prod_id) & Q(user=newuser))
            if c.quantity < c.product.stock:

                c.quantity += 1
                c.save()
                amount = 0.0
                shipping_amount = 40
                cart_product = [
                    p for p in caertdetails.objects.all() if p.user == newuser]
                for p in cart_product:
                    tempamount = (p.quantity*p.product.total_price)
                    amount += tempamount
            else:

                return JsonResponse({'flag': 0})

            data = {

                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount+shipping_amount
            }
            return JsonResponse(data)

    else:
        if request.method == 'GET':

            prod_id = request.GET['prod_id']
            print(prod_id)
            cart = Cart.objects.get(cart_id=cart_id(request))
            cart_items = caertdetails.objects.filter(cart=cart)
            c = caertdetails.objects.get(Q(variation=prod_id) & Q(cart=cart))
            if c.quantity < c.product.stock:

                c.quantity += 1
                c.save()
                amount = 0.0
                shipping_amount = 40
                cart_product = [
                    p for p in caertdetails.objects.all() if p.cart == cart]
                for p in cart_product:
                    tempamount = (p.quantity*p.product.total_price)
                    amount += tempamount

                data = {

                    'quantity': c.quantity,
                    'amount': amount,
                    'totalamount': amount+shipping_amount
                }
                return JsonResponse(data)
            else:
                flag = 0
                data = {

                    'flag': flag
                }
                return JsonResponse(data)


def minus_cart(request):
    if request.session.has_key('user'):
        user = request.session['user']
        if request.method == 'GET':

            prod_id = request.GET['prod_id']
            print(prod_id)
            newuser = userdetails.objects.get(username=user)
            c = caertdetails.objects.get(
                Q(variation=prod_id) & Q(user=newuser))
            c.quantity -= 1
            c.save()
            amount = 0.0
            shipping_amount = 40
            cart_product = [
                p for p in caertdetails.objects.all() if p.user == newuser]
            for p in cart_product:
                tempamount = (p.quantity*p.product.total_price)
                amount += tempamount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount+shipping_amount
            }
            return JsonResponse(data)
    else:
        if request.method == 'GET':

            prod_id = request.GET['prod_id']
            print(prod_id)
            cart = Cart.objects.get(cart_id=cart_id(request))
            c = caertdetails.objects.get(Q(variation=prod_id) & Q(cart=cart))
            c.quantity -= 1
            c.save()
            amount = 0.0
            shipping_amount = 40
            cart_product = [
                p for p in caertdetails.objects.all() if p.cart == cart]
            for p in cart_product:
                tempamount = (p.quantity*p.product.total_price)
                amount += tempamount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount+shipping_amount
            }
            return JsonResponse(data)


def remove_cart(request):
    if request.session.has_key('user'):
        user = request.session['user']
        if request.method == 'GET':

            prod_id = request.GET['prod_id']
            print(prod_id)
            newuser = userdetails.objects.get(username=user)
            c = caertdetails.objects.get(
                Q(variation=prod_id) & Q(user=newuser))
            c.delete()
            amount = 0.0
            shipping_amount = 40
            cart_product = [
                p for p in caertdetails.objects.all() if p.user == newuser]
            for p in cart_product:
                tempamount = (p.quantity*p.product.total_price)
                amount += tempamount
            data = {
                # 'quantity':c.quantity,
                'amount': amount,
                'totalamount': amount+shipping_amount
            }

            return JsonResponse(data)
    else:
        if request.method == 'GET':

            prod_id = request.GET['prod_id']
            print(prod_id)
            cart = Cart.objects.get(cart_id=shahin(request))
            c = caertdetails.objects.get(Q(variation=prod_id) & Q(cart=cart))
            c.delete()
            amount = 0.0
            shipping_amount = 40
            cart_product = [
                p for p in caertdetails.objects.all() if p.cart == cart]
            for p in cart_product:
                tempamount = (p.quantity*p.product.total_price)
                amount += tempamount
            data = {
                # 'quantity':c.quantity,
                'amount': amount,
                'totalamount': amount+shipping_amount
            }

            return JsonResponse(data)


@never_cache
def allproduct(request):

    total_item = 0
    produc = []
    pro = order.objects.all().values('product').annotate(
        pcount=Sum('quantity')).order_by('-pcount')
    categories = Category.objects.all()
    for i in pro:
        produc.append(product.objects.get(id=i['product']))

    subcategories = Category.objects.all()
    variation = Variations.objects.all()
    if request.session.has_key('user'):
        user = request.session['user']
        try:
            newuser = userdetails.objects.get(username=user)
            wishlist = [
                i.product for i in WishList.objects.filter(user=newuser)]
        except userdetails.DoesNotExist:
            newuser = None
            wishlist = None

        newuser = userdetails.objects.get(username=user)
        total_item = caertdetails.objects.filter(user=newuser).count()
        return render(request, 'app/shop.html', {'user': user, 'products': produc, 'total_item': total_item, 'subcategories': subcategories, 'variation': variation, 'wishlist': wishlist, 'categories': categories})
    else:
        try:

            cart = Cart.objects.get(cart_id=shahin(request))
        except:

            cart = Cart.objects.create(cart_id=shahin(request))

        total_item = caertdetails.objects.filter(cart=cart).count()

        return render(request, 'app/shop.html', {'products': produc, 'user': None, 'total_item': total_item, 'variation': variation, 'categories': categories})


@never_cache
def paymentdone(request, pid=-1):

    if request.session.has_key('user'):
        user = request.session['user']

        try:
            newuser = userdetails.objects.get(username=user)

        except userdetails.DoesNotExist:
            newuser = None
        if pid == 1:
            custid = int(request.GET.get('ccustid'))
        elif pid == 2:
            custid = int(request.GET.get('custid'))
        else:
            custid = int(request.GET.get('cccustid'))
        print(custid)
        customers = customer.objects.get(id=custid)

        carts = caertdetails.objects.filter(user=newuser)

        if request.session.has_key('coupon'):

            cp = CouponCode.objects.get(code=request.session['coupon'])
            if request.session.has_key('buynow'):
                products = product.objects.get(
                    id=int(request.session['buynow']))
                order(user=newuser, product=products, quantity=1,
                      customers=customers, coupon=cp).save()
                ord = order.objects.all().order_by('-ordered_date')[0]
                ord.total = ord.product.total_price * ord.quantity
                ord.save()
                products.stock -= 1
                products.save()
            else:
                for c in carts:
                    order(user=newuser, product=c.product, quantity=c.quantity,
                          customers=customers, coupon=cp).save()
                    ord = order.objects.all().order_by('-ordered_date')[0]
                    ord.total = ord.product.total_price * ord.quantity
                    ord.save()
                    c.delete()
                    cart = c.product.stock - c.quantity

                    product.objects.filter(id=c.product.id).update(stock=cart)

            del request.session['coupon']
        else:
            if request.session.has_key('buynow'):
                products = product.objects.get(
                    id=int(request.session['buynow']))
                order(user=newuser, product=products,
                      quantity=1, customers=customers).save()

                ord = order.objects.all().order_by('-ordered_date')[0]
                ord.total = ord.product.total_price * ord.quantity
                ord.save()

                products.stock -= 1
                products.save()

            else:

                for c in carts:
                    order(user=newuser, product=c.product,
                          quantity=c.quantity, customers=customers).save()
                    ord = order.objects.all().order_by('-ordered_date')[0]
                    ord.total = ord.product.total_price * ord.quantity
                    ord.save()

                    c.delete()

        if request.session.has_key('buynow'):
            del request.session['buynow']
        return redirect('invoice')


@never_cache
def ordercancel(request, id):

    if request.session.has_key('user'):

        user = request.session['user']

        newuser = userdetails.objects.get(username=user)

        orders = order.objects.get(user=newuser, id=id)
        orders.ordered = 'Cancelled'
        orders.save()

        return redirect('orders')


@never_cache
def returnorder(request, id):

    if request.session.has_key('user'):

        user = request.session['user']

        newuser = userdetails.objects.get(username=user)

        orders = order.objects.get(user=newuser, id=id)
        orders.ordered = 'Return'
        orders.save()

        return redirect('orders')


@never_cache
def add_address(request):

    total_item = 0
    adfm = addressform(request.POST or None)

    if request.session.has_key('user'):
        user = request.session['user']

        try:
            newuser = userdetails.objects.get(username=user)
        except userdetails.DoesNotExist:
            newuser = None

        if request.method == 'POST':

            if adfm.is_valid():

                name = adfm .cleaned_data['name']
                phone = adfm .cleaned_data['phone']
                address = adfm .cleaned_data['address']
                locality = adfm .cleaned_data['locality']
                city = adfm .cleaned_data['city']
                state = adfm .cleaned_data['state']
                zipcode = adfm .cleaned_data['zipcode']

                save = customer(user=newuser, name=name, phone=phone, address=address,
                                locality=locality, city=city, state=state, zipcode=zipcode)
                save.save()

                return redirect('checkout')
            else:
                return redirect('add_address')

        else:
            newuser = userdetails.objects.get(username=user)
            total_item = caertdetails.objects.filter(user=newuser).count()
            return render(request, 'app/add_address.html', {'user': newuser, 'form2': adfm, 'total_item': total_item})
    return redirect('signin')


@never_cache
def edit_address(request, id):

    total_item = 0
    if request.session.has_key('user'):
        user = request.session['user']
        try:
            newuser = userdetails.objects.get(username=user)
        except userdetails.DoesNotExist:
            newuser = None

        if request.method == 'POST':
            ed = customer.objects.get(pk=id)
            add = addressform(request.POST, instance=ed)
            if add.is_valid():
                name = request.POST['name']
                phone = request.POST['phone']
                address = request.POST['address']
                locality = request.POST['locality']
                city = request.POST['city']
                state = request.POST['state']
                zipcode = request.POST['zipcode']

                customer.objects.filter(id=id, user=newuser).update(
                    name=name, phone=phone, address=address, locality=locality, city=city, state=state, zipcode=zipcode)

                return redirect('checkout')

        else:
            ed = customer.objects.get(pk=id)
            add = addressform(instance=ed)
            newuser = userdetails.objects.get(username=user)
            total_item = caertdetails.objects.filter(user=newuser).count()
            return render(request, 'app/editaddress.html', {'user': newuser, 'form': add, 'active': 'btn-primary', 'total_item': total_item})
    return redirect('signin')


@never_cache
def delete_address(request):
    if request.session.has_key('user'):
        user = request.session['user']

        id = request.GET['id']
        customer.objects.filter(id=id).delete()
    return redirect('checkout')


@never_cache
def wishlist(request):

    product_id = request.GET.get('wish_list')

    if request.session.has_key('user'):
        user = request.session['user']

        if request.method == 'GET':

            products = product.objects.get(id=product_id)

        try:
            newuser = userdetails.objects.get(username=user)
        except userdetails.DoesNotExist:
            newuser = None

        if WishList.objects.filter(user=newuser, product=products).exists():

            return redirect('showWishlist')
        else:
            WishList.objects.create(user=newuser, product=products).save()

            return redirect('showWishlist')
    return redirect('signin')


@never_cache
def showWishlist(request):

    if request.session.has_key('user'):
        user = request.session['user']
        newuser = userdetails.objects.get(username=user)
        variation = Variations.objects.all()
        wishlist = WishList.objects.filter(user=newuser)

        if wishlist:

            context = {
                'user': newuser,
                'wishlist': wishlist,
                'variation': variation
            }

            return render(request, 'app/wishlist.html', context)
        else:
            return render(request, 'app/emptywishlist.html', {'user': newuser})

    return redirect('signin')


@never_cache
def removewishlist(request):
    if request.session.has_key('user'):
        user = request.session['user']
        id = request.GET.get('id')

        WishList.objects.filter(id=id).delete()
        return redirect('showWishlist')
    return redirect('signin')


@never_cache
def invoice(request):
    if request.session.has_key('user'):
        user = request.session['user']

        users = userdetails.objects.get(username=user)

        invoice_details = order.objects.filter(
            user=users).order_by('-ordered_date')
        print(invoice_details)

        return render(request, 'app/invoice.html', {'user': user, 'users': users, 'invoice_details': invoice_details})


def search(request):
    if request.session.has_key('user'):
        user = request.session['user']
        products = product.objects.all()
        variation = Variations.objects.all()
        try:
            newuser = userdetails.objects.get(username=user)
            wishlist = [
                i.product for i in WishList.objects.filter(user=newuser)]
        except userdetails.DoesNotExist:
            newuser = None
            wishlist = None
        if request.method == 'POST':
            q = request.POST['q']
            posts = product.objects.filter(category__name__contains=q)

        else:

            posts = product.objects.all()
        return render(request, 'app/searchproduct.html', {'detls': posts, 'user': newuser, 'products': products, 'variation': variation, 'wishlist': wishlist})

    else:
        return render(request, 'app/searchproduct.html', {'user': None})


def filter(request):
    if request.session.has_key('user'):
        user = request.session['user']
        variation = Variations.objects.all()
        try:
            newuser = userdetails.objects.get(username=user)
            wishlist = [
                i.product for i in WishList.objects.filter(user=newuser)]
        except userdetails.DoesNotExist:
            newuser = None
            wishlist = None

        if request.method == 'GET':

            min = request.GET.get('min')
            max = request.GET.get('max')

            if min or max:

                products = product.objects.filter(
                    total_price__gte=min, total_price__lte=max)
            else:
                products = product.objects.all()

        return render(request, 'app/filter.html', {'products': products, 'variation': variation, 'user': newuser, 'wishlist': wishlist})
    return redirect('signin')
