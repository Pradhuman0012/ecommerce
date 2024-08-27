from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError
from .forms import ProductForm, CategoryForm, OrderForm
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'shop/home.html')

def about(request):
    return render(request, 'shop/about.html')
from .models import Product, Category


@login_required
def shop(request):
    # Retrieve all categories for the filter
    categories = get_all_categories()
    products = get_all_products()

    # Extract search query and category filter from GET parameters
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    if category_id:
        products = products.filter(category_id=category_id)

    # Prepare data for rendering
    data = {
        'product': products,
        'categories': categories,
    }

    return render(request, 'shop/shop.html', data)


def logout_view(request):
    return render(request, 'registration/logout.html')

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to a success page
    else:
        form = ProductForm()

    categories = get_all_categories()
    return render(request, 'shop/create_product.html', {'form': form, 'categories': categories})



def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Redirect to a success page
    else:
        form = CategoryForm()
    return render(request, 'shop/create_category.html', {'form': form})

def get_all_products():
    try:
        return Product.objects.all()
    except DatabaseError as e:
        return Product.objects.none() 

def get_all_categories():
    try:
        return Category.objects.all()
    except DatabaseError as e:
        return Category.objects.none() 

def category_list_view(request):
    categories = get_all_categories()
    return render(request, 'shop/category_list.html', {'categories': categories})

def product_list_view(request):
    products = get_all_products()
    return render(request, 'shop/product_list.html', {'products': products})

def order_confirmation(request):
    return render(request, 'order_confirmation.html')


@login_required
def buy_now(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return render(request, 'shop/buy_now.html', {'product': product})

def place_order(request):
    print("=============REQUEST================",request.POST)
    form = OrderForm(request.POST)
    if form.is_valid():
        order = form.save(commit=False)
        product = get_object_or_404(Product, id=order.product.id)
        if product.stock > 0:
                # Reduce stock
                product.stock -= 1
                product.save()

                # Save the order
                order.save()

    return redirect('order_confirmation')