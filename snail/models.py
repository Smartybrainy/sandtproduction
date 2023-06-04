from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_countries.fields import CountryField

CATEGORY_CHOICES = (
    ("GA", "Giant African"),
    ("RO", "Roman Snail"),
    ("MS", "Mediterranean Snail"),
    ("BC", "Body Cream"),
    ("BW", "Body Wash"),
    ("BS", "Black Soap"),
    ("LS", "Liquid Soap"),
    ("FBL", "Face & Body Lotion"),
    ("FBM", "Face & Body Moisturiser"),
)

LABEL_CHOICES = (
    ("P", "primary"),
    ("S", "secondary"),
    ("D", "danger")
)


class Item(models.Model):
    class Types(models.TextChoices):
        IS_SNAIL = "SNAIL", "Snail"
        IS_COSMETIC = "COSMETIC", "Cosmetic"
    item_type = models.CharField(max_length=10, choices=Types.choices, default=Types.IS_SNAIL)
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    price = models.FloatField()
    discount_price = models.FloatField()
    description_title = models.TextField()
    more_about_item = models.TextField()
    image = models.ImageField(upload_to="snail", blank=True, null=True)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    label = models.CharField(max_length=1, choices=LABEL_CHOICES)

    class Meta:
        verbose_name_plural = "Items"

    def __str__(self):
        return self.title
    
    def get_snail_absolute_url(self):
        return reverse("snail:snail-item-detail", kwargs={
            "slug": self.slug
        })
    
    def get_cosmetic_absolute_url(self):
        return reverse("cosmetics:cosmetic-detail", kwargs={
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
    

class SnailManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(item_type=Item.Types.IS_SNAIL)


class Snail(Item):
    objects = SnailManager()

    class Meta:
        proxy = True
        verbose_name_plural = "Snail Item List"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.item_type = Item.Types.IS_SNAIL
        return super().save(*args, **kwargs)
    

class CosmeticManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(item_type=Item.Types.IS_COSMETIC)

class Cosmetic(Item):
    objects = CosmeticManager()

    class Meta:
        proxy = True
        verbose_name_plural = "Cosmetic Item List"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.item_type = Item.Types.IS_COSMETIC
        return super().save(*args, **kwargs)
            

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
    ref_code = models.CharField(max_length=30, blank=True, null=True)
    shipping_address = models.ForeignKey("Address", on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey("Payments", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def get_order_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_item_price()
        return total
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=20)
    shipping_address_1 = models.CharField(max_length=150)
    nearest_bustop = models.CharField(max_length=150)
    shipping_country = CountryField(multiple=False)
    shipping_state = models.CharField(max_length=25)
    zip_code = models.CharField(max_length=15)
    use_default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name}, {self.email}'

    
class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    status = models.CharField(max_length=20, blank=True, null=True)
    tx_ref = models.CharField(max_length=20, blank=True, null=True)
    transaction_id = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} > {self.status}"