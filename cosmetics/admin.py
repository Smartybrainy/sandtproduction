from django.contrib import admin
from snail.models import Cosmetic

@admin.register(Cosmetic)
class CosmeticAdmin(admin.ModelAdmin):
  list_display = ('title', 'price', 'discount_price')
  prepopulated_fields = {"slug": ("title",)}
