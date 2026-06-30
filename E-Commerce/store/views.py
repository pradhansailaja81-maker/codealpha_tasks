from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Order, OrderItem, Wishlist, Address
from .models import Review
from django.shortcuts import redirect

# HOME PAGE
def home(request):

    query = request.GET.get('q')
    category_id = request.GET.get('category')

    products = Product.objects.all()

    if query:
        products = products.filter(
            name__icontains=query
        )

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    categories = Category.objects.all()

    cart = request.session.get('cart', {})

    cart_count = (
        sum(cart.values())
        if isinstance(cart, dict)
        else 0
    )

    return render(
        request,
        'store/home.html',
        {
            'products': products,
            'categories': categories,
            'cart_count': cart_count
        }
    )


# PRODUCT DETAILS
def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        'store/product_detail.html',
        {
            'product': product
        }
    )


# ADD TO CART
def add_to_cart(request, product_id):

    cart = request.session.get('cart', {})

    if isinstance(cart, list):
        cart = {}

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('cart')


# REMOVE FROM CART
def remove_from_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')


# INCREASE QUANTITY
def increase_quantity(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart

    return redirect('cart')


# DECREASE QUANTITY
def decrease_quantity(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')


# CART PAGE
def cart(request):

    cart = request.session.get('cart', {})

    if isinstance(cart, list):
        cart = {}

    cart_products = []
    total = 0

    for product_id, quantity in cart.items():

        try:

            product = Product.objects.get(
                id=product_id
            )

            subtotal = (
                product.price * quantity
            )

            total += subtotal

            cart_products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })

        except Product.DoesNotExist:
            pass

    cart_count = sum(cart.values())

    return render(
        request,
        'store/cart.html',
        {
            'cart_products': cart_products,
            'total': total,
            'cart_count': cart_count
        }
    )


# CHECKOUT PAGE
def checkout(request):

    return render(
        request,
        'store/checkout.html'
    )


# PAYMENT PAGE
@login_required(login_url='/login/')
def payment(request):

    cart = request.session.get('cart', {})

    total = 0
    items = []

    for product_id, quantity in cart.items():

        product = Product.objects.get(id=product_id)

        total += product.price * quantity

        items.append({
            'product': product,
            'quantity': quantity
        })

    if request.method == 'POST':

        payment_method = request.POST.get(
            'payment_method'
        )

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            payment_method=payment_method
        )

        for item in items:

            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

        request.session['cart'] = {}

        return redirect('order_success')

    return render(
        request,
        'store/payment.html',
        {
            'total': total
        }
    )


# ORDER HISTORY
@login_required(login_url='/login/')
def order_history(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'store/order_history.html',
        {
            'orders': orders
        }
    )


# SIGNUP
def signup_view(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        email = request.POST.get(
            'email'
        )

        password = request.POST.get(
            'password'
        )

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'Username already exists'
            )

            return redirect('signup')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            'Account created successfully'
        )

        return redirect('login')

    return render(
        request,
        'store/signup.html'
    )


# LOGIN
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        messages.error(
            request,
            'Invalid username or password'
        )

    return render(
        request,
        'store/login.html'
    )


# LOGOUT
def logout_view(request):

    logout(request)

    return redirect('home')

@login_required(login_url='/login/')
def add_to_wishlist(request, product_id):

    product = Product.objects.get(id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('wishlist')


@login_required(login_url='/login/')
def remove_from_wishlist(request, wishlist_id):

    item = Wishlist.objects.get(
        id=wishlist_id,
        user=request.user
    )

    item.delete()

    return redirect('wishlist')


@login_required(login_url='/login/')
def wishlist(request):

    items = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        'store/wishlist.html',
        {
            'items': items
        }
    )



@login_required(login_url='/login/')
def profile(request):

    total_orders = Order.objects.filter(
        user=request.user
    ).count()

    wishlist_count = Wishlist.objects.filter(
        user=request.user
    ).count()

    return render(
        request,
        'store/profile.html',
        {
            'total_orders': total_orders,
            'wishlist_count': wishlist_count
        }
    )


@login_required(login_url='/login/')
def admin_dashboard(request):

    if not request.user.is_superuser:
        return redirect('home')

    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()

    recent_orders = Order.objects.order_by(
        '-created_at'
    )[:5]

    return render(
        request,
        'store/admin_dashboard.html',
        {
            'total_products': total_products,
            'total_orders': total_orders,
            'total_users': total_users,
            'recent_orders': recent_orders
        }
    )


def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    reviews = Review.objects.filter(
        product=product
    ).order_by('-created_at')

    return render(
        request,
        'store/product_detail.html',
        {
            'product': product,
            'reviews': reviews
        }
    )

@login_required(login_url='/login/')
def add_review(request, product_id):

    product = Product.objects.get(
        id=product_id
    )

    if request.method == 'POST':

        rating = request.POST.get('rating')

        comment = request.POST.get('comment')

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )

    return redirect(
        'product_detail',
        product_id=product.id
    )


def buy_now(request, product_id):

    cart = {
        str(product_id): 1
    }

    request.session['cart'] = cart

    return redirect('address')



@login_required(login_url='/login/')
def address(request):

    if request.method == 'POST':

        Address.objects.create(
            user=request.user,
            full_name=request.POST['full_name'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            pincode=request.POST['pincode']
        )

        return redirect('payment')

    return render(request, 'store/address.html')
  
@login_required(login_url='/login/')
def order_success(request):

    return render(
        request,
        'store/order_success.html'
    )

