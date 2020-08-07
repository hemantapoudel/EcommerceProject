from django.shortcuts import render

# Create your views here.
from .models import *
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import EmailMessage
# Create your views here.

class BaseView(View):
    template_view={}
    template_view['categories']=Category.objects.all()
    template_view['subcategories']=Subcategory.objects.all()

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
    

#for rest api
from .serializers import *
from rest_framework import viewsets

class ItemViewSet(viewsets.ModelViewSet):
    queryset=Item.objects.all()
    serializer_class=ItemSerializers

    



