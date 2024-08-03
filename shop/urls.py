from django.urls import path, include
from .views import home, logout_view

urlpatterns = [
    path('', home, name='home'),
    path('logout/', logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    
]
