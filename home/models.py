from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import ModelForm

STATUS=(('active','active'),('','default'))
STOCK=(('In Stock','In Stock'),('Out of Stock','Out of Stock'))
Label=(('Hot','Hot'),('New','New'),('Sale','Sale'))

ORDER=(('New','New'),('Accepted','Accepted'),('Rejected','Rejected'))

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    status = models.CharField(choices=STATUS,max_length=200,blank=True)
    def __str__(self):
        return self.title

    def GetCategoryUrls(self):
        return reverse("home:category",kwargs={'slug':self.slug})


class Subcategory(models.Model):
    title=models.CharField(max_length=200)
    slug=models.CharField(max_length=200)
    status=models.CharField(choices=STATUS, max_length=200,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

    def GetSubcategoryUrls(self):
        return reverse("home:subcategory",kwargs={'slug':self.slug})

class Item(models.Model):
    title = models.CharField(max_length=300)
    price = models.IntegerField()
    discounted_price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='Images')
    description = models.TextField(blank=True)
    slug = models.CharField(max_length=300,unique=True)
    stock = models.CharField(max_length=100,choices=STOCK)
    brand = models.CharField(max_length=300)
    Labels = models.CharField(max_length=100,choices=Label,blank=True)
    special_offer = models.BooleanField(default=False)
    front=models.BooleanField(default=False)
    new=models.BooleanField(default=False)
    hotdeal=models.BooleanField(default=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.title

    def GetItemUrls(self):
        return reverse("home:product",kwargs={'slug':self.slug})

class Contact(models.Model):
    name=models.CharField(max_length=200)
    subject=models.TextField()
    message=models.TextField()
    email=models.EmailField()
    def __str__(self):
        return self.name

class Cart(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug=models.TextField()
    title=models.CharField(max_length=100,blank=True)
    image=models.ImageField(blank=True)
    description=models.TextField(blank=True)
    price=models.IntegerField(default=0)
    quantity=models.IntegerField(default=1)
  
    def __str__(self):
        return self.user.username
    
    def delete_cart(self):
        return reverse("home:delete_cart",kwargs={'slug':self.slug})

    @property
    def total(self):
        return self.quantity*self.price


class Wish(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug=models.TextField()
    title=models.CharField(max_length=100,blank=True)
    image=models.ImageField(blank=True)
    description=models.TextField(blank=True)
    price=models.IntegerField(default=0)
    def __str__(self):
        return self.user.username
    
    def delete_wish(self):
        return reverse("home:delete_wish",kwargs={'slug':self.slug})


class Order(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    email=models.EmailField(max_length=150,blank=True)
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    phone=models.CharField(max_length=20)
    def __str__(self):
        return self.fname + ' ' + self.lname

class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields=['fname','lname','email','address','city','phone']
        

class OrderProducts(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100,blank=True)
    quantity=models.IntegerField()
    price=models.IntegerField()
    orders=models.CharField(max_length=100,choices=ORDER,default='New')
    def __str__(self):
        return self.title
    





    


