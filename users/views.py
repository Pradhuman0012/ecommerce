from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm

# Create your views here.
@login_required
def user_profile(request):
    return render(request, 'user_profile.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('/accounts/login')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})