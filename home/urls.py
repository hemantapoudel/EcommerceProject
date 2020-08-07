from .views import *
from django.urls import path
from django.contrib.auth import views as auth_views

app_name="home"
urlpatterns = [
    path('', HomeView.as_view(),name="home"),
    path('product/<slug>', ItemView.as_view(),name="product"),
    path('category/<slug>', CategoryView.as_view(),name="category"),
    path('subcategory/<slug>', SubcategoryView.as_view(),name="subcategory"),
    path('search', SearchView.as_view(), name="search"),
    path('signup', signup, name="signup"),
    path('contact/',Contactus,name="contact"),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='change-password.html',
            success_url = '/'
        ),
        name='change_password'
    ),
    
]