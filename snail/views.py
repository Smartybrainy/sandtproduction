from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
import random
import string
from .models import Item, OrderItem, Order, Address
from .forms import CheckoutForm

def is_valid_form(values):
    valid = True
    for field in values:
        if field == " ":
            valid = False
    return valid
  

class HomePage(ListView):
    model = Item
    queryset = Item.objects.all()


class ProductDetailView(DetailView):
    model = Item


@login_required
def add_to_cart(request, slug):
    user = request.user
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=user,
            ordered=False
        )
    order_qs = Order.objects.filter(user=user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("snail:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("snail:order-summary")
    else:
        order_date = timezone.now()
        new_order = Order.objects.create(user=user, ordered_date=order_date)
        new_order.items.add(order_item)
        new_order.save()
        messages.info(request, "This item was added to your cart.")
        return redirect("snail:order-summary")


@login_required
def remove_from_cart(request, slug):
    user = request.user
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed to your cart.")
            return redirect("snail:order-summary")
        else:
            messages.info(request, "This item is not in your cart.")
            return redirect("snail:order-summary")
    messages.info(request, "Sorry you do not have an order.")
    return redirect("snail:order-summary")


@login_required
def remove_single_from_cart(request, slug):
    user = request.user
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
                return redirect("snail:order-summary")
            else:
                order.items.remove(order_item)
                order_item.delete()
                messages.info(request, "This item was removed from your cart.")
                return redirect("snail:order-summary")
    messages.info(request, "Sorry you do not have an order.")
    return redirect("snail:order-summary")


class OrderSumamryView(LoginRequiredMixin, View):
    template_name = "templates/order_summary.html"

    def get(self, *args, **kwargs):
        user = self.request.user
        try:
            order = Order.objects.get(user=user, ordered=False)
            context = {
                "order": order
            }
            return render(self.request, self.template_name, context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("snail:home-page")
    

class Checkout(View):
    template_name = "templates/snippet/checkout.html"

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
            "form": form,
            "order": order
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                use_default=True
            )
            if shipping_address_qs.exists():
                context.update({"default_shipping_address": shipping_address_qs[0]})

            return render(self.request, self.template_name, context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order.")
            return redirect("snail:order-summary")
        
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                print(form.cleaned_data)
                use_default_shipping_address = form.cleaned_data.get('use_default_shipping_address')
                
                if use_default_shipping_address:
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        use_default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(self.request, 'You do not have a default shipping address.')
                        return redirect("snail:checkout")
                else:   
                    first_name = form.cleaned_data.get("first_name")
                    last_name = form.cleaned_data.get("last_name")
                    email = form.cleaned_data.get("email")
                    shipping_address_1 = form.cleaned_data.get("shipping_address_1")
                    nearest_bustop = form.cleaned_data.get("nearest_bustop")
                    shipping_country = form.cleaned_data.get("shipping_country")
                    shipping_state = form.cleaned_data.get("shipping_state")
                    zip_code = form.cleaned_data.get("zip_code")

                    if is_valid_form([first_name, last_name, email, shipping_address_1, nearest_bustop, shipping_country, shipping_state, zip_code]):
                        shipping_address = Address(
                            user=self.request.user,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            shipping_address_1=shipping_address_1,
                            nearest_bustop=nearest_bustop,
                            shipping_country=shipping_country,
                            shipping_state=shipping_state,
                            zip_code=zip_code
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()
                    
                        set_default_shipping_address = form.cleaned_data.get('set_default_shipping_address')

                        if set_default_shipping_address:
                            shipping_address.use_default = True
                            shipping_address.save()
                    else:
                        messages.warning(self.request, "Please fill in your shipping address")
                        return redirect("snail:checkout")

                payment_option = form.cleaned_data.get('payment_option')
                if payment_option == "F":
                    messages.info(self.request, "Shipping address added successfully")
                    return redirect('snail:payment', payment_option="flutterwave")
                elif payment_option == "P":
                    messages.info(self.request, "Shipping address added successfully")
                    return redirect("snail:payment", payment_option="paystack")
                else:
                    messages.warning(self.request, "Invalid payment option selected, please try again.")
                    return redirect("snail:checkout")

            messages.warning(self.request, "Some went wrong, please fill all fields.")
            return redirect("snail:checkout")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order.")
            return redirect("snail:order-summary")
        

class Payment(View):
    template_name = 'templates/payment.html'

    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.shipping_address:
            context = {
                "order": order
            }
            return render(self.request, self.template_name, context)
        messages.warning(self.request, "You do not have a shipping address, please add one.")
        return redirect("snail:checkout")