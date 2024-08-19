from django.urls import path, include
from .views import home, logout_view, about, shop, create_product, create_category, category_list_view, product_list_view

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('shop/', shop, name='shop'),
    path('create_product/', create_product, name='create_product'),
    path('create_category/', create_category, name='create_category'),
    path('category_list/', category_list_view, name='category_list'),
    path('product_list/', product_list_view, name='product_list'),
    path('logout/', logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]