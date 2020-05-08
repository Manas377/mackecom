from django import template
from ..models import Cart

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        count_qs = Cart.objects.filter(user=user, ordered=False)
        if count_qs.exists():
            items_qs = count_qs[0].items.all()
            count = 0
            for items in items_qs[0:]:
                count = items.qty + count
            return count
    else:
        return 0



