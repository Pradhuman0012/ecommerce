from django.urls import path, include
from .views import home, logout_view, about, shop   

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('shop/', shop, name='shop'),
    path('logout/', logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    
]
