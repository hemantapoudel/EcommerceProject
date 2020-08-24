from django.contrib import admin

# Register your models here.
from .models import *

class OrderProductInline(admin.TabularInline):
    model=OrderProducts
    extra=0

class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderProductInline]



# Register your models here.
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Item)
admin.site.register(Contact)
admin.site.register(Cart)
admin.site.register(Wish)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProducts)


