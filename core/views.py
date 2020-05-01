from django.shortcuts import render
from .models import Item, OrderedItem, Cart
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone


# def home_view(request):
#     context = {
#         "items": Item.objects.all()
#     }
#     return render(request, 'home-page.html', context)

class HomeView(ListView):
    model = Item
    template_name = 'home-page.html'


def checkout_view(request):
    return render(request, 'checkout-page.html')


class ProductDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    ordered_item = OrderedItem.objects.get_or_create(item=item)
    cart_qs = Cart.objects.filter(user=request.user, ordered=False)
    if cart_qs.exists():
        cart = cart_qs[0]
        if cart.items.filter(item__slug=item.slug).exists():
            ordered_item.qty += 1
            ordered_item.save()
        else:
            cart.items.add(ordered_item)
    else:
        order_date = timezone.now()
        cart = Cart.objects.create(user=request.user, order_date=order_date)
        cart.items.add(ordered_item)
    return redirect("core:product", slug=slug)
    # return render(request, "product-page.html", {'slug': slug})
