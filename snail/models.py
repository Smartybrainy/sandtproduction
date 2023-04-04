from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_countries.fields import CountryField

CATEGORY_CHOICES = (
    ("GA", "Giant African"),
    ("RO", "Roman Snail"),
    ("MS", "Mediterranean Snail")
)

LABEL_CHOICES = (
    ("P", "primary"),
    ("S", "secondary"),
    ("D", "danger")
)

class Item(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    price = models.FloatField()
    discount_price = models.FloatField()
    description_title = models.TextField()
    more_about_item = models.TextField()
    image = models.ImageField(upload_to="snail", blank=True, null=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    label = models.CharField(max_length=1, choices=LABEL_CHOICES)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("snail:snail-item-detail", kwargs={
            "slug": self.slug
        })
    
    def get_add_to_cart_url(self):
        return reverse("snail:add-to-cart", kwargs={
            "slug": self.slug
        })
    
    def get_remove_from_cart_url(self):
        return reverse("snail:remove-from-cart", kwargs={
            "slug": self.slug
        })
    
    def get_remove_single_from_cart_url(self):
        return reverse("snail:remove-single-from-cart", kwargs={
            "slug": self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.item.title
    
    def get_total_item_price(self):
        return self.quantity * self.item.price
    
    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price
    
    def get_item_amount_saved(self):
        return self.get_total_item_price() - self.get_total_item_discount_price()
    
    def get_final_item_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    shipping_address = models.ForeignKey("Address", on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey("Payment", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def get_order_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.CharField(max_length=25)
    shipping_address_1 = models.CharField(max_length=150)
    nearest_bustop = models.CharField(max_length=150)
    shipping_country = CountryField(multiple=False)
    shipping_state = models.CharField(max_length=25)
    zip_code = models.CharField(max_length=15)
    use_default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name}, {self.email}'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    payment_charge_id = models.CharField(max_length=50)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username