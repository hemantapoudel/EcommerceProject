from django.shortcuts import render

# Create your views here.
from .models import *
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

# Create your views here.

class BaseView(View):
    template_view={}
    template_view['categories']=Category.objects.all()
    template_view['subcategories']=Subcategory.objects.all()
    template_view['smartphone_sub']=Subcategory.objects.filter(category_id=1)
    template_view['camera_sub']=Subcategory.objects.filter(category_id=2)
    template_view['laptop_sub']=Subcategory.objects.filter(category_id=3)
    template_view['accessories_sub']=Subcategory.objects.filter(category_id=4)
    
class HomeView(BaseView):
    def get(self,request):
        self.template_view['items']=Item.objects.filter(front = True)
        self.template_view['smartphones']=Item.objects.filter(category_id=1)
        self.template_view['laptops']=Item.objects.filter(category_id=3)
        self.template_view['accessories']=Item.objects.filter(category_id=4)
        return render(request,'index.html',self.template_view)

class ItemView(BaseView):
    def get(self,request,slug):
        
        self.template_view['view_items']=Item.objects.filter(slug=slug)

        self.template_view['view_itemss']=Item.objects.filter(category_id=1)
        return render(request,'product.html',self.template_view)




class CategoryView(BaseView):
    def get(self,request,slug):
        category_id = Category.objects.get(slug=slug).id
        self.template_view['category_item']=Item.objects.filter(category_id=category_id)
        return render(request,'category.html',self.template_view)

class SubcategoryView(BaseView):
    def get(self,request,slug):
        subcategory_id = Subcategory.objects.get(slug=slug).id
        self.template_view['subcategory_item']=Item.objects.filter(subcategory_id=subcategory_id)
        return render(request,'subcategory.html',self.template_view)

class Hotdeal(BaseView):
    def get(self,request):
        self.template_view['hot_items']=Item.objects.filter(hotdeal=True)
        return render(request,'hotdeal.html',self.template_view)


def signup(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request,'The username is already taken')
                return redirect('home:signup')
            
            elif User.objects.filter(email=email).exists():
                messages.error(request,'This email is already registered')
                return redirect('home:signup')

            else:
                user = User.objects.create_user(
                        first_name = fname,
                        last_name = lname,
                        username = username,
                        email = email, 
                        password=password

                )
                user.save()
                messages.success(request,'You are successfully registered')
                return redirect('home:signup')
        else:
            messages.error(request,'The password does not matched')
            return redirect('home:signup')

    return render(request,'signup.html')

class SearchView(BaseView):
        def get(self,request):
            query = request.GET.get('Search')
            self.template_view['search_result']=Item.objects.filter(title__icontains=query)
            self.template_view['search_for'] = query
            return render(request,'search.html',self.template_view)

def Contactus(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']
        info= Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
        )
        info.save()
        email=EmailMessage(
            'New Message',
            f'<html><body><b>Name : {name} <br> Email:{email}<br> Subject:{subject}<br> Message:{message} </body></html>',
            email,['feedmymind18@gmail.com']

        )
        email.content_subtype='html'
        email.send()
    return render(request,"contact.html")
    
def cart(request):
    # views={}
    current_user=request.user
    # views['carts']=Cart.objects.filter(checkout=False,user_id=current_user.id)
    carts=Cart.objects.filter(checkout=False,user_id=current_user.id)
    total=0
    for i in carts:
        total += i.price*i.quantity
    views={'carts':carts,'total':total}
    return render(request,'cart.html',views)
@login_required

def add_to_cart(request):
    if request.method=='POST':
        slug=request.POST['slug']
        title=request.POST['title']
        image=request.POST['image']
        description=request.POST['description']
        price=request.POST['price']

        if Cart.objects.filter(slug=slug).exists():
            quantity=Cart.objects.get(slug=slug).quantity
            Cart.objects.filter(slug=slug).update(quantity=quantity+1)
            return redirect('home:cart')
        else:
            my_cart=Cart.objects.create(
                user = request.user,
                slug = slug,
                title=title,
                image=image,
                description=description,
                price=price
            )
            my_cart.save()
            return redirect('home:cart')
    else:
        return redirect('/')

def delete_cart(request,slug):
    if Cart.objects.filter(slug=slug).exists():
        Cart.objects.filter(slug=slug).delete()
        return redirect('/cart')
    else:
        return redirect('/cart')
#*************************************************************************************
def wish(request):
    views={}
    views['wishs']=Wish.objects.filter(user=request.user)
    return render(request,'wishlist.html',views)

@login_required

def add_to_wish(request):
    if request.method=='POST':
        slug=request.POST['slug']
        title=request.POST['title']
        image=request.POST['image']
        description=request.POST['description']
        price=request.POST['price']

        if Wish.objects.filter(slug=slug).exists():
            messages.error(request,'already in list')
            return redirect('home:wish')
        else:
            my_wish=Wish.objects.create(
                user = request.user,
                slug = slug,
                title= title,
                image=image,
                description=description,
                price=price
            )
            my_wish.save()
            return redirect('home:wish')
    else:
        return redirect('/')

def delete_wish(request,slug):
    if Wish.objects.filter(slug=slug).exists():
        Wish.objects.filter(slug=slug).delete()
        return redirect('/wish')
    else:
        return redirect('/wish')


def checkoutproducts(request):
    current_user=request.user
    checks=Cart.objects.filter(user_id=current_user.id)
    alltotal=0
    for i in checks:
        alltotal += i.price*i.quantity
    if request.method=="POST":
       form=OrderForm(request.POST)
       if form.is_valid():
            detail=Order()
            detail.fname=form.cleaned_data['fname']
            detail.lname=form.cleaned_data['lname']
            detail.email=form.cleaned_data['email']
            detail.address=form.cleaned_data['address']
            detail.phone=form.cleaned_data['phone']
            detail.city=form.cleaned_data['city']
            detail.save()

            checks=Cart.objects.filter(user_id=current_user.id)
            for x in checks:
                data=OrderProducts()
                data.user_id=current_user.id
                data.order_id=detail.id
                data.id=x.id
                data.title=x.title
                data.quantity=x.quantity
                data.price=x.price
                data.save()

            Cart.objects.filter(user_id=current_user.id).delete()
    form=OrderForm()
    views={'checks':checks,'alltotal':alltotal,'form':form}
    
    return render(request,'checkout.html',views)

#for rest api
from .serializers import *
from rest_framework import viewsets

class ItemViewSet(viewsets.ModelViewSet):
    queryset=Item.objects.all()
    serializer_class=ItemSerializers


    



