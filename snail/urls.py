from django.urls import path
from .views import (
    HomePage,
    ProductDetailView,
    add_to_cart, 
    remove_from_cart,
    remove_single_from_cart,
    OrderSumamryView,
    Checkout,
    Payment
    )

app_name = "snail"

urlpatterns = [
    path('', HomePage.as_view(), name="home-page"),
    path('snail-item-detail/<slug>/', ProductDetailView.as_view(), name="snail-item-detail"),
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart"),
    path('remove-single-from-cart/<slug>/', remove_single_from_cart, name="remove-single-from-cart"),
    path('order-summary/', OrderSumamryView.as_view(), name="order-summary"),
    path('checkout/', Checkout.as_view(), name="checkout"),
    path('payment/<payment_option>/', Payment.as_view(), name="payment"),
]