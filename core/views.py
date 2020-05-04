from django.shortcuts import render
from .models import Item, OrderedItem, Cart
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages


# def home_view(request):
#     context = {
#         "items": Item.objects.all()
#     }
#     return render(request, 'home-page.html', context)

class HomeView(ListView):
    model = {Item, OrderedItem}
    template_name = 'home-page.html'


def checkout_view(request):
    return render(request, 'checkout-page.html')


class ProductDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    ordered_item, created = OrderedItem.objects.get_or_create(item=item, user=request.user, is_ordered=False)
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
        cart.items.add(ordered_item.pk)
    messages.info(request, '{} Was added to your cart, total quantity: {}'.format(item.title, ordered_item.qty))
    return redirect("core:product", slug=slug)
    # return render(request, "product-page.html", {'slug': slug})


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    ordered_item = OrderedItem.objects.get(item=item, user=request.user, is_ordered=False)
    cart_qs = Cart.objects.filter(user=request.user, ordered=False)
    if cart_qs.exists():
        cart = cart_qs[0]
        if cart.items.filter(item__slug=item.slug).exists():
            cart.items.remove(ordered_item)
            ordered_item.delete()
        else:  # Also Send a Message that the item does not exist in cart
            return redirect("core:product", slug=slug)
    messages.warning(request, '{} was removed from your cart'.format(item.title))
    return redirect("core:product", slug=slug)


def reduce_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    ordered_item = OrderedItem.objects.get(item=item, user=request.user, is_ordered=False)
    cart_qs = Cart.objects.filter(user=request.user, ordered=False)
    if cart_qs.exists():
        cart = cart_qs[0]
        if cart.items.filter(item__slug=item.slug).exists():
            ordered_item.qty -= 1
            ordered_item.save ()
            if ordered_item.qty == 0:
                ordered_item.delete()
    return redirect("core:product", slug=slug)
