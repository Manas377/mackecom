from django.contrib import admin
from .models import Item, OrderedItem, Cart, CATEGORY_CHOICES, LABEL_COLOUR_CHOICES

admin.site.register(Item)
admin.site.register(OrderedItem)
admin.site.register(Cart)
