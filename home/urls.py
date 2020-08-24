from .views import *
from django.urls import path,include
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
    path('add_to_cart', add_to_cart, name="add_to_cart"),
    path('cart',cart, name="cart"),
    path('delete_cart/<slug>',delete_cart, name="delete_cart"),
    path('add_to_wish', add_to_wish, name="add_to_wish"),
    path('wish',wish, name="wish"),
    path('delete_wish/<slug>',delete_wish, name="delete_wish"),
    path('hot_deal/',Hotdeal.as_view(), name="hot_deal"),
    path('checkout',checkoutproducts, name="checkoutproducts"),
    
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name="password_reset"),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    path('change-password/',auth_views.PasswordChangeView.as_view(template_name='change-password.html',success_url = '/' ),name='change_password'),

    
]