from django.http import HttpResponse
from django.shortcuts import *
from .models import *
from django.contrib.auth import *
from django.contrib import messages
import json


def home(request):
    if request.user.is_staff:
        return redirect('admindashboard')
    data = Carousel.objects.all()
    dic = {'data':data}
    return render(request, 'index.html', dic)       
         
def index(request):
    return render(request, 'navigation.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request, 'contact.html')     


def main(request):
    if request.user.is_staff:
        return redirect('admindashnoard')
    data = Carousel.objects.all()
    dic = {'data':data}
    return render(request, 'index.html', dic) 

def adminLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                messages.success(request,"Login Successfully")
                return redirect('admindashboard')
            else:
                messages.success(request,"Invalid Credentials")
        except:
            messages.success(request, "Invalid Credentials")
    return render(request, 'admin_login.html')

def adminHome(request):
    if not request.User.is_staff:
        return redirect('adminlogin')
    return render(request, 'admin_base.html')

def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('adminlogin')
    user = UserProfile.objects.filter()
    category = Category.objects.filter()
    product = Product.objects.filter()
    new_order = Booking.objects.filter(status=1)
    dispatch_order = Booking.objects.filter(status=2)
    way_order = Booking.objects.filter(status=3)
    deliver_order = Booking.objects.filter(status=4)
    cancel_order = Booking.objects.filter(status=5)
    return_order = Booking.objects.filter(status=6)
    order = Booking.objects.filter()
    read_feedback = Feedback.objects.filter(status=1)
    unread_feedback = Feedback.objects.filter(status=2)
    return render(request, 'admin_dashboard.html', locals())


def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        Category.objects.create(name=name)
        messages.success(request, "Category added")
        return redirect('view_category')
    return render(request, 'add_category.html', locals())

def view_category(request):
    if not request.user.is_staff:
        return redirect('adminlogin')
    category = Category.objects.all()
    return render(request, 'view_category.html', locals())

def edit_category(request, pid):
    if not request.user.is_staff:
        return redirect('adminlogin')
    category = Category.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        messages.success(request,"Category Updated")
        return redirect('view_category')
    return render(request, 'edit_category.html', locals()) 

def delete_category(request, pid):
    if not request.user.is_staff:
        return redirect('adminlogin')
    category = Category.objects.get(id=pid)
    category.delete()
    messages.success(request,"category Deleted")
    return redirect('view_category')

def add_product(request):
    if not request.user.is_staff:
        return redirect('adminlogin')
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        image = request.FILES['image']
        catobj = Category.objects.get(id=cat)
        Product.objects.create(name=name, price=price, discount=discount, category=catobj, description=desc, image=image)
        messages.success(request, "Product added")
    return render(request, 'add_product.html', locals())  

def view_product(request):
    if not request.user.is_staff:
        return redirect('adminlogin')
    product = Product.objects.all()
    return render(request, 'view_product.html', locals())      

def edit_product(request, pid):
    if not request.user.is_staff:
        return redirect('adminlogin')
    product = Product.objects.get(id=pid)
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        try:
            image = request.FILES['image']
            product.image = image
            product.save()
        except:
            pass
        catobj = Category.objects.get(id=cat)
        Product.objects.filter(id=pid).update(name=name, price=price, discount=discount, category=catobj, description=desc)
        messages.success(request, "Product Updated")
        return redirect('view_product')
    return render(request, 'edit_product.html', locals())    

def delete_product(request, pid):
    if not request.user.is_staff:
        return redirect('adminlogin')
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect('view_product')

def registration(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        mobile = request.POST['mobile']
        image = request.FILES['image']
        user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password)
        UserProfile.objects.create(user=user, mobile=mobile, address=address, image=image)
        messages.success(request, "Registeration Successful")
    return render(request, 'registration.html', locals())

def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "User login successfully")
            return redirect('home')
        else:
            messages.success(request,"Invalid Credentials")
    return render(request, 'userlogin.html', locals()) 

def profile(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    user = User.objects.get(id=request.user.id)
    data = UserProfile.objects.get(user=user)
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        address = request.POST['address']
        mobile = request.POST['mobile']
        try:
            image = request.FILES['image']
            data.image = image
            data.save()
        except:
            pass
        user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname)
        UserProfile.objects.filter(id=data.id).update(mobile=mobile, address=address)
        messages.success(request, "Profile updated")
        return redirect('profile')
    return render(request, 'profile.html', locals()) 

