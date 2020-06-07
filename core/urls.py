from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<slug>/', views.ProductDetailView.as_view(), name='product'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('product/add-product/<slug>/', views.add_to_cart, name='add_product'),
    path('product/remove-product/<slug>', views.remove_from_cart, name='remove_from_cart'),
    path('summary/', views.SummaryView.as_view(), name='order-summary')
]