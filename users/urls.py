from django.urls import path, include
from .views import user_profile, signup_view

urlpatterns = [
    path('user/', user_profile, name='user'),
    path('signup/', signup_view, name='signup'),
    
]
