from django import template
from snail.models import Order

register = template.Library()

def cart_count(user):
    if user.is_authenticated:
      order_qs = Order.objects.filter(
          user=user,
          ordered=False
      )
      if order_qs.exists():
          return order_qs[0].items.count()
      return 0
    return 0

cart_count = register.filter(cart_count, is_safe=True)