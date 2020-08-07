from .models import *
from rest_framework import serializers
class ItemSerializers(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields=['id','title','price','discounted_price','image','slug','stock','brand','Labels','category','subcategory','special_offer']
