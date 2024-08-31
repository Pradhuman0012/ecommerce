from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError
from .forms import ProductForm, CategoryForm, OrderForm
from django.http import HttpResponse
from .models import Order
from decimal import Decimal
from .tasks import send_order_confirmation_email, test_task
# Create your views here.

def home(request):
    test_task.delay()
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
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))
        payment_method = request.POST.get('payment_method')
        user_email = request.POST.get('email')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return HttpResponse("Product not found", status=404)

        if product.stock <= 0:
            return HttpResponse("Sorry, this product is out of stock.", status=400)

        if quantity > product.stock:
            return HttpResponse("The quantity requested exceeds the available stock.", status=400)

        # Calculate the total amount
        amount = Decimal(product.price) * quantity

        #update stock
        product.stock -= quantity
        product.save()

        # Create the order
        order =Order.objects.create(
            user=request.user,
            product=product,
            payment_method=payment_method,
            amount=amount
        )

        # Trigger the Celery task to send an email
        print("===user_email===",user_email)
        print("==order.id==",order.id)
        send_order_confirmation_email.delay(
            user_email,
            order.id,
            order.product.name,
            quantity,
            payment_method,
            amount
            )

        # Optionally, you can redirect to a success page or show a confirmation message
        return redirect('order_confirmation')

    # Render the order form if not POST request
    return HttpResponse('some error occur')


def oderHistory(request,user):
    order_history= Order.objects.filter(user=user).order_by('-created_at')
    # Get distinct payment methods from orders
    used_payment_methods = Order.objects.values_list('payment_method', flat=True).distinct()
    payment_method = request.GET.get('payment_method', '')
    search_query = request.GET.get('search', '')
    
    if search_query:
        order_history = Order.objects.filter(product__name__icontains=search_query).order_by('-created_at')
    if payment_method:
        order_history= Order.objects.filter(user=user,payment_method = payment_method).order_by('-created_at')

    return render(request, 'shop/order_history.html',{'order_history':order_history,'used_payment_methods':used_payment_methods})