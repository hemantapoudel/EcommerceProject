from django.db import models
from django.urls import reverse
STATUS=(('active','active'),('','default'))
STOCK=(('In Stock','In Stock'),('Out of Stock','Out of Stock'))
Label=(('Hot','Hot'),('New','New'),('Sale','Sale'))
# Create your models here.

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

