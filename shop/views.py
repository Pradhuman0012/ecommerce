from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
# from django.views.generic import TemplateView

# class HomePageView(TemplateView):
#     template_name = 'shop/home.html'

def home(request):
    return render(request, 'shop/home.html')


def logout_view(request):
    return render(request, 'registration/logout.html')