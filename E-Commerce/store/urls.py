from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),


    path(
        'remove-from-cart/<int:product_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'increase/<int:product_id>/',
        views.increase_quantity,
        name='increase_quantity'
    ),

    path(
        'decrease/<int:product_id>/',
        views.decrease_quantity,
        name='decrease_quantity'
    ),

    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'payment/',
        views.payment,
        name='payment'
    ),

    path(
        'orders/',
        views.order_history,
        name='order_history'
    ),

    path(
        'signup/',
        views.signup_view,
        name='signup'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
    'add-to-cart/<int:product_id>/',
    views.add_to_cart,
    name='add_to_cart'
    ),

    path(
    'wishlist/',
    views.wishlist,
    name='wishlist'
),

path(
    'add-to-wishlist/<int:product_id>/',
    views.add_to_wishlist,
    name='add_to_wishlist'
),

path(
    'remove-from-wishlist/<int:wishlist_id>/',
    views.remove_from_wishlist,
    name='remove_from_wishlist'
),

path(
    'profile/',
    views.profile,
    name='profile'
),

path(
    'admin-dashboard/',
    views.admin_dashboard,
    name='admin_dashboard'
),
path(
    'buy-now/<int:product_id>/',
    views.buy_now,
    name='buy_now'
),

path(
    'address/',
    views.address,
    name='address'
),

path(
    'order-success/',
    views.order_success,
    name='order_success'
),

]