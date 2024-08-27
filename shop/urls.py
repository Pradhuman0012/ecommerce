from django.urls import path, include
from shop import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('place_order/', views.place_order, name='place_order'),
    path('create_product/', views.create_product, name='create_product'),
    path('create_category/', views.create_category, name='create_category'),
    path('category_list/', views.category_list_view, name='category_list'),
    path('product_list/', views.product_list_view, name='product_list'),
    path('product/<int:pk>/buy/', views.buy_now, name='buy_now'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('logout/', views.logout_view, name='logout'),
    
    path('accounts/', include('django.contrib.auth.urls')),
]