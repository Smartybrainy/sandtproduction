from django.contrib import admin

from .models import Item, OrderItem, Order, Address, Payment


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ('title', 'price', 'discount_price')
    prepopulated_fields = {"slug": ("title",)}


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'item',
                    'quantity',
                    'ordered',
                    )
    
class OrderAdmin(admin.ModelAdmin):
    list_display = (
                    'user',
                    'ordered',
                    'ordered_date'
                    )


admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address)
admin.site.register(Payment)