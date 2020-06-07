from django.shortcuts import render
from .models import Item, OrderedItem, Cart
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404, redirect, get_list_or_404
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm


class HomeView(ListView):
    model = Item
    paginate_by = 4
    template_name = 'home-page.html'


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm
        cart = get_object_or_404(Cart, user=self.request.user)
        context = {
            'form': form,
            'cart': cart
        }
        return render(self.request, 'checkout-page.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST)
        print(self.request.POST)
        if form.is_valid():
            print("form is valid")
            print(form.cleaned_data)
            return redirect('core:checkout')
        messages.warning(self.request, "Checkout Failed")
        return redirect('core:checkout')


class ProductDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'


@login_required()
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


@login_required
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


class SummaryView(View):
    def get(self, *args, **kwargs):
        try:
            cart = get_object_or_404(Cart, user=self.request.user, ordered=False)
            if cart:
                context = {
                    'object': cart
                }
            return render(self.request, 'cart-summary.html', context)

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order" )
            return redirect("core:home")



