from django.urls import path, include
from .views import user_profile, signup_view

urlpatterns = [
    path('user_profile/', user_profile, name='user_profile'),
    path('signup/', signup_view, name='signup'),
    
]