def logoutuser(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('main')

def change_password(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    if request.method == 'POST':
        o = request.POST.get('old')
        n = request.POST.get('new')
        c = request.POST.get('confirm')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('main')
            else:
                messages.success(request, "Password not matching")
                return redirect('change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('change_password')
    return render(request, 'change_password.html')

def user_product(request,pid):
    if pid == 0:
        product = Product.objects.all()
    else:
        category = Category.objects.get(id=pid)
        product = Product.objects.filter(category=category)
    allcategory = Category.objects.all()
    return render(request, "user-product.html", locals())

def product_detail(request, pid):
    product = Product.objects.get(id=pid)
    latest_product = Product.objects.filter().exclude(id=pid).order_by('-id')[:10]
    return render(request, "product_detail.html", locals()) 

def addToCart(request, pid):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    myli = {"objects":[]}
    try:
        cart = Cart.objects.get(user=request.user)
        myli = json.loads((str(cart.product)).replace("'", '"'))
        try:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
        except:
            myli['objects'].append({str(pid):1})
        cart.product = myli
        cart.save()
    except:
        myli['objects'].append({str(pid): 1})
        cart = Cart.objects.create(user=request.user, product=myli)
    return redirect('cart')
 
def incredecre(request, pid):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    cart = Cart.objects.get(user=request.user)
    if request.GET.get('action') == "incre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
    if request.GET.get('action') == "decre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        if myli['objects'][0][str(pid)] == 1:
            del myli['objects'][0][str(pid)]
        else:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) - 1
    cart.product = myli
    cart.save()
    return redirect('cart')

def cart(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    try:
        cart = Cart.objects.get(user=request.user)
        product = (cart.product).replace("'", '"')
        myli = json.loads(str(product))
        product = myli['objects'][0]
        print(product)
    except:
        product = []
    lengthpro = len(product)
    return render(request, 'cart.html', locals())    

def deletecart(request, pid):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    cart = Cart.objects.get(user=request.user)
    product = (cart.product).replace("'", '"')
    myli = json.loads(str(product))
    del myli['objects'][0][str(pid)]
    cart.product = myli
    cart.save()
    messages.success(request, "Delete Successfully")
    return redirect('cart')              


def booking(request):
    user = UserProfile.objects.get(user=request.user)
    cart = Cart.objects.get(user=request.user)
    total = 0
    deduction = 0
    discounted = 0
    productid = (cart.product).replace("'", '"')
    productid = json.loads(str(productid))
    try:
        productid = productid['objects'][0]
    except:
        messages.success(request, "Cart is empty, Please add product in cart.")
        return redirect('cart')
    for i,j in productid.items():
        product = Product.objects.get(id=i)
        total += int(j) * float(product.price)
        price = float(product.price) * (100 - float(product.discount)) / 100
        discounted += int(j) * price
    deduction = total - discounted
    if request.method == "POST":
        return redirect('/payment/?total='+str(total)+'&discounted='+str(discounted)+'&deduction='+str(deduction))
    return render(request, "booking.html", locals())
    
def myOrder(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    order = Booking.objects.filter(user=request.user)
    return render(request, "my-order.html", locals())

def user_order_track(request, pid):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    return render(request, "user-order-track.html", locals())

def change_order_status(request, pid):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    order = Booking.objects.get(id=pid)
    status = request.GET.get('status')
    if status:
        order.status = status
        order.save()
        messages.success(request, "Order status changed.")
    return redirect('myorder')

def user_feedback(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    user = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        Feedback.objects.create(user=request.user, message=request.POST['feedback'])
        messages.success(request, "Feedback sent successfully")
    return render(request, "feedback-form.html", locals())
    

def manage_feedback(request):
    if not request.user.is_staff:
        return redirect('adminlogin')
    action = request.GET.get('action', 0)
    feedback = Feedback.objects.filter(status=int(action))
    return render(request, 'manage_feedback.html', locals())

def delete_feedback(request, pid):
    if not request.user.is_staff:
        return redirect('adminlogin')
    feedback = Feedback.objects.get(id=pid)
    feedback.delete()
    messages.success(request, "Deleted successfully")
    return redirect('/manage-feedback/?action=1')

def read_feedback(request, pid):
    if not request.user.is_staff:
        return redirect('adminlogin')
    feedback = Feedback.objects.get(id=pid)
    feedback.status = 1
    feedback.save()
    return HttpResponse(json.dumps({'id':1, 'status':'success'}), content_type="application/json")    

def payment(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    total = request.GET.get('total')
    cart = Cart.objects.get(user=request.user)
    if request.method == "POST":
        book = Booking.objects.create(user=request.user, product=cart.product, total=total)
        cart.product = {'objects': []}
        cart.save()
        messages.success(request, "Book Order Successfully")
        return redirect('myorder')
    return render(request, 'payment.html', locals())

def manage_order(request):
    if not request.user.is_staff:
        return redirect('adminlogin')
    action = request.GET.get('action', 0)
    order = Booking.objects.filter(status=int(action))
    order_status = ORDERSTATUS[int(action)-1][1]
    if int(action) == 0:
        order = Booking.objects.filter()
        order_status = 'All'
    return render(request, 'manage_order.html', locals()) 


def delete_order(request, pid):
    if not request.user.is_staff:
        return redirect('adminlogin')
    order = Booking.objects.get(id=pid)
    order.delete()
    messages.success(request, 'Order Deleted')
    return redirect('/manage-order/?action='+request.GET.get('action'))

def admin_order_track(request, pid):
    if not request.user.is_staff:
        return redirect('adminlogin')
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    status = int(request.GET.get('status',0))
    if status:
        order.status = status
        order.save()
        return redirect('admin_order_track', pid)
    return render(request, 'admin-order-track.html', locals())

def manage_user(request):
    if not request.user.is_staff:
        return redirect('adminlogin')
    userprofile = UserProfile.objects.all()
    return render(request, 'manage_user.html', locals())

def delete_user(request, pid):
    if not request.user.is_staff:
        return redirect('adminlogin')
    user = User.objects.get(id=pid)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect('manage_user')

def admin_change_password(request):
    if not request.user.is_staff:
        return redirect('adminlogin')
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('main')
            else:
                messages.success(request, "Password not matching")
                return redirect('admin_change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('admin_change_password')
    return render(request, 'admin_change_password.html') 

